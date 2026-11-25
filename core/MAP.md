# MAP — `core/` (Pipeline & Công Cụ "Điểm Đọc")

> **Agent: đọc file này thay vì mở từng file Python.** Mỗi mục cho biết file làm gì,
> hàm chính, và khi nào cần đọc code gốc.

---

## Tổng quan

`core/` chứa **pipeline dựng video** và các công cụ bảo trì hệ thống. Mỗi module là một lệnh độc lập, gọi được riêng hoặc qua `run.py`. Chúng chia sẻ logic chung qua package `diemdoc/`.

```
m1_scraper → m1b_llm_writer → m0_validate → m2_timeline → m3_voice → m5_sync → m4_render → m5_qa → m6_compose → m7_publish
(cào tin)     (biên kịch)                               (ViTTS)    (Whisper)  (dựng hình)         (ghép âm)
                                                           run_day.py điều phối toàn diện hằng ngày
                                                           doctor.py chẩn đoán hệ thống
                                                           clean.py dọn dẹp cache an toàn
                                                           audio_check.py kiểm toán âm lượng
```

---

## `diemdoc/` — Thư viện dùng chung

Không module nào tự viết lại logic đã có ở đây.

| File | Chứa gì | Hàm/API chính |
|---|---|---|
| `paths.py` | Mọi đường dẫn tuyệt đối tính từ ROOT. Portable 100%. An toàn Drive. | `ROOT`, `ASSETS`, `FONTS`, `SFX`, `BGM`, `ICONS`, `LOGO`, `TEMPLATES`, `DESIGN`, `SPEC`, `PROJECTS`, `WORK`, `project_dir()`, `work_project_dir()`, `rel_to_root()`, `file_url()` |
| `timeline.py` | Truy cập `video_timeline.json`. | `load_timeline()`, `save_timeline()`, `cards_of()`, `scene_start()`, `scene_duration()`, `total_duration()`, `card_reveal()`, `set_scene_timing()`, `find_scene()` |
| `tts_text.py` | Chuẩn hoá văn bản cho TTS & ánh xạ ngược từ hiển thị (bao gồm quy chuẩn số Việt Nam, từ viết tắt thể thao và đơn vị tiền tệ USD đọc thành "đô"). | `prepare(display_text) -> (tts_text, token_map)`, `load_pronunciation_dict()` |
| `unknown_names.py`| Quét và phát hiện tên riêng thể thao chưa có trong từ điển. | `scan_text_for_unknown_names()`, `scan_project_scripts()` |
| `whisper_batch_worker.py` | Tiến trình con chạy Whisper độc lập theo lô, tự giải phóng RAM. | Chạy qua subprocess tách biệt |
| `sync.py` | Căn chỉnh thời gian từng từ + **neo ngữ nghĩa**. | `align_words_to_ground_truth()`, `resolve_cue_points()`, `find_phrase_time()`, `group_karaoke_chunks()`, `syllabic_sync()` |
| `audio.py` | Xử lý âm thanh: cắt lặng, ducking sidechain, playlist BGM, SFX track, loudness 2-pass (-14 LUFS). | `build_sfx_track()`, `build_bgm_playlist()`, `apply_sidechain_ducking()`, `two_pass_loudnorm()`, `measure_loudness()`, `measure_voice_bgm_separation()`, `mix_master_audio()` |
| `publisher.py` | ★ Trung tâm chuẩn hóa xuất bản cho 3 Loại Video (Giọng đọc `config/voice.json`, lọc sạch triệt để tag kỹ thuật `[Nam]`/`[Nữ]`/`[TIN XX]`/`[01]` & ghi chú giọng đọc nội bộ qua `sanitize_chapter_label()` / `sanitize_public_text()`, `mota.txt` 2 phần Sentence Case, **Hệ thống 3 kiểu Thumbnail đồng bộ**: Video Long 16:9 xuất đủ 3 kiểu A `cyber_split` / B `magazine_bento` / C `clash_diagonal`, Video Short 9:16 mặc định chọn ngẫu nhiên 1 trong 3 kiểu). | `load_voice_preset()`, `sanitize_chapter_label()`, `sanitize_public_text()`, `write_mota_16x9()`, `write_mota_9x16()`, `render_thumbnail_16x9_single()`, `render_thumbnail_9x16()`, `compute_9x16_hero_font_size()`, `THUMB_STYLES`, `DEFAULT_LONG_ABC_STYLES` |
| `short_batch.py` | ★ Bộ khung tái sử dụng dựng lô video Shorts 9:16 (nạp/kiểm ảnh, contact sheet QA, ViTTS đơn giọng hoặc song giọng theo đoạn `voice_segments` + chuẩn hóa `-16 LUFS` từng đoạn, merge JSON ngày, A/V drift trim, tự động gắn Short Outro qua `short_outro`, xuất bản qua `publisher` & `m8_news_bridge`). | `ShortDayContext`, `copy_and_verify_images()`, `build_contact_sheet()`, `synthesize_item_audio()`, `merge_day_metadata()`, `build_and_publish_short()`, `run_short_batch()` |
| `short_outro.py` | ★ Tự động chọn ngẫu nhiên & ghép nối Outro 9:16 trái giới tính giọng đọc (`config/shorts.json["outro"]` + `logo/short_outros/`). | `load_short_outro_config()`, `normalize_voice_gender()`, `pick_short_outro()`, `append_short_outro()` |
| `jsonio.py` | Đọc/ghi JSON an toàn Unicode + hash nội dung (cho cache). | `load_json()`, `save_json()`, `hash_obj()`, `hash_file()` |
| `log.py` | Logging có màu và prefix. | `log()`, `ok()`, `warn()`, `err()`, `step()`, `banner()`, `die()` |

---

## `vendor/` — Thư viện nhúng độc lập (Vendored Packages)

| Package | Phiên bản | Nguồn | Mục đích |
|---|---|---|---|
| `vieneu` | `3.8.1` | `core/vendor/vieneu` | Bộ phát sinh giọng đọc tiếng Việt ViTTS `v3turbo` (Minh Quân Pro) chạy độc lập nội bộ, không phụ thuộc repo ngoài. |

---

## Các Module Pipeline

### `run_day.py` — Điều phối sản xuất tự động hằng ngày (Mới — GĐ5c)
- **Mục đích**: Master orchestrator nối liền toàn bộ quy trình sản xuất theo mô hình 2 lệnh tiêu chuẩn của chủ kênh:
  1. `prepare`: Cào tin (`m1`) -> Lọc tin -> LLM Writer (`m1b`) -> Tạo timeline 16:9 và `shorts_units.json` (3 video 9:16) -> Xuất Sổ Chứng Cứ (`WORK/goi_duyet_noi_dung.md`). DỪNG LẠI tại đây để chủ kênh kiểm duyệt nội dung.
  2. `build`: Sau khi duyệt, chạy trọn gói từ timeline/units: Giọng đọc ViTTS (`m3`) -> Đồng bộ phụ đề Whisper/Syllabic (`m5_sync`) -> Validate (`m0`) -> QA Layout & Vision (`m5_qa`) -> Render Playwright (`m4`) -> Master Audio Ducking & Loudnorm (-14 LUFS) (`m6`) -> Đóng gói xuất bản (`m7`) cho cả 1 video chính 16:9 và 3 video phụ 9:16.
- **Tính năng cao cấp**:
  - Cơ chế **Resume an toàn cấp tin** lưu vết tại `.run_state` (`completed_169`, `completed_916`), nếu ngắt giữa chừng, chạy lại sẽ tự động bỏ qua các tin đã render mà không mất công làm lại. Dùng cờ `--force` khi muốn render lại toàn bộ.
  - Cờ `--workers N` (mặc định 1) hỗ trợ đa tiến trình Playwright Chromium song song, tính toán trước mốc `global_offset` để giữ liền mạch dòng chảy hạt và ticker.
  - Cờ `--shorts focus|digest|all` cho phép render Focus Short (gộp 3-5 tin chi tiết) hoặc Digest Short ("đọc nhanh" lướt qua các tin) từ `shorts.json`.
  - Hỗ trợ `--engine html` v2 với 2 template `long_sports_news_v2.html` và `short_news_v2.html`, tự động xoay vòng 5 layout (`full`, `split`, `polaroid`, `cinema`, `triptych`), lớp hạt lấp lánh nhẹ, ticker tin tiếp theo, và chuẩn hóa âm thanh master EBU R128 (-14 LUFS, True Peak <= -1.0 dBTP, độ lệch Video-Audio < 1 ms).
- **Cách dùng**:
  - `python3 core/run_day.py prepare --since "2026-10-15 00:01"`
  - `python3 core/run_day.py build --day 16.10.2026 --engine html --shorts focus --workers 3`
  - `python3 core/run_day.py build --item 1 --engine html`
  - `python3 core/run_day.py build --force`

### `m1_scraper.py` — Bộ cào và lọc tin thể thao tự động (Nâng cấp — 22.11.2026)
- **Mục đích**: Cào tin tức thể thao tự động song hành từ cả báo Việt Nam và báo Thế giới cấu hình tại `config/sources.json` (hỗ trợ `--region all|vn|world`); hỗ trợ cửa sổ thời gian chuẩn kênh (`--period weekly`: 00:01 T2 tuần trước -> 23:59 CN tuần trước; `--period yesterday`: 12:00 trưa hôm qua -> hiện tại; `--since` & `--until` múi giờ ICT UTC+7); loại bỏ tin chứa từ khóa cấm, live blog và tin đồn chuyển nhượng (song ngữ Việt/Anh); bóc tách text sạch qua `trafilatura` (có fallback RSS summary) và lọc ảnh lớn sạch không logo/watermark (`is_clean_large_image_url`, chặn `wm1-` và stock watermark). Lưu vào `WORK/temp_raw_news.json`.
- **Cách dùng**:
  - `python3 core/m1_scraper.py --period weekly` (tổng hợp trọn tuần trước 00:01 T2 -> 23:59 CN)
  - `python3 core/m1_scraper.py --period yesterday` (tổng hợp cả VN + Thế giới từ 12:00 trưa hôm qua đến hiện tại)
  - `python3 core/m1_scraper.py --period yesterday --region world` (chỉ quét báo Thế giới)
  - `python3 core/m1_scraper.py --since "2026-10-15 00:01" --until "2026-10-17 23:59"` (cào tin theo khoảng ngày tùy chọn)
  - `python3 core/m1_scraper.py --rss` (cào tự động 50 tin mới nhất từ các nguồn RSS)

### `m1b_llm_writer.py` — Tự động hóa Kịch Bản LLM & Sổ Chứng Cứ (Đã có — GĐ5a Ph2)
- **Mục đích**: Tự động chuyển đổi tin cào `WORK/temp_raw_news.json` thành kịch bản timeline `video_timeline.json` (OpenAI/Gemini/Anthropic hoặc fallback `mock_llm_call()` chuẩn 100%), tuân thủ semantic anchoring, bắt buộc trích nguồn báo, tự tải ảnh bìa vào `images_ready/`, và sinh Gói Duyệt Nội Dung `WORK/goi_duyet_noi_dung.md` phục vụ chủ kênh kiểm chứng trong 5 phút.
- **Cách dùng**:
  - `python3 core/m1b_llm_writer.py --project _tin_trong_ngay`
  - `python3 core/m1b_llm_writer.py --mock` (chạy thử nghiệm offline không gọi API)

### `m0_validate.py` — Kiểm tra tĩnh timeline
- **Mục đích**: Cổng chặn trước khi render. Kiểm tra schema, neo ngữ nghĩa (`trigger_word`), và phân bổ nhịp.
- **Cách dùng**: `python3 core/m0_validate.py <project>`

### `m2_timeline_builder.py` — Chuẩn hóa timeline (Nâng cấp tự động — GĐ5c)
- **Mục đích**: Chuẩn hóa timeline (`--normalize`), tự động parse các trường stringified JSON (`items`, `pillars`, `rows`, `parts`...), tự động sửa/neo lại `trigger_word` để khớp nguyên văn `script_text`, tự động bổ sung trường dữ liệu bắt buộc theo component spec (`kinetic-statement`, `stat-bento-trio`, `three-pillars`, `photo-card`).
- **Cách dùng**: `python3 core/m2_timeline_builder.py <project> --normalize`

### `m3_voice.py` — ViTTS Provider (Minh Quân Pro) (Đã có — GĐ4, nâng cấp v4.1 No-Cut)
- **Mục đích**: Sinh giọng đọc master `voiceover.wav` (lưu ngoài Drive trong `WORK/<project>/`) và dữ liệu `audio_sync.json`.
- **Đặc tính**: ViTTS v3turbo Minh Quân Pro (spd 1.12, pch 0.93, temp 0.6), trần `max_chars=768` phonemes chống cắt câu ngầm, thuật toán `_split_long_sentence` tách cú pháp tự nhiên (không index slice), khoảng thở `inter_sentence_pause=0.25s`, cache SHA-256 `v4.1_diemdoc_nocut`, sample-accurate timing.
- **Cách dùng**:
  - `python3 core/m3_voice.py <project>`
  - `python3 core/m3_voice.py <project> --scene 2`
  - `python3 core/m3_voice.py <project> --units units.json` (cho video phụ 9:16)
  - `python3 core/m3_voice.py <project> --no-cache`

### `m5_sync.py` — Đồng bộ phụ đề & Cue-Points (Đã có — GĐ4)
- **Mục đích**: Căn chỉnh mốc thời gian từng từ (`word_timestamps.json`), gom `karaoke_chunks` (44 ký tự 16:9 / 26 ký tự 9:16), neo `trigger_word` cho card, cập nhật `_start_time` và `_duration` cho từng scene.
- **Đặc tính**: Ground-truth alignment dựa trên text gốc; chạy Whisper-small theo batch trong tiến trình riêng giải phóng RAM; fallback syllabic tự động; cờ `--check` nghiệm thu tính đơn điệu và độ lệch.
- **Cách dùng**:
  - `python3 core/m5_sync.py <project>` (mặc định whisper-small)
  - `python3 core/m5_sync.py <project> --sync syllabic` (siêu tốc <0.1s)
  - `python3 core/m5_sync.py <project> --check`

### `m4_render.py` — Điều phối dựng hình
- **Mục đích**: Đọc timeline, gom nhóm cảnh, gọi engine Playwright Virtual Clock render JPEG pipe vào FFmpeg. Hỗ trợ cache theo hash từng cảnh.
- **Cách dùng**:
  - `python3 core/m4_render.py <project>`
  - `python3 core/m4_render.py <project> --preview` (15fps)
  - `python3 core/m4_render.py <project> --scene 2` (1 cảnh)
  - `python3 core/m4_render.py <project> --force` (bỏ cache)

### `m5_qa.py` — Kiểm duyệt chất lượng 4 tầng
- **Mục đích**: Bốn tầng QA: L1 schema, L2 layout, L3 vision (`--shots` sinh contact sheet), L4 nội dung.
- **Cách dùng**: `python3 core/m5_qa.py <project> --shots`

### `m6_compose.py` — Ghép nối & Xử lý âm thanh Master (Đã nâng cấp — GĐ4)
- **Mục đích**: Nối các video cảnh bằng "cut" (`concat -c copy`), dựng âm thanh master MỘT LẦN từ `voiceover.wav` liên tục, tạo single SFX track, tạo BGM playlist acrossfade (fade-in 1.5s, fade-out 3s), ducking qua `sidechaincompress`, và chuẩn hoá 2-pass loudnorm YouTube (`-14.0 LUFS`, True Peak $\le -1.0$ dBTP). Nghiệm thu lệch video-audio $\le 1$ frame.
- **Cách dùng**:
  - `python3 core/m6_compose.py <project>`
  - `python3 core/m6_compose.py <project> --bgm-pool sports_hype`

### `m7_publish.py` — Đóng gói xuất bản
- **Mục đích**: Xuất video hoàn chỉnh, sinh bộ 3 ảnh thumbnail 16:9 (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`) hoặc 1 ảnh 9:16, và tạo mô tả SEO `mota.txt`.
- **Cách dùng**: `python3 core/m7_publish.py <project>`

### `m8_news_bridge.py` — Cầu nối dữ liệu Thethao.json sang Timeline HTML v2
- **Mục đích**: Đọc dữ liệu từ `thethao.json` và thư mục `images/` (đã qua lọc của pipeline PIL), sắp xếp ảnh chuẩn xác theo số thứ tự, trích xuất danh sách câu, phân bổ hình ảnh chống lặp ảnh liền kề. Hỗ trợ hiển thị 3 ảnh trong 1 khung hình (Triptych) cho tiêu đề mở đầu và hiển thị 1 ảnh đơn lẻ với hòa trộn chuyển cảnh (crossfade) cho từng câu. Tích hợp Kế hoạch ngày (Daily Plan) xác định (deterministic) xoay vòng bố cục chống trùng lặp, định dạng chip ngày bắt buộc tiếng Việt, lọc nguồn ảnh sạch và ticker `TIN TIẾP THEO`.
- **Lia ảnh toàn cảnh 9:16 (Panoramic Full-Span Pan)**: Hàm `compute_pan_params` tính toán hành trình lia quét camera tự động qua 90-95% chiều rộng ảnh (`travel = 600 - 1350px`) với tốc độ điện ảnh 400-550 px/s và đổi chiều xen kẽ (`dir_toggle`), bám sát các pha bóng trên sân mà không bao giờ lộ viền đen hay bị chậm rì rì.
- **Đồng bộ thời gian Audio-Ground-Truth (100% không dùng Whisper)**: Mốc câu tính trực tiếp từ độ dài audio thực tế kết hợp bù trừ `audio_title` + 0.8s silence và dò khoảng lặng `silencedetect` của ffmpeg (vết cắt trùng khoảng lặng thật $\pm 0$ms, cumulative drift = 0). Mốc từ bên trong từng câu được nội suy theo trọng số âm tiết tiếng Việt mở rộng (chuẩn hóa số, từ viết tắt) và dấu câu (nghỉ dấu phẩy, chấm).
- **Hỗ trợ 2 Chế Độ Shorts Nâng Cao & Truyền Dữ Liệu Đồ Thị `sentence_charts`**:
  - `build_news_timeline()` & `build_focus_short_timeline()`: Hỗ trợ gắn cấu hình `sentence_charts` theo chỉ số câu (`sent.chart`) để hiển thị đồ thị số liệu Cyber-Stadium trực tiếp trên từng câu nội dung thay cho khung ảnh đơn thuần.
  - `build_focus_short_timeline()`: Gộp 3-5 tin chi tiết thành 1 video 9:16 trên template `short_news_v2.html`, chuyển tin mượt mà với hero title card + whoosh (~0.4s), cập nhật category pill/credit theo từng tin.
  - `build_digest_short_timeline()`: Đọc lướt nhanh các tin (5-7s/tin) trên template `short_digest_v2.html`, 1 ảnh nét nhất + tiêu đề lớn + câu tóm tắt $\le 25$ từ đọc bằng ViTTS Minh Quân Pro + karaoke nhảy từng từ, âm thanh được chuẩn hóa 2-pass loudnorm YouTube.
- **Cách dùng**: Được gọi tự động từ `run_day.py` khi dùng cờ `--engine html --shorts focus|digest|all`.

### `build_shorts_17_11.py` & `collect_shorts_images_17_11.py` — Dựng Trọn Bộ 3 Video Shorts Tin Tổng Hợp (17.11.2026)
- **Mục đích**:
  + `collect_shorts_images_17_11.py`: Bóc tách kịch bản viết liền thành từng câu và các phân đoạn chủ thể, tìm và tải 82 ảnh tư liệu sắc nét qua DDGS (lọc sạch watermark/stock rác), cập nhật `thethao.json`, `image_plan.json`, `image_credits.json` và xuất 4 bảng đối chứng Contact Sheet QA.
  + `build_shorts_17_11.py`: Điều phối dựng tuần tự 3 video shorts tin tổng hợp (Quốc tế 1: Nam #15; Quốc tế 2: Nam #15; Việt Nam: Nữ #14) qua ViTTS v3turbo, Playwright Virtual Clock + GSAP deterministic trên template `short_news_v2.html`, tự động gắn Outro 5s, căn chỉnh A/V drift <= 1 frame, xuất Thumbnail 9:16 Cyber-Stadium và mô tả YouTube SEO `_mota.txt`.
- **Cách dùng**:
  - `python3 -B core/collect_shorts_images_17_11.py`
  - `python3 -B core/build_shorts_17_11.py` (dựng trọn bộ cả 3 video)
  - `python3 -B core/build_shorts_17_11.py --only 1` (chỉ dựng tin 1)

### `build_shorts_04_05.py` & `build_short_thumbnails.py` — Sản xuất Video Shorts & Thumbnails Typographic 9:16
- **Mục đích**: Tự động sinh giọng đọc ViTTS Minh Quân Pro, tính toán nhịp đọc, render video Playwright Chromium (9:16, 1080x1920) với hiệu ứng lia ảnh ngang full chiều cao 1430px, sub Karaoke cố định 48px và render bộ ảnh thumbnail dọc typographic chuẩn đồ họa Anton/Oswald.
- **Cách dùng**:
  - `python3 core/build_shorts_04_05.py`
  - `python3 core/build_short_thumbnails.py`

### `build_ronaldo_images.py` — Bộ thu thập ảnh tư liệu video chuyên đề (Mới — 25.10.2026)
- **Mục đích**: Chia kịch bản 9 cảnh chuyên đề Cristiano Ronaldo thành từng câu, sinh kế hoạch ảnh (tiêu đề 3 ảnh; câu <42 từ = 1; 42–65 từ = 2; >65 từ = 3), tìm ảnh qua DDGS (`size=Large`, `layout=Wide`), lọc ảnh ngang `W/H ≥ 1.18` và rộng `≥ 800px`, chặn ~40 nguồn rác/watermark (alamy, getty, vecteezy, ytimg, pinimg...), khử trùng lặp aHash (Hamming ≤ 6), sinh `kich_ban_tung_cau.txt` + `thethao.txt` + `thethao.json` + `image_plan.json` + contact sheet QA theo cảnh.
- **Cách dùng**:
  - `python3 -B core/build_ronaldo_images.py` (resume tự động theo slot)
  - `python3 -B core/build_ronaldo_images.py --force` (tải lại toàn bộ)
  - `python3 -B core/build_ronaldo_images.py --sheets` (chỉ sinh lại contact sheet)

### `build_text_audio_comparison.py` — Tạo bộ so sánh phát âm TTS text-audio
- **Mục đích**: Trích xuất toàn bộ danh sách tên riêng/thuật ngữ quốc tế trong kịch bản ngày, xuất file đối chiếu `danh-sach.txt` và sinh 3 luồng âm thanh so sánh (có gạch nối lúc đầu, không gạch viết liền, đọc thô nguyên bản) kèm khoảng nghỉ 0.9s giữa các từ.
- **Cách dùng**: `python3 core/build_text_audio_comparison.py`

### `build_messi_thumbnails_cinematic.py` — Render 3 Thumbnail 16:9 Cinematic Split cho Lionel Messi
- **Mục đích**: Tái tạo 3 Thumbnail 16:9 A/B/C theo phong cách Cinematic Split của video Ronaldo 25.10.2026 bằng Playwright và `templates/thumbnail_16x9_sports.html`.
- **Cách dùng**: `python3 core/build_messi_thumbnails_cinematic.py`

### `build_messi_shorts.py` — Dựng 2 Video Shorts 9:16 cho Lionel Messi (Tin 1 & Tin 2)
- **Mục đích**: Dựng 2 video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`), tự động xuất 2 thumbnail dọc và mô tả SEO vào `outputs/30.10.2026/shorts/`.
- **Cách dùng**: `python3 core/build_messi_shorts.py`

### `build_messi_shorts_03_04_05.py` — Dựng 3 Video Shorts 9:16 cho Lionel Messi (Tin 3, 4, 5)
- **Mục đích**: Dựng 3 video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`), tự động xuất 3 thumbnail dọc và mô tả SEO vào `outputs/30.10.2026/shorts/`.
- **Cách dùng**: `python3 core/build_messi_shorts_03_04_05.py`

### `build_short_51_the_do.py` — Dựng Video Short 9:16 Trận Đấu 51 Thẻ Đỏ Ở Brazil (04.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) về trận cầu kỷ lục thế giới 51 thẻ đỏ giữa Uberlandia và Mamore. Tự động xuất Thumbnail dọc Cyber-Stadium typographic Anton 130px, bảng đối chứng hình ảnh QA (`contact_scene_01.jpg`) và file mô tả SEO YouTube/TikTok vào `outputs/Orther/04.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_51_the_do.py`

### `build_short_de_miguel.py` — Dựng Video Short 9:16 Tưởng Nhớ Tiền Đạo Jesús de Miguel (04.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) tưởng nhớ tiền đạo Jesús de Miguel (Tenerife) đột ngột qua đời ở tuổi 30 sau tai nạn trên sân cỏ. Áp dụng kỹ thuật chuyển màu xám trắng (B&W) trang nghiêm cho ảnh chân dung cầu thủ, badge đôi tách biệt (`Nguồn: ...` góc trái và `Ảnh: ...` động theo từng ảnh góc phải), tự động xuất Thumbnail dọc Cyber-Stadium, bảng đối chứng hình ảnh QA (`contact_scene_02.jpg`) và file mô tả SEO vào `outputs/Orther/04.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_de_miguel.py`

### `build_short_doi_luat_de_miguel.py` — Dựng Video Short 9:16 Đề Nghị Đổi Luật Bóng Đá Sau Bi Kịch De Miguel (04.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) về làn sóng yêu cầu FIFA và IFAB đổi luật bảo vệ cầu thủ từ cựu thủ môn Colombia Nelson Ramos và trọng tài Tây Ban Nha Joan Fabregas sau bi kịch de Miguel. Tự động xuất Thumbnail dọc Cyber-Stadium typographic Anton 130px, bảng đối chứng hình ảnh QA (`contact_scene_03.jpg`) và file mô tả SEO vào `outputs/Orther/04.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_doi_luat_de_miguel.py`

### `build_short_bi_kich_va_cham.py` — Dựng Video Short 9:16 Những Bi Kịch Do Va Chạm Trên Sân Cỏ Thế Giới (04.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) tổng hợp các bi kịch va chạm đau lòng nhất lịch sử bóng đá (Jesús de Miguel, Raul Ramirez, Serhiy Perkhun, Choirul Huda, Akli Fairuz). Áp dụng kỹ thuật Memorial Grayscale (B&W) trang nghiêm cho các chân dung cầu thủ tử nạn, Lower-Third 2 góc động, xuất 1 tiêu đề duy nhất theo yêu cầu, Thumbnail dọc Cyber-Stadium và bảng đối chứng hình ảnh QA (`contact_scene_04.jpg`) vào `outputs/Orther/04.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_bi_kich_va_cham.py`

### `build_short_real_madrid_aek.py` — Dựng Video Short 9:16 Siêu Phẩm Phút 90+2 Real Madrid Thắng AEK Athens 3-2 (05.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) về chiến thắng lội ngược dòng nghẹt thở 3-2 của Real Madrid trước chủ nhà AEK Athens tại Champions League. Kịch bản bao quát trọn vẹn diễn biến cả trận (Koita mở tỷ số 12', Bellingham đánh gót 1-1 32', Pilios 2-1 75', Mbappé gỡ hòa 2-2 78', siêu phẩm nã đại bác 90+2 của Valverde), 12 ảnh hiện trường độ nét cao AP/Reuters/Getty Images, phân bổ ảnh xen kẽ theo câu, Lower-Third 2 góc động, xuất đúng 1 tiêu đề duy nhất theo yêu cầu người dùng, Thumbnail dọc Cyber-Stadium typographic Anton 115px và bảng đối chứng hình ảnh QA (`contact_scene_01.jpg`) vào `outputs/Orther/05.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_real_madrid_aek.py`

### `build_short_como_lens_9_1.py` — Dựng Video Short 9:16 Đội Bóng Của Cesc Fàbregas Thắng 9-1 Kỷ Lục Cúp C1 (05.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) về chiến thắng hủy diệt 9-1 của tân binh Como trước RC Lens tại Champions League. Kịch bản bao quát kỷ lục 9 bàn thắng sân khách đầu tiên lịch sử cúp C1, cân bằng kỷ lục thắng đậm nhất của Liverpool và Real Madrid, cú hat-trick của Anastasios Douvikas, khoảnh khắc Nico Paz giơ áo tri ân tiền đạo quá cố Jesús de Miguel, tài năng 18 tuổi Matteo Papaccioli nổ súng ngày ra mắt, và triết lý kiểm soát bóng đỉnh cao của Cesc Fàbregas. Tích hợp 12 ảnh hiện trường độ nét cao EPA/AP/Reuters/Getty Images/Cadena SER, phân bổ xen kẽ theo câu, Lower-Third 2 góc động, xuất 1 tiêu đề duy nhất theo yêu cầu, Thumbnail dọc Cyber-Stadium typographic Anton 130px và bảng đối chứng hình ảnh QA (`contact_scene_02.jpg`) vào `outputs/Orther/05.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_como_lens_9_1.py`

### `build_short_man_city_leipzig.py` — Dựng Video Short 9:16 Haaland Ghi Bàn Thứ 62 Giúp Man City Hạ Leipzig 3-2 (05.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) về màn rượt đuổi tỷ số kịch tính 5 bàn thắng giữa Man City và RB Leipzig tại Red Bull Arena. Kịch bản bao quát pha đệm bóng ấn định 3-2 phút 78 của Erling Haaland, cột mốc 62 bàn sau 61 trận Champions League, pha dọn cỗ của Elliot Anderson, cuộc đấu trí giữa Enzo Maresca và Martin Demichelis. Tích hợp 12 ảnh hiện trường độ nét cao AP/Getty Images/Reuters/The Guardian, phân bổ xen kẽ theo câu, Lower-Third 2 góc động, xuất 1 tiêu đề duy nhất theo yêu cầu, Thumbnail dọc Cyber-Stadium typographic Anton 115px và bảng đối chứng hình ảnh QA (`contact_scene_03.jpg`) vào `outputs/Orther/05.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_man_city_leipzig.py`

### `build_short_liverpool_fenerbahce.py` — Dựng Video Short 9:16 Thảm Họa Bóng Chết Khiến Liverpool Thua Fenerbahce 2-3 (05.11.2026)
- **Mục đích**: Dựng video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) về thất bại sốc 2-3 của Liverpool trước Fenerbahce tại chảo lửa Sukru Saracoglu. Kịch bản bao quát bàn mở tỷ số lịch sử của sao mai 19 tuổi Trey Nyoni, bàn nâng tỷ số của Alexander Isak, cú sút phạt của Greenwood, sai lầm bóng bổng của hàng thủ The Reds, pha đánh đầu ấn định 3-2 của Vedat Muriqi, và chiến thắng ý nghĩa của HLV tạm quyền Dirk Kuyt. Tích hợp 12 ảnh hiện trường độ nét cao AP/Getty Images/The Guardian, phân bổ xen kẽ theo câu, Lower-Third 2 góc động, xuất 1 tiêu đề duy nhất theo yêu cầu, Thumbnail dọc Cyber-Stadium typographic Anton 130px và bảng đối chứng hình ảnh QA (`contact_scene_04.jpg`) vào `outputs/Orther/05.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_liverpool_fenerbahce.py`

### `build_shorts_02_11.py` — Dựng Trọn Bộ 8 Video Shorts 9:16 (02.11.2026)
- **Mục đích**: Dựng 8 video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`) theo 8 chủ đề tuyển chọn từ bản tin tuần (Harry Kane, Messi & Ronaldo, Malaysia, Man Utd, Man City & Arsenal, HLV Popov, CLB CAHN, U17 Việt Nam). Hỗ trợ tính toán lia ảnh ngang (`pan_horizontal`), xuất 8 thumbnail dọc Cyber-Stadium và 8 file mô tả SEO YouTube vào `outputs/02.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_02_11.py [id_shorts...]`

### `build_digest_25_tin.py` — Dựng Video Shorts "Tin Nhanh Thể Thao: 25 Tin" 9:16
- **Mục đích**: Dựng video đọc lướt nhanh toàn cảnh 25 tin thể thao tuần qua trên HTML engine v2 (`short_digest_v2.html`). Nội dung 25 tin được biên tập rõ ràng, cụ thể số liệu; tích hợp pill đếm tin động (`TIN 01/25` đến `TIN 25/25`), Cyber-Stadium Cyan neon, audio ducking và whoosh SFX chuyển cảnh mượt mà. Xuất thumbnail dọc và mô tả SEO với 25 timestamps vào `outputs/02.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_digest_25_tin.py`

### `build_messi_shorts_06_to_09.py` — Dựng 4 Video Shorts 9:16 cho Lionel Messi (Tin 6, 7, 8, 9)
- **Mục đích**: Dựng 4 video dọc chuẩn 1080x1920 @ 30fps trên HTML engine v2 (`short_news_v2.html`), tự động xuất 4 thumbnail dọc và mô tả SEO vào `outputs/30.10.2026/shorts/`.
- **Cách dùng**: `python3 core/build_messi_shorts_06_to_09.py`

### `build_short_ronaldo_gia_tu.py` — Dựng Video Short 9:16 Ronaldo Giã Từ ĐTQG (06.11.2026)
- **Mục đích**: Dựng video dọc 1080x1920 @ 30fps về sự kiện Cristiano Ronaldo chính thức giã từ đội tuyển Bồ Đào Nha sau 23 năm (234 trận, 146 bàn thắng), trao lại áo số 7 và từ chối trận tri ân của FPF. Xuất video, thumbnail và mota tại `outputs/Orther/06.11.2026/shorts/`.
- **Cách dùng**: `python3 core/build_short_ronaldo_gia_tu.py`

### `build_short_goc_khuat_ronaldo_jesus.py` — Dựng Video Short 9:16 Góc Khuất Ronaldo & HLV Jorge Jesus (06.11.2026)
- **Mục đích**: Dựng video dọc 1080x1920 @ 30fps về cuộc khủng hoảng rạn nứt giữa Ronaldo và HLV Jorge Jesus, Ronaldo phớt lờ HLV trước ngày công bố danh sách, Chủ tịch Andorinha tố HLV phản bội và làn sóng tri ân. Xuất video, thumbnail và mota tại `outputs/Orther/06.11.2026/shorts/`.
- **Cách dùng**: `python3 core/build_short_goc_khuat_ronaldo_jesus.py`

### `build_short_cycle_ball.py` — Dựng Video Short 9:16 Bóng Đá Trên Xe Đạp Cycle-Ball (07.11.2026)
- **Mục đích**: Dựng video dọc 1080x1920 @ 30fps về môn thể thao độc lạ Cycle-ball (Radball) vừa bế mạc giải vô địch thế giới 2026 tại Ludwigsburg, Đức với chức vô địch 8-1 của đội tuyển Áo. Sử dụng giọng nữ chính Ngọc Huyền Mẫu 14 (speed: 1.12, pitch: 1.10). Xuất video, thumbnail và mota tại `outputs/Orther/07.11.2026/shorts/`.
- **Cách dùng**: `python3 core/build_short_cycle_ball.py`

### `build_short_man_utd_khung_hoang.py` — Dựng Video Short 9:16 Khủng Hoảng Phong Độ Manchester United (07.11.2026)
- **Mục đích**: Dựng video dọc 1080x1920 @ 30fps về cuộc khủng hoảng phong độ và nghịch lý dứt điểm tại Manchester United (167 cú sút dẫn đầu Ngoại hạng Anh nhưng chỉ ghi 10 bàn, rơi xuống thứ 17 cận kề nhóm xuống hạng, Michael Carrick chịu áp lực nặng nề đúng dịp kỷ niệm 40 năm Sir Alex Ferguson cập bến Old Trafford, liên hệ Didier Deschamps, và phát ngôn gây tranh cãi của tỷ phú Avram Glazer). Sử dụng giọng nam mới Minh Quân Pro Mẫu 15 (speed: 1.12, pitch: 0.93), 12 ảnh hiện trường độ nét cao AP/Reuters/Getty Images/Sky Sports, Lower-Third 2 góc động, 1 tiêu đề duy nhất trong mota.txt, Thumbnail dọc và QA contact sheet tại `outputs/Orther/07.11.2026/shorts/`.
- **Cách dùng**: `python3 core/build_short_man_utd_khung_hoang.py`

### `build_shorts_08_11.py` — Dựng Bộ Đôi Video Shorts 9:16 Ngày 08.11.2026 (Nottingham 3-1 Man City & MU Thứ 18)
- **Mục đích**: Tự động hóa sản xuất trọn bộ 2 video Short 9:16: (1) Địa chấn Nottingham Forest đè bẹp Manchester City 3-1 nhờ cú đúp của Liam Delap và bàn mở tỷ số của Jair Cunha; (2) Manchester United bị đẩy xuống vị trí thứ 18, chính thức rơi vào nhóm cầm đèn đỏ Ngoại hạng Anh. Sử dụng giọng nam Minh Quân Pro Mẫu 15, chuẩn âm lượng loudnorm -14.04 LUFS, True Peak <= -3.4 dBTP, 12 ảnh hiện trường HD mỗi tin, Lower-Third 2 góc động, 2 bảng ảnh đối chứng QA `contact_scene_01.jpg` & `contact_scene_02.jpg`, 2 thumbnail dọc Cyber-Stadium Anton 115px và file mô tả SEO YouTube 1 tiêu đề duy nhất tại `outputs/Orther/08.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_08_11.py`

### `build_shorts_09_11.py` — Dựng Bộ Đôi Video Shorts 9:16 Ngày 09.11.2026 (Man Utd 4-4 Aston Villa & Dư Chấn Hậu Đại Chiến)
- **Mục đích**: Tự động hóa sản xuất trọn bộ 2 video Short 9:16: (1) Trận rượt đuổi tỷ số 8 bàn thắng điên rồ Man Utd 4-4 Aston Villa tại Old Trafford, bàn gỡ phút 90+6 của Patrick Dorgu; (2) Dư chấn và tin bên lề: Unai Emery bực tức bỏ về ở phút 96, tranh cãi bàn thua va chạm với thủ môn Zion Suzuki, Michael Carrick họp báo kiên quyết không từ chức, và MU dậm chân ở vị trí 18 nhóm rớt hạng. Giọng nam Minh Quân Pro Mẫu 15, chuẩn âm lượng loudnorm -14.04 LUFS, True Peak <= -3.6 dBTP, 12 ảnh hiện trường HD mỗi video, Lower-Third 2 góc động, 2 bảng đối chứng QA, 2 thumbnail dọc Anton 115px và file mô tả SEO YouTube 1 tiêu đề duy nhất tại `outputs/Orther/09.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_09_11.py`

### `build_short_alcaraz_paris_masters.py` — Dựng Video Short 9:16 Carlos Alcaraz Lần Đầu Vô Địch Paris Masters (09.11.2026)
- **Mục đích**: Tự động hóa sản xuất video Short 9:16 về chiến tích lịch sử của Carlos Alcaraz tại Paris Masters 2026 (hạ Ben Shelton 7-6, 7-5 sau 1h57p, cứu 4 break-point set một, ngược dòng set hai, trả món nợ US Open, đoạt danh hiệu Masters 1000 thứ 9 để sánh ngang Novak Djokovic và Rafael Nadal với kỷ lục 5 năm liên tiếp vô địch Masters, danh hiệu thứ 5 mùa giải 2026). Sử dụng giọng nam Minh Quân Pro Mẫu 15, chuẩn âm lượng loudnorm -14.04 LUFS, True Peak -3.09 dBTP, 12 ảnh hiện trường HD (AP/Reuters/Getty Images/ATP Tour), Lower-Third 2 góc động, bảng đối chứng QA `contact_scene_03.jpg`, thumbnail dọc Cyber-Stadium Anton 110px và file mô tả SEO YouTube 1 tiêu đề duy nhất tại `outputs/Orther/09.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_short_alcaraz_paris_masters.py`

### `build_digest_dual_voice.py` — Dựng Video Tin Nhanh 25 Tin Song Song Nam - Nữ (09.11.2026)
- **Mục đích**: Tự động hóa sản xuất video Short 9:16 đọc nhanh toàn cảnh 25 tin thể thao tuần qua (02/11 – 09/11/2026) qua 2 giọng đọc Nam (`Minh Quân Pro`) và Nữ (`Ngọc Huyền`) luân phiên (tin lẻ Nam, tin chẵn Nữ). Render qua `short_digest_v2.html` với bộ đếm tin, header cố định, Lower-Third 2 góc động và âm thanh đạt chuẩn EBU R128 (-14.42 LUFS, TP -1.36 dBTP, drift 0.7 ms). Xuất bản tại `outputs/09.11.2026/shorts/Short_Tin_Nhanh_25_Tin_Nam_Nu.mp4` kèm Thumbnail 9:16 và mô tả SEO.
- **Cách dùng**: `python3 -B core/build_digest_dual_voice.py`

### `build_short_01_ronaldo.py` — Dựng Focus Short 01 Ronaldo Giã Từ ĐTQG (09.11.2026)
- **Mục đích**: Tự động hóa sản xuất video Focus Short 9:16 gộp Tin 01 + Tin 02 từ bản tin tuần, nhấn mạnh góc nhìn "Tin nóng tuần qua" về quyết định giã từ ĐTQG Bồ Đào Nha và góc khuất rạn nứt giữa Cristiano Ronaldo với HLV Jorge Jesus. Render qua `short_news_v2.html` (80.13s), Lower-Third 2 góc động, chuẩn âm lượng -14.04 LUFS, TP -3.69 dBTP, drift 21.7 ms. Xuất bản tại `outputs/09.11.2026/shorts/Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG.mp4` kèm Thumbnail 9:16 và mô tả SEO.
- **Cách dùng**: `python3 -B core/build_short_01_ronaldo.py`

### `build_shorts_02_to_05.py` — Tự Động Hóa Dựng Bộ 4 Video Shorts (Short 2, 3, 4, 5) (09.11.2026)
- **Mục đích**: Tự động hóa sản xuất trọn bộ 4 video Shorts 9:16 gộp 2-3 tin từ bản tin tuần 09.11.2026 với nhãn "Tin nóng thể thao tuần qua", render qua `short_news_v2.html`, Lower-Third 2 góc động, chuẩn âm thanh EBU R128 (-14.06 LUFS, True Peak <= -2.6 dBTP, drift <= 0.7 ms). Xuất bản trọn bộ video, thumbnail 9:16 và mô tả SEO tại `outputs/09.11.2026/shorts/`:
  + Short 2 (Tin 7, 8, 10): Man City gục ngã, MU rơi nhóm đèn đỏ, Chelsea thua sốc (102.97s).
  + Short 3 (Tin 3, 4, 5): Cúp C1 điên rồ: Como thắng 9-1, Real Madrid & Haaland (103.37s).
  + Short 4 (Tin 16, 18, 21): Tuyển Việt Nam gọi Olaha Mạnh Đức, Công Phượng tỏa sáng (71.97s).
  + Short 5 (Tin 12, 13): Bi kịch đau lòng sân cỏ & Tiếng chuông cảnh tỉnh bóng đá (64.07s, Memorial Grayscale).
- **Cách dùng**: `python3 -B core/build_shorts_02_to_05.py --only 2,3,4,5`

### `build_unified_short.py` — Pipeline Dựng Video Shorts Kịch Bản Thống Nhất Liền Mạch (10.11.2026)
- **Mục đích**: Sản xuất video Short 9:16 với kịch bản dẫn chuyện viết mới liền mạch từ đầu đến cuối (Unified Script, ~120-160 từ, 30-55s), thay vì chắp ghép thô các tin riêng lẻ. Tự động sinh giọng đọc ViTTS Minh Quân Pro mới 100%, nội suy âm tiết Karaoke 1-1, phân bổ ảnh động theo ngữ cảnh, Lower-Third 2 góc động (`📰 NGUỒN` + `📷 ẢNH`), chuẩn âm lượng EBU R128 (-14.03 LUFS, True Peak <= -1.6 dBTP, drift <= 0.7 ms), kết xuất Thumbnail dọc 9:16 Cyber-Stadium và File mô tả SEO YouTube 2 phần. Hỗ trợ chạy tuần tự từng video một.
- **Cách dùng**: `python3 -B core/build_unified_short.py --short <ID>` (hỗ trợ Short 6, 7, 8, 10).

### `build_shorts_10_11.py` — Dựng Bộ Đôi Video Shorts 9:16 Ngày 10.11.2026 (Mourinho vs Guardiola & FIFPRO World 11)
- **Mục đích**: Tự động hóa sản xuất trọn bộ 2 video Short 9:16: (1) Jose Mourinho chính thức xô đổ kỷ lục tỷ lệ thắng của Pep Guardiola tại La Liga với 77% sau 126 trận, dẫn dắt Real Madrid thắng 8 trận liên tiếp và nhận giải HLV xuất sắc nhất tháng 10; (2) Harry Kane (chủ nhân Quả bóng vàng) bất ngờ bị loại khỏi FIFPRO World 11 năm 2026 bởi Erling Haaland (28.4% vs 27.6%), trong khi Lionel Messi xác lập kỷ lục vô tiền khoáng hậu 18 lần góp mặt, Kylian Mbappé dẫn đầu bình chọn (46%) và Lamine Yamal lập kỳ tích 2 năm liên tiếp lọt đội hình tiêu biểu trước tuổi 20. Tích hợp giọng nam Minh Quân Pro Mẫu 15, chuẩn âm lượng loudnorm -14.04 LUFS, True Peak <= -3.1 dBTP, 12 ảnh hiện trường HD mỗi video, Lower-Third 2 góc động, 2 bảng đối chứng thị giác QA (`contact_scene_01.jpg` & `contact_scene_02.jpg`), 2 thumbnail dọc Cyber-Stadium Anton (105px & 95px) và file mô tả SEO YouTube 1 tiêu đề duy nhất tại `outputs/Orther/10.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_10_11.py`

### `build_shorts_11_11.py` — Dựng Bộ Ba Video Shorts 9:16 Ngày 11.11.2026 (Man Utd, Stephanie Case & Trịnh Thu Vinh)
- **Mục đích**: Tự động hóa sản xuất trọn bộ 3 video Short 9:16: (1) Sir Jim Ratcliffe triệu tập Jason Wilcox và Omar Berrada tới Monaco họp bàn sa thải Michael Carrick trước thềm đại chiến Liverpool; Paul Merson chỉ trích MU "xây nhà trên vũng nước" (Giọng Nam: Minh Quân Pro Mẫu 15); (2) Stephanie Case - người phụ nữ đầu tiên chạy 100 dặm (160,93 km) giữa âm 35 độ C tại Nam Cực trong 24h31p, phá kỷ lục nam hơn 5 giờ (Giọng Nữ: Ngọc Huyền Mẫu 14); (3) Trịnh Thu Vinh đoạt HC bạc 25m súng ngắn nữ thế giới 2026 tại Qatar, trở thành VĐV Việt Nam đầu tiên giành vé dự Olympic Los Angeles 2028 (Giọng Nữ: Ngọc Huyền Mẫu 14). Tích hợp kiến trúc TTS v4.1 không cắt câu, 36 ảnh HD 100% sạch watermark, Lower-Third 2 góc động, 3 bảng đối chứng thị giác QA (`contact_scene_01.jpg`, `02.jpg`, `03.jpg`), 3 thumbnail dọc Cyber-Stadium Anton và 3 file mô tả SEO YouTube 1 tiêu đề duy nhất tại `outputs/Orther/11.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_11_11.py`

### `build_shorts_11_11_p2.py` — Dựng Bổ Sung 2 Video Shorts 9:16 Ngày 11.11.2026 (CLB Long An & 5 Ứng Viên Man Utd)
- **Mục đích**: Tự động hóa sản xuất Tin #05 (Giọng Nữ Ngọc Huyền Mẫu 14 — VFF đình chỉ vô thời hạn nhóm bán độ CLB Long An, 14 ảnh HD sạch, 48.17s, -14.02 LUFS) và Tin #06 (Giọng Nam Minh Quân Pro Mẫu 15 — 5 ứng viên sáng giá kế nhiệm Michael Carrick tại Man Utd, 16 ảnh HD sạch, 53.80s, -14.04 LUFS) qua `diemdoc.publisher`, `m8_news_bridge` và `short_news_v2.html`. Tự động hợp nhất an toàn `thethao.json`, `image_credits.json`, `image_plan.json` (bảo toàn Tin #01..#04), xuất bảng đối chứng `contact_scene_05.jpg` & `06.jpg`, Thumbnail dọc 9:16 (`publisher.render_thumbnail_9x16`) và Mô tả SEO 2 phần (`publisher.write_mota_9x16`) tại `outputs/Orther/11.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_11_11_p2.py`

### `build_shorts_12_11.py` — Dựng Bộ Đôi Video Shorts 9:16 Ngày 12.11.2026 (Việt Nam 2-0 Đài Loan & HLV Park Hang-seo)
- **Mục đích**: Tự động hóa sản xuất qua `diemdoc.short_batch`: Tin #01 (Giọng Nam Minh Quân Pro Mẫu 15 — Đội tuyển Việt Nam thắng thuyết phục Đài Loan 2-0 tại sân Thiên Trường ngày 11/11, 5 tân binh đá chính, Olaha Mạnh Đức & Đình Bắc ghi bàn, 14 ảnh VnExpress sạch, 43.50s, -14.02 LUFS) và Tin #02 (Giọng Nữ Ngọc Huyền Mẫu 14 — HLV Park Hang-seo nhận án cấm 2 trận & phạt 13.333 baht dù đứng ra bảo vệ học trò John Baggio trước lời miệt thị ở Thai League 2, 14 ảnh sạch, 51.17s, -14.02 LUFS). Xuất trọn bộ video MP4 9:16, bảng đối chứng QA (`contact_scene_01.jpg`, `02.jpg`), Thumbnail dọc Cyber-Stadium và Mô tả SEO 2 phần tại `outputs/Orther/12.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_12_11.py`

### `build_shorts_12_11_p2.py` — Dựng Video Short 9:16 Tin #03 Ngày 12.11.2026 (Gerrard: Yamal Hay Hơn Messi & Ronaldo Ở Tuổi 19 + 3 Đồ Thị DataViz)
- **Mục đích**: Tự động hóa sản xuất Tin #03 (Giọng Nam Minh Quân Pro Mẫu 15) qua `diemdoc.short_batch` & `short_news_v2.html`, kết hợp 15 ảnh tư liệu sạch và **3 cảnh đồ thị dữ liệu động Cyber-Stadium DataViz** (bảng màu dark-mode đã kiểm chứng `validate_palette.py`: `#0095D6`, `#C98500`, `#D55181`) gồm `grouped_race` (73 bàn & 69 kiến tạo), `duel_stack` (Yamal 142 G+A vs Messi+Ronaldo 94 G+A cộng lại), và `trophy_race` (8 danh hiệu lớn gồm Euro 2024, World Cup 2026, 3 La Liga, 2 Siêu cúp TBN, 1 Cúp Nhà vua), Lower-Third động `📊 ĐỒ HỌA` / `📷 ẢNH`, `contact_scene_03.jpg`, Thumbnail 9:16 và Mô tả SEO YouTube tại `outputs/Orther/12.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_12_11_p2.py`

### `build_shorts_12_11_p3.py` — Dựng Bổ Sung 2 Video Shorts 9:16 Tin #04 & Tin #05 Ngày 12.11.2026 (Mỹ Rút U17 World Cup & Quang Liêm 99%)
- **Mục đích**: Tự động hóa sản xuất qua `diemdoc.short_batch`: **Tin #04** (`58.43s`, Giọng Nam Minh Quân Pro Mẫu 15, `I = -14.02 LUFS`, `TP = -1.76 dBTP`, Drift `10.7 ms`, 14 ảnh sạch `contact_scene_04.jpg` về việc Mỹ rút khỏi VCK U17 World Cup 2026 tại Qatar, án phạt FIFA từ 20000 franc Thụy Sĩ và lịch đấu bảng G của U17 Việt Nam) và **Tin #05** (`51.63s`, Giọng Nữ Ngọc Huyền Mẫu 14, `I = -14.02 LUFS`, `TP = -2.83 dBTP`, Drift `7.7 ms`, 12 ảnh sạch `contact_scene_05.jpg`, 6 avatar kỳ thủ bảng B kèm **2 đồ thị DataViz động `grouped_race`** về chiến thắng độ chính xác 99% trước Artemiev & bảng xếp hạng Bảng B Elo 2735). Hợp nhất an toàn cùng Tin #01–#03 và xuất Thumbnail 9:16 + Mô tả SEO tại `outputs/Orther/12.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_12_11_p3.py`

### `build_shorts_13_11.py` — Dựng Bộ Đôi Video Shorts 9:16 Ngày 13.11.2026 (Pochettino Man Utd & U23 Việt Nam vs Singapore)
- **Mục đích**: Tự động hóa sản xuất qua `diemdoc.short_batch`: **Tin #01** (`45.88s`, Giọng Nam Minh Quân Pro Mẫu 15, `I = -14.00 LUFS`, `TP = -2.30 dBTP`, Drift `0.0 ms`, 13 ảnh sạch `contact_scene_01.jpg`, Opening Hook HUD 3s kích thích "10 TRIỆU USD" & đồ thị Cyber-Stadium DataViz `grouped_race` tỷ lệ thắng các đời HLV Man Utd hậu Sir Alex, vụ sa thải Michael Carrick và tâm thư 142 từ bị Rio Ferdinand chỉ trích) và **Tin #02** (`46.81s`, Giọng Nữ Ngọc Huyền Mẫu 14, `I = -14.02 LUFS`, `TP = -2.53 dBTP`, Drift `11.0 ms`, 13 ảnh sạch `contact_scene_02.jpg`, Opening Hook HUD 3s kích thích "70%" kiểm soát bóng & đồ thị DataViz `grouped_race` thống kê áp đảo toàn diện U23 Việt Nam vs U23 Singapore, siêu phẩm đánh gót phút 70 của Nguyễn Bảo Long và lời ca ngợi của HLV Firdaus Kassim). Xuất trọn bộ Thumbnail dọc 9:16 + Mô tả SEO 2 phần chuẩn mực tại `outputs/Orther/13.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_13_11.py`

### `build_shorts_14_11.py` — Dựng Bộ Ba Video Shorts 9:16 Ngày 14.11.2026 (Owono 12 Trận, Hà Lan 7-0 Hy Lạp & Phan Huy Hoàng HCV Cờ Tướng)
- **Mục đích**: Tự động hóa sản xuất qua `diemdoc.short_batch` (Giọng Nam Minh Quân Pro Mẫu 15 + tự động gắn Outro giọng Nữ, Opening Hook HUD 3s đầu + 5 SFX): **Tin #01** (`52.62s`, `I = -14.02 LUFS`, `TP = -5.17 dBTP`, Drift `16.0 ms`, 13 ảnh sạch `contact_scene_01.jpg` kèm Memorial Grayscale cho ảnh tưởng niệm Jesus de Miguel); **Tin #02** (`51.28s`, `I = -14.05 LUFS`, `TP = -4.07 dBTP`, Drift `11.3 ms`, 13 ảnh sạch `contact_scene_02.jpg`, đồ thị DataViz `grouped_race` Hà Lan 7-0 Hy Lạp với cờ `NL`/`GR`); và **Tin #03** (`48.79s`, `I = -14.00 LUFS`, `TP = -4.40 dBTP`, Drift `18.3 ms`, 13 ảnh sạch `contact_scene_03.jpg`, đồ thị DataViz bảng tổng sắp đồng đội Nam/Nữ với cờ `CN`/`VN`/`HK`/`MY`). Xuất trọn bộ Thumbnail 9:16 + Mô tả SEO 2 phần `_mota.txt` tại `outputs/Orther/14.11.2026/shorts/`.
- **Cách dùng**: `python3 -B core/build_shorts_14_11.py`

### `build_shorts_16_11.py` — Dựng Tuần Tự 3 Video Shorts Song Giọng Nữ/Nam Dưới 2 Phút Ngày 16.11.2026 (Argentina, Italia & Tây Ban Nha)
- **Mục đích**: Dựng tuần tự từng video Short 9:16 qua `diemdoc.short_batch` với cơ chế song giọng `voice_segments` (Đoạn đầu tường thuật trận đấu: Giọng Nữ Ngọc Huyền Mẫu 14; Đoạn sau bình luận chuyên môn: Giọng Nam Minh Quân Pro Mẫu 15) + Opening Hook HUD 3s đầu + 5 SFX + DataViz cờ SVG + Outro 9:16 tại `outputs/Orther/16.11.2026/shorts/`: **Tin #01** Argentina 1-2 Uruguay (`59.30s`, `-13.96 LUFS`, Drift `3.0 ms`, cờ `AR`/`UY`); **Tin #02** Bỉ 4-1 Italia (`61.92s`, `-14.33 LUFS`, Drift `21.0 ms`, cờ `BE`/`IT`); và **Tin #03** Tây Ban Nha 2-3 Anh (`61.51s`, `-13.99 LUFS`, Drift `9.0 ms`, cờ `ES`/`ENG`).
- **Cách dùng**: `python3 -B core/build_shorts_16_11.py --only 1` (lần lượt `1`, `2`, `3`)

### `build_digest_16_11.py` — Dựng Video Short "Bản Tin Nhanh 26 Tin" Tuần 16.11.2026 (`< 3 Phút` Gồm Outro)
- **Mục đích**: Biên tập mới hoàn toàn 26 câu thoại tin nhanh (`shorts/digest_script_16_11.json`, không tái sử dụng văn bản/audio của bản tin dài), phân giọng theo khu vực (**Quốc tế `01..14, 25..26`**: Giọng Nam `Minh Quân Pro Mẫu 15`; **Việt Nam `15..24`**: Giọng Nữ `Ngọc Huyền Mẫu 14`) lưu vào `shorts/digest_audio/tin_01..26.wav`, tuyển chọn 26 ảnh ngang HD sắc nét kèm Contact Sheet `qa/contact_digest_16_11.jpg`, render `short_digest_v2.html` (`144.03s` thân) và ghép Outro Nữ `Outro_Short_3_Kinetic_Slam.mp4` thành `outputs/16.11.2026/shorts/Short_Tin_Nhanh_26_Tin.mp4` (`149.43s < 180s`, `I = -14.02 LUFS`, `TP = -3.91 dBTP`, Drift `9.66 ms`), kèm Thumbnail 9:16 và `_mota.txt`.
- **Cách dùng**: `python3 -B core/build_digest_16_11.py` (hoặc `--prep-only` để xuất kịch bản, QA ảnh & giọng đọc trước).

### Bộ Công Cụ Bản Tin Tuần 16.11.2026 (`weekly_16_11_data.py`, `prepare_weekly_16_11.py`, `fix_weekly_16_11_qa.py`, `generate_weekly_tts_16_11.py`, `build_weekly_16_11_video.py`, `build_thumbnails_09_11.py`)
- **Mục đích**: Sản xuất trọn gói Video Loại 1 (`weekly_digest` 16:9 `Tin-The-Thao-16-11.mp4`) cho tuần 09/11 – 15/11/2026 gồm 1 Intro song giọng mở màn (~29.23s cả bumper `logo/Intro.mp4`), 26 bản tin đọc luân phiên Nam (`primary`) / Nữ (`secondary`), 310 ảnh ngang HD sạch watermark (`--step1b` kiểm duyệt 2 vòng), ghép Cut-Concat với âm thanh PCM WAV chuẩn mẫu (`Drift = 0.00 ms`, `-14.01 LUFS`, `TP = -1.86 dBTP`) và `logo/Outro.mp4` (`6.50s`), xuất 3 ảnh bìa 16:9 (`build_thumbnails_09_11.py --day 16.11.2026`) + `mota.txt`.
- **Cách dùng**:
  - `python3 -B core/prepare_weekly_16_11.py`
  - `python3 -B core/fix_weekly_16_11_qa.py` & `python3 -B core/fix_weekly_16_11_qa.py --step1b`
  - `python3 -B core/generate_weekly_tts_16_11.py`
  - `python3 -B core/build_weekly_16_11_video.py --workers 3` (hoặc `--compose-only`)
  - `python3 -B core/build_thumbnails_09_11.py --day 16.11.2026`

### `build_short_outros.py` — Dựng 3 Mẫu Outro Cho Video Short 9:16 (5–8 Giây)
- **Mục đích**: Dựng bộ 3 mẫu Outro dọc `1080x1920 @ 30fps` lấy cảm hứng từ `logo/Outro.mp4` với 3 phong cách khác nhau: (1) `Outro_Short_1_Cyber_Pulse.mp4` (`6.50s`, Giọng Nữ Ngọc Huyền Mẫu 14), (2) `Outro_Short_2_Tactical_Broadcast.mp4` (`6.00s`, Giọng Nam Minh Quân Pro Mẫu 15), và (3) `Outro_Short_3_Kinetic_Slam.mp4` (`5.40s`, Giọng Nữ Ngọc Huyền Mẫu 14). Tích hợp ViTTS, sidechain ducking, SFX track, two-pass loudnorm (`-14 LUFS`), Playwright Virtual Clock + GSAP + `DDOverlay`, kiểm toán `audio_check.py` và xuất Contact Sheet QA tại `logo/short_outros/qa/contact_short_outros.jpg`.
- **Cách dùng**: `python3 -B core/build_short_outros.py`

### `build_short_quang_liem_v2.py` — Dựng Bản `-2` Tin #05 Với Opening Hook 3 Giây Đầu Kích Thích (12.11.2026)
- **Mục đích**: Tạo bản `-2` ([Short_Le_Quang_Liem_Thang_Van_Co_Chinh_Xac_99_Phan_Tram-2.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/Orther/12.11.2026/shorts/Short_Le_Quang_Liem_Thang_Van_Co_Chinh_Xac_99_Phan_Tram-2.mp4), `51.64s`, `I = -14.02 LUFS`, `TP = -2.06 dBTP`, Drift `7.7 ms`): giữ nguyên toàn bộ giọng đọc Ngọc Huyền Mẫu 14, câu 1–5 và 2 đồ thị DataViz của bản gốc, chỉ nâng cấp 3 giây đầu bằng `sent.hook` (Crash-Zoom, Micro-Shake, Flash, Scanline AI, 2 Shockwave Rings, HUD `0% -> 99%`, Tactical Pills nước 22 / nước 32, cắt nhanh 3 nhịp ảnh) kết hợp tầng SFX mở màn (`sub_drop_boom`, `bell_ping_highlight`, `whoosh_cinematic_1`, `pop_card`, `whoosh_cinematic_short`).
- **Cách dùng**: `python3 -B core/build_short_quang_liem_v2.py`

### `build_short_cubarsi_golden_boy.py` — Dựng Video Short 9:16 Pau Cubarsi Đoạt Giải Cậu Bé Vàng 2026 (10.11.2026)
- **Mục đích**: Tự động hóa sản xuất video Short 9:16 về chiến tích trung vệ 19 tuổi Pau Cubarsi đoạt giải Cậu bé Vàng Golden Boy 2026 do báo Tuttosport tổ chức.
- **Cách dùng**: `python3 -B core/build_short_cubarsi_golden_boy.py`

### `build_focus_short_*.py` — Bộ 6 Video Shorts Dẫn Chuyện Liền Mạch Ngày 16.11.2026 (9:16)
- **Mục đích**: Tự động hóa sản xuất trọn bộ 6 video YouTube Shorts 9:16 theo cấu trúc Dẫn chuyện Liền mạch (Unified Storytelling Narrative), áp dụng chuẩn phụ đề Karaoke không phiên âm qua `interpolate_sentence_words` và gom cụm từ thông minh `build_smart_karaoke_chunks`:
  1. `build_focus_short_golden_week.py`: Short 1 — Tuần lễ Vàng Thể thao Việt Nam (79.78s).
  2. `build_focus_short_generation_war_seamless.py`: Short 2 — Cuộc chiến thế hệ: Messi, Lamine Yamal & Harry Kane (60.05s).
  3. `build_focus_short_south_america_nightmare.py`: Short 3 — Đêm ác mộng của bóng đá Nam Mỹ (55.15s).
  4. `build_focus_short_human_limits.py`: Short 4 — Kỳ tích trí tuệ và ý chí con người (61.37s).
  5. `build_focus_short_coaches_drama.py`: Short 5 — Biến động băng ghế huấn luyện viên (66.18s).
  6. `build_focus_short_discipline_scandal.py`: Short 6 — Mặt tối sân cỏ: Bàn tay sắt VFF & Cú sốc kỷ luật (68.01s).
- **Cách dùng**: `python3 -B core/<tên_script>.py`

---

## Công Cụ Hệ Thống & Kiểm Toán

### `audio_check.py` — Kiểm toán âm thanh hậu kỳ (Đã có — GĐ4)
- **Mục đích**: Đo và nghiệm thu Integrated Loudness (I), True Peak (TP), Loudness Range (LRA), độ dìm nhạc nền BGM khi có giọng nói (Separation $\ge 18$ dB), và kiểm toán track SFX.
- **Cách dùng**: `python3 core/audio_check.py <project>`

### `pron_test.py` — Sinh mẫu nghe thử từ điển thể thao (Đã có — GĐ4)
- **Mục đích**: Tự động lấy các tên riêng/thuật ngữ thể thao rủi ro cao từ từ điển, sinh các file m4a đối chiếu vào `outputs/_samples/pron_test_XX.m4a` kèm bảng đánh giá `outputs/_samples/pron_test.md`.
- **Cách dùng**: `python3 core/pron_test.py`

### `doctor.py` — Bác sĩ hệ thống (Chẩn đoán 13 tiêu chí)
- **Mục đích**: Kiểm tra toàn diện môi trường Python, FFmpeg filters (`rubberband`, `loudnorm`, `xfade`, `sidechaincompress`, `acrossfade`), Playwright, Whisper cache, ViNeu-TTS package, bộ thư viện cào tin/audio, tài nguyên fonts/sfx/bgm/icons/logos, quy tắc Google Drive, và dung lượng ổ cứng.
- **Cách dùng**: `python3 core/doctor.py` (Exit code: 0 = PASS, 1 = FAIL).

### `clean.py` — Dọn dẹp cache an toàn (Safe Trash)
- **Mục đích**: Quét và chuyển các tệp cache render cũ, file JPEG/WAV trung gian trong `~/Library/Caches/DiemDoc` vào `~/.Trash/`.
- **Cách dùng**:
  - `python3 core/clean.py --dry-run` (kiểm tra trước dung lượng)
  - `python3 core/clean.py --apply` (thực hiện dọn dẹp)

---

### `patch_shorts_images_17_11.py` — Bộ công cụ vá & kiểm toán ảnh thể thao chuyên sâu (17.11.2026)
- **Mục đích**: Tự động rà soát, loại bỏ 100% ảnh dính watermark/logo bản quyền (`gettyimages`, `alamy`, `shutterstock`, `sky sports`...) và ảnh phi thể thao (rừng cây, e-commerce nền trắng). Sử dụng Tesseract OCR và phân tích tỷ lệ nền trắng/đen để thay thế ảnh đạt chuẩn 100%.
- **Cách dùng**: `python3 -B core/patch_shorts_images_17_11.py`

### Bộ Công Cụ Bản Tin Hằng Ngày 18.11.2026 (`daily_18_11_data.py`, `prepare_daily_18_11.py`, `generate_daily_tts_18_11.py`, `build_daily_18_11_video.py`, `build_mota_18_11.py`, `build_digest_18_11.py`)
- **Mục đích**: Sản xuất trọn gói Video Loại 1 16:9 (`Tin-The-Thao-18-11.mp4`, `808.47s` ≈ `13 phút 28 giây`, `266 MB`, `I = -14.02 LUFS`, `TP = -1.6 dBTP`, **A/V Drift `0.66 ms`**) và Video Short "Bản Tin Nhanh 17 Tin" 9:16 (`shorts/Short_Tin_Nhanh_17_Tin.mp4`, `124.77s < 180s` gồm Outro Nữ `Outro_Short_1_Cyber_Pulse.mp4`, `53 MB`, `I = -14.02 LUFS`, `TP = -4.01 dBTP`, **A/V Drift `17.32 ms`**, viết mới 17 câu thoại phân giọng Việt Nam Nữ `Ngọc Huyền` / Quốc tế Nam `Minh Quân Pro`) tại `outputs/18.11.2026/`. Xuất đầy đủ 3 Thumbnail 16:9 `thumbnail_A/B/C.jpg`, `mota.txt`, Thumbnail 9:16 + `_mota.txt` cho Short, 20 Contact Sheet QA + 9 QA video frames.
- **Cách dùng**:
  - `python3 -B core/prepare_daily_18_11.py`
  - `python3 -B core/generate_daily_tts_18_11.py`
  - `python3 -B core/build_daily_18_11_video.py --workers 2`
  - `python3 -B core/build_thumbnails_09_11.py --day 18.11.2026`
  - `python3 -B core/build_mota_18_11.py`
  - `python3 -B core/build_digest_18_11.py`

### Bộ Công Cụ Bản Tin Hằng Ngày 19.11.2026 (`daily_19_11_data.py`, `prepare_daily_19_11.py`, `fix_daily_19_11_qa.py`, `generate_daily_tts_19_11.py`, `build_daily_19_11_video.py`, `build_mota_19_11.py`, `build_digest_19_11.py`)
- **Mục đích**: Sản xuất trọn gói Video Loại 1 16:9 (`Tin-The-Thao-19-11.mp4`, `1038.27s` ≈ `17 phút 18 giây`, `344 MB`, `I = -14.01 LUFS`, `TP = -2.57 dBTP`, **A/V Drift `0.66 ms`**) gồm Intro song giọng không tiêu đề (`51.17s`, `hide_title: true`) + 18 bản tin luân phiên Nam/Nữ (`290` ảnh ngang HD 3–5 ảnh/câu trọng tâm kích hoạt đa khung `triptych`/`split`/`full`), và Video Short Tin Nhanh 18 Tin 9:16 (`shorts/Short_Tin_Nhanh_18_Tin.mp4`, `140.10s < 180s` gồm Outro Nữ `Outro_Short_1_Cyber_Pulse.mp4`, `58 MB`, `I = -14.02 LUFS`, `TP = -4.07 dBTP`, **A/V Drift `9.00 ms`**, Việt Nam Nữ `Ngọc Huyền` / Quốc tế Nam `Minh Quân Pro`). Xuất đầy đủ 3 Thumbnail 16:9 `thumbnail_A/B/C.jpg`, `mota.txt` 19 chapters, Thumbnail 9:16 + `_mota.txt`, và toàn bộ Contact Sheet QA + frame đối chứng (`outputs/19.11.2026/qa/`).
- **Cách dùng**:
  - `python3 -B core/prepare_daily_19_11.py`
  - `python3 -B core/fix_daily_19_11_qa.py`
  - `python3 -B core/generate_daily_tts_19_11.py`
  - `python3 -B core/build_daily_19_11_video.py --workers 2`
  - `python3 -B core/build_thumbnails_09_11.py --day 19.11.2026`
  - `python3 -B core/build_mota_19_11.py`
  - `python3 -B core/build_digest_19_11.py`

### Bộ Điều Phối Tổng Quát & Auto-QA (`daily_runner.py`, `qa_precheck.py`) — Nâng cấp 19.11.2026 & 20.11.2026
- **`qa_precheck.py`**: Bộ kiểm duyệt tự động trước khi render (< 2 giây) quét từ ngữ máy móc/hậu trường bị cấm, số hàng nghìn có dấu chấm, chất lượng/trùng lặp ảnh trong `image_plan.json`, độ dài từng dòng thumbnail (`<= 21` ký tự) và tiêu đề SEO (`<= 100` ký tự).
  - Cách dùng: `python3 -B core/qa_precheck.py --day <DD.MM.YYYY>`
- **`daily_runner.py`**: Bộ chạy bản tin ngày tổng quát 1 lệnh (thay thế việc nhân bản script theo từng ngày), tự động gọi Auto-QA, ViTTS, render chunk `video_only_output=True` + `h264_videotoolbox` + CDP screenshot (`--workers 3`), Cut-Concat PCM WAV `-14.0 LUFS` và render Thumbnail 16:9. Hỗ trợ `--cloud --shards 8` để đẩy phần TTS + Render lên GitHub Actions Matrix và tự động fallback về local nếu cần.
  - Cách dùng:
    + Chạy trên máy Mac: `python3 -B core/daily_runner.py --day <DD.MM.YYYY> --step all --workers 3`
    + Chạy phần nặng trên GitHub Cloud: `python3 -B core/daily_runner.py --day <DD.MM.YYYY> --cloud --shards 8`

### Bộ Điều Phối & Thực Thi Đám Mây GitHub Actions (`cloud_runner.py`, `cloud_worker.py`) — Mới 20.11.2026
- **`cloud_runner.py`**: Bộ điều phối đám mây (Zero-RAM Local Orchestrator) kết nối trực tiếp với repo Public `4Blank4/dd-render-worker`. Đóng gói dữ liệu nhẹ của ngày đang làm (`thethao.json`, `images/`...) vào `_cloud_job/payload/`, kích hoạt GitHub Actions Matrix (`1–15` máy ảo x 16 GB RAM chạy song song), tải thành phẩm theo **3 tầng ưu tiên (`dd-meta-thumbs` → `dd-video-deliverable` → `dd-audio-extras`, hỗ trợ `--skip-extras`)** về `outputs/` trên Google Drive, rồi **tự động xóa sạch `_cloud_job/` và xóa luôn Workflow Run / Artifacts trên GitHub** (Zero-Data Retention).
  - Cách dùng:
    + Khởi tạo/đồng bộ Engine lên GitHub: `python3 -B core/cloud_runner.py --init-repo`
    + Dựng Video Bản Tin Dài 16:9 trên GitHub (8 máy ảo song song): `python3 -B core/cloud_runner.py --day 20.11.2026 --mode daily_long --shards 8`
    + Dựng lô Video Shorts 9:16 trên GitHub: `python3 -B core/cloud_runner.py --day 20.11.2026 --mode short_batch --orther --shards 3`
    + Dựng Video Short Bản Tin Nhanh (Digest Short < 3 phút): `python3 -B core/cloud_runner.py --day 20.11.2026 --mode digest_short`
    + Dọn sạch dữ liệu tạm trên GitHub: `python3 -B core/cloud_runner.py --cleanup-only`
- **`cloud_worker.py`**: Worker thực thi bên trong máy ảo Ubuntu của GitHub Actions (`.github/workflows/cloud_render.yml`), xử lý phân mảnh (`--role shard`) và ghép nối tổng thành (`--role compose`) cho cả 3 chế độ `daily_long`, `short_batch` và `digest_short`.

### Bộ Công Cụ Sản Xuất Bản Tin Ngày 20.11.2026 (`daily_20_11_data.py`, `prepare_daily_20_11.py`, `apply_qa_fixes_20_11.py`, `build_mota_20_11.py`) — Mới 20.11.2026
- **`daily_20_11_data.py`**: Dữ liệu kịch bản & kế hoạch ảnh từng câu cho **Intro song giọng (`id=0`, `hide_title=True`) + 21 bản tin chọn lọc (`01..21`)** từ 12:00 19/11 đến sáng 20/11/2026, gán sẵn `stat_badges` tùy biến và phân bổ `1–5` slot ảnh/câu để kích hoạt đủ 9 layout.
- **`prepare_daily_20_11.py`**: Thu thập ảnh HD sạch (`W>=800, H>=450, W/H>=1.18`), gỡ `/thumb_w/\d+/` trên Tuổi Trẻ & Thanh Niên lấy ảnh gốc, giữ `stat_badges` trong JSON, xuất `outputs/20.11.2026/{intro_hook.json, thethao.json, image_plan.json, image_credits.json, thethao.txt, kich_ban_tung_cau.txt}` và dựng 22 bảng QA Contact Sheet + Overview (`qa/`).
- **`apply_qa_fixes_20_11.py`**: Áp dụng kết quả kiểm duyệt thị giác thủ công (thay `82` ảnh qua kiểm chứng Wikimedia/Bing/VnExpress/Tuổi Trẻ, cắt viền logo sát mép `22` ảnh, đảm bảo `0` ảnh thiếu và `0` trùng lặp liên tiếp), cập nhật lại JSON và tái dựng toàn bộ Contact Sheets.
- **`build_mota_20_11.py`**: Đọc `outputs/20.11.2026/_preview_v2/chapters_20_11.json` (22 chapters) và xuất `outputs/20.11.2026/mota.txt` chuẩn đuôi `| Điểm Đọc 20/11` qua `publisher.write_mota_16x9()`, đồng thời đồng bộ `Short_Tin_Nhanh_21_Tin_mota.txt` sang chuẩn 3 mạng xã hội (YouTube Shorts, Facebook Reels, TikTok).
- **`diemdoc/image_curator.py`**: Bộ máy thu thập và lọc ảnh HD sạch dùng chung (Wikimedia Commons API + Bing lọc từ khóa chủ thể bắt buộc + gỡ `/thumb_w/` + cắt viền logo mép).
- **Cập nhật lõi đi kèm (`clean.py`, `diemdoc/publisher.py`, `diemdoc/tts_text.py`, `qa_precheck.py`, `build_thumbnails_09_11.py`, `m1b_llm_writer.py`, `m8_news_bridge.py`, `daily_runner.py`)**:
  + `clean.py`: Mặc định `--days 0` (`--all --apply`) dọn sạch toàn bộ `~/Library/Caches/DiemDoc/` trước và sau mỗi tác vụ.
  + `diemdoc/publisher.py`: Chuẩn hóa hậu tố `| Điểm Đọc DD/MM` (hoặc `| Điểm Đọc Tuần`, `| Điểm Đọc`) cho Video Dài và 3 khối mô tả đa nền tảng (YouTube Shorts, Facebook Reels, TikTok) cho Video Short; bổ sung `compute_16x9_hero_font_size()`.
  + `diemdoc/tts_text.py` & `build_thumbnails_09_11.py`: Cache RAM từ điển viết tắt/phát âm và retry 3 lần chống lỗi Google Drive `Errno 89`.
  + `qa_precheck.py`: Phân biệt ảnh xen kẽ hợp lệ với lỗi trùng ảnh liên tiếp (`Adjacent Duplicate -> [FAIL]`), kiểm tra hậu tố `| Điểm Đọc` và 3 khối MXH.
  + `daily_runner.py` & `engines/html/renderer.py`: Giới hạn bitrate `h264_videotoolbox` (`-b:v 2600k -maxrate 3600k`) giúp video dài ~18 phút chỉ nặng `~360 MB` thay vì `2.2 GB`; bổ sung `--step mota`, `--step clean` và tự động dọn cache sau khi ghép video.

### Bộ Công Cụ Sản Xuất Bản Tin Ngày 21.11.2026 (`daily_21_11_data.py`, `prepare_daily_21_11.py`, `build_mota_21_11.py`) — Mới 21.11.2026
- **`daily_21_11_data.py`**: Dữ liệu kịch bản & 262 slot ảnh HD sạch cho **Intro song giọng (`id=0`, `hide_title=True`) + 19 tin chính độc lập (`01..19`) + Mục `20. CÁC TIN THỂ THAO KHÁC` (`voice_preset="secondary"`, 100% giọng Nữ Ngọc Huyền điểm 9 tin bên lề)**.
- **`prepare_daily_21_11.py`**: Thu thập ảnh từ `image_curator.py`, kiểm định và xuất bộ JSON đầu vào, `thumbnails_plan.json` A/B Test và 22 bảng QA Contact Sheet (`outputs/21.11.2026/qa/`).
- **`build_mota_21_11.py`**: Đọc `outputs/21.11.2026/_preview_v2/chapters_21_11.json` (21 chapters từ `00:00` đến `14:42`) và xuất `outputs/21.11.2026/mota.txt` chuẩn đuôi `| Điểm Đọc 21/11` qua `publisher.write_mota_16x9()`.

### Bộ Công Cụ Sản Xuất Bản Tin Ngày 22.11.2026 (`daily_22_11_data.py`, `prepare_daily_22_11.py`, `apply_qa_fixes_22_11.py`, `build_mota_22_11.py`, `prepare_digest_22_11.py`) — Mới 22.11.2026
- **`daily_22_11_data.py`**: Dữ liệu kịch bản & kế hoạch 271 slot ảnh HD sạch cho **Intro song giọng (`id=0`, `hide_title=True`) + 22 tin chính độc lập (`01..22`) + Mục `23. CÁC TIN THỂ THAO KHÁC` (`voice_preset="secondary"`, 100% giọng Nữ Ngọc Huyền điểm tin bên lề)** tổng hợp song hành báo VN & quốc tế (BBC, ESPN, Sky Sports, Guardian).
- **`prepare_daily_22_11.py`**: Thu thập ảnh từ `image_curator.py` (chặn `ftcdn.net`), xuất bộ JSON đầu vào (`intro_hook.json`, `thethao.json`, `image_plan.json`, `image_credits.json`), `thumbnails_plan.json` và 24 bảng QA Contact Sheet + Overview (`outputs/22.11.2026/qa/`).
- **`apply_qa_fixes_22_11.py`**: Áp dụng kết quả kiểm duyệt thị giác trên 24 Contact Sheet (thay thế ảnh stock/watermark/lỗi chủ đề, cắt viền logo, xử lý trùng kề) và tái dựng QA sheet đạt `0` lỗi, `0` cảnh báo.
- **`build_mota_22_11.py`**: Đọc `outputs/22.11.2026/_preview_v2/chapters_22_11.json` (24 chapters từ `00:00` đến `16:47`) và xuất `outputs/22.11.2026/mota.txt` chuẩn đuôi `| Điểm Đọc 22/11` qua `publisher.write_mota_16x9()`.
- **`prepare_digest_22_11.py`**: Tạo và kiểm định `outputs/22.11.2026/shorts/digest_specs.json` (22 tin nhanh: 8 tin VN giọng Nữ + 14 tin Quốc tế giọng Nam, cấu hình thumbnail 9:16 và metadata 3 MXH) để chạy `--mode digest_short` trên GitHub Cloud (`Short_Tin_Nhanh_22_Tin.mp4`, `147.200s < 180s`).

### Bộ Công Cụ Sản Xuất Bản Tin Ngày 23.11.2026 (`daily_23_11_data.py`, `prepare_daily_23_11.py`, `apply_qa_fixes_23_11.py`, `build_mota_23_11.py`, `prepare_digest_23_11.py`) — Mới 23.11.2026
- **`daily_23_11_data.py`**: Dữ liệu kịch bản chi tiết (5–6 câu/tin) & kế hoạch `165` slot ảnh HD sạch cho **Intro song giọng (`id=0`, `hide_title=True`) + 16 tin chính (`01..16`) + Mục `17. CÁC TIN THỂ THAO KHÁC` (`voice_preset="secondary"`, 100% giọng Nữ Ngọc Huyền điểm tin bên lề)** tổng hợp song hành báo VN & Quốc tế.
- **`prepare_daily_23_11.py`**: Tái sử dụng pipeline thu thập & Contact Sheet QA của `prepare_daily_22_11.py` cho `outputs/23.11.2026/`, xuất `thumbnails_plan.json` và 18 bảng QA Contact Sheet + Overview (`outputs/23.11.2026/qa/`).
- **`apply_qa_fixes_23_11.py`**: Áp dụng kết quả kiểm duyệt thị giác 18 bảng Contact Sheet (thay thế ảnh fallback sai/graphic/watermark, cắt mép logo, xử lý trùng ảnh kề) và tái dựng QA sheet đạt `0` lỗi, `0` cảnh báo.
- **`build_mota_23_11.py`**: Đọc `outputs/23.11.2026/_preview_v2/chapters_23_11.json` (18 chapters từ `00:00` đến `17:16`) và xuất `outputs/23.11.2026/mota.txt` chuẩn đuôi `| Điểm Đọc 23/11` qua `publisher.write_mota_16x9()`.
- **`prepare_digest_23_11.py`**: Tạo và kiểm định `outputs/23.11.2026/shorts/digest_specs.json` (16 tin nhanh: 6 tin VN giọng Nữ + 10 tin Quốc tế giọng Nam, cấu hình thumbnail 9:16 và metadata 3 MXH) để chạy `--mode digest_short` trên GitHub Cloud (`Short_Tin_Nhanh_16_Tin.mp4`, `127.733s < 180s`).

### Bộ Công Cụ Sản Xuất Bản Tin Tổng Hợp Tuần `Weekly-23.11.2026` (`weekly_23_11_data.py`, `prepare_weekly_23_11.py`, `build_mota_weekly_23_11.py`) — Mới 23.11.2026
- **`weekly_23_11_data.py`**: Dữ liệu kịch bản hợp nhất 6 ngày (`18–23.11.2026`) gồm **Intro song giọng (`id=0`, `hide_title=True`, 4 đoạn) + 20 chuyên đề tuần chi tiết (`01..20`) + Mục `21. CÁC TIN THỂ THAO KHÁC`**, kèm `stat_badges`, `source_refs` và ánh xạ ảnh theo câu `sentence_refs`.
- **`prepare_weekly_23_11.py`**: Tuyển chọn **`349` ảnh HD độc lập** từ `1447` ảnh nguồn của 6 ngày trong tuần (kiểm tra `ahash` + `center_crop_ahash` + `dhash` và lọc từ khóa `SENTENCE_INCLUDE_KEYWORDS`/`SCENE_EXCLUDES`), xuất bộ JSON đầu vào, `thumbnails_plan.json` (3 A/B Test cân 2 dòng) và 23 bảng QA Contact Sheet + Overview (`outputs/Weekly-23.11.2026/qa/`).
- **`build_mota_weekly_23_11.py`**: Đọc `outputs/Weekly-23.11.2026/_preview_v2/chapters_Weekly_23_11.json` (22 chapters từ `00:00` đến `22:26`) và xuất `outputs/Weekly-23.11.2026/mota.txt` chuẩn đuôi `| Điểm Đọc Tuần` qua `publisher.write_mota_16x9()`.
- **`prepare_digest_weekly_23_11.py`**: Tạo và kiểm định `outputs/Weekly-23.11.2026/shorts/digest_specs.json` gồm **Intro Hook ~5s (`is_intro=True`, 3 ảnh montage tiêu điểm `Tin_02_1`, `Tin_06_1`, `Tin_09_1`) + 20 tin tuần (`01–08` VN Nữ / `09–20` Quốc tế Nam)** để chạy `--mode digest_short` trên GitHub Cloud (`Short_Tin_Nhanh_Tuan_23_11.mp4`, `150.833s < 180s`).
- **`diemdoc/weekly_coverage.py`**: Kiểm toán độ phủ 7 ngày tuần trước (`00:01 Thứ Hai -> 23:59 Chủ Nhật`, công nhận bản tin `12:00 CN -> sáng T2` là dữ liệu ngày Chủ Nhật và chỉ rõ khoảng ngày/giờ thiếu để cào bổ sung Internet), xuất `date_chip` chuẩn `TUẦN 16–22.11 · CN 23.11.2026` dùng chung cho `daily_runner.py`, `m8_news_bridge.py` và `qa_precheck.py` (chặn `[FAIL]` nếu ghi sai khoảng tuần).
- **`build_weekly_thumb_sets_23_11.py`**: Trình dựng **2 bộ Thumbnail & Mô tả SEO hoàn toàn độc lập** cho Video Tuần (`Weekly-23.11.2026`) lưu tại `outputs/Weekly-23.11.2026/thumbnails_options/` (`bo_1_weekly_magazine/` & `bo_2_clash_impact/`), tách biệt hẳn phong cách video ngày `23.11.2026` và không ghi đè tệp gốc.

### Bộ Công Cụ Sản Xuất Bản Tin Ngày 24.11.2026 (`daily_24_11_data.py`, `prepare_daily_24_11.py`, `apply_qa_fixes_24_11.py`, `build_mota_24_11.py`, `prepare_digest_24_11.py`) — Mới 24.11.2026
- **`daily_24_11_data.py`**: Dữ liệu kịch bản cô đọng (3–5 câu/tin, chuẩn Anti-Bundling `AGENTS.md` 5.8) cho **Intro song giọng (`id=0`, `hide_title=True`) + 28 tin chính độc lập (`01..28`) + Mục `29. CÁC TIN THỂ THAO KHÁC` (`voice_preset="secondary"`, giọng Nữ Ngọc Huyền điểm tin bên lề)** tổng hợp từ `12:00 23/11` đến `08:55 24/11/2026`.
- **`prepare_daily_24_11.py`**: Tái sử dụng pipeline thu thập ảnh sạch & dựng 30 Contact Sheet QA + Overview (`outputs/24.11.2026/qa/`), lưu `thumbnails_plan.json` kèm thẻ ảnh riêng `cards` cho Kiểu 2 (`magazine_bento`) và `right_image` cho Kiểu 3 (`clash_diagonal`).
- **`apply_qa_fixes_24_11.py`**: Áp dụng kết quả kiểm duyệt thị giác 30 bảng Contact Sheet (thay sạch ảnh fallback lạc đề/e-commerce/watermark, cắt viền logo báo, giải quyết trùng ảnh kề) đạt `204/204` ảnh HD (`0` lỗi, `0` cảnh báo `qa_precheck.py`).
- **`build_mota_24_11.py`**: Đọc `outputs/24.11.2026/_preview_v2/chapters_24_11.json` (30 chapters từ `00:00` đến `19:29`) và xuất `outputs/24.11.2026/mota.txt` chuẩn đuôi `| Điểm Đọc 24/11` qua `publisher.write_mota_16x9()`.
- **`prepare_digest_24_11.py`**: Tạo và kiểm định `outputs/24.11.2026/shorts/digest_specs.json` (27 tin nhanh: 14 tin VN giọng Nữ + 13 tin Quốc tế giọng Nam, thumbnail 9:16 đồng nhất tiêu đề U17 Việt Nam, metadata 3 MXH) để chạy `--mode digest_short` trên GitHub Cloud (`Short_Tin_Nhanh_27_Tin.mp4`, `142.700s < 180s`).

### Bộ Công Cụ Sản Xuất Bản Tin Ngày 25.11.2026 (`daily_25_11_data.py`, `prepare_daily_25_11.py`, `build_mota_25_11.py`) — Mới 25.11.2026
- **`daily_25_11_data.py`**: Dữ liệu kịch bản cô đọng (chuẩn Anti-Bundling `AGENTS.md` 5.8) & `173` slot ảnh HD cho **Intro song giọng (`id=0`, `hide_title=True`) + 23 tin chính độc lập (`01..23`, luân phiên Nam/Nữ) + Mục `24. CÁC TIN THỂ THAO KHÁC` (`voice_preset="secondary"`, giọng Nữ Ngọc Huyền điểm tin bên lề)** tổng hợp từ `12:00 24/11` đến `08:20 25/11/2026` (gồm tin nóng CAHN thắng Vissel Kobe 3-1, U17 Việt Nam tăng bậc Top 8 hạng ba World Cup, Đại hội Thể thao toàn quốc 2026 với Ánh Viên/Thúy Hiền/Thùy Dung/Thùy Linh, Champions League Real thắng PSV 5-1 & Man City hòa Napoli 2-2 tri ân De Bruyne, CAS trả cúp AFCON cho Senegal, Ronaldo chạm mốc 987 bàn...).
- **`prepare_daily_25_11.py`**: Tái sử dụng pipeline `prepare_daily_22_11.py`, tự động cắt viền logo dưới 7–8% trên `15` ảnh báo Thanh Niên / Tuổi Trẻ / Xinhua có watermark, tái dựng 25 bảng QA Contact Sheet + Overview (`outputs/25.11.2026/qa/`) đạt `173/173` ảnh HD (`0` lỗi, `0` cảnh báo `qa_precheck.py`), và ghi `thumbnails_plan.json` đồng nhất 3 kiểu 16:9 (`cyber_split`, `magazine_bento`, `clash_diagonal`).
- **`build_mota_25_11.py`**: Đọc `outputs/25.11.2026/_preview_v2/chapters_25_11.json` (25 chapters từ `00:00` đến `16:47`) và xuất `outputs/25.11.2026/mota.txt` chuẩn đuôi `| Điểm Đọc 25/11` qua `publisher.write_mota_16x9()`.

