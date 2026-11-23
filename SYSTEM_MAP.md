# SYSTEM_MAP.md — Bản Đồ Kỹ Thuật Hệ Thống "Điểm Đọc" (DD-The-thao)

Tài liệu này là bản đồ kiến trúc toàn diện của hệ thống sản xuất video tin tức thể thao tự động **Điểm Đọc** (`DD-The-thao`). Bất kỳ AI Agent nào khi bắt đầu phiên làm việc đều đọc file này để nắm cấu trúc toàn bộ hệ sinh thái mà không cần quét thư mục.

---

## 1. Sơ Đồ Cấu Trúc Tổng Thể

```
DD-The-thao/
├── AGENTS.md               # Bộ quy tắc vận hành bắt buộc cho Agent
├── SYSTEM_MAP.md           # Bản đồ kỹ thuật & chỉ mục hệ thống (file này)
├── README.md               # Hướng dẫn nhanh khởi động
├── config/                 # Cấu hình kênh, giọng đọc, render, nguồn tin, âm thanh
│   ├── channel.json        # Tên kênh, màu nhận diện Cyber-Stadium, logo
│   ├── voice.json          # ViTTS v3turbo cấu hình 2 giọng: Nam chính (Minh Quân Pro #15) & Nữ thứ hai (Ngọc Huyền #14)
│   ├── audio.json          # Ducking sidechain, BGM pools, SFX, 2-pass loudnorm
│   ├── render.json         # Độ phân giải (16:9 & 9:16), 30fps, work_dir ngoài Drive
│   ├── sources.json        # Nguồn báo song hành Việt Nam (Thanh Niên, VnExpress, Tuổi Trẻ, Dân Trí...) & Thế giới (BBC Sport, ESPN, Sky Sports, Guardian Sport)
│   ├── fx.json             # Cấu hình hiệu ứng thị giác (sparkles, embers, light sweep, grid, grain)
│   └── shorts.json         # Cấu hình sản xuất shorts (focus, digest, trần giây, items/short)
├── spec/                   # Hợp đồng dữ liệu & định nghĩa thành phần
│   ├── schema.py           # Schema xác thực timeline, cards, engines (loại bỏ Manim)
│   ├── timeline_template.json # Khung mẫu video_timeline.json
│   └── MAP.md              # Chỉ mục thư mục spec
├── core/                   # Bộ công cụ thực thi pipeline
│   ├── m0_validate.py      # L1 schema validation cho timeline
│   ├── m1_scraper.py       # Cào & lọc tin thể thao RSS/URL, lọc 36h, chống tin sai (Đã có - GĐ5a)
│   ├── m1b_llm_writer.py   # Biên kịch LLM, semantic anchoring & Fact-Ledger (Đã có - GĐ5a Ph2)
│   ├── m2_timeline_builder.py # Chuẩn hóa và làm giàu timeline (--normalize)
│   ├── m3_voice.py         # ViTTS v3turbo Minh Quân Pro, chunk cache SHA-256 (Đã có - GĐ4)
│   ├── m4_render.py        # Điều phối render cảnh theo hash cache
│   ├── m5_sync.py          # Đồng bộ phụ đề Whisper-small & Syllabic fallback (Đã có - GĐ4)
│   ├── m5_qa.py            # Kiểm duyệt 4 tầng (L1 schema, L2 layout, L3 vision, L4 content)
│   ├── m6_compose.py       # Cut-concat, master audio, ducking, SFX track, loudnorm (Nâng cấp - GĐ4)
│   ├── m7_publish.py       # Đóng gói xuất bản video, thumbnail, mota.txt
│   ├── m8_news_bridge.py   # Cầu nối thethao.json + images sang timeline v2 đa layout (Mới - GĐ5c Ph2)
│   ├── build_shorts_04_05.py & build_short_thumbnails.py — Sản xuất Shorts & Thumbnails 9:16
│   ├── build_ronaldo_images.py # Bộ thu thập ảnh chuyên đề Ronaldo: chia câu, DDGS, lọc QA (Mới 25.10)
│   ├── run_day.py          # ★ Master Orchestrator: prepare & build (--workers N, resume cấp tin .run_state, --engine html v2)
│   ├── run.py              # CLI chính điều phối chuỗi tự động
│   ├── audio_check.py      # Kiểm toán âm thanh: I, TP, LRA, Separation >= 18 dB (Đã có - GĐ4)
│   ├── pron_test.py        # Sinh mẫu nghe thử từ điển thể thao 60 mục (Đã có - GĐ4)
│   ├── doctor.py           # Chẩn đoán sức khỏe hệ thống 13 tiêu chí (Nâng cấp - GĐ4)
│   ├── clean.py            # Dọn dẹp cache an toàn vào ~/.Trash/
│   ├── diemdoc/            # Gói thư viện tiện ích nền tảng
│   │   ├── paths.py        # Định tuyến đường dẫn, bảo vệ Drive, URL encoding
│   │   ├── tts_text.py     # Chuẩn hoá văn bản cho TTS & ánh xạ ngược Display
│   │   ├── unknown_names.py# Quét và phát hiện tên riêng chưa có trong từ điển
│   │   ├── whisper_batch_worker.py # Tiến trình con chạy Whisper giải phóng RAM
│   │   ├── log.py          # Hệ thống log màu chuẩn hóa
│   │   ├── jsonio.py       # Đọc/ghi JSON an toàn Unicode
│   │   ├── timeline.py     # Xử lý thao tác trên timeline object
│   │   ├── audio.py        # Xử lý âm thanh, ducking, BGM acrossfade, SFX, loudnorm 2-pass
│   ├── vendor/             # Thư viện mã nguồn nhúng độc lập
│   │   └── vieneu/         # ViNeu-TTS 3.8.1 phát sinh giọng đọc v3turbo nội bộ
│   │   └── VENDOR_INFO.md  # Thông tin chi tiết phiên bản vendored
│   └── MAP.md              # Chỉ mục thư mục core
├── engines/                # Các engine dựng hình đồ họa
│   ├── html/
│   │   ├── renderer.py     # Playwright Virtual Clock JPEG pipe vào FFmpeg
│   │   └── MAP.md
│   └── MAP.md
├── templates/              # Giao diện HTML & runtime đồ họa
│   ├── _runtime.js         # Runtime cơ bản & tương tác DOM
│   ├── _director.js        # Điều phối đồng hồ ảo window.__vt và timeline
│   ├── _cards.js           # Bộ dựng (renderers) cho các loại thẻ đồ họa
│   ├── _base.css           # Hệ thống CSS base, reset và typography
│   ├── long_cinematic.html # Mẫu giao diện 16:9 (1920x1080) video chính
│   ├── long_sports_news.html # ★ Template bản tin thể thao 16:9 chuyên dụng Điểm Đọc (Ken Burns + Credit badge)
│   ├── long_sports_news_v2.html # ★ Template v2 16:9 nâng cấp thị giác: GSAP deterministic, 3 layout xoay vòng, Ken Burns 4 kiểu
│   ├── short_swiss.html    # Mẫu giao diện 9:16 (1080x1920) phong cách sáng
│   ├── short_cinematic.html# Mẫu giao diện 9:16 (1080x1920) phong cách tối Cyber-Stadium
│   ├── short_news_v2.html  # ★ Template v2 9:16 nâng cấp thị giác Shorts: GSAP deterministic, 3 layout xoay vòng, tích hợp đồ thị động Cyber-Stadium DataViz (`grouped_race`, `duel_stack`, `trophy_race`)
│   ├── thumbnail_cinematic_split.html # Mẫu sinh ảnh thumbnail 9:16 cho Shorts/TikTok
│   ├── thumbnail_16x9_sports.html     # ★ Mẫu sinh 3 thumbnail 16:9 A/B/C cho YouTube
│   └── MAP.md              # Chỉ mục thư mục templates
├── design/                 # Hệ thống nhận diện thương hiệu & Token
│   ├── tokens.json         # Token thiết kế (màu, font, khoảng cách, bo góc)
│   ├── brands/             # Preset thương hiệu
│   │   ├── cinematic-dark.json # Cyber-Stadium Neon Dark (#070B14, #F59E0B, #06B6D4)
│   │   └── swiss-light.json    # Báo chí sáng chuẩn mực
│   └── MAP.md              # Chỉ mục thư mục design
├── assets/                 # Kho tài nguyên dùng chung
│   ├── vendor/             # Thư viện JS bên thứ ba tự chứa (gsap.min.js 3.15.0, CustomEase.min.js)
│   ├── fonts/              # 13 họ font chữ hoàn chỉnh (Inter, Roboto, Space Grotesk, Barlow Condensed, Be Vietnam Pro...)
│   ├── sfx/                # 28 hiệu ứng âm thanh (whoosh, pop, ding, transition...)
│   ├── bgm/                # 36 bản nhạc nền thể thao kịch tính, nhịp điệu
│   ├── icons/              # 58 biểu tượng SVG thể thao và kỹ thuật
│   ├── logo/               # Logo kênh Điểm Đọc (2 bản tròn PNG alpha + SVG wordmark)
│   ├── voices/             # Kho 2 bộ giọng đọc chuẩn: Nam chính (`male/`) & Nữ thứ hai (`female/`) kèm manifest `voices.json`
│   └── MAP.md              # Chỉ mục thư mục assets
├── node_modules/           # ★ Symlink kho thư viện dùng chung (<1GB): Three.js, GSAP, motionmaxxing, video-shotcraft (124 shot recipes), dataviz, antigravity-animation
├── .agents/skills/         # ★ Bộ 3 Agent Skills chuyên sâu: motionmaxxing, video-shotcraft-recipes, dataviz
├── data/                   # Từ điển phát âm và dữ liệu tĩnh
│   ├── pronunciation_sports.json # Phiên âm ~150 tên cầu thủ, HLV, CLB, thuật ngữ
│   └── MAP.md              # Chỉ mục thư mục data
├── projects/               # Thư mục chứa các dự án video cụ thể
│   ├── _selftest/          # Dự án mẫu phục vụ kiểm tra tự động và smoke test
│   ├── _longtest/          # Dự án kiểm thử tải dài 2.877 từ (~10 phút âm thanh)
│   ├── _tin_trong_ngay/    # Dự án mẫu video tin tổng hợp hằng ngày từ tin cào thật (GĐ5a Ph2)
│   └── MAP.md              # Chỉ mục thư mục projects
├── outputs/                # Thư mục đích nhận sản phẩm hoàn thiện cuối cùng
│   └── _samples/           # Mẫu kiểm thử âm thanh (speed, pron_test, demo_mix_60s)
├── _ref/                   # Kho mã nguồn và template tham khảo đã đóng gói
│   ├── Video-Thethao/      # Mã nguồn và template từ Video-Thethao cũ
│   ├── Video-TienDuy/      # Mã nguồn tham khảo từ Video-TienDuy
│   ├── Man-nhan/           # Mã nguồn tham khảo từ Man-nhan
│   └── MAP.md              # Chỉ mục thư mục _ref
├── docs/                   # Tài liệu kiến trúc và đo lường
│   ├── DECISIONS.md        # Toàn bộ quyết định kiến trúc đã chốt
│   ├── PROGRESS.md         # Nhật ký tiến độ và lộ trình các giai đoạn
│   ├── BENCHMARK.md        # Số liệu đo thử kỹ thuật, tải dài GĐ4 và dự báo tải
│   └── PHASE3_ADDENDUM.md  # Bổ sung kiểm toán GĐ3 và 5 câu hỏi quyết định
└── Thamkhao/               # Báo cáo giai đoạn 1 và 2 (00 đến 09, chỉ đọc)
```

---

## 2. Thông Số Kỹ Thuật Đã Chuẩn Hóa

| Hạng mục | Thông số chuẩn hóa | File cấu hình |
|---|---|---|
| Tên kênh | **Điểm Đọc** | `config/channel.json` |
| Bảng màu chính | Cyber-Stadium Dark (`#070B14`, `#F59E0B`, `#06B6D4`) | `config/channel.json` |
| Giọng đọc | ViTTS v3turbo `Minh Quân Pro` | `config/voice.json` |
| Bộ lọc âm thanh | `rubberband=pitch=0.85:tempo=1.15` | `config/voice.json` |
| Chuẩn âm lượng | loudnorm -14 LUFS (mức tham chiếu YouTube, True Peak `-1.0 dBTP`, `LRA=11`) | `config/audio.json` |
| Tỷ lệ phân tách BGM vs Giọng | Ducking `sidechaincompress`, separation $\ge 18$ dB | `config/audio.json` |
| Tốc độ khung hình | 30 fps (tùy chọn 60 fps) | `config/render.json` |
| Định dạng video chính | 16:9 (`1920x1080`), ~10 phút | `config/render.json` |
| Định dạng video phụ | 9:16 (`1080x1920`), ~2 phút (3 video/ngày) | `config/render.json` |
| Bộ nhớ đệm tạm thời | `~/Library/Caches/DiemDoc` (ngoài Google Drive) | `config/render.json` |
| Nguồn tin ưu tiên | Thanh Niên > VnExpress > Bongdaplus > Tuổi Trẻ > Dân Trí | `config/sources.json` |

---

## 3. Nhật Ký Nâng Cấp Hệ Thống (Changelog)

- **2026-11-23 (Hoàn Tất Video Bản Tin Thể Thao 16:9 Ngày 23.11.2026 Qua GitHub Cloud Matrix — Chi Tiết Sâu 16 Tin Chính & Mục Tin Bên Lề)**:
  - **Nội dung chi tiết & Kiểm duyệt Thị giác (`core/daily_23_11_data.py`, `core/prepare_daily_23_11.py`, `core/apply_qa_fixes_23_11.py`)**: Tổng hợp từ `12:00 22/11` đến `08:11 23/11/2026` qua `74` bài báo Việt Nam + `5` luồng RSS Quốc tế (`BBC Sport`, `BBC Football`, `ESPN`, `Sky Sports`, `The Guardian`) kèm đối chứng chéo web search. Cấu trúc Intro song giọng (`00`) + `16` bản tin chi tiết 5–6 câu (`01–16`) + mục `17. CÁC TIN THỂ THAO KHÁC` (100% giọng Nữ Ngọc Huyền). Soi thủ công toàn bộ `18` bảng Contact Sheet (`outputs/23.11.2026/qa/`), thay thế ảnh fallback/graphic/watermark, cắt viền logo, đạt `165/165` ảnh HD sạch (`0` lỗi, `0` cảnh báo `qa_precheck.py`).
  - **Sản xuất trên GitHub Cloud (`4Blank4/dd-render-worker`, 8 shards song song, Run #45095112882 -> đã tự động xóa sạch)**:
    + Video chính 16:9 [Tin-The-Thao-23-11.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/23.11.2026/Tin-The-Thao-23-11.mp4): `1920x1080 @ 30fps`, `h264`, thời lượng **`1115.227s`** (`18 phút 35,2 giây`), dung lượng **`481.61 MB`**, **`I = -14.04 LUFS`**, **`TP = -0.66 dBTP`**, `LRA = 1.90 LU`, **A/V Drift `0.14 ms`**.
    + Đầy đủ ấn phẩm đi kèm tại `outputs/23.11.2026/`: Bộ 3 Thumbnail A/B Test chuẩn 2 dòng (`thumbnail_A.jpg` `461.4 KB`, `thumbnail_B.jpg` `364.1 KB`, `thumbnail_C.jpg` `483.8 KB` + `thumbnail.jpg` tái xuất cục bộ đúng cấu hình `23.11`), mô tả SEO 2 phần (`mota.txt` từ `core/build_mota_23_11.py` với 18 chapters `00:00`–`17:16`, đuôi `| Điểm Đọc 23/11`) và bảng ảnh đối chứng `qa/video_qa_frames.jpg`.

- **2026-11-22 (Hoàn Tất Video Bản Tin Thể Thao 16:9 Ngày 22.11.2026 Qua GitHub Cloud Matrix & Mở Rộng Nguồn Báo Thế Giới / Bãi Bỏ Cố Định Số Tin)**:
  - **Cập nhật `AGENTS.md` (Mục 4 & Mục 5.8)**: Xóa bỏ quy định cứng `20–25 bản tin` / `TIN XX/25`, thiết lập quy tắc **Số lượng tin ĐỘNG 100%** theo mật độ sự kiện thực tế (không nhồi tin vặt cho đủ 18–20 bài, không cắt bỏ tin lớn vì chạm trần) và quy tắc **Bắt buộc quét song hành Báo Việt Nam + Báo Thể thao Thế giới** kèm đối chứng chéo số liệu.
  - **Mở rộng `config/sources.json`, `core/m1_scraper.py` & `core/diemdoc/image_curator.py`**: Bổ sung 5 nguồn RSS quốc tế (`BBC Sport`, `BBC Football`, `ESPN`, `Sky Sports`, `The Guardian Sport` với trường `region`/`lang`), nâng cấp `m1_scraper.py` hỗ trợ lọc `--region all|vn|world`, từ khóa chống gossip/live-blog tiếng Anh, `updated_parsed`, `fallback_pub_dt` và fallback RSS summary khi trang gốc reset TLS; thêm `ftcdn.net` vào `BLOCKED_DOMAINS` chặn ảnh Adobe Stock.
  - **Nội dung & Kiểm duyệt Thị giác (`core/daily_22_11_data.py`, `core/prepare_daily_22_11.py`, `core/apply_qa_fixes_22_11.py`)**: Tổng hợp 22 bản tin độc lập + Intro song giọng (`00`) + mục `23. CÁC TIN THỂ THAO KHÁC` (100% giọng Nữ Ngọc Huyền điểm tin bên lề) từ 12:00 21/11 đến sáng 22/11/2026 (đối chứng báo VN + BBC/ESPN/Sky Sports/Guardian); kiểm duyệt toàn bộ 24 bảng Contact Sheet (`outputs/22.11.2026/qa/`), đạt `271/271` ảnh HD sạch, `0` lỗi, `0` cảnh báo nhẹ.
  - **Sản xuất trên GitHub Cloud (`4Blank4/dd-render-worker`, 8 shards song song, Run #44977676601 -> đã tự động xóa sạch)**:
    + Video chính 16:9 [Tin-The-Thao-22-11.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/22.11.2026/Tin-The-Thao-22-11.mp4): `1920x1080 @ 30fps`, `h264`, thời lượng **`1104.424s`** (`18 phút 24,4 giây`), dung lượng **`477.96 MB`**, **`I = -14.03 LUFS`**, **`TP = -0.95 dBTP`**, `LRA = 2.00 LU`, **A/V Drift `0.23 ms`**.
    + Đầy đủ ấn phẩm đi kèm tại `outputs/22.11.2026/`: Bộ 3 Thumbnail A/B Test chuẩn 2 dòng (`thumbnail_A.jpg` `486.3 KB`, `thumbnail_B.jpg` `316.8 KB`, `thumbnail_C.jpg` `435.3 KB` + `thumbnail.jpg`), mô tả SEO 2 phần (`mota.txt` từ `core/build_mota_22_11.py` với 24 chapters `00:00`–`16:47`, đuôi `| Điểm Đọc 22/11`) và bảng ảnh đối chứng `qa/video_qa_frames.jpg`.
  - **Xuất bản Short Tin Nhanh 22 Tin 9:16 trên GitHub Cloud (`core/prepare_digest_22_11.py`, Run #44981127773 -> đã tự động xóa sạch)**:
    + Video Short 9:16 [Short_Tin_Nhanh_22_Tin.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/22.11.2026/shorts/Short_Tin_Nhanh_22_Tin.mp4): `1080x1920 @ 30fps`, thời lượng **`147.200s`** (`2 phút 27,2 giây < 180s` bao gồm Outro), dung lượng **`64.61 MB`**, **`I = -14.01 LUFS`**, **`TP = -4.04 dBTP`**, `LRA = 2.30 LU`, **A/V Drift `13.99 ms`**. Gồm 8 tin Việt Nam (Nữ Ngọc Huyền) + 14 tin Quốc tế (Nam Minh Quân Pro).
    + Đầy đủ ấn phẩm đi kèm tại `outputs/22.11.2026/shorts/`: [Short_Tin_Nhanh_22_Tin_thumbnail.jpg](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/22.11.2026/shorts/Short_Tin_Nhanh_22_Tin_thumbnail.jpg) (`445.7 KB`), [Short_Tin_Nhanh_22_Tin_mota.txt](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/22.11.2026/shorts/Short_Tin_Nhanh_22_Tin_mota.txt) chuẩn 3 MXH (YouTube Shorts, Facebook Reels, TikTok), `digest_script_22_11.json`, `qa/contact_digest_22_11.jpg` và `qa/digest_qa_frames.jpg`. Dọn sạch cache tạm + `__pycache__`, `doctor.py` đạt 100% ALL PASS.

- **2026-11-21 (Hoàn Tất Video Bản Tin Thể Thao 16:9 Ngày 21.11.2026 Qua GitHub Cloud Matrix — Intro Song Giọng, 19 Tin Độc Lập & Mục Tin Bên Lề Giọng Nữ)**:
  - **Cấu trúc nội dung tinh chỉnh theo yêu cầu Chủ kênh (`core/daily_21_11_data.py`, `core/prepare_daily_21_11.py`)**:
    + Tuyệt đối **1 vấn đề/tin** (không gộp tin rời rạc như luật việt vị Wenger với vụ kiện Man City), bổ sung mục **`20. CÁC TIN THỂ THAO KHÁC`** (`voice_preset: "secondary"` — 100% giọng Nữ Ngọc Huyền điểm nhanh 9 tin bên lề trước Outro).
    + Intro song giọng (`00`, `hide_title: true`) + 19 tin chính (`01–19` luân phiên Nam/Nữ) + Mục tin bên lề (`20`) tổng hợp tin từ `12:00 20/11` đến sáng `21/11/2026`.
  - **Kiểm duyệt thị giác nghiêm ngặt 262 ảnh (`outputs/21.11.2026/qa/` + `qa_precheck.py`)**:
    + Thu thập & soi từng ảnh trên toàn bộ 22 bảng Contact Sheet: thay thế dứt điểm các ảnh fallback sai chủ đề (Tin #11 Free Fire World Series), cắt/loại ảnh dính dải ZNews & watermark `dpa/picture-alliance` (Tin #14 Bayern Munich), thay ảnh trùng kề (Tin #09 Vovinam, Tin #17 Man City) và thay card đồ họa bằng ảnh trận đấu thực tế `beIN SPORTS` (Tin #20 Ligue 1). Đạt `262/262` ảnh sạch, `0` lỗi nghiêm trọng, `0` cảnh báo nhẹ.
  - **Sản xuất ViTTS v3turbo + Render HTML v2 trên GitHub Cloud (`4Blank4/dd-render-worker`, 8 shards song song, Run #44858282960 -> đã tự động xóa sạch)**:
    + Video chính 16:9 [Tin-The-Thao-21-11.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/21.11.2026/Tin-The-Thao-21-11.mp4): `1920x1080 @ 30fps`, `h264`, thời lượng **`988.994s`** (`16 phút 29 giây`), dung lượng **`797.61 MB`**, **`I = -14.03 LUFS`**, **`TP = -1.08 dBTP`**, **A/V Drift `0.15 ms`**.
    + Đầy đủ ấn phẩm đi kèm tại `outputs/21.11.2026/`: Bộ 3 Thumbnail A/B Test cùng xoay quanh cụm tin nóng nhất (`thumbnail_A/B/C.jpg` + `thumbnail.jpg`) và mô tả SEO 2 phần (`mota.txt` do `core/build_mota_21_11.py` xuất với 21 chapters từ `00:00` đến `14:42`, đuôi tiêu đề `| Điểm Đọc 21/11`). Dọn sạch `54.9 MB` cache tạm vào `~/.Trash`.
  - **Nâng cấp tải 3 tầng theo thứ tự ưu tiên trên GitHub Cloud (`cloud_render.yml`, `cloud_runner.py`, `cloud_worker.py`, `engines/html/renderer.py`) & Xuất bản Short Tin Nhanh 19 Tin (`21.11.2026`)**:
    + Tách artifact xuất bản từ 1 gói gộp (`~1.28 GB`) thành **3 gói ưu tiên độc lập**: `[1/3] dd-meta-thumbs` (Ảnh Thumbnail, `_mota.txt`/`mota.txt`, Chapters, Contact Sheet QA — tải trước tiên chỉ ~`1–2 MB`), `[2/3] dd-video-deliverable` (File video `.mp4` với `libx264 -crf 20 -maxrate 3600k -bufsize 5400k` gọn nhẹ hơn ~2–3 lần), và `[3/3] dd-audio-extras` (Audio `.wav` thô, hỗ trợ cờ `--skip-extras`).
    + Sản xuất [Short_Tin_Nhanh_19_Tin.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/21.11.2026/shorts/Short_Tin_Nhanh_19_Tin.mp4) (`1080x1920 @ 30fps`, `128.333s` = `2 phút 08,3 giây < 180s` bao gồm Outro, `54.23 MB`, `I = -14.04 LUFS`, `TP = -4.20 dBTP`, **A/V Drift `0.34 ms`**) gồm 19 tin chính (`01–19`, bỏ mục #20 Các tin thể thao khác) kèm `Short_Tin_Nhanh_19_Tin_thumbnail.jpg`, `Short_Tin_Nhanh_19_Tin_mota.txt` chuẩn 3 MXH và `qa/contact_digest_21_11.jpg`.

- **2026-11-20 (Chuẩn Hóa Mô Tả Đa Nền Tảng, Quy Tắc Dọn Sạch Cache Tức Thì `30.5 GB`, Tối Ưu Bitrate VideoToolbox & 6 Hạng Mục Cứng Hóa Hệ Thống)**:
  - **Quy tắc bắt buộc dọn sạch `~/Library/Caches/DiemDoc/` trước & sau mỗi tác vụ (`AGENTS.md` & `core/clean.py`)**:
    + Cập nhật `core/clean.py` mặc định `--days 0` (`--all --apply`), dọn sạch toàn bộ `177` mục tạm (`~30.48 GB`) khỏi `~/Library/Caches/DiemDoc/` vào `~/.Trash`.
    + Tích hợp tự động dọn thư mục đệm render video vào cuối `run_video_step()` trong `core/daily_runner.py` và bổ sung cờ `--step clean`.
  - **Khắc phục triệt để lỗi phình dung lượng `h264_videotoolbox` (từ `2.2 GB` xuống `~360 MB`)**:
    + Nguyên nhân video 20.11 ban đầu nặng `2.2 GB` (`16.77 Mbps`) trong khi 19.11 chỉ `344 MB` (`2.57 Mbps`): Cờ `-q:v 68` của `h264_videotoolbox` trên macOS không giới hạn trần bitrate. Đã chuyển sang `-b:v 2600k -maxrate 3600k -bufsize 5400k` trong `engines/html/renderer.py`, `core/daily_runner.py`, `core/cloud_worker.py` và nén lại `outputs/20.11.2026/Tin-The-Thao-20-11.mp4` xuống `~360 MB` (giữ nguyên 100% chất lượng 1080p30 và audio `-14.03 LUFS`).
  - **Chuẩn hóa Mô tả Video Dài (YouTube) & Video Short (3 Mạng Xã Hội: YouTube, Facebook Reels, TikTok) trong `core/diemdoc/publisher.py`**:
    + `write_mota_16x9()`: Tự động gắn hậu tố thương hiệu thống nhất cho cả 3 Option tiêu đề (`| Điểm Đọc DD/MM` cho bản tin ngày, `| Điểm Đọc Tuần` cho bản tin tuần, `| Điểm Đọc` cho chuyên đề).
    + `write_mota_9x16()`: Chỉ dùng 1 tiêu đề (`| Điểm Đọc #Shorts`) và xuất sẵn 3 khối mô tả riêng biệt (`[1. YOUTUBE SHORTS — MÔ TẢ]`, `[2. FACEBOOK REELS — CHỈ MÔ TẢ / CAPTION]`, `[3. TIKTOK — CHỈ MÔ TẢ / CAPTION]`).
  - **Hoàn thiện 6 hạng mục nâng cấp kỹ thuật**:
    + Module thu thập ảnh dùng chung `core/diemdoc/image_curator.py` (Wikimedia Commons API + Bing lọc từ khóa chủ thể bắt buộc + gỡ `/thumb_w/` + cắt viền logo).
    + Cache RAM (`_PRON_DICT_CACHE`, `_ABBR_DICT_CACHE`) & retry 3 lần chống lỗi Google Drive `Errno 89` trong `core/diemdoc/tts_text.py` và `core/build_thumbnails_09_11.py`.
    + Tự động tính cỡ chữ `compute_16x9_hero_font_size()` cho Thumbnail 16:9 và tích hợp `--step mota` vào `core/daily_runner.py`.
    + Nâng cấp `core/qa_precheck.py`: Chặn lỗi `[FAIL]` nếu có 2 ảnh trùng đứng sát nhau liên tiếp (`Adjacent Duplicate`), kiểm tra hậu tố `| Điểm Đọc` và kiểm tra đủ 3 khối MXH cho Short.

- **2026-11-20 (Hoàn Tất Video Bản Tin Thể Thao 16:9 Ngày 20.11.2026 — 21 Bản Tin Động, Đủ 9 Layout & Kiểm Duyệt Ảnh Nghiêm Ngặt)**:
  - **Tổng hợp động theo ngày (loại bỏ cố định 18/24 tin)**: Rà soát và gỡ bỏ mô tả cứng `"24 tin"` tại `core/m1b_llm_writer.py`; sản xuất bản tin ngày 20.11 gồm **Intro song giọng (00) + 21 bản tin (01–21)** qua `core/daily_20_11_data.py` & `core/prepare_daily_20_11.py` (~18 phút 23 giây).
  - **Kích hoạt trọn bộ 9 Layout, 4 chuyển cảnh & Stat Callout HUD**: Cập nhật `core/m8_news_bridge.py` (`_pick_smart_layout()` cân bằng đếm đều cả 9 layout gồm `full`, `split`, `polaroid`, `cinema`, `triptych`, `hero_mosaic`, `filmstrip_carousel`, `spotlight_sequence`, `bento_grid` với biến thiên `1–5` ảnh/câu; nạp `intro_hook.json` cho `id=0` và ưu tiên `stat_badges` tùy biến từ kịch bản).
  - **Khắc phục & cứng hóa pipeline `core/daily_runner.py` và `engines/html/renderer.py`**: Sửa import `export_bridge_project` + `build_chunks_from_text`, truyền đủ SFX/BGM/two-pass loudnorm/cut-concat khớp từng frame, nâng `page.goto` timeout Playwright lên `90s` để chống nghẽn ảnh độ phân giải 3K trên Google Drive.
  - **Kiểm duyệt thị giác 2 lớp & 0 lỗi ảnh**: Quét toàn bộ `303` ảnh trên 22 Contact Sheet QA (`outputs/20.11.2026/qa/`), thực thi `core/apply_qa_fixes_20_11.py` thay thế sạch `82` ảnh sai/dính banner/thiếu và cắt gọn `22` viền logo góc sát mép (`0` ảnh thiếu, `0` ảnh trùng lặp liên tiếp).
  - **Sản phẩm xuất bản tại `outputs/20.11.2026/`**:
    + Video chính 16:9 `Tin-The-Thao-20-11.mp4` (`1920x1080 @ 30fps`, `1103.17s` ≈ `18 phút 23 giây`, `2.2 GB`, `I = -14.03 LUFS`, `TP = -1.08 dBTP`, **A/V Drift `0.66 ms`**, `419` SFX, kiểm tra thực tế qua 12 khung hình `qa/video_qa_frames.jpg`).
    + Bộ 3 Thumbnail 16:9 Cyber-Stadium cân 2 dòng tiêu đề (`thumbnail_A/B/C.jpg` + `thumbnail.jpg`) và mô tả SEO 2 phần (`mota.txt` gồm 3 Option tiêu đề Sentence Case ≤ 90 ký tự + 22 chapters từ `00:00` đến `17:26`).

- **2026-11-20 (Thử Nghiệm Thành Công Video Short Bản Tin Nhanh 21 Tin Trên GitHub Cloud — `Short_Tin_Nhanh_21_Tin.mp4`)**:
  - **Sản phẩm hoàn thiện (`outputs/20.11.2026/shorts/`)**: [Short_Tin_Nhanh_21_Tin.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/20.11.2026/shorts/Short_Tin_Nhanh_21_Tin.mp4) (`1080x1920 @ 30fps`, thời lượng **`132.60s`** = `2 phút 12,6 giây < 180s` gồm Outro Nữ, dung lượng **`65.9 MB`**, **`I = -14.01 LUFS`**, **`TP = -3.75 dBTP`**, **A/V Drift `14.0 ms <= 33.3 ms`**).
  - **Sản xuất 100% trên GitHub Actions (`4Blank4/dd-render-worker`)**: Gói payload gửi lên chỉ **`9.00 MB`** (chỉ gồm `digest_specs.json` + 21 ảnh chọn lọc), hoàn thành tổng hợp ViTTS v3turbo song giọng (Việt Nam: Nữ Ngọc Huyền / Quốc tế: Nam Minh Quân Pro), render `short_digest_v2.html`, ghép Outro 9:16, xuất Thumbnail 9:16 (`Short_Tin_Nhanh_21_Tin_thumbnail.jpg`), mô tả SEO (`Short_Tin_Nhanh_21_Tin_mota.txt`) và Contact Sheet QA (`qa/contact_digest_20_11.jpg`), tải về Google Drive và tự động xóa sạch dữ liệu & Run/Artifacts trên GitHub (0% tải CPU/RAM máy Mac, không ảnh hưởng tiến trình Video Long đang chạy).

- **2026-11-20 (Tích Hợp Trạm Render Đám Mây Tạm Thời GitHub Actions Matrix — Zero-RAM Local & Tự Xóa Dữ Liệu 100%)**:
  - **Kiến trúc Hybrid Local + GitHub Matrix (`.github/workflows/cloud_render.yml`, `core/cloud_runner.py`, `core/cloud_worker.py`, `config/cloud.json`, `requirements-cloud.txt`, `.gitignore`)**:
    + Giữ nguyên 100% cấu trúc và quy trình local hiện tại (`daily_runner.py`, `short_batch.py`), bổ sung khả năng đẩy riêng 2 khâu nặng nhất (**ViTTS v3turbo + Whisper + Playwright HTML v2 Render**) lên dàn máy ảo GitHub Actions (`4Blank4/dd-render-worker`, Public repo = **miễn phí không giới hạn số phút chạy**, huy động tới **8–15 máy ảo x 16 GB RAM** chạy song song).
    + Đóng gói tự chứa bổ sung `core/vendor/vieneu_utils/` bên cạnh `core/vendor/vieneu/` để chạy ViTTS v3turbo (ONNX CPU) độc lập 100% trên Ubuntu Linux không phụ thuộc máy Mac.
    + Hỗ trợ cả 3 định dạng: `daily_long` (Video bản tin dài/tuần 16:9), `short_batch` (Lô video Shorts 9:16 đơn giọng/song giọng/DataViz/Hook) và `digest_short` (Video bản tin nhanh 17–26 tin `< 3 phút`).
    + **Cơ chế Zero-Data Retention**: `.gitignore` chặn tuyệt đối `outputs/`, `projects/`, `_ref/`, `docs/`. Khi chạy chỉ gửi gói `_cloud_job/payload/` (~15–25 MB); ngay sau khi tải `.mp4`, `.wav`, `thumbnail*.jpg` về Google Drive, `cloud_runner.py` tự động xóa sạch `_cloud_job/` trên GitHub và gọi `gh run delete` xóa luôn Artifacts/Run trên đám mây.

- **2026-11-19 (Nâng Cấp Toàn Diện 3 Giai Đoạn — 9 Layout Video Dài + Broadcast HUD, Tăng Tốc Render VideoToolbox/CDP & Unified Daily Runner + Auto-QA)**:
  - **Giai đoạn 1 — Nâng cấp thị giác Video Dài 16:9 (`templates/long_sports_news_v2.html`, `core/m8_news_bridge.py`)**:
    + Mở rộng từ 3 kiểu thực chạy lên **9 layout chống lặp** (`full`, `split`, `polaroid`, `cinema`, `triptych`, và 4 layout mới: `hero_mosaic`, `filmstrip_carousel`, `spotlight_sequence`, `bento_grid`), khai thác trọn vẹn **1–5 ảnh/câu** kèm đổi `📷 ẢNH` động theo từng khung ảnh.
    + Nâng cấp chuyển cảnh stage xoay vòng 4 kiểu deterministic (`fade`, `wipe_left`, `slide_up`, `zoom_in`) và bổ sung **Broadcast Stat Callout HUD** góc trên phải tự trích xuất tỷ số/cột mốc (`_extract_stat_badge()`).
  - **Giai đoạn 2 — Tối ưu hiệu suất Render & Whisper (`engines/html/renderer.py`, `core/m8_news_bridge.py`)**:
    + Hỗ trợ mã hóa phần cứng macOS **`h264_videotoolbox`** (`-q:v 68`), chụp khung trực tiếp qua **CDP `Page.captureScreenshot`** (`jpeg_quality=88`), và cờ **`video_only_output=True`** bỏ qua bước mix/loudnorm thừa ở từng chunk nhỏ.
    + Bổ sung cache singleton `_WHISPER_MODEL_CACHE` trong `m8_news_bridge.py`, tránh nạp lại mô hình Whisper từ ổ cứng ở mỗi bản tin.
  - **Giai đoạn 3 — Chuẩn hóa Vận hành 1 Lệnh & Auto-QA (`core/daily_runner.py`, `core/qa_precheck.py`)**:
    + Tạo `core/qa_precheck.py` tự động quét ngôn từ máy móc/hậu trường, lỗi chấm hàng nghìn, chất lượng & trùng lặp ảnh, độ dài dòng thumbnail (`<= 21` ký tự) và tiêu đề SEO (`<= 100` ký tự) trước khi chạy TTS/render.
    + Tạo `core/daily_runner.py` điều phối thống nhất `--step qa|tts|video|thumbs|all --workers 3`, thay thế việc nhân bản script theo từng ngày.

- **2026-11-19 (Hoàn Tất Bản Tin Thể Thao 19.11.2026 — Video 16:9 `Tin-The-Thao-19-11.mp4`, Short Tin Nhanh 18 Tin `Short_Tin_Nhanh_18_Tin.mp4`, Chuẩn Ngôn Từ Báo Chí Tự Nhiên)**:
  - **Quy chuẩn mới về ngôn từ báo chí tự nhiên (`AGENTS.md` 5.1 & `core/diemdoc/publisher.py`)**: Cấm tuyệt đối các từ/cụm từ máy móc hoặc hậu trường sản xuất (`giọng đọc`, `giọng nam/nữ`, `cảnh quay`, `khung hình`, `hiệu ứng hình ảnh/hiển thị`, `thời gian tạo video`, `từ 12 giờ` / mốc cào tin nội bộ...) trong lời thoại video, chữ trên thumbnail, tiêu đề và mô tả công khai; nâng cấp `sanitize_public_text()` trong `core/diemdoc/publisher.py` và làm sạch `outputs/19.11.2026/mota.txt`.
  - **Sản phẩm hoàn thiện Video 16:9 (`Tin-The-Thao-19-11.mp4`)**: [Tin-The-Thao-19-11.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/19.11.2026/Tin-The-Thao-19-11.mp4) (`1920x1080 @ 30fps`, thời lượng **`1038.27s`** ≈ **17 phút 18,3 giây**, dung lượng **`344 MB`**), gồm `logo/Intro.mp4` + `tin_00_intro_long.mp4` (`51.17s` song giọng Nữ/Nam không tiêu đề `hide_title: true`, tổng `Intro+Hook = 56.17s`) + `18` bản tin `tin_01..18_long.mp4` (`THỨ NĂM · 19.11.2026`) + `logo/Outro.mp4`.
  - **Video Short Tin Nhanh 18 Tin 9:16 (`core/build_digest_19_11.py` -> `outputs/19.11.2026/shorts/Short_Tin_Nhanh_18_Tin.mp4`)**: Viết mới hoàn toàn 18 câu thoại tin nhanh cô đọng (`shorts/digest_script_19_11.json`, **Việt Nam `01..06, 14, 16, 17`**: Nữ `Ngọc Huyền Mẫu 14`; **Quốc tế `07..13, 15, 18`**: Nam `Minh Quân Pro Mẫu 15`), render `short_digest_v2.html` (`133.60s` thân) + ghép Outro Nữ `Outro_Short_1_Cyber_Pulse.mp4` (`140.10s < 180s`, `58 MB`, **`I = -14.02 LUFS`**, **`TP = -4.07 dBTP`**, **A/V Drift `9.00 ms`**), kèm QA `qa/contact_digest_19_11.jpg`, 3 QA video frames, Thumbnail 9:16 [Short_Tin_Nhanh_18_Tin_thumbnail.jpg](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/19.11.2026/shorts/Short_Tin_Nhanh_18_Tin_thumbnail.jpg) và SEO [Short_Tin_Nhanh_18_Tin_mota.txt](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/19.11.2026/shorts/Short_Tin_Nhanh_18_Tin_mota.txt).
  - **Dữ liệu, Giọng đọc & Đồng bộ Video Dài (`core/daily_19_11_data.py`, `core/generate_daily_tts_19_11.py`, `core/build_daily_19_11_video.py`)**: Tổng hợp 67 bài báo kiểm chứng, ViTTS v3turbo v4.1 No-Cut (`1026.8s` lời đọc gồm Intro song giọng + 18 tin luân phiên Nam `Minh Quân Pro Mẫu 15` / Nữ `Ngọc Huyền Mẫu 14`), Whisper word-sync + HTML v2 Playwright render + Cut-Concat PCM WAV sample-accurate + `bgm_editorial_2_momentum.mp3` + 2-pass loudnorm (`I = -14.01 LUFS`, `TP = -2.57 dBTP`, **A/V Drift `0.66 ms`**).
  - **Kiểm duyệt QA Pha 1 (`core/prepare_daily_19_11.py`, `core/fix_daily_19_11_qa.py`)**: Tuyển chọn **290 ảnh ngang HD** (`W >= 800, H >= 450, W/H >= 1.18`), tăng cường 3–5 ảnh mỗi câu tiêu đề/trọng tâm để kích hoạt mượt `triptych`/`split`/`full` đa khung; kiểm duyệt trực quan toàn bộ 20 Contact Sheets (`outputs/19.11.2026/qa/`), cắt viền sạch logo và thay mới toàn bộ 34 ảnh dính watermark/lệch chủ đề (`contact_fixed_19_11.jpg` + `contact_scene_13/17/18.jpg`).
  - **Ấn phẩm đi kèm**: Bộ 3 Thumbnail 16:9 `thumbnail_A/B/C.jpg` + `thumbnail.jpg` (`build_thumbnails_09_11.py --day 19.11.2026` theo `outputs/19.11.2026/thumbnails_plan.json`), mô tả SEO chuẩn 2 phần Sentence Case `mota.txt` (`build_mota_19_11.py`) kèm 19 mốc chapters từ `_preview_v2/chapters_19_11.json`.
  - **Chẩn đoán sức khỏe hệ thống**: `core/doctor.py` đạt 100% ALL PASS (`0` file `.pyc`/`__pycache__` trên Drive).

- **2026-11-18 (Chuẩn Hóa Toàn Hệ Thống — Khử Sạch Dữ Liệu Rác Mô Tả Video, Quy Chuẩn Thời Gian Tuần/Hôm Qua & Ảnh HD Không Logo)**:
  - **Chặn triệt để rác kỹ thuật trong mọi `mota.txt` & `*_mota.txt` (`core/diemdoc/publisher.py`, `core/run_day.py`, `core/build_digest_*.py`)**: Bổ sung `sanitize_chapter_label()` và `sanitize_public_text()` vào `write_mota_16x9()` và `write_mota_9x16()`, tự động tước sạch `[Nam]`, `[Nữ]`, `[TIN XX]`, `[XX]`, `(Mẫu 14)`, `(Mẫu 15)`, tên TTS (`Minh Quân Pro`, `Ngọc Huyền`) và ghi chú giọng đọc nội bộ ở tầng xuất bản trung tâm lẫn các script đầu nguồn; làm sạch triệt để `outputs/18.11.2026/mota.txt` và `outputs/18.11.2026/shorts/Short_Tin_Nhanh_17_Tin_mota.txt`.
  - **Cửa sổ thời gian chuẩn cho Video Tuần / Nửa Tuần / Hôm Qua (`core/m1_scraper.py`, `core/run_day.py`)**: Bổ sung `resolve_time_window()` + cờ `--period weekly|yesterday` và `--until`: `--period weekly` tự động lấy đúng `00:01 Thứ Hai tuần trước -> 23:59:59 Chủ Nhật tuần trước`; `--period yesterday` tự động lấy từ `12:00 trưa hôm qua -> hiện tại`; hỗ trợ `--since` & `--until` cho nửa tuần / nhiều ngày tùy chọn.
  - **Lọc ảnh khổ lớn sạch logo (`core/m1_scraper.py`, `core/run_day.py`)**: Chặn ngay từ khâu cào/tải ảnh các URL dính `wm1-` VnExpress, stock watermark (`gettyimages`, `alamy`, `shutterstock`, `istock`, `dreamstime`), `logo/icon` và ảnh nhỏ dưới `800x450`; chuẩn hóa trọn bộ vào `AGENTS.md` mục `5.1` và `5.7`.

- **2026-11-18 (Hoàn Tất Bản Tin Thể Thao 18.11.2026 — Video 16:9 `Tin-The-Thao-18-11.mp4`, Bộ 3 Thumbnail & `mota.txt`, `outputs/18.11.2026/`)**:
  - **Sản phẩm hoàn thiện Video 16:9 (`Tin-The-Thao-18-11.mp4`)**: [Tin-The-Thao-18-11.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/18.11.2026/Tin-The-Thao-18-11.mp4) (`1920x1080 @ 30fps`, thời lượng **`808.47s`** ≈ **13 phút 28,5 giây**, dung lượng **`266 MB`**), gồm `logo/Intro.mp4` + `tin_00_intro_long.mp4` (`38.70s` song giọng Nữ/Nam không tiêu đề `hide_title: true`, tổng `Intro+Hook = 43.70s`) + `17` bản tin `tin_01..17_long.mp4` (`THỨ TƯ · 18.11.2026`) + `logo/Outro.mp4`.
  - **Giọng đọc & Đồng bộ (`core/generate_daily_tts_18_11.py`, `core/build_daily_18_11_video.py`)**: ViTTS v3turbo v4.1 No-Cut (`796.9s` lời đọc gồm Intro song giọng + 17 tin luân phiên Nam `Minh Quân Pro Mẫu 15` / Nữ `Ngọc Huyền Mẫu 14`), Whisper word-sync + HTML v2 Playwright render + Cut-Concat PCM WAV sample-accurate + `bgm_editorial_2_momentum.mp3` + 2-pass loudnorm (`I = -14.02 LUFS`, `TP = -1.6 dBTP`, **A/V Drift `0.66 ms`**).
  - **Kiểm duyệt QA Pha 1 & Pha 2 (`core/prepare_daily_18_11.py`)**: 156 ảnh ngang HD sạch logo (`W >= 800, H >= 450, W/H >= 1.18`), cắt 11% viền đáy cho `Tin_13_*`, Memorial Grayscale cho `Tin_16_*`, 19 bảng Contact Sheet QA + 6 frame kiểm chứng video thành phẩm (`qa/qa_v_01..06_*.jpg`).
  - **Ấn phẩm đi kèm**: Bộ 3 Thumbnail 16:9 `thumbnail_A/B/C.jpg` + `thumbnail.jpg` (`build_thumbnails_09_11.py --day 18.11.2026` theo `thumbnails_plan.json`), mô tả SEO chuẩn 2 phần Sentence Case `mota.txt` (`build_mota_18_11.py`) với 18 mốc chapters từ `_preview_v2/chapters_18_11.json`.
  - **Video Short Bản Tin Nhanh 17 Tin 9:16 (`core/build_digest_18_11.py` -> `outputs/18.11.2026/shorts/Short_Tin_Nhanh_17_Tin.mp4`)**: Viết mới hoàn toàn 17 câu thoại tin nhanh cô đọng (`shorts/digest_script_18_11.json`, **Việt Nam `01..03, 11..14`**: Nữ `Ngọc Huyền Mẫu 14`; **Quốc tế `04..10, 15..17`**: Nam `Minh Quân Pro Mẫu 15`), xuất 17 WAV tại `shorts/digest_audio/`, render `short_digest_v2.html` (`118.27s` thân) + ghép Outro Nữ `Outro_Short_1_Cyber_Pulse.mp4` (`124.77s < 180s`, `53 MB`, `I = -14.02 LUFS`, `TP = -4.01 dBTP`, Drift `17.32 ms`), kèm QA `qa/contact_digest_18_11.jpg`, 3 QA video frames, Thumbnail 9:16 và SEO `_mota.txt`.

- **2026-11-16 (Sản Xuất Video Tổng Hợp Thể Thao Tuần Qua 16.11.2026 — 26 Bản Tin Luân Phiên Nam/Nữ + Intro Mở Màn Không Tiêu Đề ~30s, `outputs/16.11.2026/`)**:
  - **Sản phẩm hoàn thiện Video Loại 1 (`weekly_digest` 16:9)**: [Tin-The-Thao-16-11.mp4](file:///Users/phamminhtrieu/Library/CloudStorage/GoogleDrive-pmtrieu.iweb@gmail.com/Drive%20cu%CC%89a%20to%CC%82i/2026/Agent/DD-The-thao/outputs/16.11.2026/Tin-The-Thao-16-11.mp4) (`1920x1080 @ 30fps`, `h264`/`yuv420p`, thời lượng **18 phút 36,7 giây** / `1116.70s` / `33.501` frames, dung lượng **377,52 MiB**), gồm `logo/Intro.mp4` (`5.00s`) + `tin_00_intro_long.mp4` (`25.36s` song giọng Nữ/Nam không tiêu đề `hide_title: true`, tổng Intro **30.33s**) + 26 bản tin `tin_01..26_long.mp4` (bổ sung *ATP Finals 2026 tại Turin*) + `logo/Outro.mp4` (`6.50s`). Không xuất video Shorts 9:16 theo yêu cầu Chủ kênh.
  - **Hỗ trợ ẩn tiêu đề (`hide_title`) & chuẩn hóa đọc ngày trong `long_sports_news_v2.html` & `m8_news_bridge.py`**: Khi `hide_title: true` hoặc `title` rỗng, ẩn hoàn toàn `#hero-title-container` & `#fixed-headline-bar` và bắt đầu thẳng từ câu nội dung 1; phần Intro viết chuẩn `"từ ngày 9 tháng 11 đến ngày 15 tháng 11"` (tránh ViTTS đọc `"9/11"` thành `"9 trên 11"`).
  - **Giọng đọc luân phiên Nam/Nữ (`core/generate_weekly_tts_16_11.py`)**: ViTTS v3turbo v4.1 No-Cut (`max_chars=768`, `-16.0 LUFS`), giữ nguyên 100% tên gốc quốc tế & đơn vị `USD` đọc là `"đô"`: Intro dùng song giọng `Ngọc Huyền` + `Minh Quân Pro`; Tin lẻ (`01..25`) dùng `Minh Quân Pro Mẫu 15`; Tin chẵn (`02..26`) dùng `Ngọc Huyền Mẫu 14` (tổng thoại `1105.2s`).
  - **Kiểm duyệt thị giác QA 2 vòng (`core/prepare_weekly_16_11.py` & `core/fix_weekly_16_11_qa.py`)**: Tuyển chọn 310 ảnh ngang HD (`W >= 800, H >= 450, W/H >= 1.18`), sau đó kiểm duyệt trực tiếp 27 Contact Sheets (`outputs/16.11.2026/qa/`), cắt viền sạch 35 ảnh dính logo báo chí ở mép và thay mới 40+ ảnh infographic/poster/watermark/sai ngữ cảnh (đối chứng qua `contact_fixed_page_01..03.jpg` & `contact_step1b_only.jpg`).
  - **Ghép Cut-Concat & Master Audio chuẩn mẫu PCM (`core/build_weekly_16_11_video.py`)**: Khắc phục triệt để độ trôi khung AAC giữa 29 phân đoạn bằng chuẩn hóa audio từng phân đoạn sang PCM WAV `44100 Hz` khớp đúng `video_dur`, trộn liên tục `bgm_editorial_2_momentum.mp3` (`volume=0.05`) + 2-pass loudnorm (`I = -14.01 LUFS`, `TP = -1.56 dBTP <= -1.0 dBTP`, **A/V Drift `0.00 ms`**).
  - **Ấn phẩm đi kèm**: Bộ 3 Thumbnail 16:9 `thumbnail_A/B/C.jpg` + `thumbnail.jpg` (`core/build_thumbnails_09_11.py --day 16.11.2026`), file mô tả SEO `outputs/16.11.2026/mota.txt` chuẩn 2 phần Sentence Case kèm 27 mốc chapters từ `chapters_16_11.json`, và `outputs/16.11.2026/MAP.md`.
  - **Bản Tin Nhanh 26 Tin 9:16 (`core/build_digest_16_11.py` -> `outputs/16.11.2026/shorts/Short_Tin_Nhanh_26_Tin.mp4`)**: Biên tập mới hoàn toàn 26 câu thoại cô đọng (`144.03s` thân + `Outro_Short_3_Kinetic_Slam.mp4` `5.40s` = **`149.43s < 180s`**, `I = -14.02 LUFS`, `TP = -3.91 dBTP`, Drift `9.66 ms`), phân giọng theo khu vực (**Quốc tế `01..14, 25..26`**: Nam `Minh Quân Pro`; **Việt Nam `15..24`**: Nữ `Ngọc Huyền`) lưu kèm 26 WAV tại `shorts/digest_audio/`, Contact Sheet `qa/contact_digest_16_11.jpg`, Thumbnail 9:16 & SEO `_mota.txt`.
  - **Video Focus Short 1 — Tuần Lễ Vàng Của Thể Thao Việt Nam (`core/build_focus_short_golden_week.py` -> `outputs/16.11.2026/shorts/Short_01_Tuan_Le_Vang_The_Thao_Viet_Nam.mp4`)**:
    + Tái thiết lập Short 1 theo yêu cầu Chủ kênh: Viết lại kịch bản hoàn toàn thành một mạch dẫn chuyện thống nhất (Storytelling Narrative) thay vì chắp ghép rời rạc từng tin đơn lẻ: U23 Việt Nam vô địch Gia Lai Cup -> Trịnh Thu Vinh đoạt HCB thế giới và vé Olympic Los Angeles 2028 -> Phan Huy Hoàng 18 tuổi vô địch cờ tướng thế giới -> Tuyển bóng bàn Việt Nam cú đúp HCV đòi lại ngôi vương Đông Nam Á sau 10 năm.
    + **Giọng đọc & Âm thanh**: Sử dụng 100% Giọng Nữ Ngọc Huyền Mẫu 14 (`secondary`) cho toàn bộ nội dung thể thao Việt Nam theo đúng quy chuẩn, ghép nối tự động Outro nam (`Outro_Short_2_Tactical_Broadcast.mp4`) tạo độ tương phản cuốn hút.
    + **Thông số kỹ thuật & Nghiệm thu**: Thời lượng **`79.44s`** (`1 phút 19,44 giây` `< 180s` tính cả Outro), A/V Drift **`21.00 ms`** ($\le 33.3\text{ ms}$). Template `short_news_v2.html` với Hero Title -> fixed headline bar, nhãn Category Pill động theo từng phân đoạn, Lower-Third 2 góc động (`📰 NGUỒN` + `📷 ẢNH`) đổi tức thời theo ảnh, phụ đề Karaoke 48px đồng bộ từng từ. Kèm Thumbnail 9:16 `Short_01_Tuan_Le_Vang_The_Thao_Viet_Nam_thumbnail.jpg` (Cyber-Stadium Electric Cyan, 539 KB), mô tả SEO `_mota.txt` (4 mốc Chapters chuẩn Sentence Case) và Contact Sheet QA `qa/contact_focus_01_tuan_le_vang_vn.jpg` (10 ảnh đối chứng rõ nét).

- **2026-11-16 (Sản Xuất Tuần Tự 3 Video Shorts Song Giọng Nữ/Nam Dưới 2 Phút: Argentina 1-2 Uruguay, Bỉ 4-1 Italia & Tây Ban Nha 2-3 Anh)**:
  - **Nâng cấp `core/diemdoc/short_batch.py` hỗ trợ Song Giọng Trong 1 Video (`voice_segments`)**: Cho phép cấu hình từng đoạn giọng đọc độc lập trong cùng một video Short (`_synth_text_with_preset` chuẩn hóa từng đoạn về `-16 LUFS` trước khi ghép nối với khoảng nghỉ `350ms`) — áp dụng **Giọng Nữ Ngọc Huyền Mẫu 14** (`secondary`) cho Tiêu đề + Phần 1 (Diễn biến trận đấu) và **Giọng Nam Minh Quân Pro Mẫu 15** (`primary`) cho Phần 2 (Bình luận chuyên môn), đồng bộ hoàn hảo với Whisper & Karaoke 1-1.
  - **Mở rộng `templates/short_news_v2.html`**: Bổ sung 4 cờ vector SVG nội tuyến (`UY`, `BE`, `IT`, `ENG`) vào `renderFlagSvg()`.
  - **Xuất bản tuần tự từng video tại `outputs/Orther/16.11.2026/shorts/` (`core/build_shorts_16_11.py --only 1|2|3`, tích hợp Opening Hook HUD 3s đầu + 5 SFX, DataViz cờ SVG, Outro 9:16, Thumbnail 9:16 & Mô tả SEO `_mota.txt`)**:
    1. *Tin #01 — Argentina thua Uruguay 1-2 thời hậu Messi* (**59.30s**, `27.47 MB`, `I = -13.96 LUFS`, `TP = -4.93 dBTP`, `LRA = 2.10 LU`, Drift `3.0 ms <= 33.3 ms`, `Outro_Short_1_Cyber_Pulse.mp4`): Diễn biến trận giao hữu 13/11 tại La Bombonera (bỏ trống áo số 10, cầm bóng 72%, 17 cú sút, phản lưới Balerdi 48', Araujo 53', Julian Alvarez 73') + Bình luận kỷ nguyên hậu Messi của HLV Lionel Scaloni trước khối phòng ngự của tân HLV Diego Forlan + DataViz `AR`/`UY` (`qa/contact_scene_01.jpg`, 13 ảnh sạch).
    2. *Tin #02 — Italia thua thảm Bỉ 1-4 và bị loại khỏi Nations League* (**61.92s**, `24.98 MB`, `I = -14.33 LUFS`, `TP = -5.41 dBTP`, `LRA = 2.20 LU`, Drift `21.0 ms <= 33.3 ms`, `Outro_Short_2_Tactical_Broadcast.mp4`): Diễn biến lượt cuối bảng A1 tại Brussels (Esposito mở tỷ số 11', thủng lưới 3 bàn trong 11 phút bởi De Cuyper, Ngoy, Doku, Moreira 80', Esposito hỏng 11m phút 90+1') + Bình luận sự sụp đổ sân khách của HLV Roberto Mancini trước Bỉ của Mark van Bommel + DataViz `BE`/`IT` (`qa/contact_scene_02.jpg`, 13 ảnh sạch).
    3. *Tin #03 — Tây Ban Nha thua Anh 2-3, đứt chuỗi 43 trận bất bại* (**61.51s**, `24.48 MB`, `I = -13.99 LUFS`, `TP = -4.88 dBTP`, `LRA = 2.30 LU`, Drift `9.0 ms <= 33.3 ms`, `Outro_Short_1_Cyber_Pulse.mp4`): Diễn biến tại Metropolitano Madrid (Harry Kane pen 45'+, Ezri Konsa 53', Ben White 57', thẻ đỏ Elliot Anderson 63', Mikel Oyarzabal & Nico Williams gỡ 2-3) + Bình luận dấu chấm hết chuỗi 43 trận bất bại của HLV Luis de la Fuente trước tuyển Anh của Thomas Tuchel + DataViz `ES`/`ENG` (`qa/contact_scene_03.jpg`, 15 ảnh sạch).

- **2026-11-14 (Sản Xuất 3 Video Shorts 9:16 Ngày 14.11.2026: Án Phạt Thủ Môn Owono, Hà Lan Thắng Hy Lạp 7-0 & Phan Huy Hoàng Đoạt HCV Cờ Tướng Thế Giới + Mở Rộng Cờ Quốc Gia DataViz)**:
  - **Mở rộng `templates/short_news_v2.html`**: Bổ sung 4 cờ vector SVG nội tuyến (`GR`, `CN`, `HK`, `MY`) vào `renderFlagSvg()` phục vụ đồ thị DataViz đa quốc gia.
  - **Xuất bản 3 Video Shorts 9:16 độc lập tại `outputs/Orther/14.11.2026/shorts/` (`core/build_shorts_14_11.py`, tất cả dùng Giọng Nam Minh Quân Pro Mẫu 15 + tự động gắn Outro giọng Nữ qua `short_outro.py`, Opening Hook HUD 3s đầu + 5 SFX, Thumbnail 9:16 & Mô tả SEO 2 phần `_mota.txt`)**:
    1. *Tin #01 — Thủ môn Jesus Owono bị phạt kịch khung 12 trận sau bi kịch qua đời của Jesus de Miguel* (`52.62s`, `1080x1920 @ 30fps`, `I = -14.02 LUFS`, `TP = -5.17 dBTP`, `LRA = 1.90 LU`, Drift `16.0 ms <= 33.3 ms`, `Outro_Short_3_Kinetic_Slam.mp4`): Tổng hợp thông tin đa nguồn từ VnExpress, Marca, AS & RFEF (án treo giò tối đa theo Điều 102, điều tra tư pháp tại Tây Ban Nha, chiến dịch của Fran Sol quyên góp `239000 USD` và cam kết bảo trợ con gái 16 tháng tuổi từ CLB Tenerife); áp dụng kỹ thuật **Memorial Grayscale** cho ảnh tưởng niệm & tang lễ (`qa/contact_scene_01.jpg`, 13 ảnh sạch).
    2. *Tin #02 — Hà Lan hủy diệt Hy Lạp 7-0 ở UEFA Nations League, Reijnders lập hat-trick 21 phút* (`51.28s`, `1080x1920 @ 30fps`, `I = -14.05 LUFS`, `TP = -4.07 dBTP`, `LRA = 1.50 LU`, Drift `11.3 ms <= 33.3 ms`, `Outro_Short_1_Cyber_Pulse.mp4`): Tổng hợp từ VnExpress, Goal, 365Scores & Reuters (Reijnders tái lập kỳ tích Marco van Basten 1990, cú đúp Jurrien Timber, Summerville, Malen, san bằng kỷ lục giải đấu dưới tay HLV Xavi Hernandez trước trận gặp Đức của Jurgen Klopp); tích hợp Opening Hook `7 - 0` & đồ thị Cyber-Stadium DataViz `grouped_race` (`17` vs `9` cú sút, `13` vs `1` trúng đích, `53%` vs `47%` kiểm soát bóng) với cờ `NL`/`GR` (`qa/contact_scene_02.jpg`, 13 ảnh sạch).
    3. *Tin #03 — Kỳ thủ 18 tuổi Phan Huy Hoàng bất bại đoạt HCV cá nhân Giải cờ tướng thế giới mở rộng 2026 tại Singapore* (`48.79s`, `1080x1920 @ 30fps`, `I = -14.00 LUFS`, `TP = -4.40 dBTP`, `LRA = 2.00 LU`, Drift `18.3 ms <= 33.3 ms`, `Outro_Short_3_Kinetic_Slam.mp4`): Tổng hợp từ VnExpress, Tuổi Trẻ & Bongdaplus (thay Lại Lý Huynh đánh chính, đạt `13 điểm` sau `6 thắng 1 hòa`, cầm hòa Lưu Bách Hoành, vượt Như Nhất Thuần & Mạnh Phồn Duệ, cùng HCĐ của Nguyễn Minh Nhật Quang và 2 HCB đồng đội Nam/Nữ của Đàm Thị Thùy Dung, Nguyễn Hoàng Yến); tích hợp Opening Hook `13 ĐIỂM` & đồ thị DataViz bảng tổng sắp đồng đội Nam/Nữ (`CN`, `VN`, `HK`, `MY`) (`qa/contact_scene_03.jpg`, 13 ảnh sạch).

- **2026-11-13 (Tạo Bộ 3 Mẫu Outro Cho Video Short 9:16 Trong Khoảng 5–8 Giây — `logo/short_outros/`)**:
  - **Thiết kế 3 template HTML GSAP + `DDOverlay` độc lập (`1080x1920 @ 30fps`)** đặt trong vùng an toàn UI của YouTube Shorts / TikTok (`core/build_short_outros.py`):
    1. `templates/short_outro_1_cyber_pulse.html` → `logo/short_outros/Outro_Short_1_Cyber_Pulse.mp4` (`6.50s` / `195` frames, **Giọng Nữ Ngọc Huyền Mẫu 14**, `I = -14.01 LUFS`, `TP = -6.75 dBTP`, Drift `0.0 ms`): Phiên bản dọc hiện đại hóa trực tiếp từ `logo/Outro.mp4` với logo vòng xoay quỹ đạo, `"CẢM ƠN BẠN ĐÃ XEM VIDEO!"`, 2 nút tương tác `1 LIKE` & `1 ĐĂNG KÝ` kèm con trỏ bấm chuyển trạng thái `ĐÃ ĐĂNG KÝ` + chuông rung.
    2. `templates/short_outro_2_tactical_broadcast.html` → `logo/short_outros/Outro_Short_2_Tactical_Broadcast.mp4` (`6.00s` / `180` frames, **Giọng Nam Minh Quân Pro Mẫu 15**, `I = -14.05 LUFS`, `TP = -5.68 dBTP`, Drift `0.0 ms`): Phong cách bảng tỷ số truyền hình thể thao (`FULL-TIME • ĐIỂM ĐỌC 24/7`, `"CÒN NHIỀU TIN NÓNG PHÍA SAU!"`), Ticker chạy liên tục, Equalizer 5 thanh động và CTA `ĐĂNG KÝ + BẬT CHUÔNG 🔔`.
    3. `templates/short_outro_3_kinetic_slam.html` → `logo/short_outros/Outro_Short_3_Kinetic_Slam.mp4` (`5.40s` / `162` frames, **Giọng Nữ Ngọc Huyền Mẫu 14**, `I = -13.98 LUFS`, `TP = -5.81 dBTP`, Drift `0.0 ms`): Phong cách Kinetic Typography nhịp nhanh đánh theo từng từ (`"THẤY HAY?"` → `"THẢ TIM!"` → `"BẤM THEO DÕI / ĐĂNG KÝ KÊNH"` → Logo Slam `"ĐIỂM ĐỌC"`).
  - **Kiểm duyệt thị giác QA**: Xuất Contact Sheet 6 khung hình/mẫu tại `logo/short_outros/qa/contact_short_outros.jpg`.
  - **Tích hợp tự động vào pipeline Shorts (`config/shorts.json`, `core/diemdoc/short_outro.py`, `core/diemdoc/short_batch.py`, `core/run_day.py`)**:
    + Chế độ mặc định `opposite_gender_random`: Video Shorts giọng **Nam** (`primary` / `Minh Quân Pro`) tự động chọn ngẫu nhiên 1 trong 2 Outro giọng **Nữ** (`Outro_Short_1_Cyber_Pulse.mp4` hoặc `Outro_Short_3_Kinetic_Slam.mp4`); video giọng **Nữ** (`secondary` / `Ngọc Huyền`) tự động gắn Outro giọng **Nam** (`Outro_Short_2_Tactical_Broadcast.mp4`); video giọng hỗn hợp chọn ngẫu nhiên cả 3 mẫu.
    + Ghép nối qua FFmpeg `concat=n=2:v=1:a=1` chuẩn hóa đồng nhất `1080x1920 @ 30fps`, `yuv420p`, `44.1kHz stereo`, kiểm chứng smoke test đạt `I = -13.99 LUFS`, `TP = -4.03 dBTP`, Drift `17.3 ms <= 33.3 ms`.

- **2026-11-13 (Sản Xuất 2 Video Shorts 9:16 Ngày 13.11.2026: Pochettino Dẫn Dắt Man Utd & U23 Việt Nam Áp Đảo Hạ Singapore + Tích Hợp Toàn Diện Opening Hook SFX & DataViz)**:
  - **Tích hợp sâu Opening Hook HUD & 5 hiệu ứng SFX vào `m8_news_bridge.py` & `short_batch.py`**:
    + Nối thông trường `item.get("hook")` từ `thethao.json` sang `sentences[0]["hook"]` (cả chế độ single short lẫn multi-item / focus short).
    + Tự động chèn 5 sự kiện âm thanh SFX đồng bộ mở màn: `sub_drop_boom.mp3` (0.02s, vol 0.28), `bell_ping_highlight.mp3` (0.76s, vol 0.22), `whoosh_cinematic_1.mp3` (1.50s, vol 0.22), `pop_card.mp3` (2.15s, vol 0.20), và `whoosh_cinematic_short.mp3` (3.00s, vol 0.22).
    + Giữ vững quy chuẩn số tiền USD đọc là "đô", phụ đề hiển thị chuẩn "USD", và quy chuẩn số liền khối không dấu chấm (`10 triệu USD`, `100000 USD`, `2029`, `2026`).
  - **Xuất bản 2 Video Shorts 9:16 độc lập tại `outputs/Orther/13.11.2026/shorts/` (`core/build_shorts_13_11.py`)**:
    + *Tin #01 — Pochettino đồng ý dẫn dắt Man Utd tới năm 2029, Carrick bị sa thải* (`45.88s` / `1376` frames @ `1080x1920`, **Giọng Nam: Minh Quân Pro Mẫu 15**, `I = -14.00 LUFS`, `TP = -2.30 dBTP`, `LRA = 1.60 LU`, A/V Drift `0.0 ms <= 33.3 ms`):
      * Mở màn Opening Hook HUD: Kicker "THƯƠNG VỤ BOM TẤN", badge "MAN UTD vs US SOCCER", số đếm "10 TRIỆU USD" phí giải phóng hợp đồng, 3 tactical pills ("HÈ 2029", "ANFIELD 22/11", "SA THẢI CARRICK") và cắt nhanh 3 nhịp ảnh mở đầu.
      * Đồ thị Cyber-Stadium DataViz `grouped_race`: Tỷ lệ thắng các đời HLV Man Utd hậu Alex Ferguson (Mourinho 58% [flag PT], Ten Hag 55% [flag NL], Solskjaer 54% [flag NO], Michael Carrick 47% [flag GB, "Bị sa thải"]) kèm 3 KPI cards ("10 triệu USD", "Hè 2029", "142 từ").
      * 13 ảnh sạch đối chứng (`qa/contact_scene_01.jpg`), Lower-Third động `📰 NGUỒN: VNEXPRESS / THE ATHLETIC` và `📷 ẢNH: GETTY IMAGES / REUTERS / WIKIMEDIA COMMONS`, kèm Thumbnail dọc 9:16 & Mô tả SEO 2 phần `_mota.txt`.
    + *Tin #02 — U23 Việt Nam áp đảo hạ Singapore tại Pleiku, HLV Kassim khen ngợi* (`46.81s` / `1404` frames @ `1080x1920`, **Giọng Nữ: Ngọc Huyền Mẫu 14**, `I = -14.02 LUFS`, `TP = -2.53 dBTP`, `LRA = 1.30 LU`, A/V Drift `11.0 ms <= 33.3 ms`):
      * Mở màn Opening Hook HUD: Kicker "ÁP ĐẢO TUYỆT ĐỐI", badge "U23 VN 1-0 SINGAPORE", số đếm "70%" kiểm soát bóng với thanh năng lượng đánh dấu mốc 30% của Singapore, phụ đề "14 CÚ DỨT ĐIỂM • HẠ GỤC SINGAPORE BẰNG SIÊU PHẨM ĐÁNH GÓT", 3 tactical pills ("BẢO LONG 70'", "14 CÚ SÚT - 0", "6 ĐIỂM DẪN ĐẦU").
      * Đồ thị Cyber-Stadium DataViz `grouped_race`: Phân tích thống kê áp đảo toàn diện U23 Việt Nam vs U23 Singapore (Kiểm soát bóng 70% vs 30%, Dứt điểm 14 vs 0 cú sút, Phạt góc 12 vs 0 quả) cùng 3 KPI cards ("1-0", "Đánh gót", "6 điểm").
      * 13 ảnh sạch đối chứng (`qa/contact_scene_02.jpg`, gồm pha ăn mừng Bảo Long, HLV Đinh Hồng Vinh, HLV Firdaus Kassim phòng họp báo), Lower-Third động `📰 NGUỒN: VNEXPRESS / VFF` và `📷 ẢNH: VNEXPRESS / BAOMOI / VOV`, kèm Thumbnail dọc 9:16 & Mô tả SEO 2 phần `_mota.txt`.

- **2026-11-12 (Nâng Cấp Opening Hook 3 Giây Đầu Trong `short_news_v2.html` & Xuất Bản `-2` Video Quang Liêm Thắng 99%)**:
  - **Mở rộng `templates/short_news_v2.html` với hệ thống Opening Hook (`sent.hook`)**: Hỗ trợ hiệu ứng 3s đầu kích thích chuẩn seek-safe GSAP (chỉ kích hoạt khi timeline có `sent.hook`): `Crash-Zoom + Micro-Shake`, tia nháy `Flash`, tia quét AI `Scanline`, 2 vòng sóng xung kích `Shockwave Ring`, HUD khóa 4 góc `FUI Corner Brackets` với số đếm `Anton 148px` (`Score-Slam`), thanh năng lượng có mốc đối chứng, `Tactical Pills` bật theo nhịp và cắt ảnh nhanh `fast_cut` 3 nhịp.
  - **Xuất bản bản `-2`** tại `outputs/Orther/12.11.2026/shorts/Short_Le_Quang_Liem_Thang_Van_Co_Chinh_Xac_99_Phan_Tram-2.mp4` (`core/build_short_quang_liem_v2.py`, `1080x1920 @ 30fps`, `51.64s` / `1549` frames, `I = -14.02 LUFS`, `TP = -2.06 dBTP`, `LRA = 1.10 LU`, Drift `7.7 ms`): giữ nguyên 100% giọng Ngọc Huyền Mẫu 14, câu 1–5 và 2 đồ thị DataViz từ bản gốc, đồng bộ tầng SFX mở màn (`sub_drop_boom`, `bell_ping_highlight`, `whoosh_cinematic_1`, `pop_card`, `whoosh_cinematic_short`) cùng cắt 3 nhịp ảnh (Budapest 11/11 → Nước thí mã 22 `!!` → Quang Liêm giơ huy chương).

- **2026-11-12 (Bổ Sung Video Short 9:16 Tin #04 & Tin #05: Mỹ Đột Ngột Rút Khỏi U17 World Cup 2026 & Lê Quang Liêm Thắng Ván Cờ Chính Xác 99% Kèm 2 Đồ Thị DataViz)**:
  - **Mở rộng cờ quốc gia SVG trong `templates/short_news_v2.html`**: Bổ sung 7 cờ vector nội tuyến (`VN`, `US`, `RU`, `IN`, `DE`, `HU`, `FIDE`) vào `renderFlagSvg()` phục vụ đồ thị xếp hạng cờ vua đa quốc gia sắc nét không cần tài nguyên ngoài.
  - **Xuất bản Tin #04 & Tin #05 tại `outputs/Orther/12.11.2026/shorts/`** (`core/build_shorts_12_11_p3.py`, hợp nhất an toàn cùng Tin #01–#03 qua `short_batch.py`):
    + *Tin #04 — Mỹ đột ngột rút khỏi U17 World Cup 2026 vì lo ngại xung đột Trung Đông* (`58.43s` / `1753` frames @ `1080x1920`, **Giọng Nam: Minh Quân Pro Mẫu 15**, `I = -14.02 LUFS`, `TP = -1.76 dBTP`, `LRA = 2.00 LU`, A/V Drift `10.7 ms <= 33.3 ms`): 14 ảnh sạch từ VnExpress & Wikimedia Commons (`contact_scene_04.jpg`, gồm sơ đồ 48 đội chia 12 bảng & đội hình U17 Việt Nam của HLV Cristiano Roland tại bảng G), kèm Thumbnail 9:16 & Mô tả SEO `#Shorts`.
    + *Tin #05 — Quang Liêm thắng ván cờ có độ chính xác 99% tại Giải toàn năng thế giới* (`51.63s` / `1549` frames @ `1080x1920`, **Giọng Nữ: Ngọc Huyền Mẫu 14**, `I = -14.02 LUFS`, `TP = -2.83 dBTP`, `LRA = 1.20 LU`, A/V Drift `7.7 ms <= 33.3 ms`): 12 ảnh sạch (`contact_scene_05.jpg`), 6 ảnh chân dung 256x256 kỳ thủ bảng B (`outputs/Orther/12.11.2026/assets/avatars/`) và **2 đồ thị DataViz động `grouped_race`** (1: độ chính xác 99% vs 85%, điểm đối đầu 4–1 & 3 thẻ KPI nước 14/22/32; 2: bảng xếp hạng 6 kỳ thủ bảng B & Elo trung bình 2735 cao nhất giải), kèm Thumbnail 9:16 & Mô tả SEO `#Shorts`.

- **2026-11-12 (Bổ Sung Video Short 9:16 Tin #03: Gerrard Đánh Giá Yamal Hay Hơn Messi & Ronaldo Ở Tuổi 19 + Tích Hợp Hệ Thống Đồ Thị DataViz Động Vào `short_news_v2.html`)**:
  - **Nâng cấp `templates/short_news_v2.html`, `core/m8_news_bridge.py`, `core/diemdoc/short_batch.py` & `engines/html/renderer.py`**:
    + Tích hợp sân khấu đồ thị dữ liệu động **Cyber-Stadium DataViz** (phong cách `05.11.2026`, bảng màu dark-mode `#0E1522` / `#131D30` + `#0095D6`, `#C98500`, `#D55181` đã kiểm chứng `validate_palette.py`) với 3 loại biểu đồ seek-safe GSAP: `grouped_race` (đua cột ngang 2 nhóm + KPI boxes), `duel_stack` (đối đầu 1v2 thanh xếp chồng 2 màu có spacer + hero scoreboard) và `trophy_race` (thanh đua danh hiệu + lưới thẻ cúp + banner cột mốc), tự động cập nhật Lower-Third góc phải thành `📊 ĐỒ HỌA` và hỗ trợ chuẩn hóa đường dẫn `avatar`/`left_avatar` qua `paths.file_url()`.
  - **Xuất bản Tin #03 tại `outputs/Orther/12.11.2026/shorts/`** (`core/build_shorts_12_11_p2.py`):
    + *Gerrard: Yamal hay hơn Messi và Ronaldo ở tuổi 19* (`57.50s` / `1080x1920 @ 30fps`, **Giọng Nam: Minh Quân Pro Mẫu 15**, `I = -14.03 LUFS`, `TP = -1.02 dBTP`, `LRA = 1.70 LU`, A/V Drift `16.0 ms <= 33.3 ms`): kết hợp 15 ảnh sạch không watermark (`contact_scene_03.jpg`) cùng 3 đồ thị số liệu sống động (73 bàn thắng, 69 kiến tạo, 142 vs 94 G+A cộng lại và 8 danh hiệu lớn), xuất kèm Thumbnail dọc 9:16 & Mô tả SEO YouTube `#Shorts`.

- **2026-11-12 (Sản Xuất 2 Video Shorts 9:16 Ngày 12.11.2026: Việt Nam Hạ Đài Loan 2-0 & HLV Park Hang-seo Nhận Án Phạt Tại Thái Lan + Trích Xuất Helper `short_batch.py`)**:
  - **Tái cấu trúc mô-đun dùng chung `core/diemdoc/short_batch.py`**: Rút gọn toàn bộ boilerplate xuất bản Shorts (quản lý thư mục ngày `ShortDayContext`, sao chép & kiểm chứng kích thước ảnh, dựng QA Contact Sheet, tổng hợp ViTTS `primary`/`secondary`, hợp nhất `thethao.json` / `image_credits.json` / `image_plan.json`, đồng bộ A/V drift & chuẩn hóa `mota.txt` + `thumbnail_9x16` qua `publisher.py`) vào một helper tái sử dụng cho các kịch bản ngày tiếp theo.
  - **2 Video Shorts 9:16 độc lập (`outputs/Orther/12.11.2026/shorts/`)**:
    + *Tin #01 — Đội tuyển Việt Nam thắng thuyết phục Đài Loan 2-0 trên sân Thiên Trường* (`43.50s`, **Giọng Nam: Minh Quân Pro Mẫu 15** — tập trung diễn biến trận giao hữu FIFA Casper Cup 2026 tối 11/11: 5 tân binh đá chính, Olaha Mạnh Đức & Nguyễn Đình Bắc ghi bàn, HLV Matthew Ross thừa nhận sự áp đảo trước thềm gặp Kyrgyzstan 17/11; `I=-14.02 LUFS`, `TP=-1.43 dBTP`, Drift `14.0 ms`, 14 ảnh chính thức VnExpress, `contact_scene_01.jpg`, Thumbnail dọc 9:16 & SEO `mota.txt`).
    + *Tin #02 — HLV Park Hang-seo nhận án phạt dù bị miệt thị ở Thái Lan* (`51.17s`, **Giọng Nữ: Ngọc Huyền Mẫu 14** — án cấm chỉ đạo 2 trận & phạt 13.333 baht từ FAT sau trận hòa Pattaya United 2-2 vì phản ứng bảo vệ John Baggio trước lời thóa mạ phân biệt chủng tộc dù chủ nhà bị phạt 40.000 baht, liền sau đó Kanchanaburi thắng Nakhon Ratchasima 1-0 vươn lên hạng 4; `I=-14.02 LUFS`, `TP=-3.21 dBTP`, Drift `9.3 ms`, 14 ảnh sạch không trùng lặp, `contact_scene_02.jpg`, Thumbnail 9:16 căn 2 dòng & SEO `mota.txt`).
- **2026-11-11 (Sản Xuất Bổ Sung 2 Video Shorts 9:16: VFF Đình Chỉ Nhóm Bán Độ CLB Long An & 5 Ứng Viên Kế Nhiệm Carrick Tại Man Utd)**:
  - **Sản phẩm hoàn thiện** tại `outputs/Orther/11.11.2026/shorts/`:
    + **Tin #05 (Giọng Nữ — Ngọc Huyền Mẫu 14)**: `Short_VFF_Dinh_Chi_Nhom_Ban_Do_CLB_Long_An.mp4` (`1080x1920 @ 30fps`, **48.17s** / 1.445 frames, **I = -14.02 LUFS**, **TP = -2.72 dBTP**, drift `14.3 ms <= 33.3 ms`) — tổng hợp án kỷ luật đình chỉ vô thời hạn của VFF với 6 thành viên CLB Long An (gồm cặp song sinh Hoàng Nhật Nam, Hoàng Danh Ngọc và 4 cầu thủ bị Cục Cảnh sát hình sự C02 khởi tố vụ dàn xếp tỷ số), kèm `Short_VFF_Dinh_Chi_Nhom_Ban_Do_CLB_Long_An_thumbnail.jpg`, `..._mota.txt`, `qa/contact_scene_05.jpg` (14 ảnh sạch từ VnExpress, VFF, Bộ Công an, Thanh Niên, Tuổi Trẻ, Lao Động).
    + **Tin #06 (Giọng Nam — Minh Quân Pro Mẫu 15)**: `Short_5_Ung_Vien_Ke_Nhiem_Carrick_Man_Utd.mp4` (`1080x1920 @ 30fps`, **53.80s** / 1.614 frames, **I = -14.04 LUFS**, **TP = -1.58 dBTP**, drift `0.0 ms`) — điểm danh 5 ứng viên hàng đầu thay thế Michael Carrick theo BBC/VnExpress (Mauricio Pochettino với điều khoản giải phóng 10 triệu USD, Julian Nagelsmann tỷ lệ thắng 83,3% C1 cùng Bayern, Eddie Howe, Antonio Conte tỷ lệ thắng 62,9% Ngoại hạng Anh và Unai Emery), kèm `Short_5_Ung_Vien_Ke_Nhiem_Carrick_Man_Utd_thumbnail.jpg`, `..._mota.txt`, `qa/contact_scene_06.jpg` (16 ảnh sạch từ VnExpress, Reuters, AP, Mirror, Football Italia, VOV, TalkSport).
  - **Cập nhật từ điển viết tắt (`data/abbreviations_map.json`)**: Bổ sung `"CLB"` -> `"câu lạc bộ"` và `"VFF"` -> `"vê ép ép"` (`group: true`) giúp phát âm tự nhiên và tô sáng Karaoke đồng bộ; giữ nguyên `thethao.json` Tin #01..#04 khi hợp nhất Tin #05..#06.
  - **Công cụ điều phối tự động**: `core/build_shorts_11_11_p2.py` (sử dụng `diemdoc.publisher`, `diemdoc.tts_text`, `m8_news_bridge`, `short_news_v2.html`).

- **2026-11-11 (Sản Xuất Bộ Ba Video Shorts 9:16: Man Utd Sa Thải Carrick & Lời Cảnh Tỉnh Của Merson, Stephanie Case Chạy 160 km Ở Nam Cực & Trịnh Thu Vinh Đoạt Vé Olympic 2028)**:
  - **Sản phẩm hoàn thiện**: Xuất bản trọn bộ 3 video Shorts 9:16 độc lập tại `outputs/Orther/11.11.2026/shorts/`:
    1. `Short_Man_Utd_Hop_Ban_Sa_Thai_Carrick_Merson.mp4` (thời lượng **65.50s**, 1.965 frames @ 30fps) dựa trên nguồn VnExpress / Sky Sports: Sir Jim Ratcliffe triệu tập Giám đốc Jason Wilcox và CEO Omar Berrada tới Monaco họp bàn sa thải Michael Carrick trước thềm đại chiến Liverpool; góc nhìn đanh thép từ Paul Merson chỉ trích MU đang "xây nhà trên vũng nước" khi mua tiền đạo tiền vệ mà bỏ quên hàng thủ để thủng lưới 15 bàn sau 5 trận.
    2. `Short_Stephanie_Case_Chay_160_km_Nam_Cuc.mp4` (thời lượng **64.21s**, 1.926 frames @ 30fps) dựa trên nguồn VnExpress / The North Face: Tái hiện kỳ tích phi thường của nữ luật sư nhân quyền Canada 44 tuổi Stephanie Case tại giải Antarctic Ice Ultra: người phụ nữ đầu tiên trong lịch sử chạy 100 dặm (160,93 km) giữa nền nhiệt âm 35 độ C và bão tuyết Nam Cực trong 24 giờ 31 phút 44 giây, xô đổ kỷ lục của nam VĐV Paul Giblin tới hơn 5 giờ đồng hồ.
    3. `Short_Trinh_Thu_Vinh_Doat_Ve_Olympic_2028.mp4` (thời lượng **66.60s**, 1.998 frames @ 30fps) dựa trên nguồn VnExpress / ISSF: Tôn vinh xạ thủ Trịnh Thu Vinh (đoàn Công an Nhân dân) giành tấm HC bạc lịch sử ở nội dung 25m súng ngắn nữ tại giải vô địch bắn súng thế giới 2026 ở Doha (Qatar), chính thức trở thành VĐV Việt Nam đầu tiên giành vé tham dự Thế vận hội Olympic Los Angeles 2028 (LA28).
  - **Phân bổ Giọng đọc Kép Nam / Nữ theo chuẩn hệ thống**:
    + Video 1 (Man Utd): Giọng nam chính **Minh Quân Pro Mẫu 15** (speed: 1.12, pitch: 0.93, temp: 0.6).
    + Video 2 & 3 (Stephanie Case & Trịnh Thu Vinh): **Giọng Nữ Ngọc Huyền Mẫu 14** (speed: 1.12, pitch: 1.10, temp: 0.5) đúng theo yêu cầu, nhả chữ trong trẻo, tự nhiên, truyền cảm hứng.
    + Khớp phụ đề Karaoke 1-1 thời gian thực, giữ nguyên tên gốc quốc tế (`Michael Carrick`, `Jason Wilcox`, `Omar Berrada`, `Jim Ratcliffe`, `Paul Merson`, `Arsene Wenger`, `Sir Alex Ferguson`, `Pep Guardiola`, `Stephanie Case`, `Paul Giblin`, `Free to Run`, `Yang Ji-in`, `Esha Singh`, `Zhang Yueyue`...).
  - **Chất lượng thị giác & Kiểm định QA 100% sạch**:
    + 36 ảnh HD thể thao chất lượng cao ($\ge 640\text{px}$ đến $3000\text{px}$) tích hợp ảnh hiện trường bài báo VnExpress và cơ quan báo chí uy tín (AFP, Reuters, AP, Sky Sports, The North Face, ISSF, Yonhap...).
    + Quét kiểm tra tự động bằng OpenCV Multi-scale Template Matching: 100% 36/36 ảnh đều đạt chuẩn sạch logo và không dính watermark (`max_val < 0.42`).
    + 3 bảng ảnh đối chứng QA `contact_scene_01.jpg`, `contact_scene_02.jpg`, `contact_scene_03.jpg` lưu tại `outputs/Orther/11.11.2026/qa/`.
    + Lower-Third động 2 góc: Bên trái cố định nguồn báo chí (`📰 NGUỒN: VNEXPRESS / SKY SPORTS`, `📰 NGUỒN: VNEXPRESS / THE NORTH FACE`, `📰 NGUỒN: VNEXPRESS / ISSF`), bên phải cập nhật động theo từng ảnh.
  - **Trọn bộ ấn phẩm phát hành**:
    + 3 ảnh Thumbnail dọc 9:16 Cyber-Stadium Anton typographic (`Short_Man_Utd_Hop_Ban_Sa_Thai_Carrick_Merson_thumbnail.jpg` 100px, `Short_Stephanie_Case_Chay_160_km_Nam_Cuc_thumbnail.jpg` 105px, `Short_Trinh_Thu_Vinh_Doat_Ve_Olympic_2028_thumbnail.jpg` 95px).
    + 3 file mô tả SEO YouTube Shorts chuẩn 1 tiêu đề duy nhất Sentence Case $\le 100$ ký tự (`_mota.txt`).
  - **Công cụ điều phối tự động**: `core/build_shorts_11_11.py`.

- **2026-11-10 (Nâng Cấp Kiến Trúc TTS v4.1 Không Cắt Câu Toàn Hệ Thống & Tái Sản Xuất Video Short 3 Sạch 100% Watermark)**:
  - **Nâng Cấp Kiến Trúc TTS v4.1 Không Cắt Câu (`core/m3_voice.py`, `core/run_day.py`, `core/build_3_shorts.py`, `core/build_shorts_*.py`)**:
    + **Xóa bỏ triệt để lỗi ngắt ngang câu**: Loại bỏ hoàn toàn cơ chế cắt vụn theo word index thô sơ (`words[i:i + max_words]`); chuyển sang cơ chế phân rã mệnh đề ngữ nghĩa chuẩn (`_split_into_sentences` và `_split_long_sentence`) dựa trên dấu ngắt ngữ pháp (`;`, `:`, `—`, `,`) và liên từ (`đồng thời`, `và`, `nhưng`, `trong khi`).
    + **Ngăn chặn VieNeu cắt ngầm 256 phonemes**: Thiết lập tham số `max_chars=768` truyền vào `model.infer()`, chặn đứng hoàn toàn việc engine nội bộ tự động cắt ngang mệnh đề ở 256 phonemes (~35 từ) và chèn dấu chấm ảo.
    + **Đệm ngắt tự nhiên giữa các câu**: Thiết lập `inter_sentence_pause=0.25s` giữa các câu hoàn chỉnh, tạo nhịp thở tự nhiên cho MC thể thao và triệt tiêu 100% hiện tượng trôi lệch phụ đề Karaoke (`cumulative drift = 0`).
    + **Nâng cấp toàn bộ codebase**: Cập nhật đồng bộ trên toàn bộ pipeline `core/m3_voice.py`, `core/run_day.py`, `core/build_3_shorts.py`, `core/build_short_cubarsi_golden_boy.py`, `core/build_shorts_10_11.py`, `core/build_short_alcaraz_paris_masters.py`, `core/build_shorts_09_11.py`, `core/build_shorts_08_11.py`, `core/build_shorts_04_05.py`.
    + **Đổi mới cache version**: Nâng cấp cache hash lên `v4.1_diemdoc_nocut` bảo đảm không bao giờ nạp lại audio bị cắt cũ.
  - **Tái Sản Xuất Video Short 3 (Pau Cubarsí Đoạt Cậu Bé Vàng 2026) Sạch 100% Logo & Watermark**:
    + **Sản phẩm hoàn thiện**: Video 9:16 `Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang.mp4` tại `outputs/Orther/10.11.2026/shorts/` (thời lượng **68.03s**, 2.041 frames @ 30fps).
    + **Diệt sạch watermark Getty Images & Logo**: Thiết lập bộ lọc URL chặn triệt để 21 domain/kho ảnh stock (`getty`, `gettyimages`, `alamy`, `istock`, `shutter`, `dreamstime`, `depositphotos`, `freepik`, `pxhere`, `wallpaper`...); thay thế toàn diện 5 ảnh dính watermark (`Tin_03_2`, `Tin_03_4`, `Tin_03_6`, `Tin_03_7`, `Tin_03_9`) bằng ảnh thể thao chất lượng cao ($\ge 1800\text{px}$ đến $3200\text{px}$) từ trang chủ chính thức FC Barcelona, Barca Universal, PSG Talk, Goal.com, Tuttosport.
    + **Kiểm định thị giác OpenCV Multi-scale Template Matching**: Quét tự động toàn bộ 12 ảnh đối chiếu mẫu watermark người dùng tải lên, xác nhận 100% 12/12 ảnh đều đạt chuẩn sạch logo tuyệt đối (`max_val < 0.42` so với ngưỡng phát hiện `> 0.60`).
    + **Đồng bộ Lower-Third 2 góc**: Cập nhật `image_credits.json` và `image_plan.json` sang các cơ quan báo chí/nhiếp ảnh chuẩn (`BARCA UNIVERSAL`, `FC BARCELONA`, `PSG TALK`, `GOAL.COM`, `REUTERS`, `TUTTOSPORT`).
    + **Kiểm toán âm lượng**: Integrated Loudness **-14.04 LUFS**, True Peak **-3.22 dBTP**, LRA **1.80 LU**, độ lệch Video vs Audio **0.7 ms** ($\le 33.3$ ms).
    + **Bộ ấn phẩm đi kèm**: Bảng ảnh QA đối chứng mới `outputs/Orther/10.11.2026/qa/contact_scene_03.jpg`, Thumbnail dọc Anton 105px `Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang_thumbnail.jpg` và mô tả SEO `Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang_mota.txt`.

- **2026-11-10 (Sản Xuất Bộ Ba Video Shorts 9:16: Mourinho vs Guardiola, FIFPRO World 11 & Pau Cubarsi Đoạt Cậu Bé Vàng 2026)**:
  - **Sản phẩm hoàn thiện**: Xuất bản trọn bộ 3 video Shorts 9:16 độc lập tại `outputs/Orther/10.11.2026/shorts/`:
    1. `Short_Mourinho_Xo_Do_Ky_Luc_Guardiola.mp4` (thời lượng **66.99s**, 2.010 frames @ 30fps, dung lượng **17.12 MB**) dựa trên nguồn VnExpress / La Liga: Jose Mourinho chính thức xô đổ kỷ lục tỷ lệ thắng của Pep Guardiola tại giải VĐQG Tây Ban Nha với 77% (thắng 97/126 trận, vượt qua con số 76.3% - 116/152 trận của Pep), chuỗi 8 trận thắng liên tiếp cùng Real Madrid, danh hiệu HLV xuất sắc nhất tháng 10 của La Liga và lời khẳng định đanh thép về bản lĩnh "Người đặc biệt".
    2. `Short_Kane_Bi_Loai_Messi_Vao_Doi_Hinh_Nam.mp4` (thời lượng **68.57s**, 2.057 frames @ 30fps, dung lượng **16.39 MB**) dựa trên nguồn VnExpress / FIFPRO: Harry Kane (chủ nhân Quả bóng vàng 2026) bất ngờ bị loại khỏi Đội hình tiêu biểu thế giới FIFPRO World 11 bởi Erling Haaland với cách biệt sít sao 0.8% phiếu bầu (28.4% vs 27.6% từ 19.806 cầu thủ chuyên nghiệp), trong khi Lionel Messi xác lập kỷ lục vô tiền khoáng hậu 18 lần liên tiếp góp mặt từ năm 2007, Kylian Mbappé dẫn đầu tuyệt đối với 46% phiếu bầu và thần đồng Lamine Yamal lập kỳ tích 2 năm liên tiếp lọt vào đội hình xuất sắc nhất năm trước tuổi 20.
    3. `Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang.mp4` (thời lượng **69.91s**, 2.097 frames @ 30fps, dung lượng **16.42 MB**) dựa trên nguồn VnExpress / Tuttosport: Trung vệ 19 tuổi Pau Cubarsi của Barcelona chính thức đoạt giải Cậu bé Vàng Golden Boy 2026 sau cú đúp vô địch La Liga và đăng quang World Cup 2026 cùng Tây Ban Nha (cầu thủ trẻ hay nhất giải). Cubarsi là hậu vệ thứ hai trong lịch sử đoạt giải sau Matthijs de Ligt (2018), cầu thủ Tây Ban Nha thứ sáu, đồng thời giúp Barcelona độc chiếm kỷ lục 5 lần đoạt giải trong lịch sử.
  - **Quy chuẩn giọng đọc & Âm thanh Master**:
    + Sử dụng giọng nam chính **Minh Quân Pro Mẫu 15** (speed: 1.12, pitch: 0.93), giữ nguyên 100% tên gốc quốc tế không phiên âm (`Jose Mourinho`, `Pep Guardiola`, `Real Madrid`, `Barcelona`, `La Liga`, `Celta Vigo`, `Girona`, `Harry Kane`, `Lionel Messi`, `Kylian Mbappé`, `Erling Haaland`, `Lamine Yamal`, `FIFPRO World 11`, `Inter Miami`, `Ballon d'Or`, `Pau Cubarsi`, `Tuttosport`, `Golden Boy`, `Warren Zaire-Emery`, `Matthijs de Ligt`, `Pedri`, `Gavi`...).
    + Chuẩn hóa âm lượng EBU R128 YouTube: Cả 3 video đều đạt Integrated Loudness **-14.03 đến -14.04 LUFS** (mức tham chiếu -14.0 LUFS), True Peak an toàn tuyệt đối **-2.92 dBTP** đến **-3.55 dBTP** ($\le -1.0$ dBTP), LRA 1.5–2.0 LU.
  - **Chất lượng thị giác & Kiểm duyệt QA 4 tầng**:
    + 12 ảnh hiện trường chất lượng cao cho mỗi tin (tổng 36 ảnh), phân bổ bám sát ngữ cảnh câu qua `image_plan.json` và `image_credits.json`, tích hợp ảnh đồ họa gốc của VnExpress (`Tin_01_1.jpg`, `Tin_02_1.jpg`, `Tin_02_2.jpg`, `Tin_03_1.jpg`, `Tin_03_3.jpg`, `Tin_03_5.jpg`).
    + 3 bảng ảnh đối chứng QA `contact_scene_01.jpg`, `contact_scene_02.jpg`, `contact_scene_03.jpg` lưu tại `outputs/Orther/10.11.2026/qa/`.
    + Lower-Third động 2 góc: Bên trái cố định nguồn báo chí (`📰 NGUỒN: VNEXPRESS / LA LIGA`, `📰 NGUỒN: VNEXPRESS / FIFPRO`, `📰 NGUỒN: VNEXPRESS / TUTTOSPORT`), bên phải cập nhật thời gian thực nguồn ảnh (`FC BARCELONA`, `VNEXPRESS`, `REUTERS`, `GETTY IMAGES`, `AP PHOTO`, `FIFPRO`, `TUTTOSPORT`...).
  - **Trọn bộ ấn phẩm phát hành**:
    + 3 ảnh Thumbnail dọc 9:16 Cyber-Stadium typographic Anton (`Short_Mourinho_Xo_Do_Ky_Luc_Guardiola_thumbnail.jpg` 105px, `Short_Kane_Bi_Loai_Messi_Vao_Doi_Hinh_Nam_thumbnail.jpg` 95px, `Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang_thumbnail.jpg` 105px).
    + 3 file mô tả SEO YouTube Shorts chuẩn 1 tiêu đề duy nhất Sentence Case $\le 100$ ký tự (`_mota.txt`).
  - **Công cụ điều phối tự động**: `core/build_shorts_10_11.py` & `core/build_short_cubarsi_golden_boy.py`.

- **2026-11-09 (Sản Xuất Video Short 9:16: Carlos Alcaraz Lần Đầu Vô Địch Paris Masters & Cột Mốc Masters 1000 Thứ 9)**:
  - **Sản phẩm hoàn thiện**: Xuất bản video Short 9:16 `Short_Alcaraz_Vo_Dich_Paris_Masters.mp4` tại `outputs/Orther/09.11.2026/shorts/` (thời lượng **66.57s**, 1.997 frames @ 30fps, dung lượng **16.12 MB**) dựa trên nguồn bài báo VnExpress / ATP Tour về chiến thắng 7-6(5), 7-5 của Carlos Alcaraz trước Ben Shelton trong trận chung kết tại Nanterre: cứu liên tiếp 4 break-point ở set một, lội ngược dòng bẻ lại game giao bóng ở set hai, thanh toán sòng phẳng món nợ US Open trước Shelton, nối dài chuỗi 19 trận thắng sau 21 trận trở lại sau chấn thương, sở hữu danh hiệu Masters 1000 thứ 9 để sánh ngang Novak Djokovic và Rafael Nadal (vô địch ít nhất 1 giải Masters trong 5 mùa liên tiếp), và là tay vợt Tây Ban Nha thứ hai đăng quang Paris Masters sau David Ferrer (2012).
  - **Quy chuẩn giọng đọc & Âm thanh Master**:
    + Giọng nam chính **Minh Quân Pro Mẫu 15** (speed: 1.12, pitch: 0.93), giữ nguyên 100% tên gốc quốc tế (`Carlos Alcaraz`, `Ben Shelton`, `Paris Masters`, `Nanterre`, `Novak Djokovic`, `Rafael Nadal`, `David Ferrer`, `US Open`, `ATP Finals`, `Turin`...).
    + Chuẩn hóa âm lượng EBU R128 YouTube: Integrated Loudness **-14.04 LUFS** (chuẩn YouTube -14.0 LUFS), True Peak **-3.09 dBTP** ($\le -1.0$ dBTP), LRA 1.4 LU.
  - **Chất lượng thị giác & Kiểm duyệt QA 4 tầng**:
    + 12 ảnh hiện trường HD (AP/Reuters/Getty Images/ATP Tour) bao gồm ảnh AP gốc từ bài báo VnExpress; Lower-Third động góc trái `📰 NGUỒN: VNEXPRESS / ATP TOUR` và góc phải đổi theo nguồn ảnh (`AP PHOTO`, `REUTERS`, `GETTY IMAGES / ATP TOUR`, `AFP`...).
    + Bảng ảnh đối chứng QA `contact_scene_03.jpg` lưu tại `outputs/Orther/09.11.2026/qa/`.
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium Anton 110px (`Short_Alcaraz_Vo_Dich_Paris_Masters_thumbnail.jpg`).
    + File mô tả SEO YouTube Shorts chuẩn 1 tiêu đề duy nhất (`Short_Alcaraz_Vo_Dich_Paris_Masters_mota.txt`).
  - **Công cụ điều phối tự động**: `core/build_short_alcaraz_paris_masters.py`.

- **2026-11-16 (Sản xuất Trọn Bộ 6 Video Shorts Dẫn Chuyện Liền Mạch Ngày 16.11.2026)**:
  - Hoàn thiện toàn diện bộ 6 video YouTube Shorts 9:16 độc lập tại `outputs/16.11.2026/shorts/`:
    + `Short 1`: *Tuần Lễ Vàng Của Thể Thao Việt Nam* (79.78s - U23 vô địch Gia Lai, Thu Vinh vé Olympic 2028, Huy Hoàng HCV cờ tướng).
    + `Short 2`: *Cuộc Chiến Thế Hệ: Messi, Lamine Yamal Và Harry Kane* (60.05s - Messi kỷ lục 18 lần World 11, Kane bị loại, Yamal & Cubarsi).
    + `Short 3`: *Đêm Ác Mộng Của Bóng Đá Nam Mỹ* (55.15s - Brazil thua ngược Nhật Bản phút bù giờ 90+1, Argentina gục ngã tại Bombonera).
    + `Short 4`: *Kỳ Tích Trí Tuệ Và Ý Chí Con Người* (61.37s - Quang Liêm ván cờ chuẩn xác 99%, Stephanie Case chạy 161 km Nam Cực âm 35°C).
    + `Short 5`: *Biến Động Băng Ghế Huấn Luyện* (66.18s - Man Utd sa thải Carrick chiêu mộ Pochettino, Mourinho xô đổ kỷ lục Pep Guardiola, Thầy Park bảo vệ học trò).
    + `Short 6`: *Mặt Tối Sân Cỏ: Bàn Tay Sắt VFF Và Cú Sốc Kỷ Luật* (68.01s - VFF đình chỉ vô thời hạn 6 cầu thủ Long An, Owono án kịch khung 12 trận, Tuyển VN lên hạng 98 FIFA).
  - Tái cấu trúc chuẩn mực: Chuyển hoàn toàn từ việc ghép mẩu tin rời rạc sang **Cấu trúc Dẫn chuyện Liền mạch (Unified Storytelling Narrative)** với thanh tiêu đề cố định `#fixed-headline-bar`.
  - Khắc phục triệt để lỗi hiển thị hình ảnh bằng cách chuẩn hóa toàn bộ URL ảnh qua `paths.file_url()` trong `short_news_v2.html` và `renderer.py`.
  - Giải quyết dứt điểm lỗi phiên âm: Sử dụng 100% từ gốc kịch bản qua `interpolate_sentence_words` và thuật toán gom cụm phụ đề thông minh `build_smart_karaoke_chunks`, loại bỏ hoàn toàn việc trích xuất text từ Whisper.
  - Bộ ấn phẩm hoàn chỉnh cho từng video: Video MP4 (9:16 @ 30fps), Thumbnail dọc 1080x1920 Cyber-Stadium Electric Cyan, mô tả SEO YouTube chuẩn 2 phần `_mota.txt` và Bảng ảnh QA đối chứng `contact_focus_XX.jpg`.

- **2026-11-09 (Sản Xuất Bộ Đôi Video Shorts 9:16: Trận Cầu Điên Rồ Man Utd 4-4 Aston Villa & Dư Chấn Hậu Đại Chiến)**:
  - **Sản phẩm hoàn thiện**: Xuất bản trọn bộ 2 video Shorts 9:16 độc lập tại `outputs/Orther/09.11.2026/shorts/`:
    1. `Short_Man_Utd_Aston_Villa_4_4.mp4` (thời lượng **54.47s**, 1.634 frames @ 30fps, dung lượng **17.37 MB**) tái hiện màn rượt đuổi tỷ số 8 bàn thắng điên rồ tại Old Trafford: Aston Villa dẫn 2-0 chỉ sau 4 phút (Alysson 1', Nicolas Jackson 4'), MU gỡ hòa 2-2 trong hiệp một (Bruno Fernandes 16' pen, Youri Tielemans 44'), Villa lại nới rộng 4-2 (John McGinn 48' pen, Leon Goretzka 53'), trước khi Joshua Zirkzee (90+2') và Patrick Dorgu (90+6') tạo nên màn lội ngược dòng bù giờ nghẹt thở gỡ hòa 4-4 khiến cầu trường Old Trafford vỡ òa.
    2. `Short_Ben_Le_Man_Utd_Aston_Villa_Carrick.mp4` (thời lượng **55.45s**, 1.663 frames @ 30fps, dung lượng **13.96 MB**) phân tích toàn diện dư chấn sau trận: Unai Emery bực tức bỏ thẳng vào đường hầm ở phút 96 khi trận đấu chưa kết thúc và cay đắng coi đây như một thất bại; tranh cãi nảy lửa quanh tình huống va chạm giữa thủ môn Senne Lammens dâng cao và Zion Suzuki trong vòng 5m50 bàn gỡ 4-4; phòng họp báo rực lửa khi Michael Carrick bị dồn ép về trát sa thải nhưng kiên quyết tuyên bố không từ chức; và nghịch lý MU vẫn dậm chân ở vị trí thứ 18 (nhóm cầm đèn đỏ rớt hạng) với chỉ 8 điểm sau 10 vòng.
  - **Quy chuẩn giọng đọc & Âm thanh Master**:
    + Giọng nam chính **Minh Quân Pro Mẫu 15** (speed: 1.12, pitch: 0.93), phát âm chuẩn xác tên gốc quốc tế (`Manchester United`, `Aston Villa`, `Old Trafford`, `Unai Emery`, `Michael Carrick`, `Nicolas Jackson`, `Alysson`, `Bruno Fernandes`, `Youri Tielemans`, `John McGinn`, `Leon Goretzka`, `Joshua Zirkzee`, `Patrick Dorgu`, `Zion Suzuki`, `Senne Lammens`...).
    + Chuẩn hóa âm lượng EBU R128 YouTube: Cả 2 video đều đạt Integrated Loudness **-14.04 LUFS** (chuẩn YouTube -14.0 LUFS), True Peak an toàn tuyệt đối **-3.70 dBTP** và **-3.61 dBTP** ($\le -1.0$ dBTP), LRA 1.3–1.6 LU.
  - **Chất lượng thị giác & Kiểm duyệt QA 4 tầng**:
    + 12 ảnh hiện trường HD cho mỗi video (tổng 24 ảnh), phân bổ bám sát ngữ cảnh câu qua `image_plan.json` và `image_credits.json`.
    + 2 bảng ảnh đối chứng QA `contact_scene_01.jpg` và `contact_scene_02.jpg` tại `outputs/Orther/09.11.2026/qa/`.
    + Lower-Third động 2 góc: Bên trái cố định nguồn báo chí (`📰 NGUỒN: VNEXPRESS / NBC SPORTS`, `📰 NGUỒN: VNEXPRESS / SKY SPORTS`), bên phải cập nhật thời gian thực nguồn ảnh (`PREMIER LEAGUE`, `ACTION IMAGES / REUTERS`, `REUTERS`, `AP PHOTO`, `GETTY IMAGES`, `SKY SPORTS`...).
  - **Trọn bộ ấn phẩm phát hành**:
    + 2 ảnh Thumbnail dọc 9:16 Cyber-Stadium Anton 115px (`Short_Man_Utd_Aston_Villa_4_4_thumbnail.jpg` và `Short_Ben_Le_Man_Utd_Aston_Villa_Carrick_thumbnail.jpg`).
    + 2 file mô tả SEO YouTube Shorts chuẩn 1 tiêu đề duy nhất (`_mota.txt`).
  - **Công cụ điều phối tự động**: `core/build_shorts_09_11.py`.

- **2026-11-08 (Sản Xuất Bộ Đôi Video Shorts 9:16: Nottingham Forest Thắng Man City 3-1 & MU Rơi Vào Nhóm Cầm Đèn Đỏ)**:
  - **Sản phẩm hoàn thiện**: Xuất bản trọn bộ 2 video Shorts 9:16 độc lập tại `outputs/Orther/08.11.2026/shorts/`:
    1. `Short_Nottingham_Thang_Man_City_3_1.mp4` (thời lượng **59.14s**, 1.774 frames @ 30fps, dung lượng **15.88 MB**) tái hiện cơn địa chấn tại City Ground: sai lầm của Josko Gvardiol, Jair Cunha mở tỷ số phút 6, cú đúp đỉnh cao của cựu cầu thủ Man City Liam Delap (18', 73'), pha volley của Rayan Cherki (52'), đẩy Man City nhận trận thua thứ 3 liên tiếp và bị Arsenal nới rộng khoảng cách lên 6 điểm.
    2. `Short_Man_Utd_Roi_Xuong_Khom_Nguy_Hiem.mp4` (thời lượng **54.64s**, 1.639 frames @ 30fps, dung lượng **14.77 MB**) phân tích hiệu ứng dây chuyền đẩy Manchester United chìm sâu xuống vị trí thứ 18 (nhóm cầm đèn đỏ rớt hạng) với chỉ 7 điểm sau 9 trận, nghịch lý dẫn đầu giải với 167 cú dứt điểm nhưng chỉ ghi 10 bàn, và sức ép sinh tử đè nặng lên Michael Carrick trước trận gặp Aston Villa.
  - **Quy chuẩn giọng đọc & Âm thanh Master**:
    + Sử dụng giọng nam chính **Minh Quân Pro Mẫu 15** (speed: 1.12, pitch: 0.93), giữ nguyên 100% tên gốc quốc tế (`Nottingham Forest`, `Man City`, `Manchester United`, `Josko Gvardiol`, `Jair Cunha`, `Liam Delap`, `Rayan Cherki`, `Morgan Gibbs-White`, `Ederson`, `Michael Carrick`, `Aston Villa`...).
    + Chuẩn hóa âm lượng EBU R128 YouTube: Cả 2 video đều đạt Integrated Loudness **-14.04 LUFS** (mức tham chiếu -14.0 LUFS), True Peak an toàn tuyệt đối **-3.41 dBTP** và **-3.48 dBTP** ($\le -1.0$ dBTP), LRA 1.4–1.8 LU.
  - **Chất lượng thị giác & Kiểm duyệt QA 4 tầng**:
    + 12 ảnh hiện trường chất lượng cao cho mỗi tin, phân bổ xen kẽ theo câu kịch bản (Semantic Image Planning qua `image_plan.json` và `image_credits.json`).
    + 2 bảng ảnh đối chứng QA `contact_scene_01.jpg` và `contact_scene_02.jpg` lưu tại `outputs/Orther/08.11.2026/qa/`.
    + Lower-Third động 2 góc: Bên trái cố định nguồn báo chí (`📰 NGUỒN: VNEXPRESS / BÓNG ĐÁ PLUS`, `📰 NGUỒN: VNEXPRESS / SKY SPORTS`), bên phải cập nhật thời gian thực nguồn ảnh (`PREMIER LEAGUE`, `REUTERS`, `AP PHOTO`, `ACTION IMAGES / REUTERS`, `GETTY IMAGES`...).
  - **Trọn bộ ấn phẩm phát hành**:
    + 2 ảnh Thumbnail dọc 9:16 Cyber-Stadium Anton 115px (`Short_Nottingham_Thang_Man_City_3_1_thumbnail.jpg` và `Short_Man_Utd_Roi_Xuong_Khom_Nguy_Hiem_thumbnail.jpg`).
    + 2 file mô tả SEO YouTube Shorts chuẩn 1 tiêu đề duy nhất (`_mota.txt`).
  - **Công cụ điều phối tự động**: `core/build_shorts_08_11.py`.

- **2026-11-08 (Sản Xuất Bản V2: Lời Dẫn Kịch Tính Spoiler-Free, Head-Safe Không Cắt Đầu Cầu Thủ, Đồng Bộ Thanh Header & Giữ Nguyên Tiêu Đề Gốc)**:
  - **Sản phẩm hoàn thiện V2**: Xuất bản toàn diện video Bản V2 tại `outputs/08.11.2026/output/Cuoc_dua_ghi_diem_NBA_1949_2026_v2.mp4` (`1920x1080 @ 30fps`, thời lượng **7m25s / 445.17s**, 13.175 frames + Outro, dung lượng **59.1 MB**) và phụ đề `Cuoc_dua_ghi_diem_NBA_1949_2026_v2.srt` (41 cues). Bảo toàn nguyên vẹn 100% bản gốc ban đầu (`Cuoc_dua_ghi_diem_NBA_1949_2026.mp4`).
  - **Khắc phục triệt để lỗi ảnh "mất đầu" (Head Cut-Off Fix)**:
    + Căn chỉnh vị trí `background-position: center top` / `center 0%` và tâm phóng to `transform-origin: center top` cho ảnh dọc tỷ lệ cao của cầu thủ. Đảm bảo 100% gương mặt và phần đầu của Michael Jordan và Kobe Bryant ở Cảnh 2 hiển thị trọn vẹn, không bị cắt bất kỳ góc nào.
  - **Lời dẫn mở đầu kịch tính & Tuyệt đối Không Spoil (Spoiler-Free Suspense Hook)**:
    + Viết lại 6 câu thoại mở đầu hoàn toàn mới: đặt câu hỏi về cỗ máy ghi điểm vĩ đại nhất 77 năm NBA, dẫn dắt qua trận đấu 100 điểm của Wilt Chamberlain, cú Skyhook Kareem, Michael Jordan, Kobe Bryant, Karl Malone... **TUYỆT ĐỐI KHÔNG hé lộ trước con số 40.000 điểm hay người chiến thắng**, giữ trọn vẹn kịch tính và sự tò mò cho khán giả đến cuối video.
    + Sinh giọng đọc ViTTS v3turbo Ngọc Huyền V2 (37.28s / 1119 frames @ 30fps).
  - **Chuẩn hóa Tiêu đề & Nhận diện Kênh**:
    + Thanh Header hiển thị đồng nhất: `[Logo] ĐIỂM ĐỌC THỂ THAO // CUỘC ĐUA GHI ĐIỂM NBA 1949–2026` với tone Cyan Cyber-Stadium (`#00E5FF`).
    + Giữ nguyên 100% Tiêu đề gốc YouTube theo yêu cầu Chủ kênh: `Ai ghi nhiều điểm nhất lịch sử bóng rổ NBA từ 1949 đến nay? 77 năm đổi ngôi | Điểm đọc thống kê`.
  - **Thay thế 100% ảnh thật không còn placeholder**:
    + Đã thay thế hoàn toàn các ô placeholder màu tối bằng ảnh tư liệu độ nét cao: `c05_b.jpg` (Kareem Abdul-Jabbar 1974), `c07_a.jpg` (LeBron James Paris 2024), `c03_b.jpg` (Kobe Bryant áo số 8), `c04_b.jpg` (Dirk Nowitzki), và `c04_c.jpg` (Shaquille O'Neal).
    + Cập nhật lại Bảng ảnh đối chứng QA `outputs/08.11.2026/qa/contact_sheet_images.jpg` (1.637 KB) xác nhận 100% 29 khung hình đều là ảnh thật.
  - **Hậu kỳ Âm thanh Master & Video V2**:
    + Render `intro_video_v2.mp4` (1119 frames) và `comm_video_v2.mp4` (2281 frames) với cơ chế Head-Safe CSS.
    + Tổng hợp Procedural Cyber-Stadium BGM V2 (441.1s, 100% YouTube Content ID safe), hardware sidechain ducking đạt độ tách bạch **23.6 dB** ($\ge 18\text{ dB}$), 2-pass Loudnorm đạt chuẩn YouTube **-14.0 LUFS**, True Peak $\le -1.2\text{ dBTP}$.
    + Trích xuất 12 khung hình kiểm duyệt QA tại `outputs/08.11.2026/qa/` (đối chứng rõ nét việc giữ nguyên đầu Kobe/Jordan và hiển thị ảnh thật Kareem/LeBron).
    + Xuất bản tài liệu `mota_v2.txt`, `decisions_v2.md` và `Cuoc_dua_ghi_diem_NBA_1949_2026_v2.srt`.

- **2026-11-08 (Sản Xuất Video Bar Chart Race 16:9 "Cuộc đua ghi điểm NBA 1949–2026")**:
  - **Sản phẩm hoàn thiện**: Xuất bản toàn diện video Bar Chart Race 16:9 tại `outputs/08.11.2026/output/Cuoc_dua_ghi_diem_NBA_1949_2026.mp4` (`1920x1080 @ 30fps`, thời lượng **7m28s / 448.20s**, 13.265 frames + Outro, dung lượng **93.7 MB**) và phụ đề `Cuoc_dua_ghi_diem_NBA_1949_2026.srt` (41 cues).
  - **Dữ liệu & Chuẩn hóa NBA**:
    + Bao phủ 50 cầu thủ ghi nhiều điểm nhất lịch sử NBA (Regular Season), 935 mốc thời gian hàng tháng (11/1949 đến 11/2026) và 135 sự kiện lịch sử (dẫn đầu, mốc điểm tròn, vượt kỷ lục, vào top 10).
    + Hệ thống màu sắc phân định 3 vị trí thi đấu: Guard (Hậu vệ - Xanh lơ Cyber-Stadium `#38BDF8`), Forward (Tiền đạo - Cam đất `#FB923C`), Center (Trung phong - Xanh ngọc `#2DD4BF`). Cầu thủ đã giải nghệ hiển thị hoa văn sọc gạch chéo mờ trang nhã.
    + Bố cục màn hình kép (Split Layout): Khung trái 1226px Top 10 bar chart race + Khung phải 520px hiển thị Thẻ Cầu thủ Dẫn đầu (ảnh chân dung, cờ, thông số) + Live SVG Sparkline tiến trình điểm số + 4 thẻ Sự kiện Lịch sử gần nhất trượt vào từ góc dưới.
  - **Phân bổ Giọng đọc kép chuyên sâu**:
    + *Mở đầu (Giọng Nữ Ngọc Huyền - 6 câu, 40.36s / 1210 frames)*: Dẫn nhập 77 năm lịch sử NBA, giới thiệu 3 vị trí thi đấu, cỗ máy ghi điểm thời kỳ đầu và vạch xuất phát mùa giải 1949–1950.
    + *Phần đua biểu đồ (Giọng Nam Minh Quân Pro - 27 câu bình luận chuyên sâu, 325.83s / 9775 frames)*: Bình luận sắc bén 27 bước ngoặt lịch sử (George Mikan, Bob Pettit, trận 100 điểm của Wilt Chamberlain, Kareem Abdul-Jabbar dẫn đầu kỷ lục 39 năm, Michael Jordan, Karl Malone, Kobe Bryant, Dirk Nowitzki, thời khắc LeBron James phá kỷ lục 38.387 điểm ngày 07/02/2023 và cán mốc 40.000 điểm ngày 02/03/2024).
    + *Tổng kết & Đánh giá cuối (76.02s / 2280 frames)*: Phân đoạn 3A (Nữ Ngọc Huyền tổng kết 4 câu, header `"TỔNG KẾT BẢNG XẾP HẠNG — ĐIỂM ĐỌC"`, Layout T5 đối sánh biểu đồ toàn cảnh và Top 10 vĩ đại) và Phân đoạn 3B (Nam Minh Quân Pro đánh giá chuyên sâu 4 câu, header `"BÌNH LUẬN & ĐÁNH GIÁ — ĐIỂM ĐỌC"`, 7 huyền thoại từng dẫn đầu, độ bền bỉ qua 22 mùa giải của LeBron James, và triển vọng của Luka Doncic trước mốc 40.000 điểm).
  - **Nghiệm thu đồng bộ Lookahead Hard-Sync**:
    + 27/27 mốc bình luận PASS 100% trong `sync_report.csv` (độ trễ $\le 1$ frame @ 30fps).
    + Tự động giảm tốc nhịp đua xuống 20% khi có lời bình luận, viền highlight trắng neon 0.8s trên thanh bar liên quan.
  - **Chất lượng thị giác & Kiểm duyệt QA**:
    + Thu thập 29 ảnh tư liệu chất lượng cao từ Wikimedia Commons (CC/Public Domain), kiểm duyệt qua bảng ảnh đối chứng `outputs/08.11.2026/qa/contact_sheet_images.jpg`, loại bỏ triệt để ảnh e-commerce hay ảnh dính watermark.
    + Trích xuất 10 khung hình kiểm duyệt QA lưu tại `outputs/08.11.2026/qa/` (từ `qa_01_intro.jpg` đến `qa_10_outro.jpg`).
    + Layout T5 khung 16:9 (`960x540px`) giữ nguyên toàn vẹn biểu đồ snapshot cuối cùng.
  - **Âm thanh Procedural BGM & Loudnorm chuẩn YouTube**:
    + Nhạc nền điện tử Cyber-Stadium tự sinh bằng thuật toán toán học (Numpy/Scipy), miễn nhiễm 100% với YouTube Content ID.
    + Sidechain ducking đạt độ tách bạch **23.4 dB** (vượt chuẩn $\ge 18\text{ dB}$).
    + Chuẩn hóa âm lượng 2-pass đạt **-14.0 LUFS**, True Peak $\le -1.2\text{ dBTP}$, `LRA = 11`.
  - **Bộ 3 Thumbnail A/B/C 1080p & Tài liệu xuất bản**:
    + `thumbnail_A.jpg` (LeBron James vs Kareem: "AI GHI NHIỀU ĐIỂM NHẤT LỊCH SỬ BÓNG RỔ NBA? 77 NĂM ĐỔI NGÔI!")
    + `thumbnail_B.jpg` (Cột mốc 40.000 điểm: "40.000 ĐIỂM: BỨC TƯỜNG CỦA LEBRON JAMES AI CÓ THỂ XÔ ĐỔ?")
    + `thumbnail_C.jpg` (Thế hệ trẻ & Tương lai: "LUKA DONCIC CÓ THỂ VƯỢT LEBRON JAMES? THẾ HỆ TRẺ LIỆU CÓ CƠ HỘI?")
    + Tài liệu SEO `mota.txt` chuẩn 2 phần (3 phương án tiêu đề $\le 100$ ký tự + mô tả + 11 mốc chapters thật), `decisions.md` và `credits.json`.

- **2026-11-07 (Sản Xuất Video Bar Chart Race 16:9 "Cuộc đua chặng thắng F1 1950–2026")**:
  - **Sản phẩm hoàn thiện**: Xuất bản toàn diện video Bar Chart Race 16:9 tại `outputs/07.11.2026/output/Cuoc_dua_chang_thang_F1_1950_2026.mp4` (`1920x1080 @ 30fps`, thời lượng **7m25s / 444.90s**, 13.347 frames, dung lượng **75.1 MB**) và phụ đề `Cuoc_dua_chang_thang_F1_1950_2026.srt` (42 cues).
  - **Dữ liệu & Chuẩn hóa F1**:
    + Bao phủ 40 tay đua vĩ đại (đạt từ 9 chặng thắng trở lên), 919 tháng thi đấu (05/1950 đến 11/2026) và 110 sự kiện lịch sử (dẫn đầu, cột mốc, vượt hạng, thắng cuối, vào top 10).
    + Chuyển sang hiển thị **MÙA GIẢI** lớn rõ nét, loại bỏ hiển thị tháng để khắc phục hoàn toàn sự lệch tháng trong dữ liệu lịch sử.
    + Bảo toàn mốc 74 chặng thắng của Max Verstappen khớp Formula 1 official, ghi nhận Kimi Antonelli không lọt top 10.
  - **Phân bổ Giọng đọc kép chuyên sâu**:
    + *Mở đầu (Giọng Nữ Ngọc Huyền - 6 câu, 38.81s / 1164 frames)*: Dẫn nhập 76 năm lịch sử, giải thích quy tắc màu đỏ (còn thi đấu) và màu xám (đã ngừng thắng), nguồn dữ liệu FIA/StatsF1, và vạch xuất phát Silverstone 1950.
    + *Phần đua biểu đồ (Giọng Nam Minh Quân Pro - 28 câu bình luận chuyên sâu, 329.23s / 9877 frames)*: Bình luận chiều sâu 28 bước ngoặt lịch sử (Ascari, Fangio, Clark, Stewart, Prost, Senna, kỷ nguyên 91 chặng Schumacher, kỷ lục 106 chặng Hamilton, Verstappen bứt phá).
    + *Tổng kết & Đánh giá cuối (70.87s / 2126 frames)*: Phân đoạn 3A (Nữ Ngọc Huyền tổng kết 4 câu, header `"TỔNG KẾT BẢNG XẾP HẠNG — ĐIỂM ĐỌC"`, Hamilton 106, Schumacher 91, Verstappen 74) và Phân đoạn 3B (Nam Minh Quân Pro đánh giá chuyên sâu 4 câu, header `"BÌNH LUẬN & ĐÁNH GIÁ — ĐIỂM ĐỌC"`, 7 huyền thoại từng dẫn đầu, lịch đua 6-10 chặng xưa vs 24 chặng nay, cơ hội của Verstappen trước 2030).
  - **Nghiệm thu đồng bộ Lookahead Hard-Sync**:
    + 28/28 mốc bình luận PASS 100% trong `sync_report.csv` (độ trễ $\le 1$ frame @ 30fps).
    + Tự động giảm tốc nhịp đua xuống 20% khi có lời bình luận, viền highlight trắng neon 0.8s trên thanh bar liên quan.
  - **Chất lượng thị giác & Kiểm duyệt QA**:
    + Thu thập 29 ảnh chất lượng cao CC/Public Domain, kiểm duyệt qua `outputs/07.11.2026/qa/contact_sheet_images.jpg`, loại bỏ triệt để ảnh mô hình đồ chơi/e-commerce.
    + Nhúng 16/16 cờ quốc gia SVG Base64 sắc nét và logo kênh Điểm Đọc.
    + Layout T5 khung 16:9 (`960x540px`) bảo đảm hiển thị trọn vẹn 100% Top 10 không bị cắt chữ.
  - **Âm thanh Procedural BGM & Loudnorm chuẩn YouTube**:
    + Nhạc nền điện tử Cyber-Stadium tự sinh bằng thuật toán toán học (Numpy/Scipy), miễn nhiễm 100% với YouTube Content ID.
    + Sidechain ducking đạt độ tách bạch **24.0 dB** (vượt chuẩn $\ge 18\text{ dB}$).
    + Chuẩn hóa âm lượng 2-pass đạt **-14.0 LUFS**, True Peak $\le -1.2\text{ dBTP}$, `LRA = 11`.
  - **Bộ 3 Thumbnail A/B/C 1080p & Tài liệu xuất bản**:
    + `thumbnail_A.jpg` (Hamilton vs Schumacher: "AI THẮNG NHIỀU NHẤT LỊCH SỬ FORMULA 1? 76 NĂM ĐỔI NGÔI!")
    + `thumbnail_B.jpg` (Cột mốc 106 chặng: "106 CHẶNG THẮNG: BỨC TƯỜNG CỦA HAMILTON AI CÓ THỂ XÔ ĐỔ?")
    + `thumbnail_C.jpg` (Tương lai 2030: "VERSTAPPEN CÓ THỂ VƯỢT LEWIS HAMILTON? 74 CHẶNG Ở TUỔI 29!")
    + Tài liệu SEO `mota.txt` chuẩn 2 phần (3 phương án tiêu đề $\le 100$ ký tự + mô tả + 11 mốc chapters thật), `decisions.md` và `credits.json`.

- **2026-11-07 (Sản Xuất Video Short 9:16: Nghịch Lý Manchester United & Cuộc Khủng Hoảng Cận Kề Nhóm Xuống Hạng)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_Man_Utd_Khung_Hoang_Phong_Do.mp4` tại `outputs/Orther/07.11.2026/shorts/` (thời lượng **72.77s**, 2.183 frames @ 30fps, dung lượng **18.73 MB**) khai thác toàn diện cuộc khủng hoảng phong độ và nghịch lý dứt điểm tại Old Trafford theo các nguồn tin quốc tế và trong nước mới nhất (5–7.11.2026): dẫn đầu Ngoại hạng Anh với 167 cú dứt điểm nhưng chỉ ghi 10 bàn, tỷ lệ chuyển hóa thuộc nhóm thấp nhất giải đấu, chìm sâu xuống vị trí thứ 17 cận kề nhóm xuống hạng; chiếc ghế nóng của Michael Carrick lung lay dữ dội đúng dịp kỷ niệm 40 năm Sir Alex Ferguson cập bến MU (06.11.1986); rò rỉ liên hệ bí mật với cựu thuyền trưởng Pháp Didier Deschamps; và làn sóng phẫn nộ sau phát ngôn của đồng sở hữu Avram Glazer khẳng định giá trị thương mại không phụ thuộc vào thành tích sân cỏ.
  - **Nâng cấp Giọng Nam Mới & Kiểm toán âm thanh**:
    + Chuyển đổi sang **Giọng Nam mới Minh Quân Pro Mẫu 15** (`speed: 1.12, pitch: 0.93, temperature: 0.6` — chất giọng ấm áp, tự nhiên, thoát ly hoàn toàn khỏi độ trầm cũ 0.85).
    + Integrated Loudness **-14.04 LUFS** (chuẩn YouTube -14.0 LUFS), True Peak **-2.43 dBTP** ($\le -1.0$ dBTP), LRA **2.10 LU**.
  - **Bộ ảnh & QA Contact Sheet**:
    + 12 ảnh hiện trường độ nét cao AP/Reuters/Getty Images/Sky Sports/VnExpress ($\ge 1000\text{px}$ đến $2000\text{px}$) được lập kế hoạch phân bổ xen kẽ bám sát từng câu kịch bản.
    + Contact Sheet QA lưu tại `outputs/Orther/07.11.2026/qa/contact_scene_02.jpg`.
  - **Lower-Third 2 góc chuẩn mới**:
    + Góc trái: `📰 NGUỒN: VNEXPRESS / BÁO CHÍ ANH` (màu Cyan `#38BDF8`).
    + Góc phải: Động theo từng ảnh (`PREMIER LEAGUE`, `AP PHOTO`, `ACTION IMAGES / REUTERS`, `MAN UTD / GETTY IMAGES`, `GETTY IMAGES`, `SKY SPORTS`, `VNEXPRESS`).
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium (`Short_Man_Utd_Khung_Hoang_Phong_Do_thumbnail.jpg`, 1080x1920) phong cách typographic Anton 120px + Oswald + PlexMono.
    + File mô tả SEO YouTube Shorts & TikTok (`Short_Man_Utd_Khung_Hoang_Phong_Do_mota.txt`) với 1 tiêu đề duy nhất.
  - **Công cụ điều phối**: `core/build_short_man_utd_khung_hoang.py`.

- **2026-11-07 (Tái Sản Xuất Video Short 9:16: Bóng Đá Trên Xe Đạp Cycle-Ball Với Giọng Nữ Chuẩn Hệ Thống)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_Bong_Da_Xe_Dap_Cycle_Ball.mp4` tại `outputs/Orther/07.11.2026/shorts/` (thời lượng **70.84s**, 2.125 frames @ 30fps, dung lượng **21.40 MB**) giới thiệu môn thể thao độc lạ Radball (Cycle-ball) vừa kết thúc giải vô địch thế giới 2026 tại Ludwigsburg, Đức.
  - **Chuyển đổi Giọng Nữ chính**: Sử dụng preset **Ngọc Huyền Mẫu 14** (`speed: 1.12, pitch: 1.10, temperature: 0.5`), âm sắc trong trẻo, nhịp điệu sinh động, khớp 1-1 với phụ đề Karaoke.
  - **Kiểm toán âm lượng**: Integrated Loudness **-14.03 LUFS**, True Peak **-4.25 dBTP**, LRA **1.40 LU**.
  - **Trọn bộ ấn phẩm**: Video, Thumbnail dọc 9:16 Cyber-Stadium Anton 130px, mô tả SEO 1 tiêu đề duy nhất và Contact Sheet QA `contact_scene_01.jpg`.
  - **Công cụ điều phối**: `core/build_short_cycle_ball.py`.

- **2026-11-06 (Sản Xuất Bộ Đôi Video Short 9:16 Xoay Quanh Sự Kiện Ronaldo Giã Từ ĐTQG Bồ Đào Nha)**:
  - **Video 1 (Ronaldo)**: `Short_Ronaldo_Gia_Tu_Bo_Dao_Nha.mp4` (thời lượng **69.83s**, 2.095 frames @ 30fps) tổng kết hành trình 23 năm, 234 trận, 146 bàn thắng, quyết định nhường áo số 7 và từ chối trận tri ân.
  - **Video 2 (Góc khuất bên lề)**: `Short_Goc_Khuat_Ronaldo_Jorge_Jesus.mp4` (thời lượng **69.83s**, 2.095 frames @ 30fps) phân tích rạn nứt giữa Ronaldo và HLV Jorge Jesus, thái độ phớt lờ, phản ứng từ Chủ tịch Andorinha và thông điệp tri ân từ Al Hilal, Real Madrid, Sporting CP, Man Utd, Rafael Leão, Bruno Fernandes.
  - **Quy chuẩn phát hành**: Đầy đủ 3 mẫu thumbnail A/B/C lựa chọn, 1 tiêu đề duy nhất trong mota.txt, Lower-Third 2 góc động tại `outputs/Orther/06.11.2026/shorts/`.

- **2026-11-05 (Sản Xuất Bộ Đôi Video Short 9:16: Haaland Giúp Man City Hạ Leipzig 3-2 & Liverpool Thua Ngược Fenerbahce 2-3)**:
  - **Video Man City**: `Short_Man_City_Ha_Leipzig_3_2.mp4` (68.73s, 2.062 frames @ 30fps) ghi nhận bàn thắng thứ 62 sau 61 trận cúp C1 của Haaland.
  - **Video Liverpool**: `Short_Liverpool_Thua_Nguoc_Fenerbahce.mp4` (69.23s, 2.077 frames @ 30fps) phân tích sai lầm bóng bổng của hàng thủ The Reds trước đội bóng của Dirk Kuyt.
  - **Quy chuẩn phát hành**: 1 tiêu đề duy nhất, 12 ảnh hiện trường HD, Lower-Third động 2 góc, thumbnail Anton, QA contact sheet tại `outputs/Orther/05.11.2026/shorts/`.

- **2026-11-05 (Sản Xuất Video Short 9:16: Đội Bóng Của Cesc Fàbregas Thắng 9-1 Lập Kỷ Lục Lịch Sử Champions League)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_Como_Thang_Lens_9_1.mp4` tại `outputs/Orther/05.11.2026/shorts/` (1080x1920 @ 30fps) tái hiện toàn cảnh chiến thắng hủy diệt 9-1 của tân binh Como trước chủ nhà RC Lens tại chảo lửa Stade Bollaert-Delelis: cân bằng kỷ lục thắng đậm nhất lịch sử Champions League (+8 bàn của Liverpool 2007 và Real Madrid 2015), đội khách đầu tiên ghi 9 bàn ở cúp C1, cú hat-trick rực sáng của Anastasios Douvikas vươn lên dẫn đầu Vua phá lưới (6 bàn), khoảnh khắc xúc động khi Nico Paz giơ áo tri ân người đàn anh quá cố Jesús de Miguel (Tenerife), măng non 18 tuổi Matteo Papaccioli nổ súng ngày ra mắt, và triết lý kiểm soát bóng 4.27 xG áp đảo của Cesc Fàbregas.
  - **Quy chuẩn tiêu đề duy nhất & Bộ ảnh QA**:
    + Tiêu đề duy nhất theo yêu cầu chuẩn SEO: `Đội bóng của Cesc Fabregas thắng 9-1 lập kỷ lục Champions League #Shorts` (Sentence Case $\le 100$ ký tự).
    + 12 ảnh hiện trường thi đấu độ phân giải cao EPA/AP/Reuters/Getty Images/Cadena SER/Wikimedia Commons ($\ge 940\text{px}$ đến $1280\text{px}$) được lập kế hoạch phân bổ xen kẽ bám sát từng câu kịch bản.
    + Contact Sheet QA lưu tại `outputs/Orther/05.11.2026/qa/contact_scene_02.jpg`.
  - **Lower-Third 2 góc chuẩn mới**:
    + Góc trái: `📰 NGUỒN: VNEXPRESS / UEFA CHAMPIONS LEAGUE` (màu Cyan `#38BDF8`).
    + Góc phải: Động theo từng ảnh (`EPA`, `AP PHOTO`, `CADENA SER`, `GETTY IMAGES`, `REUTERS`, `WIKIMEDIA COMMONS`, `VNEXPRESS`, `CD TENERIFE`).
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium (`Short_Como_Thang_Lens_9_1_thumbnail.jpg`, 1080x1920) phong cách typographic Anton 130px + Oswald + PlexMono.
    + File mô tả SEO YouTube Shorts & TikTok (`Short_Como_Thang_Lens_9_1_mota.txt`).
  - **Công cụ điều phối**: `core/build_short_como_lens_9_1.py`.

- **2026-11-05 (Sản Xuất Video Short 9:16: Siêu Phẩm Phút 90+2 Real Madrid Thắng Ngược Nghẹt Thở 3-2 AEK Athens)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_Real_Madrid_Thang_Nghet_Tho.mp4` tại `outputs/Orther/05.11.2026/shorts/` (thời lượng **69.13s**, 2.074 frames @ 30fps) tái hiện trọn vẹn diễn biến nghẹt thở của trận đấu: Aboubakary Koita mở tỷ số 12', Bellingham đánh gót san bằng 1-1 32', Stavros Pilios 2-1 75', Kylian Mbappé gỡ hòa 2-2 78' (bàn thứ 16 mùa này), và siêu phẩm nã đại bác sấm sét từ 22m của đội trưởng Federico Valverde phút 90+2 ấn định chiến thắng 3-2 cho Real Madrid.
  - **Quy chuẩn tiêu đề duy nhất & Bộ ảnh QA**:
    + Tiêu đề duy nhất theo yêu cầu chuẩn SEO: `Siêu phẩm phút 90+2 giúp Real Madrid thắng ngược nghẹt thở 3-2 #Shorts` (Sentence Case $\le 100$ ký tự).
    + 12 ảnh hiện trường thi đấu độ phân giải cao AP/Reuters/Getty Images/Real Madrid CF ($\ge 1020\times 680$ đến $1440\text{px}$) được lập kế hoạch phân bổ xen kẽ bám sát từng câu kịch bản.
    + Contact Sheet QA lưu tại `outputs/Orther/05.11.2026/qa/contact_scene_01.jpg`.
  - **Lower-Third 2 góc chuẩn mới**:
    + Góc trái: `📰 NGUỒN: VNEXPRESS / UEFA CHAMPIONS LEAGUE` (màu Cyan `#38BDF8`).
    + Góc phải: Động theo từng ảnh (`AP PHOTO`, `REUTERS`, `GETTY IMAGES / UEFA`, `REUTERS / UEFA`, `REAL MADRID CF`, `REUTERS / AP`).
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium (`Short_Real_Madrid_Thang_Nghet_Tho_thumbnail.jpg`, 1080x1920) phong cách typographic Anton 115px + Oswald + PlexMono.
    + File mô tả SEO YouTube Shorts & TikTok (`Short_Real_Madrid_Thang_Nghet_Tho_mota.txt`).
  - **Công cụ điều phối**: `core/build_short_real_madrid_aek.py`.

- **2026-11-09 (Sản Xuất Hoàn Tất Trọn Bộ Video Tuần: Video 16:9 Hoàn Chỉnh ~12 Phút & Video Shorts 9:16 "Tin Nhanh 25 Sự Kiện Nóng Bỏng" Chuẩn Cyber-Stadium)**:
  - **Quy trình vận hành phối hợp 3 Pha (3-Phase Co-Pilot Workflow)**:
    + **Pha 1 (Gemini 3.8 Flash High)**: Lập kế hoạch 25 bản tin tuần (`thethao.json`), thu thập 200 ảnh tư liệu HD, kết xuất 25 bảng Contact Sheet QA (`outputs/09.11.2026/qa/`) và sinh chuỗi giọng đọc ViTTS v3turbo Minh Quân Pro Mẫu 15 (`speed: 1.12, pitch: 0.93`, EBU R128 -16.0 LUFS).
    + **Pha 2 (Gemini 4 Argon Checkpoint)**: Thẩm định thị giác toàn diện 25 bảng cảnh, lọc bỏ ảnh rác, ảnh dọc, ảnh nhầm ngữ cảnh, thay thế triệt để 40 ảnh lỗi bằng ảnh phóng sự chính xác và chuẩn hóa kịch bản timeline.
    + **Pha 3 (Gemini 3.8 Flash High)**: Render hoàn tất Video Master 16:9, Video Shorts 9:16, 3 Thumbnails YouTube A/B/C, 2 file mô tả SEO YouTube và kiểm toán âm thanh.
  - **Sản phẩm Video Chính 16:9 Hoàn Chỉnh**:
    + File video: `outputs/09.11.2026/Tin-The-Thao-09-11.mp4` (1920x1080 @ 30fps, thời lượng **717.3s / 11 phút 57 giây**, 21.520 frames, dung lượng **229.87 MB**).
    + Tổng hợp toàn cảnh 25 sự kiện thể thao chấn động: Ronaldo chia tay ĐTQG Bồ Đào Nha, Como đè bẹp Torino 9-1 lịch sử, Man City thua sốc Brighton, Man United khủng hoảng chạm đáy, Real Madrid ngược dòng C1, V-League vòng 11 và Olaha được triệu tập lên tuyển Việt Nam.
    + Bố cục xoay vòng 5 layouts (Full crossfade, Split 2 panel song song, Triptych 3 panel) đồng bộ nhịp phụ đề Karaoke tự nhiên, tiêu đề cố định 1 hàng (`#fixed-headline-bar` với thuật toán co font DOM thật `fitHeadlineDOM`).
    + Trọn bộ 3 Thumbnail 16:9 A/B/C (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`) và `thumbnail.jpg` đẳng cấp điện ảnh Cyber-Stadium cùng `outputs/09.11.2026/mota.txt` chuẩn SEO (3 option tiêu đề $\le 96$ ký tự, 25 chapters chi tiết).
  - **Sản phẩm Video Shorts 9:16 "Tin Nhanh Thể Thao: Toàn Cảnh 25 Sự Kiện Nóng Bỏng"**:
    + File video: `outputs/09.11.2026/shorts/Short_Tin_Nhanh_25_Tin_The_Thao.mp4` (1080x1920 @ 30fps, thời lượng **168.83s / 2 phút 48 giây**, 5.065 frames).
    + Kịch bản lướt nhanh 25 tin cô đọng, pill số tin cyan neon (`TIN 01/25` đến `TIN 25/25`), chuyển cảnh whoosh cinematic và phụ đề Karaoke 4 từ/cụm nổi bật.
    + Kèm Thumbnail 9:16 typography khối lớn (`Short_Tin_Nhanh_25_Tin_thumbnail.jpg`) và file mô tả `Short_Tin_Nhanh_25_Tin_mota.txt`.
  - **Kiểm toán chất lượng âm thanh Điểm Đọc (Doctor & Audio Check)**:
    + Integrated Loudness: **-14.02 LUFS** (mục tiêu YouTube -14.0 LUFS) $\rightarrow$ ĐẠT CHUẨN.
    + True Peak: **-1.54 dBTP** ($\le -1.0$) $\rightarrow$ ĐẠT CHUẨN.
    + Loudness Range (LRA): **1.70 LU** ($\le 14.0$) $\rightarrow$ ĐẠT CHUẨN.
    + Độ lệch Video vs Audio: **29.6 ms** ($\le 33.3$ ms = 1 frame @ 30fps) $\rightarrow$ ĐẠT CHUẨN.
    + 100% 28 bài kiểm tra hệ thống `core/doctor.py` đều ĐẠT CHUẨN (ALL PASS).

- **2026-11-09 (Chuẩn Hóa & Đồng Bộ Toàn Diện Hệ Thống 3 Loại Video Kênh "Điểm Đọc")**:
  - **Thiết lập kiến trúc thống nhất 3 Loại Video**:
    1. **Loại 1 — Video Tổng Hợp Thông Tin Hằng Tuần (`weekly_digest` — 16:9)**: Lưu tại `outputs/<DD.MM.YYYY>/`, bật `date-chip`, dùng `templates/long_sports_news_v2.html`, xuất kèm 3 Thumbnail 16:9 A/B/C + `mota.txt` 2 phần + `qa/`.
    2. **Loại 2 — Video Dài Theo Chủ Đề / Yêu Cầu Riêng (`thematic_long` — 16:9)**: Lưu tại `outputs/<DD.MM.YYYY>/` (có `special_topic`/`no_date`) hoặc `outputs/Orther/<DD.MM.YYYY>/`, ẩn `date-chip` (`hide_date_chip: true`), xuất kèm 3 Thumbnail 16:9 A/B/C + `mota.txt` 2 phần + `qa/`.
    3. **Loại 3 — Video Ngắn Tin Tức Hằng Ngày / Ý Tưởng Riêng (`short_news` — 9:16)**: Lưu tại `outputs/Orther/<DD.MM.YYYY>/shorts/` (tin lẻ) hoặc `outputs/<DD.MM.YYYY>/shorts/` (Focus Short 2–5 tin / Digest Short 25 tin), dùng `templates/short_news_v2.html` hoặc `templates/short_digest_v2.html`, xuất kèm 1 Thumbnail dọc 9:16 (`templates/thumbnail_9x16_sports.html`) + `_mota.txt` 2 phần.
  - **Xây dựng Module Xuất Bản Trung Tâm `core/diemdoc/publisher.py`**:
    + Chuẩn hóa nạp giọng đọc từ `config/voice.json` (`load_voice_preset`: Nam chính `Minh Quân Pro` Mẫu 15 `speed=1.12, pitch=0.93, temp=0.6`; Nữ thứ hai `Ngọc Huyền` Mẫu 14 `speed=1.12, pitch=1.10, temp=0.5`) trên toàn bộ `m8_news_bridge.py`, `run_day.py`, `m3_voice.py`.
    + Chuẩn hóa cấu trúc file mô tả `mota.txt` 2 phần duy nhất (`write_mota_16x9` & `write_mota_9x16`: `=== TIÊU ĐỀ YOUTUBE ===` Sentence Case $\le 100$ ký tự + `=== MÔ TẢ VIDEO ===` gồm lời dẫn, điểm nhấn, `⏱️ MỐC THỜI GIAN (CHAPTERS):`, nguồn báo, lời kêu gọi đăng ký và dòng `#DiemDoc...` cuối; loại bỏ hoàn toàn `=== HASHTAGS ===` rời rạc).
    + Chuẩn hóa render ảnh bìa ngang 16:9 (`render_thumbnail_16x9_single`) và ảnh bìa dọc 9:16 (`render_thumbnail_9x16`) đồng bộ 100% bảng màu Cyber-Stadium Electric Cyan (`#00E5FF`).
  - **Đồng bộ hóa Giao diện 3 Template HTML v2 (`long_sports_news_v2.html`, `short_news_v2.html`, `short_digest_v2.html`)**:
    + Cả 3 template đều áp dụng chuẩn **Lower-Third 2 góc màn hình**: góc trái `#lt-news-source` (`📰 NGUỒN: <TÊN BÁO>`, màu `#38BDF8`) và góc phải `#lt-photo-credit` (`📷 ẢNH: <NGUỒN ẢNH>`, màu `#F1F5F9` tự động đổi theo từng ảnh/tin qua GSAP).
    + Nâng cấp `templates/short_news_v2.html` và `build_focus_short_timeline` trong `core/m8_news_bridge.py`: Hỗ trợ hoàn hảo Focus Short gộp 2–5 tin (tự động hiện `Hero Title` lớn khi đọc tiêu đề đầu mỗi bản tin `is_title: true`, sau đó thu về `#fixed-headline-bar` và cập nhật `#cat-pill`, `#lt-news-source`, `#lt-photo-credit` theo từng tin, đồng thời chuẩn hóa âm lượng `two_pass_loudnorm` `-14.0 LUFS`).

- **2026-11-04 (Chuẩn Hóa Quy Trình Shorts Riêng Lẻ Trong `outputs/Orther/`, Nguồn Động 2 Góc & Hiệu Ứng Tưởng Niệm Grayscale)**:
  - **Tách biệt thư mục dự án riêng lẻ (`outputs/Orther/<DD.MM.YYYY>/`)**: Quy chuẩn hóa toàn bộ các video Short chuyên đề riêng biệt vào thư mục `outputs/Orther/` theo từng ngày sản xuất, không trộn lẫn vào luồng bản tin dài hằng ngày.
  - **Quy chuẩn hiển thị Lower-Third 2 góc màn hình**:
    + Góc dưới bên trái: Cố định `📰 NGUỒN: <TÊN BÁO CHÍ>` (màu cyan `#38BDF8`).
    + Góc dưới bên phải: Động `📷 ẢNH: <TÊN NGUỒN ẢNH>` tự động cập nhật đồng bộ 100% thời gian thực trên mỗi lần chuyển ảnh bằng GSAP `tl.set(...)`.
  - **Quy chuẩn Semantic Image Planning**: Ánh xạ ảnh theo nội dung từng câu qua `image_plan.json` và `image_credits.json`, hỗ trợ ảnh chính lặp lại 2–3 lần xen kẽ mượt mà.
  - **Kỹ thuật hiệu ứng tưởng niệm (Memorial Grayscale)**: Tự động chuyển đổi màu trắng đen/xám cho các ảnh chân dung tưởng niệm cầu thủ qua đời, bảo đảm sắc thái điện ảnh, trang trọng và tôn kính.

- **2026-11-04 (Sản Xuất Video Short 9:16: Những Bi Kịch Do Va Chạm Trên Sân Cỏ Thế Giới)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_Bi_Kich_Va_Cham_San_Co.mp4` tại `outputs/Orther/04.11.2026/shorts/` (thời lượng **67.43s**, 2.023 frames @ 30fps) tổng kết toàn cảnh các tai nạn va chạm kinh hoàng trong lịch sử bóng đá thế giới từ Jesús de Miguel (2026), Raul Ramirez (2025), Serhiy Perkhun (2001), Choirul Huda (2017) đến Akli Fairuz (2014).
  - **Quy chuẩn tiêu đề duy nhất & Bộ ảnh QA**:
    + Tiêu đề duy nhất theo yêu cầu chuẩn SEO: `Những bi kịch va chạm đau lòng nhất lịch sử bóng đá thế giới #Shorts` (Sentence Case $\le 100$ ký tự).
    + 12 ảnh phân giải cao ($\ge 678\text{px}$ đến $2000\text{px}$) với kỹ thuật Memorial Grayscale (B&W) trang trọng cho các chân dung cầu thủ tử nạn (`Tin_04_2.jpg`, `Tin_04_3.jpg`, `Tin_04_4.jpg`, `Tin_04_6.jpg`, `Tin_04_9.jpg`, `Tin_04_12.jpg`).
    + Contact Sheet QA lưu tại `outputs/Orther/04.11.2026/qa/contact_scene_04.jpg`.
  - **Lower-Third 2 góc chuẩn mới**:
    + Góc trái: `📰 NGUỒN: VNEXPRESS / CADENA SER / REUTERS`
    + Góc phải: Động theo từng ảnh (`CADENA SER / REUTERS`, `CD TENERIFE (B&W)`, `CD COLINDRES (B&W)`, `CSKA MOSCOW (B&W)`, `PERSELA LAMONGAN (B&W)`, `DETIK SPORT / REUTERS`, `PERSIRAJA BANDA ACEH (B&W)`, `WIKIMEDIA COMMONS`).
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium (`Short_Bi_Kich_Va_Cham_thumbnail.jpg`, 1080x1920) phong cách typographic Anton 130px + Oswald + PlexMono.
    + File mô tả SEO YouTube Shorts & TikTok (`Short_Bi_Kich_Va_Cham_mota.txt`).
  - **Công cụ điều phối**: `core/build_short_bi_kich_va_cham.py`.

- **2026-11-04 (Sản Xuất Video Short 9:16: Đề Nghị Đổi Luật Bóng Đá Sau Bi Kịch De Miguel)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_Doi_Luat_De_Miguel.mp4` tại `outputs/Orther/04.11.2026/shorts/` (thời lượng **67.30s**, 2.019 frames @ 30fps) phân tích hậu sự kiện bi kịch Jesús de Miguel, ghi nhận đề xuất từ cựu thủ môn Colombia Nelson Ramos và trọng tài Tây Ban Nha Joan Fabregas kêu gọi FIFA và IFAB siết chặt luật bảo vệ cầu thủ.
  - **Bộ ảnh & QA Contact Sheet**:
    + 12 ảnh phân giải cao ($\ge 683\text{px}$ đến $4912\text{px}$) minh họa: Nelson Ramos (Caracol / Colprensa), trụ sở FIFA Zurich, thẻ đỏ trọng tài, Koen Casteels (VfL Wolfsburg) & Christian Gentner (VfB Stuttgart) trong tiền lệ chấn thương Bundesliga 2017, chân dung tưởng niệm de Miguel (B&W).
    + Contact Sheet QA lưu tại `outputs/Orther/04.11.2026/qa/contact_scene_03.jpg`.
  - **Lower-Third 2 góc chuẩn mới**:
    + Góc trái: `📰 NGUỒN: VNEXPRESS / BÁO CHÍ QUỐC TẾ`
    + Góc phải: Động theo từng ảnh (`COLPRENSA / CARACOL`, `CD TENERIFE (B&W)`, `VNEXPRESS / LA LIGA HYPERMOTION`, `RAC1 / EFE`, `FC ANDORRA / RAC1`, `WIKIMEDIA COMMONS`).
  - **Giọng đọc & Karaoke chuẩn xác**: Sử dụng ViTTS v3turbo Minh Quân Pro, giữ nguyên 100% tên gốc quốc tế (`Jesús de Miguel`, `FIFA`, `IFAB`, `Nelson Ramos`, `Colombia`, `Jesus Owono`, `Joan Fabregas`, `Điều 12`).
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium (`Short_Doi_Luat_De_Miguel_thumbnail.jpg`, 1080x1920) phong cách typographic Anton 130px + Oswald + PlexMono.
    + File mô tả SEO chuẩn YouTube Shorts & TikTok (`Short_Doi_Luat_De_Miguel_mota.txt`).
  - **Công cụ điều phối**: `core/build_short_doi_luat_de_miguel.py`.

- **2026-11-04 (Sản Xuất Video Short 9:16: Thế Giới Bóng Đá Bàng Hoàng Trước Sự Ra Đi Đột Ngột Của Jesús de Miguel)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_De_Miguel_Qua_Doi_Tenerife.mp4` tại `outputs/Orther/04.11.2026/shorts/` (thời lượng **69.70s**, 2.091 frames @ 30fps) dựa trên nguồn bài báo VnExpress và truyền thông Tây Ban Nha về sự ra đi thương tâm của tiền đạo 30 tuổi CLB Tenerife sau tai nạn trên sân.
  - **Kỹ thuật Memorial Grayscale & Đối chứng QA**:
    + Áp dụng bộ lọc xám trắng (B&W) trang nghiêm cho toàn bộ ảnh chân dung tưởng niệm cầu thủ (`Tin_02_1.jpg`, `Tin_02_2.jpg`, `Tin_02_5.jpg`).
    + 12 ảnh phân giải cao ($\ge 1000\text{px}$ đến $3400\text{px}$) minh họa chi tiết: chân dung de Miguel, sân vận động Heliodoro Rodríguez López, tình huống va chạm, thông điệp chia sẻ từ Kylian Mbappé, Pedri, Gerard Piqué, Rafael Nadal, SVĐ Santiago Bernabéu và thông cáo chính thức của CLB Tenerife, FC Andorra.
    + Contact Sheet QA lưu tại `outputs/Orther/04.11.2026/qa/contact_scene_02.jpg`.
  - **Lower-Third 2 góc chuẩn mới**:
    + Góc trái: `📰 NGUỒN: VNEXPRESS / BÁO CHÍ TÂY BAN NHA`
    + Góc phải: Động theo từng ảnh (`CD TENERIFE (B&W)`, `MIGUEL ANGEL SANCHEZ (B&W)`, `LA NACIÓN / LA LIGA`, `WIKIMEDIA COMMONS`, `FC ANDORRA / LA LIGA`).
  - **Giọng đọc & Karaoke chuẩn xác**: Sử dụng ViTTS v3turbo Minh Quân Pro, giữ nguyên 100% tên gốc quốc tế (`Jesús de Miguel`, `Tenerife`, `Andorra`, `Jesus Owono`, `Kylian Mbappé`, `Real Madrid`, `Pedri`, `Barcelona`, `Gerard Piqué`, `Rafael Nadal`, `Pau Gasol`, `Castellon`, `UEFA`, `Cúp Nhà vua`).
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium (`Short_De_Miguel_thumbnail.jpg`, 1080x1920) phong cách typographic Anton 130px + Oswald + PlexMono.
    + File mô tả SEO chuẩn YouTube Shorts & TikTok (`Short_De_Miguel_mota.txt`).
  - **Công cụ điều phối**: `core/build_short_de_miguel.py`.

- **2026-11-04 (Sản Xuất Video Short 9:16: Trận Đấu 51 Thẻ Đỏ Điên Rồ Tại Brazil Phá Kỷ Lục Guinness)**:
  - **Sản phẩm hoàn thiện**: Video 9:16 `Short_Tran_Dau_51_The_Do_Brazil.mp4` tại `outputs/Orther/04.11.2026/shorts/` (thời lượng **67.27s**, 2.018 frames @ 30fps, dung lượng **19.7 MB**) dựa trên nguồn bài báo VnExpress và hồ sơ bóng đá Brazil về trận bán kết lượt đi U20 bang Minas Gerais giữa Uberlandia và Mamore trên sân Parque do Sabia.
  - **Chất lượng hình ảnh & QA 100% sạch**: Bộ 10 ảnh ngang độ phân giải cao ($\ge 1020\text{px}$ đến $3888\text{px}$) ghi lại hiện trường xô xát, sân vận động Parque do Sabia và khoảnh khắc rút thẻ đỏ, kèm Contact Sheet đối chứng tại `outputs/04.11.2026/qa/contact_scene_01.jpg`.
  - **Giọng đọc & Karaoke chuẩn xác**: Sử dụng ViTTS v3turbo Minh Quân Pro (pitch 0.85, speed 1.15), khớp phụ đề Karaoke thời gian thực 1-1 không phiên âm tên riêng gốc (`Uberlandia`, `Mamore`, `Parque do Sabia`, `Fernando Patrick Modesto`, `Guinness`, `Argentina`...).
  - **Kiểm toán âm thanh chuẩn mực**: Integrated Loudness **-14.03 LUFS** (chuẩn YouTube -14.0), True Peak **-2.91 dBTP** ($\le -1.0$), LRA **1.70 LU**, độ lệch Video vs Audio chỉ **1.3 ms** ($\le 33.3$ ms = 1 frame @ 30fps).
  - **Trọn bộ ấn phẩm phát hành**:
    + Thumbnail dọc 9:16 Cyber-Stadium (`Short_Tran_Dau_51_The_Do_thumbnail.jpg`, 1080x1920) phong cách typographic Anton 130px + Oswald + PlexMono.
    + File mô tả SEO chuẩn YouTube Shorts & TikTok (`Short_Tran_Dau_51_The_Do_mota.txt`).
  - **Công cụ điều phối**: `core/build_short_51_the_do.py`.


- **2026-11-03 (Sản Xuất Hoàn Tất 8 Video Shorts Chuyên Sâu & 1 Video Shorts "Tin Nhanh 25 Tin Thể Thao" 9:16 Chuẩn Cyber-Stadium)**:
  - **Sản xuất trọn bộ 8 Video Shorts chuyên sâu 9:16 (Short_01 đến Short_08)**:
    + Định dạng dọc `1080x1920 @ 30fps`, thời lượng tối ưu 35s - 50s/video.
    + Khắc phục hoàn toàn lỗi căn chỉnh ảnh: ảnh ngang được căn giữa mượt mà (`transform: scale(...) translate(...)`), không bị co ép hoặc lệch lề trái.
    + Đồng bộ phụ đề Karaoke theo thời gian thực (ViTTS Minh Quân Pro), chuẩn hóa phát âm tên riêng và từ viết tắt (`data/abbreviations_map.json`: Man Utd -> "MU").
    + Đầy đủ Thumbnail 9:16 và file mô tả `_mota.txt` cho từng video.
  - **Phát hành Video Shorts "Tin Nhanh Thể Thao: Toàn Cảnh 25 Sự Kiện Tuần Qua"**:
    + Video: `outputs/02.11.2026/shorts/Short_Tin_Nhanh_25_Tin_The_Thao.mp4` (thời lượng **168.5s** / 2 phút 48 giây, 5055 frames @ 30fps, dung lượng **37.4 MB**).
    + Viết lại 100% nội dung cho 25 bản tin: thông tin rõ ràng, số liệu cụ thể (ai, làm gì, giải thưởng/kết quả chi tiết), triệt tiêu hoàn toàn cách giật tít mơ hồ.
    + Nâng cấp template `short_digest_v2.html`: tone màu Electric Cyan Cyber-Stadium (`#00E5FF`), pill đếm tin động cyan (`TIN 01/25` đến `TIN 25/25`), chuyển cảnh whoosh cinematic và ducking BGM mượt mà.
    + Ấn phẩm kèm theo: Thumbnail dọc `Short_Tin_Nhanh_25_Tin_thumbnail.jpg` và `Short_Tin_Nhanh_25_Tin_mota.txt` với 25 chapters mốc thời gian chi tiết.

- **2026-11-05 (Dự Án Video Ngang 16:9 — Cuộc Đua Ghi Bàn 1990–2026 — BẢN -2 Hoàn Thiện)**:
  - **Sản xuất hoàn tất Video Bản -2 (v2)**: `outputs/05.11.2026/output/Cuoc_dua_ghi_ban_1990_2026_v2.mp4` (1920x1080 @ 30fps, thời lượng **389.25s / 6 phút 29.2 giây**, dung lượng **23.62 MB**).
  - **Khắc phục 100% lỗi hình ảnh phản hồi từ người dùng**:
    1. **Khung biểu đồ bên trái (Cảnh bình luận)**: Thay thế hoàn toàn ảnh chụp lỗi nền trắng bằng snapshot frame cuối cùng chuẩn mực từ engine render đồ thị Cyber-Stadium (`final_chart_frame_clean.jpg`, nền tối `#0E1522` đồng bộ thương hiệu, RGB mean 47.78).
    2. **Thẻ dữ liệu bên phải**: Viết lại toàn bộ nội dung và audio bình luận khẳng định chỉ số cập nhật thực tế: Cristiano Ronaldo đạt **985 bàn**, Lionel Messi đạt **937 bàn** (cách biệt 48 bàn), Robert Lewandowski đạt **743 bàn**. Biểu đồ dừng ở đợt cập nhật 982 và 933 bàn, và đến nay hai siêu sao đã vươn tới 985 và 937 bàn. Triệt tiêu hoàn toàn các từ ngữ tiêu cực "sai số" hoặc "khác biệt nguồn".
  - **Cải cách đồng bộ Hard Sync & Testable Claims**:
    + Chẩn đoán Bản 1 (`sync_report_old.csv`) phát hiện dồn toa hàng đợi FIFO gây trễ trung bình 3.897s (max 6.5s).
    + Bản -2 (`sync_report_v2.csv`) áp dụng Hard Sync: **100% (43/43 sự kiện PASS logic)**, độ trễ cực đại (`max late_seconds`) giảm xuống chỉ còn **0.167s** ($\le 0.8s$), độ lệch khung hình $\le 2$ frames.
    + Đa dạng hóa 4 mẫu thoại giọng đọc: câu tin tức vượt hạng, câu gợi mở / teaser, câu tự hỏi-đáp thập niên và câu dữ liệu lịch sử.
  - **Phân bổ giọng đọc chuẩn Bản -2**:
    + **Mở đầu (Intro - 26.2s)**: Giọng nữ **Ngọc Huyền** (ViTTS v3turbo).
    + **Cuộc đua (Race - 300.63s)**: Giọng nữ **Ngọc Huyền (`female_only`)** (ViTTS v3turbo).
    + **Bình luận & Tổng kết (Commentary - 56.4s)**: Giọng nam **Minh Quân Pro** (ViTTS v3turbo).
  - **Chuẩn hóa âm thanh & Tài liệu trọn bộ**:
    + Master Audio BGM Acrossfade 3s + Sidechain Ducking tách bạch đạt **19.0 dB** ($\ge 18$ dB), chuẩn Loudnorm EBU R128 đạt **-15.15 LUFS** (True Peak -0.92 dBTP, LRA 9.7 LU).
    + Bộ tài liệu đầy đủ: `Cuoc_dua_ghi_ban_1990_2026_v2.mp4`, `Cuoc_dua_ghi_ban_1990_2026_v2.srt` (56 cues), `mota_v2.txt` (3 option tiêu đề + 7 chapters chính xác theo giây), `decisions_v2.md`, `credits_v2.json`, `sync_report_v2.csv` và `sync_report_old.csv`.

- **2026-11-05 (Dự Án Video Ngang 16:9 — Cuộc Đua Ghi Bàn 1990–2026)**:
  - **Sản xuất video đồ họa dữ liệu động (Bar Chart Race) 16:9 1920x1080 @ 30fps**: `outputs/05.11.2026/output/Cuoc_dua_ghi_ban_1990_2026.mp4` (thời lượng **377.64s / 6 phút 17.6 giây**, 11.149 frames, dung lượng **50.73 MB**).
  - **Tích hợp 4 phần nối liền hoàn chỉnh**:
    1. **Mở đầu (34.5s)**: Giọng nam Minh Quân Pro, hiệu ứng thị giác điện ảnh theo 4 mẫu (T1 Ken Burns, T2 Split-screen, T3 Triptych, T4 Stat Card) với ảnh tư liệu độ phân giải cao từ Wikimedia Commons.
    2. **Phần đua (284.63s)**: Biểu đồ cột chạy 443 tháng (1990-01 đến 2026-11), 35 cầu thủ, nhúng 20 cờ quốc gia SVG Data URI, hiển thị banner thông báo cho toàn bộ 82 sự kiện, hiệu ứng viền trắng phát sáng 0.8s trên thanh cầu thủ liên quan.
    3. **Đồng hồ biến thiên tốc độ (Variable Speed Clock)**: Giọng nữ Ngọc Huyền đọc chọn lọc 42 sự kiện quan trọng (mọi lần đổi ngôi đầu, mốc 700/800/900 bàn, dừng ghi bàn top 5, vào top 10), tự động giảm tốc độ còn 20% trong lúc đọc (làm mềm vào/ra 0.4s), độ lệch video-audio đạt đúng 0 frame (chính xác từng mẫu).
    4. **Bình luận & Tổng kết (52.5s)**: Giọng nam Minh Quân Pro, layout T5 (bảng Top 10 cuối cùng 11/2026 làm mờ bên trái, ảnh tư liệu & so sánh thống kê MessivsRonaldo bên phải).
    5. **Nối Outro kênh**: Ghép nối `logo/Outro.mp4` (6.5s) bằng hiệu ứng mờ chéo hình ảnh (`xfade=fade:0.5s`) và âm thanh (`acrossfade=0.5s`).
  - **Hậu kỳ âm thanh đỉnh cao**: Master giọng đọc kết hợp 3 bản nhạc nền BGM thể thao điện tử, hạ ducking tự động qua `sidechaincompress` đạt độ tách bạch **19.6 dB** (chuẩn >= 18 dB), chuẩn hóa âm lượng EBU R128 đạt chính xác **-14.1 LUFS**, True Peak <= -1.4 dBTP.
  - **Xuất bản trọn bộ tài liệu**: `Cuoc_dua_ghi_ban_1990_2026.mp4`, `mota.txt` chuẩn SEO (3 option tiêu đề, chapters, ghi chú dữ liệu chi tiết, nguồn IFFHS/RSSSF/Transfermarkt), `decisions.md` (nhật ký quyết định kỹ thuật), `credits.json` (bản quyền ảnh & nhạc) và `Cuoc_dua_ghi_ban_1990_2026.srt` (55 mốc phụ đề chuẩn xác).

- **2026-11-02 (Tích Hợp Kho `node_modules/` Dùng Chung & 4 Bộ Thư Viện Chuyển Động / Đồ Họa Mới)**:
  - **Liên kết `node_modules/` dùng chung (`917 MB < 1 GB`) & `.agents/skills/`**: Kết nối trực tiếp `DD-The-thao/node_modules` tới `/Users/phamminhtrieu/Documents/Trieu/Numbers_Modules/node_modules` (dùng chung với `Video-TienDuy` và `Numbers`).
  - **Mở khóa 4 năng lực mới cho Engine HTML v2 (Playwright + GSAP)**:
    1. **`motionmaxxing` (`node_modules/motionmaxxing/` & `.agents/skills/motionmaxxing/`)**: Bộ runtime `motion.js` (12 đường cong gia tốc thực nghiệm từ 53 video chuyên nghiệp), thư viện 3D `hero3d` (Three.js + Bloom) và 4.300 chuyển động mẫu (`precedent.py`, `lint.mjs`, `look.py`).
    2. **`video-shotcraft` (`node_modules/video-shotcraft/` & `.agents/skills/video-shotcraft-recipes/`)**: Kho 124 thẻ công thức góc máy 30fps (`references/shots/`: nhịp cắt trailer thể thao, crash-zoom, quét HUD phân tích chiến thuật, bảng thống kê cầu thủ trượt tuần tự).
    3. **`dataviz` (`node_modules/dataviz/` & `.agents/skills/dataviz/`)**: Phương pháp thiết kế biểu đồ thống kê thể thao và công cụ kiểm chứng độ tương phản màu Cyber-Stadium (`validate_palette.py`).
    4. **`antigravity-animation` (`node_modules/antigravity-animation/`)**: Mẫu hiệu ứng hạt hình học Canvas GPU 60fps (`antigravity-basic.html` & `antigravity-pattern.html`) để nâng cấp lớp phủ `dd_overlay.js`.

- **2026-11-02 (Chuẩn Hóa Quy Trình Bắt Buộc: Bảng Ảnh Đối Chứng Contact Sheet QA & Diệt Rác E-commerce)**:
  - **Tích hợp bước phụ bắt buộc vào quy trình sản xuất**: Tự động sinh hệ thống bảng ảnh Thumbnail Grid (Contact Sheet) chi tiết tại `outputs/<ngày>/qa/` (gồm 25 bảng cảnh `contact_scene_XX.jpg` và 5 bảng tổng hợp `overview_scenes_XX_XX.jpg`), hiển thị đồng thời thumbnail sắc nét, mã định danh ảnh màu cyan và caption đối chứng.
  - **Diệt trừ triệt để ảnh rác từ khóa e-commerce**: Khắc phục dứt điểm lỗi công cụ tìm kiếm nhận nhầm từ khóa ("Bao" thành bao bột mì Meizan, "coach" thành túi xách hàng hiệu, "medal" thành sản phẩm lưu niệm...). Tự động chặn các domain bán lẻ (`shopee`, `tiki`, `lazada`, `shopify`, `susercontent`, `hstatic`...) và bộ lọc ảnh nền trắng sản phẩm.
  - **Thu thập & thẩm định 214/214 ảnh chuẩn xác**: Toàn bộ 214 ảnh tư liệu cho 25 bản tin tuần qua (26.10–01.11.2026) được đối chứng 100% khớp ngữ cảnh, độ phân giải trung bình 2.738px, tỷ lệ ngang 1.62, không watermark.

- **2026-11-02 (Sản Xuất Hoàn Tất Video Long 16:9 Tổng Hợp Thể Thao Tuần Qua — 25 Tin, Chuẩn Bố Cục 1 Hàng & QA Audio)**:
  - **Sản phẩm xuất bản chính thức**: Video 16:9 hoàn chỉnh `Tin-The-Thao-02-11.mp4` tại `outputs/02.11.2026/` (thời lượng 10 phút 32 giây / 632.1s @ 30fps, dung lượng 236 MB) tổng hợp trọn vẹn 25 tin thể thao nổi bật trong tuần qua (10 tin lớn + 15 tin phụ).
  - **Nghiệm thu chuẩn giao diện mới theo yêu cầu Chủ kênh**:
    + **Chip thứ ngày hôm nay**: Hiển thị rõ nét `THỨ HAI · 02.11.2026` với tone Electric Cyan ở Header.
    + **Tiêu đề cố định trên 1 hàng duy nhất**: Toàn bộ 25 tiêu đề được rút gọn súc tích và kết hợp thuật toán co font DOM thật (`fitHeadlineDOM`) tại `#fixed-headline-bar` của `long_sports_news_v2.html`, bảo đảm 100% nằm gọn trên 1 hàng duy nhất (triệt tiêu hoàn toàn rớt dòng).
    + **Bố cục ảnh câu chuyện đa tầng**: Ánh xạ ảnh chuẩn xác từ `image_plan.json` qua `core/m8_news_bridge.py`. Tiêu đề hiển thị Triptych 3 ảnh; nội dung hiển thị tuần tự 1-3 ảnh theo mạch lời dẫn (full crossfade, split 2 panel song song, triptych 3 panel).
    + **Sửa lỗi hiển thị đồng thời cho layout `split`**: Bổ sung nhánh xử lý riêng cho `split` trong GSAP timeline của `long_sports_news_v2.html`, bảo đảm cả 2 ảnh trái-phải đều hiển thị đồng thời ngay từ đầu câu.
    + **Kiểm toán âm thanh đạt 100% chuẩn kỹ thuật Điểm Đọc**: Integrated Loudness **-14.01 LUFS** (chuẩn YouTube -14.0), True Peak **-2.31 dBTP** ($\le -1.0$), Loudness Range (LRA) **1.80 LU**, độ lệch Video vs Audio chỉ **29.0 ms** ($\le 33.3$ ms = 1 frame @ 30fps).
    + **Trọn bộ ấn phẩm phát hành YouTube**: Đầy đủ 3 Thumbnail A/B/C (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`) và file mô tả SEO YouTube `mota.txt` với 25 chapters chi tiết từng giây.
    + **Nâng cấp Hệ thống: Thumbnail chuẩn Cinematic Cyber-Stadium (Ronaldo & Messi style)**: Tái thiết kế toàn bộ 3 Thumbnail 16:9 bằng Playwright + `templates/thumbnail_16x9_sports.html` (Typography khối lớn, tiêu đề 3 tầng màu cyan/trắng/vàng, subtitle thông số, blend mờ nền đen êm ái). Cập nhật vĩnh viễn hàm `generate_3_thumbnails_169` trong `core/run_day.py` để mọi video hằng ngày đều tự động sinh thumbnail đẳng cấp điện ảnh này.
    + **Bộ công cụ Kiểm toán Phát âm Từ Viết Tắt Thể Thao**: Xây dựng `core/build_abbreviations_test_audio.py` tổng hợp 67 từ viết tắt thường gặp (VĐQG, CLB, HLV, ĐTQG, BXH, VAR, CAHN, SLNA, U23, FIFA, PBA...) thành file audio đối chứng `outputs/02.11.2026/kiem_tra_tu_viet_tat.mp3` kèm bảng checklist mốc thời gian `danh_sach_tu_viet_tat.md` để Chủ kênh thẩm định và lập danh mục lưu ý.


- **2026-10-25 (PHẦN 2 — Chuẩn Hoá Giọng Đọc Theo Mẫu Kênh + Tên Riêng manual_overrides, Tái Sản Xuất Video Ronaldo)**:
  - **Xác lập CHUẨN GIỌNG ĐỌC bằng mẫu đo được** (`outputs/_samples/speed_1.15.m4a` — mẫu Chủ kênh chọn ngày 15.10): I = **-16.0 LUFS**, True Peak ≈ -1.4 dBTP. Điều tra phát hiện pipeline cũ chỉ peak-normalize (pydub `normalize(headroom=0.1)`) cho ra **-21.1 LUFS** — nhỏ hơn 5 LU khiến giọng nghe "nhỏ và trầm" (lỗi tái diễn ở 20.10/22.10). Chuỗi tạo giọng (ViTTS Minh Quân Pro + rubberband pitch 0.85:tempo 1.15) được chứng minh ĐÚNG bằng test tổng hợp lại chính câu trong mẫu (F0/centroid khớp tuyệt đối).
  - **Hàm mới `apply_voice_standard()` trong `core/diemdoc/audio.py`**: loudnorm 1-pass về -16 LUFS / TP -1.5 + vòng tự đo-hiệu chỉnh (lệch >0.5 LU thì bù gain thuần + alimiter). `step2_generate_audio` áp trên tổng thể title+silence+summary, bỏ `normalize(headroom)`. Nghiệm thu: audio mới -16.1/-16.2 LUFS (mục tiêu -16.0).
  - **Cơ chế `manual_overrides.json` theo thư mục ngày**: `step2` tự nạp `outputs/<ngày>/manual_overrides.json` (display → say cho TTS, màn hình/karaoke giữ nguyên tên gốc); `m8_news_bridge` nâng cấp nội suy trọng số **say-aware** (`load_say_overrides` + `_expand_say_text` + `_override_word_weights`) để mốc karaoke từng từ khớp bản đọc thật (không lệch cục bộ trong câu). Bộ tách câu `_SENTENCE_SPLIT` mới: không tách tại "..." và chấp nhận dấu đóng câu sau [.!?].
  - **Tái sản xuất toàn bộ video chuyên đề Ronaldo** (giọng chuẩn mẫu + 4 override tên riêng: "Jorge Jesus" → "Gióc Giê Giê Zút", "João Félix" → "Giô Oàn Phê Lích", "Damac" → "Đa Mắc", "24h.com.vn" → "24 H"): `Tin-The-Thao-25-10.mp4` **11:00.4 (660.45s)**, 1920x1080@30fps, 214 MB, I = -13.9 LUFS (chuẩn YouTube -14), TP -1.3 dBFS, LRA 2.0, lệch Video-Audio **23ms (≤1 frame)**, RAM đỉnh 1.22 GB, render 3752.6s.

- **2026-10-25 (Sản Xuất Video Chuyên Đề Cristiano Ronaldo — Thành Phẩm 10p59s + 2 Nâng Cấp Kỹ Thuật)**:
  - **Thành phẩm** (`outputs/25.10.2026/`): Video chính `Tin-The-Thao-25-10.mp4` (**659.3s = 10 phút 59 giây**, 1920x1080 @30fps, 213 MB) dựng bằng Engine HTML v2 (Playwright + GSAP): 9 cảnh × 88 câu, 137 ảnh QA sạch, Karaoke phụ đề Audio-Ground-Truth (cumulative drift = 0), Ken Burns + crossfade, chip ngày `CHỦ NHẬT · 25.10.2026`, Intro/Outro, BGM `bgm_editorial_2_momentum` (0.05), Loudnorm **-13.9 LUFS**, True Peak **-1.4 dBTP**, LRA 2.2, độ lệch Video-Audio **23ms (≤ 1 frame)**, RAM đỉnh 1.17 GB. Kèm 3 Thumbnail YouTube A/B/C + `mota.txt` chuẩn SEO chuyên đề (3 tiêu đề ≤64 ký tự + 10 chapters) + bản copy `_preview_v2/` (9 clip lẻ + mota tự sinh).
  - **Nâng cấp `core/m8_news_bridge.py` — bộ tách câu thông minh**: `_SENTENCE_SPLIT` không tách tại dấu ba chấm "..." (ngắt nhịp drama giữa câu) và chấp nhận dấu đóng câu `' " ) ] »` sau `[.!?]` — khắc phục bẻ vỡ phân bổ ảnh/karaoke với kịch bản có "vừa... bỏ về." hay câu kết trong ngoặc kép.
  - **Nâng cấp `core/run_day.py`**: Thêm chế độ `--shorts none` (chỉ render video chính 16:9, bỏ qua mọi Shorts) cho video chuyên đề đơn lẻ.
  - **Vận hành**: Build đầu gặp Playwright goto-timeout (2 workers tranh chấp I/O với pipeline render khác trên máy) và 1 lần Chromium treo giữa render — cả hai đều phục hồi an toàn nhờ cơ chế Resume `.run_state` cấp tin (chạy lại với `--workers 1`). TTS ViTTS Minh Quân Pro 9 cảnh (pitch 0.85, speed 1.15), tổng audio 642.5s.

- **2026-10-25 (Video Chuyên Đề Cristiano Ronaldo — Kịch Bản 9 Cảnh & Bộ 137 Ảnh Tư Liệu QA 3 Tầng)**:
  - **Kịch bản chuyên đề đã duyệt** (tiêu đề C: *"Ronaldo 41 Tuổi: Bỏ Đội Tuyển, Hỏng Phạt Đền, Cuộc Đua 1000 Bàn"*): 9 cảnh / ~2.900 từ / dự kiến 10,5–11 phút, kèm Fact-Ledger 11 nhóm chứng cứ từ The Guardian, Sky Sports, Al Jazeera, ESPN, Yahoo, Goal, World Soccer Talk, 24h.com.vn, VnExpress, Ngôi Sao (nghiên cứu web thực tế ngày 25.10.2026: vụ bỏ đội tuyển 30.9, án 30 ngày + 255 euro 19.10, hỏng phạt đền trước Neom SC 20.10, bàn 982 tranh cãi Opta/trọng tài 23.10, World Cup 2026 và cuộc đua 1000 bàn).
  - **Bộ công cụ mới `core/build_ronaldo_images.py`**: Chia câu tự động theo luật độ dài (tiêu đề 3 ảnh; <42 từ 1 ảnh; 42–65 từ 2 ảnh; >65 từ 3 ảnh), thu thập 137 ảnh ngang (`W/H ≥ 1.18`, `≥ 800px`) qua DDGS `layout=Wide`, chặn ~40 nguồn rác watermark (stock, YouTube thumbnail, vecteezy, 3D render, Pinterest, collage, forum), khử trùng lặp aHash Hamming ≤ 6, sinh trọn bộ artifact chuẩn: `kich_ban_tung_cau.txt` (137 slot), `thethao.txt`, `thethao.json` (9 items), `image_plan.json` (nhật ký nguồn từng ảnh), contact sheet QA theo cảnh tại cache ngoài Drive.
  - **QA thị giác 7 vòng lặp** bằng contact sheet + giám định ảnh AI: phát hiện và thay thế 54 lượt ảnh lỗi (watermark stock, poster đồ họa, ảnh ghép, screenshot truyền hình, ảnh rugby sai môn, ảnh photoshop, mockup áo đấu); xác minh chéo từng trường hợp báo động nhầm ở cỡ lớn. Kết quả cuối: **137/137 ảnh thật sạch, 0 watermark, 0 ảnh ghép, 100% nạp tốt**.
  - Sản phẩm trung gian tại `outputs/25.10.2026/` (137 ảnh `images/Tin_XX_N.jpg` chia 17/13/15/15/12/13/18/15/19 cho 9 cảnh), sẵn sàng cho bước build TTS → render HTML v2.

- **2026-10-22 (Chuẩn Hóa Quy Trình Sản Xuất Video Shorts 9:16 & Thiết Kế Đồ Họa Cao Cấp)**:
  - **Quy chuẩn định dạng Video Shorts 9:16**:
    + **Thời lượng chuẩn**: Từ **1:30 đến 2:30** (90s – 150s), biên soạn bám sát theo từng câu kịch bản video dài, khai thác triệt để kho tư liệu hình ảnh chất lượng cao.
    + **Bố cục khung hình & Hiệu ứng Pan toàn cảnh (`templates/short_news_v2.html`)**:
      * Header phía trên (`top: 44px`): Logo capsule, chip danh mục, chip ngày phát hành.
      * Thanh tiêu đề cố định (`top: 135px`): Nền tối viền vàng neon, co font tự động theo DOM, giữ cố định suốt video giúp người xem nắm bắt ngay chủ đề.
      * Khung ảnh gần full chiều cao (`top: 245px; bottom: 245px; height: 1430px`, chiếm ~75% màn hình): Chỉ hiển thị duy nhất 1 ảnh tại một thời điểm, giữ nguyên tỉ lệ ảnh gốc. Camera pan mượt mà chạy ngang hết ảnh (luân phiên từ phải sang trái hoặc từ trái sang phải), kết hợp chuyển cảnh ngẫu nhiên (`crossfade`, `slide_fade`, `scale_fade`).
      * Hộp phụ đề Karaoke (`bottom: 45px`): Cố định ở vị trí an toàn, cỡ chữ lớn 48px, luôn hiển thị 100% thời lượng, highlight từ đọc màu vàng kim rực rỡ theo âm thanh thực tế.
    + **Giọng đọc & Phát âm**:
      * ViTTS Minh Quân Pro tự nhiên (`pitch = 1.0`, `speed = 1.15`).
      * Chuẩn phát âm từ mượn/địa danh: `"Palladium"` đọc là `"Pa la đi um"` (viết liền mạch, không dấu gạch ngang) đảm bảo nhịp đọc nhanh, dứt khoát, mượt mà.
    + **Quy chuẩn Thumbnail dọc 9:16 (`core/build_short_thumbnails.py`)**:
      * Tỉ lệ chia đôi hoàn hảo: 58% nửa trên là ảnh hành động sắc nét, tương phản cao, phủ lớp vignette điện ảnh và đính huy hiệu thương hiệu ĐIỂM ĐỌC bo tròn phát sáng.
      * 42% nửa dưới là sân khấu typographic: Kicker monospace cyan neon 26px, Hero title Anton 115–125px giật tít tương phản cực đại, Subtitle Oswald 46px, thanh dải màu gradient vàng-cyan và meta tags chuyên nghiệp.
  - Hoàn tất xuất bản trọn bộ 3 video Short ngày 22.10.2026 (`Short_01`: 01:34, `Short_02`: 01:36, `Short_03`: 01:32) kèm bộ 3 thumbnail thiết kế chuyên nghiệp và file mô tả `mota.txt` chuẩn SEO.

- **2026-10-21 (Tinh Tuyển & Nâng Cấp Hình Ảnh Chuyên Sâu Ballon d'Or 2026 — 20 Ảnh/Cảnh Điểm Nhấn & 0 Watermark)**:
  - **Lọc sạch 100% Watermark & Ảnh Ghép**: Đánh số thứ tự liên tục lại cho toàn bộ ảnh hợp lệ sau khi Chủ kênh xóa các ảnh dính watermark stock (Alamy, Getty, Dreamstime) và ảnh ghép split-screen.
  - **Bổ sung ảnh sạch chất lượng cao editorial**: Tải bổ sung đạt mốc **20 ảnh/cảnh** cho Cảnh 3 (Harry Kane) và Cảnh 4 (Lamine Yamal & Ronaldo Nazário), cùng 15–16 ảnh/cảnh cho 6 cảnh còn lại. Tổng cộng **135 ảnh ngang chất lượng cao** ($\ge 800\text{px}$, không watermark, không ảnh ghép) từ các hãng tin uy tín (Sky Sports, Goal, UEFA, BBC, TalkSport, FC Barcelona...).
  - **Tái tạo Thumbnail YouTube & Re-render trọn gói**:
    + Sinh mới 3 Thumbnail YouTube cực kỳ bắt mắt: `thumbnail_A.jpg` (Harry Kane Sky Sports), `thumbnail_B.jpg` (Lamine Yamal World Cup), `thumbnail_C.jpg` (Ballon d'Or Trophy London Palladium) và `thumbnail.jpg`.
    + Re-render toàn bộ 8 video clip 16:9, ghép nối video chính `Tin-The-Thao-20-10.mp4` (384.3s) và 4 video Shorts 9:16.
  - **Bác sĩ hệ thống**: `core/doctor.py` đạt **100% ALL PASS**. Dọn sạch hoàn toàn `.pyc` vào Trash.

- **2026-10-20 (Sản Xuất Chuyên Đề Đặc Biệt: Quả Bóng Vàng - Ballon d’Or 2026 & Mở Rộng 10–15 Ảnh/Cảnh)**:
  - **Mở rộng nguồn tin & Nghiên cứu chuyên sâu**: Tích hợp dữ liệu từ báo chí quốc tế (France Football, L'Équipe, The Athletic, The Guardian, Marca, TNT Sports) và tỷ lệ cược quốc tế (Betfair, Bet365) về Gala Ballon d'Or 2026 lần thứ 70 tại London Palladium, tri ân Sir Stanley Matthews 1956, cuộc đua Harry Kane (61 bàn thắng) vs Lamine Yamal (vô địch World Cup 2026, kỷ lục 19 tuổi so găng Ronaldo Nazário 1997), các giải thưởng Yashin, Kopa và cú sốc Aitana Bonmatí vắng mặt vì chấn thương.
  - **Bổ sung Từ điển Thể thao (`data/pronunciation_sports.json`)**: Bổ sung hơn 30 tên riêng và giải thưởng mới (Sir Stanley Matthews, London Palladium, Joan García, Unai Simón, David Raya, Pau Cubarsí, Alexia Putellas, Aitana Bonmatí, Melchie Dumornay, Ewa Pajor, Khadija Shaw, Vozinha, Thierry Henry, Kate Scott, Kopa Trophy, Yashin Trophy...).
  - **Nâng cấp độ phủ ảnh phong phú (10–15 ảnh/cảnh)**: Thu thập và xác thực thành công **108 ảnh ngang chất lượng cao** ($W/H \ge 1.18$, $\ge 600\text{px}$) chia đều cho 8 cảnh, phân loại chuẩn xác theo nhân vật/sự kiện thực tế (Kane, Yamal, Mbappé, Messi, các thủ môn, cúp vàng, sân khấu London).
  - **Sản xuất trọn gói ngày 20.10.2026 (`outputs/20.10.2026/`)**:
    + 1 Video chính 16:9 (`Tin-The-Thao-20-10.mp4`, **384.3s ~ 6.4 phút**, 8 cảnh) kết hợp hiệu ứng Smart Ratio, Ken Burns zoompan, xfade mượt mà giữa 13–15 ảnh/cảnh, intro, outro và mix BGM `bgm_editorial_2_momentum.mp3` (vol 0.05).
    + 4 Video Shorts 9:16 (`short_01.mp4` đến `short_04.mp4`, 12–14s/video) trong thư mục `shorts/`.
    + 3 Thumbnail YouTube chuẩn SEO bắt mắt (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`) và `thumbnail.jpg`.
    + File mô tả chuẩn SEO YouTube `mota.txt` kèm 3 tùy chọn tiêu đề và danh sách chương mốc thời gian chính xác 100%.
  - **Kiểm định kỹ thuật**: `core/doctor.py` đạt **100% ALL PASS**. Dọn dẹp cache sạch sẽ tuân thủ Safe Trash.

- **2026-10-19 (Pha 1 & 2 — Tự Chứa Thư Viện, Cầu Nối m8_news_bridge & Bộ Đôi Template v2 Đa Bố Cục)**:
  - **Tự chứa thư viện JS & Font tiếng Việt**: Copy `gsap.min.js` (3.15.0) và plugin `CustomEase.min.js` vào `assets/vendor/js/`, tạo `assets/vendor/VENDOR_INFO.md`. Chuyển symlink `node_modules` và `package.json` trong `DD-The-thao` vào `~/.Trash/` (giữ nguyên thư mục nguồn). Bổ sung 2 họ font tiếng Việt chuẩn: `Barlow Condensed` (tiêu đề) và `Be Vietnam Pro` (nội dung/phụ đề) tại `assets/fonts/`.
  - **Tạo `config/fx.json` & Lớp hiệu ứng Canvas 2D**: Tạo file cấu hình tham số trực quan (sparkles, embers, light sweep 7s, grid lines, vignette, grain toggle). Tích hợp Canvas 2D deterministic dùng PRNG `mulberry32` có seed theo mã tin, vị trí hạt là hàm của $t$, pre-render sprite hạt bằng offscreen canvas.
  - **Nâng cấp khung hình ảnh & Không gian 16:9**: Bổ sung 4 góc bracket kiểu viewfinder (`.corner-bracket`), viền sáng thương hiệu nhẹ (glow), đổ bóng sâu. Không gian hai bên trong layout 16:9 được lấp đầy bằng Side HUD (thông tin chuyên mục/tín hiệu bên trái, equalizer bars động bên phải) không để đen trống.
  - **Khung bản tin phát sóng & Ticker đáy**: Lower-third cố định (category badge + source credit + date), badge số thứ tự `TIN 01/04`, ticker chạy ngang ở đáy (16:9) chạy tiêu đề các tin kế tiếp bằng hàm của $t$.
  - **Chữ & Âm thanh SFX**: Tiêu đề hiện từng từ (staggered word reveal); từ khóa/tỷ số được scale pop kèm 8 hạt lấp lánh bung ra khi karaoke đọc tới. Tích hợp sự kiện SFX (`whoosh_cinematic_short.mp3` khi đổi ảnh/cảnh, `pop_card.mp3` khi bật từ khóa) qua module `_build_sfx` của renderer.
  - **Cầu nối dữ liệu `core/m8_news_bridge.py`**: Đọc `thethao.json` và thư mục `images/` (sau bước lọc ảnh của engine PIL), chia câu, phân bổ 2–3 ảnh/câu (~2–3s/ảnh), xoay vòng 3 bố cục (`full_image`, `split_image`, `polaroid`), gán biến thể Ken Burns (`zoom_in`, `zoom_out`, `pan_left`, `pan_right`) và 3 kiểu chuyển cảnh (`wipe`, `push`, `zoom`) theo hash ổn định.
  - **Tích hợp cờ `--engine html|pil` và `--item` trong `core/run_day.py`**: Mặc định chạy `pil` (FFmpeg/Pillow 1-169.py & 1-916.py); tùy chọn `--engine html` kích hoạt pipeline v2.
  - **Nghiệm thu tin số 1 và số 3 (19.10.2026)**:
    + Xuất bản copy preview và 4 ảnh contact sheet vào `outputs/19.10.2026/_preview_v2/`.
    + Tin 1 (37.57s): 16:9 (162s), 9:16 (160s). Lệch A/V: **3.3 ms** ($\le 33.3\text{ ms}$). Loudness: **-14.04 LUFS**, True Peak: **-2.74 dBTP**.
    + Tin 3 (35.77s): 16:9 (154s), 9:16 (144s). Lệch A/V: **15.3 ms** ($\le 33.3\text{ ms}$). Loudness: **-14.04 LUFS**, True Peak: **-2.39 dBTP**.
    + QA 4 tầng: **0 overflow, 0 overlap**, 100% ảnh load thành công.
    + Bác sĩ hệ thống `core/doctor.py`: **100% ALL PASS**.

- **2026-10-17 (Nhiệm Vụ Khẩn Cấp Lần 4 — Fix Lỗi Map Ảnh JSON, 100% Ảnh Ngang & Thiết Kế Mới Thumbnail YouTube)**:
  - **Sửa triệt để lỗi Map ảnh JSON (`thethao.json`)**: Sửa lỗi logic trong `step1b_map_images_to_json`, quét chính xác 100% tất cả tệp `Tin_{idx:02d}_{seq}.jpg`, map đầy đủ các khóa `"image_1"`, `"image_2"`, `"image_3"`, `"image_4"`... cho toàn bộ 24 bản tin. Kích hoạt hoàn hảo vòng lặp `xfade` chuyển cảnh mờ kết hợp Ken Burns zoompan trong module FFmpeg 1-169.py.
  - **Thiết lập quy tắc cứng 100% Ảnh Ngang**: Loại bỏ hoàn toàn các ảnh đứng (`ratio < 1.15`), chỉ chọn lọc và tải các ảnh có tỷ lệ ngang chuẩn ($W/H \ge 1.18$), tải bù ảnh ngang chất lượng cao $\ge 1200\text{px}$ qua DDGS.
  - **Diệt trừ ảnh game & ads**: Bổ sung negative keywords (`-game -mobile -fc -esports -shopee -lazada`), sửa lỗi gán nhầm ID bài báo trong `thethao.txt` (khắc phục dứt điểm việc ảnh game FC Mobile nhảy vào tin Billiards của Trần Quyết Chiến), dọn sạch các file `art_*_cover.jpg` vào thùng rác.
  - **Viết mới hàm `create_youtube_thumbnail` độc lập**: Cắt ảnh 16:9 sắc nét, phủ Gradient đen 60% bên trái màn hình, Badge đỏ `#E74C3C` `"ĐIỂM ĐỌC • {date_str}"`, tiêu đề font `Roboto-Black.ttf` cỡ lớn (80-96pt) màu VÀNG `#F1C40F` có shadow đen đậm cực kỳ bắt mắt cho 3 phiên bản `thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`.
  - **Sản xuất hoàn tất video thành phẩm**: Video 16:9 (`Tin-The-Thao-16-10.mp4`, 927.5s ~ 15.5 phút) với 24 bản tin sâu sắc, 93 ảnh ngang sắc nét và 6 video Shorts 9:16.

- **2026-10-16 (Đại Phẫu Khôi Phục Toàn Diện Engine FFmpeg/Pillow 1-169.py & Tinh Chọn Ảnh Chuyên Sâu)**:
  - **Khôi phục 100% Engine gốc của Chủ kênh**: Chuyển đổi toàn diện từ HTML/Playwright sang engine PIL + FFmpeg nguyên bản (`1-169.py` cho video 16:9 và `1-916.py` cho Shorts 9:16), giữ nguyên font `Roboto-Black.ttf`, `Roboto-Regular.ttf`, vẽ tiêu đề header, gradient tối dưới chân và hộp phụ đề subtitle nền đen mờ bo chữ sắc nét.
  - **Tái thiết lập cấu trúc lưu trữ 1 thư mục ngày**: Mọi thành phẩm của ngày tập trung tại `outputs/DD.MM.YYYY/` (VD: `outputs/16.10.2026/`) gồm `thethao.txt`, `thethao.json`, `mota.txt`, 3 Thumbnail (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`), thư mục `images/`, `audio/`, `audio-title/`, `shorts/` và DUY NHẤT 1 file MP4 dài hoàn chỉnh `Tin-The-Thao-16-10.mp4`. Toàn bộ file trung gian (frame jpeg, wav tạm) cách ly ngoài Drive tại `~/Library/Caches/DiemDoc/`.
  - **Tích hợp Bộ Lọc & Tinh Chọn Ảnh Thông Minh (Intelligent Image Curation)**:
    + Un-thumb CDN báo chí: Tự động loại bỏ tiền tố `thumb_w/\d+/`, `zoom/\d+_\d+/` để lấy ảnh gốc camera $2048 \times 1366$ đến $2560 \times 1706$.
    + Lọc bỏ ảnh rác phát sóng: Tự động phát hiện và loại bỏ các ảnh banner quảng cáo đài truyền hình (FPT Play, TV360, nền đen tuyền với `dark_ratio > 65%`).
    + Lọc trùng lặp bằng 3D Histogram Correlation: Đo tương quan màu sắc ($\ge 0.85$) phát hiện ảnh trùng góc chụp/khoảnh khắc, tự động giữ ảnh có độ phân giải lớn nhất và xóa ảnh nhỏ.
    + Thuật toán DDGS Fallback (`size=Large`): Tự động tìm bù ảnh chất lượng cao $\ge 1200\text{px}$ khi bài báo thiếu ảnh; giới hạn 3–4 ảnh tối ưu nhất mỗi tin.
    + Chốt chặn kiểm duyệt (Manual QA): Tự động dừng tại terminal để Chủ kênh trực tiếp kiểm tra thư mục `images/` trước khi render video.
  - **Sản xuất trọn gói ngày 16.10.2026**:
    + Video chính 16:9 (`Tin-The-Thao-16-10.mp4`): Dài **927.5 giây (~15.5 phút)** với 24 bản tin sâu sắc, đầy đủ hiệu ứng xfade, Ken Burns zoompan, mix nhạc nền `bgm_editorial_2_momentum.mp3` (vol 0.05), khớp Intro/Outro.
    + 6 Video Shorts 9:16: Dài 11–13s/video nằm trong `outputs/16.10.2026/shorts/` kèm thumbnail dọc riêng biệt.
  - Gỡ bỏ hoàn toàn giới hạn cứng 36 giờ, bổ sung bộ lọc thời gian `--since` linh hoạt (múi giờ ICT UTC+7).
  - Thu thập thành công **103 bài báo thể thao chính thức** từ mốc `2026-10-15 00:01` từ 4 nguồn chính thống (Thanh Niên, Tuổi Trẻ, VnExpress, Dân Trí), bóc tách sạch và loại bỏ tin đồn vô căn cứ.
  - Tự động hóa biên soạn LLM kịch bản 16:9 (11 Cảnh, 38 Graphic Cards, 876 từ) và kịch bản 3 video Short 9:16. Xuất bản Sổ Chứng Cứ `WORK/goi_duyet_noi_dung.md` phục vụ duyệt nội dung trước khi render.
  - Nâng cấp `m2_timeline_builder.py --normalize`: Tự động parse stringified JSON fields (`items`, `pillars`, `rows`, `parts`...), tự động sửa và neo lại `trigger_word` để khớp chính xác `script_text`, tự động bổ sung trường bắt buộc cho `kinetic-statement`, `stat-bento-trio`, `three-pillars`, `photo-card`.
  - Nâng cấp `core/diemdoc/audio.py` (`build_sfx_track`): Hỗ trợ đa hình nhận cả `dict` (timeline) và `list` (events list từ renderer), sửa lỗi `AttributeError` khi dựng SFX.
  - Nâng cấp `engines/html/renderer.py`: Tối ưu hóa cơ chế kiểm tra và tái sử dụng video encode hoàn chỉnh từ thư mục tạm nếu thời lượng khớp, xử lý tuple trả về từ `build_sfx_track`.
  - Xuất bản trọn gói 4 video thành phẩm vào `outputs/_tin_trong_ngay/`:
    + 1 Video chính 16:9 (`diem-doc-sports-20261016.mp4`, 350.4s ~ 5.84 phút) kèm 3 thumbnail A/B/C, mô tả SEO và phụ đề tiếng Việt.
    + 3 Video phụ 9:16 (`Short-01-Quick-Digest.mp4`, `Short-02-Hot-Topic-1.mp4`, `Short-03-Hot-Topic-2.mp4`) kèm thumbnail dọc và metadata riêng biệt.
  - Nghiệm thu âm thanh Master: Loudness $I = -14.1$ LUFS (ĐẠT CHUẨN [-14.8, -13.2] LUFS), $TP = -1.2$ dBTP ($\le -1.0$ dBTP), Ducking separation 23.1 dB ($\ge 18$ dB), độ lệch Audio vs Video 0.0 ms!
  - `core/doctor.py` đạt **100% ALL PASS**.

- **2026-10-19 (Giai Đoạn 5d - Nâng Cấp Template v2 & Lớp Hiệu Ứng Dùng Chung DDOverlay)**:
  - Nâng cấp bộ đôi template `templates/long_sports_news_v2.html` (16:9) và `templates/short_news_v2.html` (9:16):
    + Xóa bỏ 100% nhãn máy móc: bộ đếm câu (`CÂU 01/05`), nhãn tin (`TIN 01/04`), HUD trạng thái tín hiệu, biểu tượng thanh âm thanh, nhãn ảnh báo chí generic (`ẢNH: BÁO CHÍ CHÍNH THỐNG` chỉ hiện khi có tên báo thật).
    + Chuẩn hóa tiêu đề: Cấm dấu `...`, Hero Title 3s đầu (Barlow Condensed ExtraBold, từ khóa vàng `#F59E0B`, chữ hiện theo từ) rồi thu về thanh tiêu đề cố định VẪN NGUYÊN VĂN, co font tự động bằng đo DOM thật (sàn 30px ở 16:9, 44px ở 9:16).
    + Tối ưu 9:16: Tận dụng khoảng trống 250px phía trên ảnh cho tiêu đề cố định, phóng to khung ảnh, phụ đề Karaoke tăng lên 54px trong vùng an toàn TikTok/Shorts (cách đáy >20%, cách đỉnh >12%).
    + Ticker 16:9: Đổi nhãn thành `TIN TIẾP THEO`, chỉ chạy tiêu đề các tin phía sau không có tiền tố máy móc.
    + Tích hợp thư viện lớp phủ dùng chung tự chứa `assets/overlays/dd_overlay.js` tại `z-index: 45` (trên ảnh sân khấu, dưới chữ và karaoke) với blend `lighter`, hỗ trợ hạt lấp lánh (sparkles), bụi sáng (embers), quét sáng (light sweep), và mask giảm độ mờ trung tâm bảo vệ mặt cầu thủ.
  - Nâng cấp cầu nối `core/m8_news_bridge.py`:
    + Bắt buộc chip ngày tiếng Việt: `THỨ HAI · 19.10.2026` phân tích tự động từ thư mục/json, báo lỗi dừng build nếu thiếu.
    + Sinh Kế Hoạch Ngày (Daily Plan) xác định (deterministic) 5 layouts (`full`, `split`, `polaroid`, `cinema`, `triptych`), chống trùng lặp layout giữa các câu liền kề và giữa các tin kế tiếp, chống lặp ảnh liền kề. In bảng kế hoạch ngày ra log.
- **2026-10-19 (Giai Đoạn 5c Ph4 - Chuẩn Hóa Đồng Bộ Âm Thanh Audio-Ground-Truth & Gỡ Bỏ Whisper Khỏi Engine HTML)**:
  - **Gỡ bỏ hoàn toàn Whisper khỏi Engine HTML v2**: Loại bỏ toàn bộ lời gọi mô hình Whisper trong `core/m8_news_bridge.py` cho cả 16:9, 9:16, Focus Short và Digest Short, tiết kiệm 100% tài nguyên tính toán và bộ nhớ.
  - **Triển khai Thuật toán Audio-Ground-Truth Timing**:
    + Mốc câu được tính trực tiếp từ độ dài audio thực tế, tự động bù trừ độ dài `audio_title` và khoảng lặng 0.8s trước khi bắt đầu summary.
    + Ranh giới câu được neo chính xác vào tâm khoảng lặng thực tế qua `silencedetect` của ffmpeg (vết cắt trùng khoảng lặng thật trong phạm vi $\pm 0$ms, cumulative drift = 0 theo định nghĩa).
    + Mốc từ bên trong từng câu được nội suy theo trọng số âm tiết tiếng Việt mở rộng (chuẩn hóa số, từ viết tắt, từ ghép) và dấu câu (nghỉ dấu phẩy $+0.8$, dấu chấm $+1.6$).
  - **Chuẩn hóa Chất lượng Âm thanh YouTube Master**:
    + Gia cố `two_pass_loudnorm` trong `core/diemdoc/audio.py` với `target_tp = -1.5` dBTP và cơ chế bảo vệ True Peak không bao giờ vượt $-1.0$ dBTP.
    + Áp dụng `two_pass_loudnorm` trực tiếp vào pipeline Digest Short master audio.
  - **Cập nhật Cấu hình Short (`config/shorts.json`)**: Cập nhật `seconds_per_item: [5, 7]` cho Digest Short và sửa thuật toán ước tính thời lượng khớp với nội dung `digest_line` thực tế.
  - **Nghiệm thu Toàn diện**:
    + `core/audio_check.py` đạt 100% chuẩn kỹ thuật trên cả 3 thể loại: Tin 1 16:9 (Loudness -14.04 LUFS, TP -2.89 dBTP, lệch 3.3 ms), Focus Short (Loudness -14.04 LUFS, TP -2.27 dBTP, lệch 10.3 ms), Digest Short (Loudness -14.02 LUFS, TP -2.36 dBTP, lệch 21.3 ms).
    + Toàn bộ độ lệch video-audio đều $\le 1$ frame (33.3 ms).
    + Chẩn đoán hệ thống: `python3 -B core/doctor.py` đạt **100% ALL PASS**.

- **2026-10-19 (Giai Đoạn 5c Ph3 - Hoàn Thiện & Chạy Toàn Ngày 19.10.2026 Engine HTML v2)**:
  - Tối ưu hóa UI/UX cả 2 template v2:
    + Loại bỏ hoàn toàn sự trùng lặp ngày/chuyên mục: Ngày chỉ xuất hiện 1 lần duy nhất ở Header, xóa bỏ chip ngày ở lower-third và hero title.
    + Bố cục 9:16: Co gọn vùng ảnh (`top: 300px; bottom: 550px`), nâng hộp phụ đề Karaoke lên vùng `bottom: 395px` (chiếm 72–79.4% chiều cao màn hình, hoàn toàn ra khỏi vùng 20% che khuất của UI TikTok/Shorts).
    + Cập nhật kiểm tra tự động trong `core/m5_qa.py`: Cảnh báo nếu hộp phụ đề 9:16 vượt ngưỡng 80% chiều cao khung hình.
    + Sửa triệt để dấu tiếng Việt trên khung Polaroid bằng font `Barlow Condensed` / `Be Vietnam Pro`.
    + Tăng kích thước hạt lấp lánh (sparkles 6–12px, embers 7–15px) và mở rộng canvas sprite lên 26px trong `dd_overlay.js` để hạt sáng rõ, sắc nét trên khung video thường.
  - Tích hợp liên tục chuyển động hạt qua điểm cắt (Seamless Cut-Concat Particle Flow):
    + Bổ sung tham số `global_offset_sec` vào `m8_news_bridge.py` và `run_day.py` (tích lũy thời lượng các tin trước đó), truyền vào `DDOverlay.update(sec, globalOffsetSec)`, đảm bảo hạt lấp lánh và sóng quét chuyển động liền mạch không giật qua các điểm nối giữa các tin.
  - Chạy full-day build 4 tin bằng lệnh `python3 -B core/run_day.py build --day 19.10.2026 --engine html`:
    + Render thành công 4 clip 16:9 + 4 video Shorts 9:16 + 1 video dài 16:9 ghép nối 4 tin hoàn chỉnh kèm Intro, Outro, BGM (0.05), xuất bản kèm 3 Thumbnail YouTube A/B/C và `mota.txt` vào `outputs/19.10.2026/_preview_v2/`.
    + Nghiệm thu: Lệch video-audio $\le 9.3$ ms ($\le 1$ frame = 33.3 ms), QA layout 0 tràn khung, 0 chồng lấn, Karaoke nằm trọn $\le 80\%$, `doctor.py` đạt 100% ALL PASS.

- **2026-10-19 (Giai Đoạn 5c Ph4 - Thử Nghiệm Quy Mô Lớn 24 Bản Tin, Đa Tiến Trình & Resume)**:
  - Nâng cấp `core/run_day.py`:
    + Thêm cờ `--workers N` (mặc định 1) hỗ trợ render đa tiến trình Playwright Chromium đồng thời qua `ThreadPoolExecutor`.
    + Tính toán trước mốc thời gian tích lũy `global_offset` từ file audio để dòng chảy hạt, sóng ánh sáng và ticker chạy liền mạch 100% xuyên suốt giữa các tin mà không bị gián đoạn hay trôi lệch.
    + Tích hợp cơ chế **Resume an toàn cấp tin** qua file `.run_state` (`completed_169`, `completed_916`): Nếu tiến trình bị gián đoạn, chạy lại sẽ tự động nhận diện và bỏ qua các tin đã hoàn thành chỉ trong < 0.2s. Bổ sung cờ `--force` cho phép render lại toàn bộ khi cần.
    + Bổ sung bộ giám sát mức RAM đỉnh nền (`psutil`) đo lường bộ nhớ tiêu thụ thực tế của toàn bộ cây tiến trình (Python + các tiến trình Playwright Chromium + FFmpeg).
  - Chạy thử nghiệm thành công quy mô lớn trên toàn bộ 24 bản tin của ngày `16.10.2026` trong vùng đệm `~/Library/Caches/DiemDoc/bigrun_test/` (hoàn toàn không ghi đè dữ liệu thật trong `outputs/16.10.2026/`):
    + Render trọn vẹn 24 video 16:9 (`tin_01_long.mp4` đến `tin_24_long.mp4`).
    + Sản xuất 2 Focus Shorts theo phê duyệt của Chủ kênh: Focus Short 1 (`[15, 1, 17]`) và Focus Short 2 (`[13, 3, 18]`).
    + Ghép nối thành công video dài 16:9 `Tin-The-Thao-16-10_v2.mp4` (24 tin + Intro + Outro + BGM 0.05 + 3 Thumbnails YouTube A/B/C + `mota.txt`).
    + Chuẩn hóa âm thanh master EBU R128 (-14 LUFS) kết hợp kẹp độ dài chính xác bằng `atrim` và `-t` đạt độ lệch Video-Audio siêu chính xác: **0.3 ms** (chuẩn <= 33.3 ms).
    + Xuất contact sheet kiểm chứng 5 điểm cắt chuyển cảnh ngẫu nhiên + Intro/Outro: `contact_sheet_cuts.jpg`.
  - Nghiệm thu hiệu năng & kiểm toán:
    + Dung lượng video dài: **222.7 MB** (tiết kiệm **69.7%** dung lượng so với bản PIL cũ 734.3 MB).
    + Thời lượng video: 927.29s (15m 27s), khớp 24/24 cảnh tin.
    + Mức RAM đỉnh (Peak RAM process tree): **2954.0 MB (~2.88 GB)**, vận hành an toàn trên MacBook Air 8 GB RAM.
    + Kiểm toán âm thanh `audio_check.py`: Đạt 100% ALL PASS cho cả video dài 16:9 (-13.95 LUFS, TP -1.22 dBTP, drift 0.3 ms) và 2 Focus Shorts (-14.04 LUFS và -14.03 LUFS).
    + Chẩn đoán hệ thống: `python3 -B core/doctor.py` đạt **100% ALL PASS**.

- **2026-10-19 (Giai Đoạn 5c Ph3 - Ra Mắt 2 Thể Loại Shorts Mới: Focus Short & Digest Short)**:
  - Bổ sung cấu hình điều phối `config/shorts.json` cho phép Chủ kênh tùy biến:
    + `focus`: `items_per_short: [3, 4]`, trần `max_seconds: 170`, gom tin theo thứ tự `order`.
    + `digest`: `max_items: 10`, `seconds_per_item: [7, 10]`, trần `max_seconds: 120`.
    + Tự động in bảng kế hoạch Short ra terminal (tin nào vào short nào, tổng giây ước tính, cảnh báo nếu vượt trần và đề xuất bỏ tin cuối thay vì cắt câu).
  - Triển khai **Focus Short** (`short_focus_01.mp4`): Gộp 3-5 tin chi tiết thành 1 video 9:16 trên `templates/short_news_v2.html`. Giữa các tin có chuyển cảnh mượt mà (~0.4s) kèm SFX whoosh, thẻ tiêu đề Hero xuất hiện đầu mỗi tin làm mốc phân tách trực quan (không gắn nhãn máy móc), cập nhật headline bar, category pill và credit theo từng tin, hạt lấp lánh chạy liền mạch với offset toàn cục.
  - Triển khai **Digest Short** (`short_digest_01.mp4`): Dạng video lướt tin nhanh ("Đọc nhanh thể thao") trên template mới `templates/short_digest_v2.html`. Mỗi tin 7-10s gồm 1 ảnh nét nhất + tiêu đề lớn nguyên văn (co font DOM) + 1 câu tóm tắt $\le 25$ từ đọc bằng ViTTS Minh Quân Pro, phụ đề karaoke nhảy từng từ căn chuẩn bằng Whisper.
  - Tích hợp tham số `--shorts default|focus|digest|all` vào `core/run_day.py build --engine html`.
  - Nghiệm thu: `audio_check.py` đạt 100% (Loudness -14 LUFS, True Peak $\le -1.0$ dBTP, lệch video-audio $\le 1$ frame = 33.3 ms), xuất 2 contact sheet điểm cắt (`contact_sheet_focus_transitions.png` và `contact_sheet_digest_items.png`).
  - Chẩn đoán hệ thống: `python3 -B core/doctor.py` đạt **100% ALL PASS**.

- **2026-10-21 (Sản Xuất Video Chủ Đề Quả Bóng Vàng 2026 — Chuẩn Hóa HTML v2 Engine)**:
  - Cập nhật mặc định `--engine html` trong `core/run_day.py`: Chuyển đổi chính thức hệ thống render sang **HTML v2 Engine** (`templates/long_sports_news_v2.html` via Playwright + GSAP).
  - Khắc phục triệt để hiện tượng lệch phụ đề bằng **Audio Ground Truth**: Thuật toán `ffmpeg silencedetect` dò khoảng lặng thực tế kết hợp trọng số âm tiết tiếng Việt, đảm bảo phụ đề Karaoke từng từ (Word-by-word) đồng bộ hoàn hảo với giọng đọc, **Cumulative Drift = 0**.
  - Tích hợp đầy đủ 5 layouts xoay vòng (`full`, `split`, `polaroid`, `cinema`, `triptych`), lớp phủ hạt ánh sáng **DDOverlay**, chuyển động **Hero Title** và chip ngày tiếng Việt chuẩn (`THỨ BA · 20.10.2026`).
  - Mở rộng quy mô kịch bản chuẩn 10 phút kênh Điểm Đọc: **2.698 từ / 8 cảnh / 627.2 giây (10.45 phút)**, tổng hợp giọng đọc ViTTS Minh Quân Pro (`speed=1.15`, `pitch=0.85`).
  - Tinh tuyển bộ ảnh 133 ảnh sạch (Cảnh 03 Harry Kane và Cảnh 04 Lamine Yamal có 20 ảnh/cảnh), loại bỏ 100% Jonathan Tah, watermark, logo báo chí và ảnh ghép.
  - Xuất bản thành công:
    + Video chính 16:9 hoàn chỉnh: `outputs/20.10.2026/Tin-The-Thao-20-10.mp4` & `outputs/20.10.2026/_preview_v2/Tin-The-Thao-20-10_v2.mp4` (10 phút 27 giây, 1920x1080 @ 30fps).
    + 2 Video Shorts 9:16: `short_focus_01.mp4` & `short_focus_02.mp4`.
    + 3 Thumbnails YouTube: `thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`.
    + Mô tả SEO chuẩn YouTube `mota.txt` khớp từng giây theo 8 chapters.
  - `core/doctor.py` đạt **100% ALL PASS**.

- **2026-10-24 (Cập Nhật Chuẩn Hóa Toàn Hệ Thống: Bỏ Tự Ý Phiên Âm & Giữ Nguyên Tên Gốc)**:
  - Cập nhật quy chuẩn toàn diện theo chỉ đạo của Chủ kênh: **Tuyệt đối không tự ý phiên âm** tên cầu thủ, huấn luyện viên, câu lạc bộ, giải đấu hoặc thuật ngữ quốc tế.
  - Cập nhật `config/voice.json` bổ sung `"auto_transliterate": false`.
  - Cập nhật `core/diemdoc/tts_text.py`: Hàm `prepare()` mặc định giữ nguyên 100% văn bản hiển thị gốc (`display_text`) cho mô hình ViTTS Minh Quân Pro đọc trực tiếp (`Kylian Mbappé`, `Lionel Messi`, `Real Madrid`, `Palladium`...). Chất lượng phát âm chuẩn xác, mượt mà và tự nhiên hơn nhiều so với việc bẻ vụn âm tiết.
  - Hỗ trợ cơ chế `manual_overrides`: Chỉ thực hiện phiên âm khi Chủ kênh đích thân yêu cầu cụ thể sau khi kiểm duyệt video bản nháp.
  - Phụ đề Karaoke và nhịp đọc đạt tỷ lệ khớp 1-1 hoàn hảo từng từ.
  - Thẩm định trạng thái VieNeu-TTS trên GitHub: Các commit mới nhất trên GitHub chỉ liên quan đến LoRA fine-tuning và tài liệu README, không ảnh hưởng đến core model suy luận `v3turbo`. Nhằm tuân thủ tuyệt đối chỉ đạo của Chủ kênh ("Nếu có cần chỉnh/cài đặt lại thì đừng cập nhật"), hệ thống giữ nguyên gói vendored `core/vendor/vieneu` ổn định 100%, bảo toàn trọn vẹn mọi cấu hình và preset giọng đọc.
  - `core/doctor.py` đạt **100% ALL PASS**.

- **2026-10-24 (Xây dựng Bộ Thử Nghiệm & Đối Chiếu Phát Âm TTS: text-audio)**:
  - Khởi tạo thư mục `outputs/22.10.2026/text-audio/` phục vụ kiểm tra và thẩm định phát âm tên riêng/thuật ngữ quốc tế trên mô hình ViTTS Minh Quân Pro.
  - Biên soạn tài liệu `danh-sach.txt` tổng hợp 55 thực thể thể thao xuất hiện trong bản tin 22.10.2026, đối chiếu chi tiết 3 trường phái đọc: (1) Phiên âm có gạch lúc đầu, (2) Phiên âm không gạch viết liền, (3) Đọc thô nguyên bản tiếng Anh/quốc tế.
  - Xuất 3 bộ file âm thanh so sánh (định dạng WAV và MP3, chèn khoảng nghỉ 0.9s giữa các từ để người nghe phân biệt rõ ràng):
    + `01_phien_am_co_gach_luc_dau.wav` / `.mp3` (89.0s): Giọng đọc ngắt âm từng âm tiết có dấu gạch nối (Ví dụ: `Pa - la - di - um`, `Ki-li-an Em-ba-pê`).
    + `02_phien_am_khong_gach_lien_mach.wav` / `.mp3` (89.4s): Giọng đọc liền mạch, nhịp nhanh không ngắt âm (Ví dụ: `Pa la đi um`, `Ki li an Em ba pê`).
    + `03_doc_tho_nguyen_ban.wav` / `.mp3` (87.5s): Giọng đọc trực tiếp từ nguyên bản tiếng Anh/quốc tế không phiên âm (Ví dụ: `Palladium`, `Kylian Mbappé`).
  - Hệ thống đạt kiểm định `core/doctor.py` 100% ALL PASS.

- **2026-10-30 (Thiết Kế Đồ Hoạ Thumbnail Dọc 9:16 Cho Video Shorts "Ronaldo Lập Hat-trick Sau 908 Ngày")**:
  - Thiết kế và render bộ ảnh Thumbnail dọc 9:16 (`1080x1920`) chuẩn nhận diện Điểm Đọc (Cyber-Stadium Neon Dark) cho video `ronaldo_hat_trick_908_ngay_2_916.mp4`.
  - Tinh chọn Hero Image tư liệu sắc nét (`dantri_1.jpg`), căn chỉnh crop tỷ lệ 1.52x tập trung vào gương mặt gầm thét chiến thắng đầy nhiệt huyết của Cristiano Ronaldo trong màu áo vàng Al Nassr, không bị che khuất bất kỳ chi tiết quan trọng nào.
  - Phối hợp Typography thể thao cao cấp (Anton, Oswald, IBM Plex Mono, Montserrat) với gam màu Vàng `#FFC24D`, Neon Cyan `#28E0D0`, Đỏ `#FF5252`.
  - Xuất 3 biến thể A/B/C phục vụ tối ưu CTR:
    + Variant A (Master): `HAT-TRICK 908 NGÀY! CHỈ CÒN 15 BÀN!`
    + Variant B: `HAT-TRICK 908 NGÀY! CÁN MỐC 985 BÀN!`
    + Variant C: `15 PHÚT 3 BÀN THẮNG! CHỈ CÒN 15 BÀN!` (Iconic back fist-pump `vnn_201.jpg`)
  - Lưu đồng bộ thành phẩm tại thư mục dự án video: `/Video/output/ronaldo_hat_trick_908_ngay_2_916_thumbnail.jpg`, `ronaldo_hat_trick_908_ngay_2_916.jpg`, `ronaldo_hat_trick_908_ngay_2_916_thumb_[A,B,C].jpg` và `/Video/workspace/thumbnail.jpg`.

- **2026-10-30 (Sản Xuất Mở Rộng Bộ 3 Shorts 9:16: Bàn 982, World Cup 2026 & Cuộc Đua 1000 Bàn Cập Nhật 985 Bàn)**:
  - **Sản xuất trọn bộ 3 Video Shorts 9:16 mới** (`outputs/25.10.2026/shorts/`):
    + `Short_06_Ban_Thu_982_Tranh_Cai.mp4` (65.27s, 19.0 MB) kèm `Short_06_thumbnail.jpg` (366.8 KB): Drama bàn thắng thứ 982 tại Al Nassr, Opta phán phản lưới, biên bản trọng tài Abdullah Al Owaidan công nhận cho Ronaldo.
    + `Short_07_World_Cup_2026_Ky_Cuoi_Cung.mp4` (90.58s, 30.2 MB) kèm `Short_07_thumbnail.jpg` (375.1 KB): Kỷ lục vĩ đại 20 năm ghi bàn ở 6 kỳ World Cup liên tiếp (2006–2026, 11 bàn), bi kịch dừng bước trước Tây Ban Nha và câu nói "lương tâm trong sáng".
    + `Short_08_Cuoc_Dua_1000_Ban_Moi_Nhat.mp4` (43.82s, 12.6 MB) kèm `Short_08_thumbnail.jpg` (454.1 KB): Cập nhật nóng nhất dữ liệu mới: Ronaldo vừa rực sáng với cú hat-trick hủy diệt, cán mốc 985 bàn thắng sự nghiệp, khoảng cách tới cột mốc 1.000 bàn chỉ còn đúng 15 bàn thắng!
    + Sinh giọng đọc mới bằng ViTTS Minh Quân Pro (pitch 0.85, tempo 1.15, loudnorm -16 LUFS), đồng bộ mốc thời gian phụ đề bằng Whisper Audio-Ground-Truth triệt tiêu hoàn toàn lệch sync.
    + Sinh 3 Thumbnail dọc typographic 9:16 (`Short_06_thumbnail.jpg`, `Short_07_thumbnail.jpg`, `Short_08_thumbnail.jpg`) qua engine Playwright + Chromium.
    + Xuất bộ tài liệu mô tả độc lập (`Short_06_mota.txt`, `Short_07_mota.txt`, `Short_08_mota.txt`), cập nhật file master `mota.txt`, `shorts.json`, `shorts.txt` và đồng bộ toàn bộ tài nguyên vào `_preview_v2/`.

- **2026-10-28 (Sản Xuất Trọn Bộ 3 Shorts 9:16 & Nâng Cấp Toàn Diện Thumbnail Dự Án 25.10.2026)**:
  - **Sản xuất trọn bộ 3 Video Shorts 9:16 độc lập** (`outputs/25.10.2026/shorts/`):
    + `Short_02_Loi_Hua_Bi_Pha_Vo.mp4` (68.24s, 19.8 MB) kèm `Short_02_thumbnail.jpg` (389.3 KB): Biến cố HLV Jorge Jesus nuốt lời hứa đá chính trước trận Na Uy và cuộc rời đi trong đêm 30/9.
    + `Short_03_Mot_Quoc_Gia_Bi_Chia_Re.mp4` (65.62s, 18.2 MB) kèm `Short_03_thumbnail.jpg` (289.9 KB): Đất nước Bồ Đào Nha nứt toạc, lời xin lỗi ngày 6/10 và sự thật bị giấu kín tại phòng họp báo.
    + `Short_04_Ban_An_30_Ngay_255_Euro.mp4` (60.98s, 21.2 MB) kèm `Short_04_thumbnail.jpg` (233.8 KB): Bản án 30 ngày đình chỉ, mức phạt 255 euro (~7,4 triệu VNĐ) và nghịch lý chỉ bằng 40 giây lương tại Al Nassr.
    + Toàn bộ 3 short render trên Engine HTML v2 (`short_news_v2.html`) với hiệu ứng hạt ánh sáng DDOverlay, âm thanh chuẩn hóa loudnorm -14 LUFS, phụ đề karaoke Audio-Ground-Truth và chuyển động ảnh Ken Burns cinematic.
    + Xuất siêu dữ liệu và mô tả chuẩn SEO đa nền tảng vào `shorts.json` và `shorts.txt`.
  - **Tái thiết kế Thumbnail 16:9 (v2) — Xử lý triệt để lỗi che mặt chủ thể**:
    + Crop cận cảnh (close-up x3) khuôn mặt Ronaldo đưa lệch trọn vẹn sang 65% khung hình bên phải (`hero_A_alnassr.jpg`, `hero_B_bench.jpg`, `hero_C_tears.jpg`).
    + Thu hẹp Stage chữ bên trái xuống 38% và co dải gradient đen lại $\le 35\%$, đảm bảo 100% khuôn mặt và biểu cảm của Ronaldo sáng rõ, sắc nét, không bị che khuất.
    + Xuất bản đầy đủ bộ 3 phương án A/B/C (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`, `thumbnail.jpg`) và đồng bộ vào cả `outputs/25.10.2026/` lẫn `_preview_v2/`.
    + Đồng bộ toàn bộ video shorts, thumbnails và `mota.txt` sang `outputs/25.10.2026/_preview_v2/`.

- **2026-10-24 (Sản xuất mở rộng Video Shorts 04 & 05 — Chuẩn hóa 9:16 & Typographic)**:
  - Hoàn thiện sản xuất 2 video Short 9:16 từ Cảnh 05 và Cảnh 07 theo đúng chuẩn của Short 01, 02, 03:
    + `Short_04_Doi_Trong_Kylian_Mbappe_vs_Lionel_Messi.mp4`: Thời lượng 01:45 (105.28s), 10 câu thoại bám sát 14 ảnh tư liệu `Tin_05_1.jpg` đến `Tin_05_14.jpg`.
    + `Short_05_Cu_Soc_Qua_Bong_Vang_Nu_Bonmati_vs_Putellas.mp4`: Thời lượng 01:42 (102.89s), 9 câu thoại bám sát 15 ảnh tư liệu `Tin_07_1.jpg` đến `Tin_07_15.jpg`.
  - Giữ vững các bất biến quy chuẩn:
    + Khung hình 9:16 (1080x1920 @ 30fps), chiều cao ảnh 1430px (~75% màn hình) lia ngang toàn ảnh, hiệu ứng chuyển cảnh ngẫu nhiên mượt mà (`crossfade`, `slide_fade`, `scale_fade`).
    + Subtitle Karaoke chữ lớn 48px cố định chân trang hiển thị 100% thời lượng, highlight từ đang đọc màu vàng `#F59E0B`.
    + Giọng đọc ViTTS Minh Quân Pro tự nhiên (pitch 1.0, speed 1.15), phát âm chuẩn từ điển ("Pa la đi um" không gạch nối, đọc nhanh liền mạch).
    + Sinh 2 thumbnail đồ họa chuẩn typographic `Short_04_thumbnail.jpg` (360 KB) và `Short_05_thumbnail.jpg` (274 KB) bằng Playwright template đồng bộ.
    + Cập nhật đầy đủ mô tả SEO, phương án tiêu đề và hashtags vào `outputs/22.10.2026/shorts/mota.txt`.
    + `core/doctor.py` đạt 100% ALL PASS.

- **2026-10-22 (Sản xuất Video Bản Tin Đặc Biệt: Ballon d'Or 2026 - Tối ưu Chuyển Cảnh Tinh Gọn)**:
  - Hoàn thiện kịch bản chi tiết và sản xuất trọn gói video đặc biệt **Ballon d'Or 2026** (10 phút 27 giây, 2.698 từ / 8 cảnh / ~627s audio) tại `outputs/22.10.2026/`.
  - Bộ 119 ảnh tư liệu landscape ngang ($W/H \ge 1.25$, độ phân giải $\ge 800\text{px}$) được lọc sạch 100% không dính logo/watermark, không dính ảnh ghép.
  - Cập nhật quy chuẩn hiển thị ảnh theo yêu cầu trực quan tinh gọn ("CHỈ HIỆU ỨNG CHUYỂN ẢNH"):
    + **Cảnh Tiêu Đề Mở Đầu**: Hiển thị 3 ảnh trong 1 khung hình (Triptych 3-panel layout với khung trung tâm viền vàng Cyber-Stadium) trong suốt phần đọc tiêu đề (~5s).
    + **Toàn Bộ Các Câu Nội Dung Tiếp Theo**: Hiển thị 1 ảnh đơn lẻ tại một thời điểm (Layout Full thuần túy, loại bỏ hoàn toàn các khung hình phức tạp/khung kép gây rối mắt). Đối với các câu dài chứa 2 ảnh, tự động hòa trộn chuyển cảnh mượt mà (smooth crossfade / dissolve) ở mốc giữa câu.
    + Bảo toàn trọn vẹn phụ đề Karaoke hiển thị chuẩn quốc tế chạy chữ theo khoảng lặng âm thanh thực tế và lớp hạt ánh sáng DDOverlay.
  - Hoàn thành đóng gói xuất bản đầy đủ:
    + Video chính 16:9: `outputs/22.10.2026/Tin-The-Thao-22-10.mp4` (10m 27s, 1920x1080 @ 30fps, 214.7 MB, Loudnorm -14 LUFS).
    + Bộ 3 ảnh Thumbnail YouTube 16:9 A/B/C tối ưu tương phản cao và giật tít chuẩn SEO: `thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`.
    + File SEO `mota.txt` chuẩn YouTube với 3 phương án tiêu đề đúng độ dài vàng 64 ký tự (không bị cắt cụt trên mobile) và timeline chi tiết.
    + Trọn bộ 3 Video Shorts 9:16 đã đổi tên trực quan (`Short_01_Dai_Chien_Harry_Kane_vs_Lamine_Yamal.mp4`, `Short_02_Cuoc_Dua_Yashin_Trophy_Gang_Tay_Vang.mp4`, `Short_03_Cu_Soc_Qua_Bong_Vang_Roi_Paris.mp4`), kèm bộ 3 ảnh Thumbnail 9:16 chuyên dụng và file `shorts/mota.txt`.

- **2026-10-19 (Giai Đoạn 5c Ph2 - Nâng Cấp Giao Diện Thể Thao Đa Dạng v2)**:
  - Xây dựng Master Orchestrator `core/run_day.py` hỗ trợ quy trình 2 lệnh chuẩn cho Chủ kênh:
    + `prepare`: Cào tin (`m1`) -> Lọc tin -> LLM Writer (`m1b`) -> Tạo kịch bản 16:9 & `shorts_units.json` (3 video 9:16) -> Xuất Sổ Chứng Cứ (`WORK/goi_duyet_noi_dung.md`). DỪNG LẠI tại đây để chủ kênh kiểm chứng nguồn tin và phê duyệt kịch bản.
    + `build`: Đọc timeline/units đã duyệt -> Giọng đọc ViTTS Minh Quân Pro (`m3`) -> Đồng bộ phụ đề Whisper/Syllabic (`m5_sync`) -> Validate (`m0`) -> QA Layout & Vision (`m5_qa`) -> Render Playwright (`m4`) -> Master Audio Ducking & Loudnorm (-14 LUFS) (`m6`) -> Đóng gói xuất bản (`m7`).
  - Tích hợp cơ chế **Resume an toàn** (`WORK/.run_state`), tự động lưu vết và tiếp tục từ bước dở dang khi gặp sự cố, hỗ trợ cờ `--force` chạy lại từ đầu và cờ `--mock-render` kiểm thử siêu tốc.
  - Tích hợp pipeline video phụ 9:16: Tự động chuyển đổi `shorts_units.json` (1 Quick Digest + 2 Deep Dive Hot Topics) sang timeline 9:16 (`short_cinematic.html`, max karaoke chars = 26), sản xuất độc lập và đóng gói trọn gói vào `outputs/_tin_trong_ngay/shorts/short_1/`, `short_2/`, `short_3/`.
  - Nghiệm thu End-to-End: Toàn bộ quy trình `build` cho 4 video (1 video 16:9 + 3 video 9:16) hoàn tất trong 184.6s. Bộ công cụ chẩn đoán `core/doctor.py` đạt **100% ALL PASS**.

- **2026-10-16 (Giai Đoạn 5b - Giao Diện Tin Tức Thể Thao, Xử Lý Ảnh & Thumbnail)**:
  - Xây dựng template bản tin thể thao 16:9 chuyên dụng `templates/long_sports_news.html`: Kế thừa bộ khung runtime `_runtime.js`, `_director.js`, `_cards.js`, `_base.css`, áp dụng brand Cyber-Stadium Neon Dark, tối ưu hiển thị 6 component thể thao chủ lực (`title-banner`, `photo-card`, `quote-card`, `fact-list`, `stat-callout`, `dual-number-clash`).
  - Tích hợp hiệu ứng Ken Burns (zoom nhẹ, pan chậm) cho ảnh trong `photo-card` với cơ chế đồng bộ trực tiếp Virtual Clock deterministic của Playwright. Thiết kế badge nguồn ảnh (`📷 NGUỒN: ...`) góc dưới ảnh chuẩn mực báo chí.
  - Tối ưu hóa bộ máy xuất bản `core/m7_publish.py`:
    + Render tự động 3 thumbnail 16:9 (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`) tương ứng 3 góc tiếp cận thử nghiệm A/B/C trên YouTube (Kịch tính / Ngôi sao / Phân tích) bằng template `templates/thumbnail_16x9_sports.html`.
    + Sinh file mô tả `mota.txt` chuẩn SEO YouTube hoàn toàn bằng tiếng Việt (3 phương án tiêu đề, tóm tắt lôi cuốn, mốc thời gian chapters, trích nguồn báo chí, tags & hashtags).
  - Khắc phục các lỗi nền tảng: Thêm hàm `mix_audio` trong `core/diemdoc/audio.py`, chuẩn hoá đường dẫn ảnh tương đối sang `file://` trong `engines/html/renderer.py`, sửa flex-height của `fact-list` để triệt tiêu lỗi tràn khung.
  - Kiểm định QA 4 tầng thành công: Chạy `m5_qa.py _tin_trong_ngay --shots` đạt **0 overlap, 0 overflow (không tràn khung, không chồng lấn)**, tải 100% ảnh hợp lệ và xuất contact sheet `qa_contact_sheet.jpg`.

- **2026-10-16 (Giai Đoạn 5a Phần 2 - Tự Động Hóa Kịch Bản LLM & Sổ Chứng Cứ Fact-Ledger)**:
  - Xây dựng module `core/m1b_llm_writer.py`: Tự động đọc dữ liệu tin cào từ `WORK/temp_raw_news.json`, biên kịch kịch bản video theo giọng đọc BLV thể thao kịch tính, dứt khoát.
  - Tích hợp chuẩn JSON Schema từ `spec/schema.py` (`S.to_json_schema()`), hỗ trợ gọi OpenAI / Gemini / Anthropic API hoặc tự động fallback sang `mock_llm_call()` chuẩn xác 100%.
  - Bắt buộc dẫn nguồn bài báo trong lời thoại (`"Theo VnExpress..."`, `"Theo báo Thanh Niên..."`), neo ngữ nghĩa chặt chẽ (`trigger_word` xuất hiện nguyên văn và đúng thứ tự), khai thác tối đa component thể thao (`title-banner`, `photo-card`, `quote-card`, `fact-list`, `stat-callout`, `dual-number-clash`).
  - Tự động tải và nội địa hóa ảnh tư liệu từ web vào `projects/<project>/images_ready/` đảm bảo hợp đồng đường dẫn tương đối.
  - Tự động sinh Gói Duyệt Nội Dung (Fact-Ledger) tại `WORK/goi_duyet_noi_dung.md` chứa tóm tắt 1 câu, kịch bản chi tiết in đậm số liệu/tên riêng/thời gian và bảng đối chiếu chứng cứ trích dẫn kèm link kiểm chứng 5 phút.
  - Sinh dự án mẫu `projects/_tin_trong_ngay/video_timeline.json` (4 cảnh, 10 cards, 226 từ, 3 ảnh ready) và vượt qua 100% kiểm tra của `m0_validate.py --strict` (**ALL PASS, HỢP LỆ, 0 lỗi, 0 cảnh báo**).

- **2026-10-31 (Quy Chuẩn Cyber-Stadium Electric Cyan, Whisper Sentence Alignment & Hoàn Thành Video Lionel Messi 12m36s)**:
  - **Sản xuất video chuyên đề Lionel Messi**: 9 cảnh (2991 từ, 75 câu), Full HD 1920x1080 @ 30fps bằng engine HTML v2 (Playwright + GSAP virtual clock), thời lượng 12 phút 36 giây (755.9s), Master Audio -13.95 LUFS (chuẩn YouTube -14.0 LUFS), True Peak -1.18 dBTP, độ lệch A/V đạt chuẩn 23.3 ms.
  - **Quy chuẩn số Việt Nam**: Cấm viết dấu chấm hàng nghìn như `1.400` hay `1.180` (tránh ViTTS đọc sai thành số thập phân hoặc ngắt câu). Tự động dọn chấm số hàng nghìn trong `core/diemdoc/tts_text.py`.
  - **Quy chuẩn màu sắc Cyber-Stadium**: Chuyển vĩnh viễn từ tone Cam cũ sang tone **Xanh dương điện ảnh / Electric Cyan** (`#00E5FF`, `#06B6D4`, `#38BDF8`), hiệu ứng Cyan Neon Glow mát mắt, hiện đại, thể thao đỉnh cao và tương phản cực tốt trên nền đen `#060911`.
  - **Quy chuẩn video chuyên đề (Bỏ Date Chip)**: Tự động ẩn chip thứ ngày (`header-date-chip`) khỏi giao diện video và thumbnail đối với video chuyên đề hồ sơ nhân vật/sự kiện không nhắc đến ngày tháng.
  - **Đồng bộ Lời và Phụ đề Karaoke 1-1 bằng Whisper Alignment**: Tích hợp mô hình Whisper base kết hợp `difflib.SequenceMatcher` vào `core/m8_news_bridge.py` (`_align_sentences_whisper`), loại bỏ triệt để hiện tượng cắt nhầm vào khoảng lặng ngắn giữa câu, khớp chuẩn 100% từng mốc câu và từ.
  - **Khắc phục lỗi tái sử dụng cache video**: Nâng cấp `engines/html/renderer.py` bổ sung cờ `force` để dọn sạch `_tmp_*` và không copy nhầm `video_only.mp4` cũ khi cần render mới.
  - **Xuất bản trọn bộ thành phẩm**: Video `Tin-The-Thao-30-10.mp4`, 3 Thumbnail chuẩn A/B/C (`thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`) với badge "ĐIỂM ĐỌC • CHUYÊN ĐỀ HUYỀN THOẠI" tone cyan mát mắt, và mô tả SEO chuẩn `mota.txt` tại `outputs/30.10.2026/`.

- **2026-11-01 (Tối Ưu Hoàn Toàn 3 Thumbnail 16:9 Messi — Khắc Phục Lỗi Khuất Nhân Vật Chính)**:
  - **Khắc phục triệt để lỗi nhân vật chính Messi bị che khuất và tối đen**:
    - Nâng cấp layout `templates/thumbnail_16x9_sports.html`: Mở rộng sân khấu ảnh Hero lên 68% (từ 62%), thu gọn panel chữ còn 42% (từ 52%) chuẩn hệt video Ronaldo 25.10.2026.
    - Cắt tỉa lớp gradient che phủ: Chỉ chuyển tiếp từ 0% đến 35% ở mép giao nhau với cột chữ, từ 35% trở đi hoàn toàn trong suốt 100% (không che một pixel nào của nhân vật). Bỏ hẳn gradient đen phủ 65% từ đáy.
    - Thay thế ảnh tư liệu sắc nét và định vị lại điểm vàng (`object-position`):
      + Variant A: `Tin_01_5.jpg` (Messi áo hồng Inter Miami giang tay ăn mừng bàn thắng cực kỳ nổi bật, `obj_pos: 55% 20%`, độ sáng vùng Hero tăng từ 56.5 lên 115.0).
      + Variant B: `Tin_02_7.jpg` (Messi ôm trọn Quả Bóng Vàng 2023 rạng rỡ, `obj_pos: 60% 18%`, độ sáng vùng Hero tăng từ 21.2 lên 92.4 — tăng hơn 430%).
      + Variant C: `Tin_06_1.jpg` (Messi được kiệu trên vai nâng cúp World Cup 2022 giữa biển pháo hoa vàng Lusail, `obj_pos: 50% 20%`, độ sáng vùng Hero tăng từ 53.0 lên 118.3).
    - Tái xuất bản đồng bộ tại: `outputs/30.10.2026/thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`, `thumbnail.jpg`.

- **2026-10-31 (Hoàn Thiện 3 Thumbnail 16:9 Cinematic Split & Trọn Bộ 9 Video Shorts 9:16 Lionel Messi)**:
  - **Tái tạo 3 Thumbnail 16:9 A/B/C theo phong cách Cinematic Split của video Ronaldo 25.10.2026**:
    - Nâng cấp `templates/thumbnail_16x9_sports.html` bổ sung class màu `.hl-cyan`, gradient mask tối ưu và placeholder `__THUMB_FOOTER_TAG__`.
    - Render bằng Playwright Chromium viewport 1920x1080 @ 95% quality JPEG qua `core/build_messi_thumbnails_cinematic.py`.
    - Variant A (Tuổi 39 & 48 Danh Hiệu): Messi Inter Miami 2026, headline "MESSI TUỔI 39: 48 CHIẾC CÚP VÀ ĐỈNH CAO CÔ ĐỘC!".
    - Variant B (Kỷ Lục 8 Quả Bóng Vàng): Messi nâng cúp Ballon d'Or 2023, headline "8 QUẢ BÓNG VÀNG! BỨC TƯỜNG BẤT TỬ CỦA LIONEL MESSI".
    - Variant C (Cúp Vàng World Cup & Vĩ Đại Nhất): Messi nâng cúp thế giới Lusail trong áo Bisht, headline "VÌ SAO MESSI VĨ ĐẠI NHẤT LỊCH SỬ? CHẤM HẾT TRANH CÃI!".
    - Xuất bản tại: `outputs/30.10.2026/thumbnail_A.jpg`, `thumbnail_B.jpg`, `thumbnail_C.jpg`, `thumbnail.jpg`.
  - **Sản xuất trọn gói 9 Video Shorts 9:16 (Tin 1 đến Tin 9) cho YouTube Shorts / TikTok / Reels**:
    - Dựng trên HTML engine v2 (`templates/short_news_v2.html`) tỷ lệ 1080x1920 @ 30fps qua `core/build_messi_shorts.py`, `core/build_messi_shorts_03_04_05.py` và `core/build_messi_shorts_06_to_09.py`.
    - Cầu nối đồng bộ tự động `core/m8_news_bridge.py` kết hợp Whisper alignment chuẩn 1-1 không lệch nhịp:
      + `Short_01_Messi_Tuoi_39_48_Danh_Hieu.mp4` (81.50s, 23.5 MB, 2.445 frames).
      + `Short_02_Ky_Luc_8_Ballon_dOr_Khong_Doi_Thu.mp4` (82.40s, 21.6 MB, 2.472 frames).
      + `Short_03_672_Ban_Thang_Di_San_Camp_Nou.mp4` (78.20s, 25.4 MB, 2.346 frames).
      + `Short_04_Ky_Tich_91_Ban_Thang_2012.mp4` (78.67s, 21.6 MB, 2.360 frames).
      + `Short_05_936_Ban_466_Kien_Tao_Sieu_Pham_Da_Phat.mp4` (82.34s, 24.7 MB, 2.470 frames).
      + `Short_06_Tu_Nuoc_Mat_Den_4_Cup_Vang_Argentina.mp4` (88.93s, 24.8 MB, 2.668 frames).
      + `Short_07_Ky_World_Cup_Thu_6_Ky_Luc_21_Ban.mp4` (80.99s, 26.7 MB, 2.430 frames).
      + `Short_08_Con_Dia_Chan_Inter_Miami_Nu_Stadium.mp4` (86.17s, 29.5 MB, 2.585 frames).
      + `Short_09_Dinh_Nghia_Lai_Su_Vi_Dai_Vi_The_Bat_Tu.mp4` (83.37s, 32.4 MB, 2.501 frames).
    - Tự động sinh đầy đủ 9 Thumbnail dọc 9:16 (`Short_01_thumbnail.jpg` đến `Short_09_thumbnail.jpg`) chuẩn chia nửa cinematic split và 9 file mô tả SEO (`Short_01_mota.txt` đến `Short_09_mota.txt`) tại `outputs/30.10.2026/shorts/`.

- **2026-11-02 (Sản Xuất Video Thể Thao Tuần 02.11.2026, Từ Điển Viết Tắt & Tinh Chỉnh Toàn Diện 4 Shorts 9:16)**:
  - **Sản xuất trọn gói Video Tin Thể Thao 16:9 Tuần Qua (02.11.2026)**:
    - 25 bản tin (10 tin lớn + 15 tin phụ), thời lượng 10 phút 32 giây (632.1s, 236 MB) tại `outputs/02.11.2026/Tin-The-Thao-02-11.mp4`.
    - Kiểm toán âm thanh: Loudness -14.01 LUFS (mục tiêu -14), True Peak -2.31 dBTP ($\le -1.0$), LRA 1.80 LU, độ lệch Video-Audio 29.0 ms ($\le 33.3$ ms = 1 frame) đạt 100% ALL PASS.
  - **Từ điển chữ viết tắt thể thao & thời sự (`data/abbreviations_map.json`)**:
    - Khảo sát thực tế qua audio 67 từ `kiem_tra_tu_viet_tat.mp3`. Tích hợp 35 từ viết tắt được chủ kênh xác nhận (VĐQG, ĐTQG, Cúp QG, CAHN, SLNA, BXH, TTCN, HCV, HCB, HCĐ, KO, Man Utd, Man United, MU, CĐV, HLV, VĐV, BTC...).
    - Tích hợp `load_abbreviations_dict()` vào `core/diemdoc/tts_text.py`: `Man Utd` & `Man United` được đọc chuẩn thành `"Manchester United"`, `MU` đọc là `"em u"`, trong khi giao diện HTML và Karaoke vẫn giữ nguyên chữ viết tắt gọn gàng và nhóm sáng đồng bộ (`group: true`).
  - **Quy chuẩn chính tả tiếng Việt (Sentence Case)**:
    - Chấm dứt triệt để lỗi Title Case ("In Đậm Ký Tự Đầu"). Toàn bộ 25 tiêu đề, tên nhóm và mô tả trong `thethao.json`, `thethao.txt` và `mota.txt` tuân thủ nghiêm ngặt chuẩn Sentence Case (chỉ viết hoa đầu câu, danh từ riêng và từ viết tắt).
  - **Bộ 3 Thumbnail YouTube 16:9 Playwright & Cập Nhật Option C (Tin 7)**:
    - Thumbnail A: Harry Kane đoạt Quả bóng vàng 2026.
    - Thumbnail B: Quả bóng vàng Mọi thời đại - vinh danh Cristiano Ronaldo & tranh cãi Messi.
    - Thumbnail C: ĐT Malaysia - Bê bối 7 cầu thủ gian lận nhập tịch được xóa án phạt (ảnh thật 2560x1707).
  - **Chuẩn hoá file `mota.txt` chuẩn SEO YouTube**:
    - Tiêu đề $\le 100$ ký tự (85–86 ký tự), đúng 2 phần Tiêu đề + Mô tả, loại bỏ các cụm từ sáo rỗng ("thước phim phân tích") và loại bỏ hashtag thừa.
  - **Sản xuất trọn gói & Tối ưu toàn diện 4 Video Shorts 9:16 (outputs/02.11.2026/shorts/)**:
    - **Khắc phục triệt để lỗi "Sub chưa khớp thoại"**:
      + Bổ sung cơ chế sinh mốc thời gian (Word Timestamps) và Karaoke Chunks cho cảnh Tiêu đề (0.0s đến `summary_start`) trong `core/m8_news_bridge.py`. Hộp phụ đề dưới đáy màn hình hiển thị và tô sáng chính xác từng từ của Tiêu đề ngay từ giây 0, chuyển tiếp mượt mà sang Câu 1 mà không bị nhảy cóc hoặc trôi lệch.
      + Nâng cấp thuật toán đếm âm tiết `_count_syllables()` tính toán chính xác trọng số cho tỉ số ("0-2" = 3 âm tiết), số tự nhiên hàng nghìn/hàng chục ("61" = 3, "38" = 3, "2026" = 5) và tên riêng quốc tế (Kane, Mbappé, Yamal, Manchester, United, Lisandro, Martinez, Bruno, Fernandes...), triệt tiêu hoàn toàn hiện tượng tô sáng chạy trước giọng đọc.
    - **Khắc phục triệt để lỗi "Ảnh bị đứng" & Lệch khuôn mặt nhân vật**:
      + Căn giữa 100% khung hình ảnh trong `templates/short_news_v2.html` (`top: 50%; left: 50%; transform: translate(-50%, -50%); object-fit: cover; object-position: center;`). Nhân vật chính (Kane, Martinez, cầu thủ Malaysia...) luôn nằm trọn vẹn ở tâm điểm thị giác màn hình dọc 1080x1920, không bị cắt xén mất mặt hay lệch sát mép.
      + Tái thiết kế động cơ GSAP Ken Burns: chuyển động liên tục kéo dài toàn bộ thời gian hiển thị (`duration = sliceDur + margin`), kết hợp crossfade mượt mà giữa các ảnh trong cùng 1 câu. Ảnh luôn chuyển động điện ảnh mượt mà từng mili-giây, không bao giờ bị dừng/đứng hình.
    - **Khắc phục triệt để lỗi "Ảnh không khớp nội dung"**:
      + Short 2: Thay thế ảnh Rodri cầm QBV bằng ảnh chân dung Harry Kane chính diện lịch lãm nhận giải (`Tin_01_7.jpg`), khớp 100% khi người đọc nhắc tới Harry Kane.
      + Short 4: Loại bỏ vĩnh viễn ảnh hoạt hình Encanto vào Trash, thay bằng ảnh thật Lisandro Martínez (#6) trong màu áo Manchester United, phát âm chuẩn "Manchester United", khớp từng câu với thẻ đỏ và trận thua 0-2.
      + Short 3: Nâng cấp kịch bản ảnh từ 1 ảnh/câu lên 2 ảnh/câu phân bổ đều 8 ảnh ĐT Malaysia, thời lượng chuẩn 34.6s kèm intro tiêu đề trọn vẹn.
    - **Xuất xưởng thành phẩm**:
      + `Short_01_Harry_Kane_Doat_Qua_Bong_Vang_2026.mp4` (41.6s, 13.8 MB): Kane nhận QBV 2026, kỷ lục 61 bàn thắng, Mbappe, Yamal.
      + `Short_02_Tranh_Cai_Messi_Top_5_Vinh_Danh_Ronaldo.mp4` (40.7s, 14.1 MB): Tranh cãi Top 5 Messi vs Ronaldo nhận QBV Mọi thời đại.
      + `Short_03_Be_Boi_Nhap_Tich_Malaysia_Xoa_An.mp4` (34.6s, 12.4 MB): 7 cầu thủ gian lận nhập tịch Malaysia được xóa án phạt FIFA.
      + `Short_04_Man_Utd_Cham_Day_38_Nam_The_Do_Martinez.mp4` (41.5s, 13.1 MB): Man Utd thua 0-2 Chelsea, thẻ đỏ Lisandro Martinez, giọt nước mắt Bruno Fernandes.
    - Tạo đầy đủ 4 Thumbnail dọc Cyber-Stadium (`Short_01_thumbnail.jpg` đến `Short_04_thumbnail.jpg`) và 4 file mô tả SEO (`Short_01_mota.txt` đến `Short_04_mota.txt`).
    - Chẩn đoán `doctor.py` đạt 100% ALL PASS.

- **2026-11-05 (Sản Xuất Hoàn Tất Video 16:9 Chuyên Đề: 10 Kỷ Lục Bóng Đá Gần Như Không Thể Phá)**:
  - Dự án: `10_ky_luc_bong_da` (Video 16:9 ~8 phút 55 giây, 1920x1080 @ 30fps, 2.358 từ, 12 scenes, 24 cards).
  - Chủ đề: *"Messi 91 bàn, Pelé 3 World Cup, Miura 59 tuổi — kỷ lục nào khó phá nhất?"*.
  - Giọng đọc: ViTTS v3turbo Minh Quân Pro (Sample 15: speed=1.12, pitch=0.93, temp=0.6).
  - Kỹ thuật render & đồng bộ:
    + Thu thập 108 ảnh tư liệu phân bổ 12 cảnh, tạo 13 bảng QA contact sheet kiểm duyệt không dính watermark/e-commerce.
    + Đồng bộ phụ đề Syllabic Ground-truth Alignment: 2.360 từ, 606 cụm Karaoke chunks, 24/24 cards neo chính xác 100% (anchored).
    + Render từng cảnh độc lập qua Playwright Virtual Clock + GSAP, cache cấp scene, ghép nối Cut Concat demuxer (-c copy).
    + Master audio: Sidechain ducking phân tách giọng/BGM 30.5 dB (chuẩn >= 18 dB), SFX track 11 sự kiện, Two-pass Loudnorm YouTube (-14.37 LUFS, True Peak -1.07 dBTP).
    + Độ lệch video-audio đạt chuẩn tuyệt đối: 0.7 ms (<= 1 frame / 33.3 ms).
  - Bộ xuất bản đầy đủ:
    + Video: `outputs/10_ky_luc_bong_da/10_ky_luc_bong_da.mp4` (29 MB).
    + 3 Thumbnails 16:9 A/B/C: `thumbnail_A.jpg` (Kỷ lục bất tử - Messi), `thumbnail_B.jpg` (Cuộc đua vĩ đại - CR7), `thumbnail_C.jpg` (Ngọn núi Everest - Pelé) + `thumbnail.jpg`.
    + Metadata SEO YouTube: `mota.txt` (3 phương án tiêu đề A/B/C, 12 mốc chapters, nguồn báo chí, tags & caption mạng xã hội).
    + Kịch bản phụ đề: `sub_tieng_viet.txt`.

- **2026-11-01 (Nâng cấp Video Intro & Outro Chính Thức Kênh Điểm Đọc v2)**:
  - Tái thiết kế toàn diện 2 video mở đầu và kết thúc cho kênh **Điểm Đọc** đồng bộ chuẩn thương hiệu Cyber-Stadium:
    + **Intro.mp4 chính thức (5.0s @ 30fps)**: Phong cách Kinetic Minimalist (chọn từ mẫu Intro 4). Giọng đọc nữ Bắc Trúc Ly tự nhiên, hấp dẫn (*"Điểm Đọc tin giúp bạn! Tổng hợp thể thao chính thống và xem nhanh theo từng mốc nội dung."*). Kết hợp âm nhạc điện tử dồn dập `bgm_upbeat_3_intro_7s.mp3`, laser sweep neon Cyan/Gold và 2 âm strike line đồng bộ từng frame với mốc 01 & 02.
    + **Outro.mp4 chính thức (6.5s @ 30fps)**: Phong cách Cinematic Horizontal Rail (chọn từ mẫu Outro 6). Giọng đọc nữ Bắc Trúc Ly (*"Cảm ơn bạn đã xem video! Hãy dành tặng Điểm Đọc một Like và một Đăng ký để tiếp thêm động lực cho chúng mình nhé!"*). Kết hợp nhạc Lo-Fi chill `bgm_lofi_vibes.mp3`, hiệu ứng pop card **1 LIKE** và tiếng chuông ngân **1 ĐĂNG KÝ** sinh động kèm fade to black cuối mượt mà.
  - Lưu trữ an toàn các phiên bản Intro/Outro cũ vào thư mục `old/` tại `logo/old/` (chính sách Safe Trash & Lưu trữ lịch sử).
  - Vị trí chuẩn hoá: `logo/Intro.mp4`, `logo/Outro.mp4` và thư mục sản phẩm ngày `outputs/01.11.2026/` (đã dọn dẹp thư mục projects thừa và các tệp dư thừa theo chỉ đạo).

- **2026-11-05 (Tích Hợp Giọng Nữ Chuẩn Thứ Hai & Cấu Trúc Kho Giọng `assets/voices/`)**:
  - Thử nghiệm và đánh giá toàn diện 11 giọng đọc nữ bản địa của mô hình ViTTS v3turbo và 16 biến thể tinh chỉnh chuyên sâu.
  - Phê duyệt chính thức **Giọng Nữ Thứ Hai (Secondary Voice)**: **Ngọc Huyền Mẫu 14** (`voice: "Ngọc Huyền"`, `speed: 1.12`, `pitch: 1.10`, `temperature: 0.5`). Thuật toán nâng pitch +10% tôn vinh chất âm thanh cao, trong trẻo, bay bổng đặc trưng của phái nữ mà không hề bị chói tai.
  - Tái cấu trúc thư mục tài nguyên `assets/voices/`:
    + `assets/voices/voices.json`: Manifest tổng quản lý 2 giọng chuẩn của hệ thống.
    + `assets/voices/male/`: Giọng nam chính **Minh Quân Pro Mẫu 15** (`spd 1.12, pch 0.93, temp 0.6`), lưu trữ `voice.json`, `sample_15_Minh_Quan_Pro_var15_spd1.12_pch0.93.m4a` & `.wav`.
    + `assets/voices/female/`: Giọng nữ thứ hai **Ngọc Huyền Mẫu 14** (`spd 1.12, pch 1.10, temp 0.5`), lưu trữ `voice.json`, `sample_14_Ngoc_Huyen_var14_spd1.12_pch1.10.m4a` & `.wav`.
  - Nâng cấp `config/voice.json`: Tích hợp khối `presets` quản lý cả `primary` (nam chính) và `secondary` (nữ thứ hai).
  - Nâng cấp `core/m3_voice.py`: Hỗ trợ cờ `--voice` thông minh (nhận diện các alias `female`, `nu`, `ngoc_huyen`, `14`, `secondary` hoặc `male`, `nam`, `15`, `primary`) và tự động đọc `voice_config` từ timeline hoặc `voice.json` cấp project.

- **2026-11-07 (Sản Xuất Video Short 9:16 Thể Thao Độc Lạ: Bóng Đá Trên Xe Đạp Cycle-Ball Tại `outputs/Orther/07.11.2026/`)**:
  - Dựng hoàn tất video Short 9:16 chuyên đề về môn thể thao kỳ lạ Cycle-ball (Radball) vừa khép lại giải vô địch thế giới 2026 tại Ludwigsburg, Đức:
    + **File video MP4**: `Short_Bong_Da_Xe_Dap_Cycle_Ball.mp4` (67.25s, 20.2 MB, 1080x1920 @ 30fps).
    + **Âm lượng**: Integrated Loudness -14.04 LUFS (chuẩn YouTube), True Peak -3.38 dBTP, LRA 1.60 LU.
    + **Nội dung & Luật chơi**: Cấm cầu thủ chạm chân xuống sàn, dùng bánh xe đạp không phanh để rê dắt, chuyền bóng và dứt điểm; chiến thắng 8-1 của cặp đôi Áo Patrick Schnetzer & Markus Bröll; lịch sử hơn 140 năm từ năm 1883 của Nick Kaufmann được UCI công nhận.
    + **Tư liệu & Lower-Third**: 12 ảnh HD từ UCI và Wikimedia Commons (độ phân giải 1020px - 3000px); góc trái hiển thị `📰 NGUỒN: VNEXPRESS / UCI`, góc phải cập nhật động nguồn ảnh theo từng frame.
    + **Tài nguyên đi kèm**: Thumbnail dọc Cyber-Stadium `Short_Bong_Da_Xe_Dap_Cycle_Ball_thumbnail.jpg` (376.5 KB), mô tả SEO YouTube đúng 1 tiêu đề duy nhất `Short_Bong_Da_Xe_Dap_Cycle_Ball_mota.txt`, và bảng ảnh đối chứng QA `contact_scene_01.jpg`.

- **2026-11-06 (Sản Xuất 2 Video Shorts Chuyên Đề Về Cristiano Ronaldo Giã Từ ĐTQG Tại `outputs/Orther/06.11.2026/`)**:
  - Triển khai toàn diện 2 video Shorts 9:16 chuyên đề về sự kiện Cristiano Ronaldo chính thức giã từ đội tuyển Bồ Đào Nha sau 23 năm huyền thoại:
    1. **Short 01**: *Cristiano Ronaldo giã từ đội tuyển Bồ Đào Nha sau 23 năm huyền thoại* (`Short_Ronaldo_Gia_Tu_Bo_Dao_Nha.mp4`, 70.68s, 18.1 MB, -14.04 LUFS) — Quyết định chia tay xúc động ở tuổi 41, trao lại áo số 7 thiêng liêng, kỷ lục 234 trận và 146 bàn thắng quốc tế, đỉnh cao Euro 2016, và sự kiên định từ chối đá trận tri ân hình thức của FPF để ngẩng cao đầu trọn vẹn.
    2. **Short 02**: *Góc khuất Ronaldo phớt lờ HLV Jorge Jesus khi chia tay Bồ Đào Nha* (`Short_Goc_Khuat_Ronaldo_Jorge_Jesus.mp4`, 74.61s, 18.7 MB, -14.04 LUFS) — Hé lộ cuộc khủng hoảng niềm tin gay gắt: Ronaldo đi trước 24h không thèm báo HLV Jorge Jesus, phát ngôn phân trần về bức ảnh lớn của Jorge Jesus trên Canal 11, Chủ tịch CLB Andorinha Duarte Santos tố HLV đâm sau lưng, và làn sóng tri ân toàn cầu từ Thủ tướng, Georgina Rodriguez cùng các cựu đồng đội.
  - Tuân thủ nghiêm ngặt chuẩn kỹ thuật Điểm Đọc:
    + Thư mục lưu trữ riêng biệt ngoài bản tin hằng ngày: `outputs/Orther/06.11.2026/` (gồm `thethao.json`, `thethao.txt`, `image_credits.json`, `image_plan.json`, `images/`, `audio/`, `audio-title/`, `shorts/`, `qa/`).
    + Lower-Third động 2 góc: Bên trái là nguồn báo chí uy tín (`📰 NGUỒN: VNEXPRESS / REUTERS / AP` / `📰 NGUỒN: VNEXPRESS / A BOLA / CANAL 11`), bên phải cập nhật động nguồn ảnh theo từng lần đổi khung hình.
    + Đúng 1 tiêu đề duy nhất trong `mota.txt`, viết hoa chuẩn Sentence Case tiếng Việt, giữ nguyên 100% danh từ riêng quốc tế (Cristiano Ronaldo, Jorge Jesus, Pedro Proenca, Duarte Santos, Georgina Rodriguez, Euro 2016...).
    + Âm lượng chuẩn YouTube loudnorm -14.04 LUFS, True Peak $\le -1.57$ dBTP, ducking BGM và SFX hoàn chỉnh.

- **2026-11-05 (Sản Xuất 4 Video Shorts Chuyên Đề Cúp C1 Tại Thư Mục Tách Biệt `outputs/Orther/05.11.2026/`)**:
  - Triển khai quy chuẩn mới cho dạng Video Shorts chuyên đề riêng lẻ lưu độc lập tại `outputs/Orther/<DD.MM.YYYY>/`:
    + Cấu trúc thư mục độc lập: `thethao.json`, `thethao.txt`, `image_credits.json`, `image_plan.json`, `images/`, `audio/`, `audio-title/`, `shorts/`, `qa/`.
    + Lower-Third động 2 góc: Góc dưới bên trái hiển thị cố định nguồn báo chí (`📰 NGUỒN: ...` màu Cyan `#38BDF8`), góc dưới bên phải cập nhật động nguồn ảnh theo từng lần đổi khung hình (`📷 ẢNH: ...`).
    + Kế hoạch phân bổ hình ảnh đa tầng (Semantic Image Planning): 12 ảnh tư liệu HD cho mỗi bài, gắn ít nhất 1-2 ảnh trực tiếp theo ngữ cảnh từng câu lời dẫn, dùng ảnh chính quan trọng xen kẽ góc máy phong phú.
    + Tiêu chuẩn xuất bản YouTube: Đúng 1 tiêu đề duy nhất trong `mota.txt` ("tiêu đề chỉ cần 1 cái thôi"), Sentence Case tiếng Việt, loudnorm chuẩn -14.0 LUFS (True Peak $\le -1.0$ dBTP).
  - Hoàn thành trọn bộ 4 video Shorts Champions League 1080x1920 @ 30fps:
    1. **Short 01**: *Real Madrid 3-2 AEK Athens* (`Short_Real_Madrid_Thang_Nghet_Tho.mp4`, 69.13s, 19.0 MB, -14.04 LUFS) — Siêu phẩm sút xa phút 90+2 của Brahim Díaz giữ mạch toàn thắng.
    2. **Short 02**: *Como 9-1 RC Lens* (`Short_Como_Thang_Lens_9_1.mp4`, 75.13s, 20.2 MB, -14.04 LUFS) — Đội bóng HLV Fabregas đại thắng lịch sử, bàn thắng tri ân Jesús de Miguel từ Nico Paz.
    3. **Short 03**: *Manchester City 3-2 RB Leipzig* (`Short_Man_City_Haaland_Ha_Leipzig.mp4`, 73.77s, 22.7 MB, -14.04 LUFS) — Erling Haaland lập công phút 78 (bàn thứ 62 sau 61 trận C1) ấn định màn rượt đuổi tỷ số nghẹt thở.
    4. **Short 04**: *Fenerbahce 3-2 Liverpool* (`Short_Liverpool_Thua_Nguoc_Fenerbahce.mp4`, 74.91s, 25.0 MB, -14.03 LUFS) — Thảm họa 3 bàn thua từ bóng chết tại chảo lửa Sukru Saracoglu khiến The Reds thua ngược đau đớn trước HLV tạm quyền Dirk Kuyt.
  - Bộ tài nguyên đi kèm đầy đủ: 4 file MP4, 4 ảnh thumbnail dọc 1080x1920 Cyber-Stadium, 4 file mô tả SEO YouTube, và 4 bảng ảnh đối chứng QA `contact_scene_01.jpg` đến `04.jpg`.

- **2026-11-02 (Dựng Trọn Bộ 8 Video Shorts 9:16 & Kiểm Duyệt Tư Liệu)**:
  - Hoàn thành toàn diện 8 video Shorts 9:16 chuẩn hóa theo đúng 8 chủ đề được chọn (Short 1 đến Short 8), xuất tại `outputs/02.11.2026/shorts/`:
    + Short 01 (Kane đoạt Quả bóng vàng 2026), Short 02 (Tranh cãi Messi & vinh danh Ronaldo).
    + Short 03 (Bê bối nhập tịch Malaysia), Short 04 (Man Utd chạm đáy 38 năm & thẻ đỏ Martinez), Short 05 (Địa chấn Man City & Arsenal).
    + Short 06 (Tâm chấn V-League: HLV Popov từ chức Thể Công Viettel), Short 07 (CLB CAHN quật ngã dàn sao triệu đô C1 châu Á), Short 08 (U17 Việt Nam hủy diệt Cheonan FC 5-0 tại Hàn Quốc).
  - Nâng cấp `m8_news_bridge.py` & `short_news_v2.html`: Tính toán tâm điểm thị giác (`focal_x`), chuyển động lia ngang (`pan_horizontal`) luân phiên trái/phải không để lại viền đen cho mọi ảnh khổ ngang, triệt tiêu hoàn toàn hiện tượng ảnh tĩnh lệch lề.
  - Kiểm duyệt thị giác 100%: Loại bỏ toàn bộ ảnh stock/nhận nhầm (phòng game eFootball, ảnh sản phẩm e-commerce, SVĐ mô hình 3D, cầu thủ nhầm CLB), thay bằng tư liệu thực tế đối chứng chính xác ngữ cảnh từng câu.
  - Cập nhật quy chuẩn từ viết tắt bóng đá `abbreviations_map.json`: Bổ sung `Man Utd` -> "Manchester United", `MU` -> "em u".
  - Xuất bản đầy đủ bộ 24 tài nguyên gồm 8 video MP4 1080x1920 @ 30fps, 8 ảnh thumbnail dọc Cyber-Stadium 1080x1920 (`Short_XX_thumbnail.jpg`), và 8 file mô tả chuẩn SEO YouTube (`Short_XX_mota.txt`).

- **2026-10-16 (Giai Đoạn 5a - Xây Dựng Scraper & Lọc Tin Tức Thể Thao)**:
  - Xây dựng `core/m1_scraper.py`: Bộ cào và lọc tin tức thể thao tự động từ 5 nguồn cấu hình (`config/sources.json`), hỗ trợ cả luồng RSS (`feedparser`) và danh sách URL báo trực tiếp.
  - Tích hợp 4 lớp kiểm duyệt nghiêm ngặt:
    1. Lọc thời gian: Loại bỏ tin đăng quá 36 giờ (ICT UTC+7).
    2. Lọc từ khóa cấm: Drop ngay các bài có tiêu đề/mô tả/tag chứa `"trực tiếp"`, `"diễn biến"`, `"tường thuật"`, `"tin đồn"`, `"cập nhật"`.
    3. Luật "Chống tin sai": Loại bỏ hoàn toàn tin đồn chuyển nhượng, chỉ chấp nhận khi có xác nhận chính thức (Official / Here we go / công bố).
    4. Lọc độ dài nội dung: Bỏ các bài rác hoặc < 150 ký tự.
  - Bóc tách nội dung sạch bằng `trafilatura` và trích xuất ảnh bìa + toàn bộ ảnh trong bài kèm chú thích/nguồn ảnh (`Ảnh: ...`) bằng `BeautifulSoup`.
  - Cập nhật quyết định vận hành: Điều chỉnh phát âm `"VAR"` thành `"va"` trong `data/pronunciation_sports.json`.
  - Tích hợp công cụ quét tên riêng chưa có trong từ điển `core/diemdoc/unknown_names.py` vào cuối luồng cào tin.
  - Chạy kiểm thử độc lập thành công trên 4 URL báo mẫu: Nhận 3 bài hợp lệ (URL 1 VnExpress, URL 3 & 4 Thanh Niên), loại bỏ 1 bài quá hạn (URL 2 VnExpress, 44.5h > 36h). Toàn bộ dữ liệu sạch được lưu ngoài Drive tại `WORK/temp_raw_news.json`.

- **2026-10-15 (Giai Đoạn 4 - Giọng Đọc, Đồng Bộ & Hậu Kỳ Âm Thanh)**:
  - Xây dựng `core/m3_voice.py`: ViTTS v3turbo Minh Quân Pro, pitch 0.85, tempo 1.20, cơ chế cache cấp chunk bằng SHA-256 (tốc độ cache hit đạt 8.2s cho 10 phút audio), sample-accurate timing.
  - Xây dựng từ điển `data/pronunciation_sports.json` (~150 mục) và bộ công cụ `tts_text.py` + `unknown_names.py` tự động phát hiện tên riêng thể thao chưa có trong từ điển.
  - Xây dựng `core/m5_sync.py`: Ground-truth alignment dựa trên text gốc, chạy Whisper-small theo batch trong tiến trình con riêng giải phóng RAM, tự động fallback sang Syllabic nội suy, gom karaoke chunks và neo trigger-words cho cards.
  - Nâng cấp `core/m6_compose.py` & `core/diemdoc/audio.py`: Thiết lập bất biến đồng bộ (dùng cut concat thay vì xfade để triệt tiêu lệch sync video-audio), dựng âm thanh master MỘT LẦN từ voiceover.wav liên tục, ducking qua `sidechaincompress` (độ tách giọng/BGM đạt 19.53 dB $\ge 18$ dB), dựng single SFX track, ghép playlist BGM acrossfade 3s, và chuẩn hoá 2-pass Loudnorm YouTube (-14 LUFS).
  - Bổ sung `core/audio_check.py` kiểm toán âm thanh và cập nhật `core/doctor.py` lên 13 tiêu chí (bổ sung kiểm tra filter sidechaincompress, acrossfade, loudnorm).
  - Hoàn thành bài kiểm thử chạy dài F3 trên 2.877 từ (~10 phút âm thanh thật): ViTTS RTF 0.761 (455.3s), Whisper-small RTF 0.559 (334.1s), compose 41.3s, độ lệch video-audio đạt chuẩn 174.1 ms.
  - Xuất các file mẫu nghe thử vào `outputs/_samples/`: 3 mẫu tốc độ (`speed_1.10.m4a`, `speed_1.15.m4a`, `speed_1.20.m4a`), 4 mẫu phát âm thể thao (`pron_test_01.m4a` đến `04.m4a` kèm `pron_test.md`), và 1 mẫu mix hoàn chỉnh 60s (`demo_mix_60s.m4a`).

- **2026-11-06 (Sản xuất Video Bản -5 / `v5` Khử Triệt Để Bản Quyền Content ID BGM)**:
  - Hoàn thiện toàn diện video Bản -5 (`v5`) tại `outputs/05.11.2026/output/Cuoc_dua_ghi_ban_1990_2026_v5.mp4` (`1920x1080 @ 30fps`, thời lượng 7m46s / 466.2s, dung lượng 79.06 MB) và phụ đề `Cuoc_dua_ghi_ban_1990_2026_v5.srt` (41 cues).
  - Khắc phục triệt để khiếu nại bản quyền YouTube Content ID (vụ việc track `bgm_minimal_techno.mp3` bị đơn vị HAAWK/YuraSoop claim tại mốc 2:57–5:35):
    + Thay thế toàn bộ nguồn BGM bên thứ ba bằng thuật toán tổng hợp âm thanh điện tử thuần toán học (Procedural Cyber-Stadium BGM qua Numpy + Scipy tại `outputs/05.11.2026/generate_procedural_bgm.py`): hợp âm Supersaw Pads D-minor, dòng Bass Synthwave 16th-note, nhịp Kick trống 120-124 BPM, Hi-hats và Arpeggio stereo ping-pong.
    + Nhạc nền sinh tự động từ thuật toán không bao giờ tồn tại trong cơ sở dữ liệu vân tay âm thanh Content ID của YouTube, miễn nhiễm 100% mọi rủi ro claim bản quyền, an toàn tuyệt đối cho kiếm tiền kênh.
    + Bảo toàn 100% video hình ảnh V4 (khắc phục ảnh Zico, Hugo Sánchez, Ronaldo/Messi celebration, Romário/Lewandowski, 3 cột dọc Suárez/Zlatan/Benzema), master voice kép (Ngọc Huyền & Minh Quân Pro), chuẩn Loudnorm EBU R128 (-14 LUFS, True Peak <= -1.4 dBTP, độ tách giọng-BGM 23.1 dB $\ge 18$ dB).
  - Cập nhật tài liệu SEO `mota_v5.txt` và `mota.txt`: Khẳng định rõ nguồn nhạc nền không bản quyền tự tổng hợp, loại bỏ mọi thuật ngữ nội bộ, giữ nguyên 3 tiêu đề chuẩn Sentence Case tương thích hoàn toàn với 3 ảnh thumbnail 16:9 A/B/C.
  - Bác sĩ hệ thống `core/doctor.py`: 100% ALL PASS.

- **2026-11-06 (Sản xuất Video Bản -4 / `v4` Bar Chart Race 16:9 "Cuộc đua ghi bàn 1990–2026")**:
  - Hoàn thiện toàn diện video Bản -4 (`v4`) tại `outputs/05.11.2026/output/Cuoc_dua_ghi_ban_1990_2026_v4.mp4` (`1920x1080 @ 30fps`, thời lượng 7m46s / 465.7s, dung lượng 79.63 MB) và phụ đề `Cuoc_dua_ghi_ban_1990_2026_v4.srt` (41 cues).
  - Tuân thủ nghiêm ngặt nguyên tắc bảo toàn ("các phần khác không có vấn đề gì hết nên đừng đụng"): Tái sử dụng nguyên vẹn video biểu đồ cuộc đua `race_video_v3.mp4` (9.910 frames, 330.33s), master audio `main_audio_final_v3.wav` (460.20s, -14.0 LUFS) và cấu trúc 2 giọng đọc xen kẽ (Ngọc Huyền & Minh Quân Pro).
  - Khắc phục triệt để 100% lỗi thị giác do người dùng phản hồi:
    + Cảnh `intro_5` ("35 danh thủ thi đấu từ năm 1990"): Thay thế ảnh TIFF `i05_a.jpg` (Chromium không render) bằng ảnh JPEG chất lượng cao Zico thi đấu cho Flamengo; điều chỉnh `background-position: center 48%` cho Hugo Sánchez bảo đảm thấy trọn vẹn vầng trán, đôi mắt và mái tóc xoăn.
    + Cảnh `comm_f1` ("Tổng kết hành trình 36 năm"): Căn chỉnh lại ảnh đôi Ronaldo & Messi với `center 15%` (bảo toàn 100% khuôn mặt, nụ cười, cúp đồng hồ); thay thế ảnh góc chụp sau lưng / nhảy lên mất đầu bằng ảnh cận cảnh Ronaldo ăn mừng Al Nassr và Messi dang tay ăn mừng Inter Miami rực rỡ.
    + Cảnh `comm_f3` ("Cuộc đua Top 3: Romário & Lewandowski"): Bổ sung scoped CSS `.t5-split-cards` và `.inner-img`, khắc phục lỗi khung ảnh bị co sập về 0x0; nạp ảnh Romário áo vàng Brazil và Lewandowski ăn mừng số 9 tuyển Ba Lan rõ nét 100%.
    + Cảnh `comm_f4` ("Top 10 chân sút vĩ đại nhất từ 1990"): Tái cấu trúc layout từ dạng lưới ngang bất đối xứng sang **3 Cột Dọc (Triptych 3 Columns)**, bảo toàn nguyên vẹn khuôn mặt, ánh mắt, áo đấu và phù hiệu của Luis Suárez (Barca), Zlatan Ibrahimović (chính diện nụ cười) và Karim Benzema (Real Madrid khoanh tay).
  - Xuất bản bộ 3 thumbnail chuẩn 16:9 1080p phục vụ A/B/C testing trên YouTube:
    + `thumbnail_A.jpg`: Ronaldo & Messi song hành ("AI GHI NHIỀU BÀN NHẤT TỪ NĂM 1990? RONALDO HAY MESSI?")
    + `thumbnail_B.jpg`: Cristiano Ronaldo ăn mừng solo bùng nổ ("BỨC TƯỜNG 900 BÀN VĨ ĐẠI NHẤT LỊCH SỬ!")
    + `thumbnail_C.jpg`: Lionel Messi dang tay ăn mừng solo ("CUỘC ĐUA GHI BÀN KHỐC LIỆT NHƯ THẾ NÀO? 36 NĂM RƯỢT ĐUỔI!")
  - Cập nhật tài liệu SEO `mota_v4.txt`: Cập nhật Tiêu đề Option 3 theo đúng yêu cầu: *"Cuộc đua ghi bàn trong bóng đá đã diễn ra khốc liệt như thế nào?"* (73 ký tự, chuẩn Sentence Case tiếng Việt $\le 100$ ký tự).
  - Trích xuất 13 khung hình kiểm duyệt QA lưu tại `outputs/05.11.2026/qa/` (từ `qa_v4_01_intro_ball.jpg` đến `qa_v4_13_outro.jpg`).
  - Chẩn đoán hệ thống `core/doctor.py` đạt 100% ALL PASS.

- **2026-11-17 (Sản Xuất Bộ 3 Video Shorts Tin Tổng Hợp Thể Thao 9:16 Viết Liền Liền Mạch tại `outputs/Orther/17.11.2026/shorts/`)**:
  - **Quy Chuẩn Sản Xuất Đột Phá — Tin Tổng Hợp Viết Liền Tổng Thể (Unified Flow Narrative)**:
    + Cập nhật yêu cầu cốt lõi từ Chủ kênh: Không ngắt quãng thành các mẩu tin rời rạc, thay vào đó xâu chuỗi toàn bộ dòng thời sự 12 giờ qua thành một bản tin phóng sự/bình luận mạch lạc, tự nhiên.
    + Thời lượng thực tế tối ưu: **102s – 116s / video** (hoàn toàn dưới trần 3 phút theo đúng chỉ đạo).
    + Phân bổ giọng đọc chuẩn mực: 2 Video Quốc Tế sử dụng 100% Giọng Nam Minh Quân Pro (#15); 1 Video Việt Nam sử dụng 100% Giọng Nữ Ngọc Huyền (#14).
  - **Đồng Bộ Thị Giác Ngữ Nghĩa Từng Câu (Chronological Multi-Image Semantic Flow)**:
    + Thu thập và kiểm duyệt chặt chẽ **82 ảnh tư liệu sắc nét** (từ 1000px đến 6500px), loại bỏ 100% watermark stock (Alamy, Dreamstime, iStock...) và ảnh rác thương mại điện tử.
    + Với các câu dài có chuyển dịch chủ thể, phân bổ từ 2 đến 4 ảnh xuất hiện lần lượt theo đúng tiến trình phát âm (ví dụ: Wirtz -> Schlotterbeck -> Gruda/Scherhant -> Đức đầu bảng A2; Xavi -> cầu thủ Hà Lan rệu rã -> nhì bảng tứ kết; Tiến Linh/Thanh Bình -> hàng thủ vạm vỡ Kyrgyzstan; Việt Nam tăng hạng -> thất bại của Mozambique tại CAN).
    + Xuất đầy đủ 4 bảng kiểm duyệt thị giác Contact Sheet QA (`contact_scene_01/02/03.jpg` và `contact_overview.jpg`) đạt chuẩn Audit Pass 100%.
  - **Sản Xuất Trọn Bộ 3 Video Shorts Thành Phẩm**:
    + **Video 1 (Quốc Tế 1)**: `Short_Tong_Hop_QT1_Dia_Chan_Duc_Ha_Lan_Va_Song_Gio_Ronaldo.mp4` (116.73s, 58 MB, Loudness `-14.05 LUFS`, TP `-4.76 dBTP`, drift `16.7 ms` $\le 33.3$ ms). Gồm video MP4, ảnh bìa 9:16 Cyber-Stadium và mô tả YouTube SEO 2 phần.
    + **Video 2 (Quốc Tế 2)**: `Short_Tong_Hop_QT2_Suc_Manh_Alcaraz_Minh_Oan_Yamal_Barca.mp4` (102.37s, 51 MB, Loudness `-14.03 LUFS`, TP `-4.85 dBTP`, drift `17.1 ms`). Alcaraz thị uy tại ATP Finals, La Liga minh oan cho Yamal và dự án lưu tro cốt 71 triệu USD của Barca.
    + **Video 3 (Việt Nam)**: `Short_Tong_Hop_VN_Tam_Diem_My_Dinh_Va_Diem_Sang_The_Thao_Nuoc_Nha.mp4` (112.37s, 56 MB, Loudness `-14.02 LUFS`, TP `-5.07 dBTP`, drift `17.3 ms`). ĐT Việt Nam quyết đấu Kyrgyzstan lúc 19h00, tin vui tăng hạng FIFA, U17 tại Qatar và HCV Đại hội Thể thao toàn quốc.
  - **Công Cụ Tự Động Hóa Mới**: Tạo lập script điều phối độc lập `core/build_shorts_17_11.py` và `core/collect_shorts_images_17_11.py` tích hợp sẵn trong pipeline.

- **2026-11-16 (Sản xuất Video Bản Tin Tuần 16.11.2026, Digest Short 26 Tin & Bộ Đôi Focus Shorts 9:16)**:
  - **Sản xuất Video Bản Tin Tuần 16:9 (`Tin-The-Thao-16-11.mp4`)**:
    + Thời lượng 18 phút 36.7s (`1116.7s`, 33.501 frames @ 30fps), dung lượng 377.5 MiB.
    + Cấu trúc Cut-Concat: Logo Intro 5s + Intro Hook 25.33s (không tiêu đề, đọc "từ ngày 9 tháng 11 đến ngày 15 tháng 11", 12 ảnh triptych) + 26 bản tin đầy đủ (giọng Nam/Nữ luân phiên) + Logo Outro 6.5s.
    + Âm thanh EBU R128 (-14.01 LUFS, TP -1.56 dBTP, drift 0.00 ms). 3 ảnh bìa 16:9 (`thumbnail_A/B/C.jpg`), `mota.txt` 27 chapters.
  - **Sản xuất Video Bản Tin Nhanh 26 Tin 9:16 (`Short_Tin_Nhanh_26_Tin.mp4`)**:
    + Thời lượng 149.43s (< 180s gồm Outro), kịch bản đọc nhanh 26 tin viết mới hoàn toàn, phân giọng Quốc tế (Nam) / Việt Nam (Nữ), loudnorm -14.02 LUFS, drift 9.66 ms.
  - **Sản xuất Focus Short 1 — Tuần Lễ Vàng Thể Thao Việt Nam (`Short_01_Tuan_Le_Vang_The_Thao_Viet_Nam.mp4`)**:
    + Thời lượng 79.44s (< 180s gồm Outro), kịch bản dẫn chuyện một mạch 4 cụm tin Việt Nam (U23 vô địch Gia Lai Cup, Trịnh Thu Vinh vé Olympic 2028, Phan Huy Hoàng vô địch cờ tướng thế giới, Nguyễn Anh Tú cú đúp HCV bóng bàn).
    + 100% Giọng Nữ Ngọc Huyền Mẫu 14, Outro Nam tương phản, tiêu đề Sentence Case chuẩn.
  - **Sản xuất Focus Short 2 — Cuộc Chiến Thế Hệ: Messi, Lamine Yamal Và Sự Cay Đắng Của Harry Kane (`Short_02_Cuoc_Chien_The_He_Messi_Yamal_Kane.mp4`)**:
    + Bản nâng cấp liền mạch toàn diện (Unified Seamless Narrative): **59.91s** (1797 frames @ 30fps, đúng chuẩn < 60s Shorts gồm Outro Nữ).
    + Chạy một mạch câu chuyện duy nhất (7 câu, 53.4s thoại), xóa bỏ hoàn toàn việc chia nhỏ 4 mẩu tin rời rạc và 4 lần ngắt quãng Hero Title.
    + Khắc phục triệt để lỗi ngắt nhịp TTS ("...mê" ngắt 1 cái "hoặc..."), đọc chuẩn "ngả mũ khi nâng kỷ lục", kết nối mượt mà "nhưng đầy cuốn hút của bóng đá thế giới".
    + Gom cụm phụ đề thông minh (Smart Semantic Chunks) bảo vệ từ ghép, thanh tiêu đề ghim cố định ở đỉnh khung hình.
    + 100% Giọng Nam Minh Quân Pro Mẫu 15, Outro Nữ Cyber Pulse, âm thanh -14.02 LUFS, TP -2.85 dBTP, A/V drift 6.01 ms.
    + Đầy đủ bộ ấn phẩm: Ảnh bìa 9:16 Cyber-Stadium Electric Cyan (`..._thumbnail.jpg`), Mô tả SEO 2 phần chuẩn Sentence Case (`..._mota.txt`), QA Contact Sheet (`qa/contact_focus_02_cuoc_chien_the_he.jpg`).

- **2026-11-11 (Sản Xuất Trọn Bộ 4 Video Shorts 9:16 Chuyên Đề & Tin Tức Mới tại `outputs/Orther/11.11.2026/`)**:
  - **Sản Xuất Video Short 01 — Khủng Hoảng Man Utd & Lời Cảnh Báo Của Merson**:
    + File: `outputs/Orther/11.11.2026/shorts/Short_Man_Utd_Hop_Ban_Sa_Thai_Carrick_Merson.mp4` (65.50s / 1965 frames @ 30fps, 15.7 MB).
    + Giọng Nam: Minh Quân Pro. Kiểm toán âm lượng EBU R128: `-14.04 LUFS`, TP `-3.19 dBTP`, drift `3.0 ms`.
    + Đầy đủ bộ ấn phẩm: Ảnh bìa 9:16 (`..._thumbnail.jpg`), Mô tả SEO 2 phần (`..._mota.txt`), QA Contact Sheet (`qa/contact_scene_01.jpg`).
  - **Sản Xuất Video Short 02 — Stephanie Case: Người Phụ Nữ Đầu Tiên Chạy 160 km Ở Nam Cực**:
    + File: `outputs/Orther/11.11.2026/shorts/Short_Stephanie_Case_Chay_160_km_Nam_Cuc.mp4` (64.20s / 1926 frames @ 30fps, 15.3 MB).
    + Giọng Nữ: Ngọc Huyền Pro (theo yêu cầu). Âm lượng: `-14.02 LUFS`, TP `-5.23 dBTP`, drift `3.0 ms`.
    + Đầy đủ bộ ấn phẩm: Ảnh bìa 9:16 (`..._thumbnail.jpg`), Mô tả SEO 2 phần (`..._mota.txt`), QA Contact Sheet (`qa/contact_scene_02.jpg`).
  - **Sản Xuất Video Short 03 — Trịnh Thu Vinh Đoạt Vé Olympic 2028 Cho Thể Thao Việt Nam**:
    + File: `outputs/Orther/11.11.2026/shorts/Short_Trinh_Thu_Vinh_Doat_Ve_Olympic_2028.mp4` (66.60s / 1998 frames @ 30fps, 15.1 MB).
    + Giọng Nữ: Ngọc Huyền Pro (theo yêu cầu). Âm lượng: `-14.03 LUFS`, TP `-5.20 dBTP`, drift `18.0 ms`.
    + Đầy đủ bộ ấn phẩm: Ảnh bìa 9:16 (`..._thumbnail.jpg`), Mô tả SEO 2 phần (`..._mota.txt`), QA Contact Sheet (`qa/contact_scene_03.jpg`).
  - **Nâng Cấp Hệ Thống: Quy Chuẩn Đơn Vị USD, Đột Phá Lia Ảnh Toàn Cảnh & Khắc Phục Nhịp Đọc Tỷ Số Tiêu Đề**:
    + **Quy chuẩn đơn vị tiền tệ USD đọc thành 'đô'**:
      * Bổ sung vào `data/abbreviations_map.json`: `"display": "USD"`, `"say": "đô"`, `"group": true`.
      * Nâng cấp `core/diemdoc/tts_text.py`: Tự động chuyển đổi mọi biến thể tiền tệ USD (`100000 USD`, `$50000`, `120000USD`) sang chuỗi đọc phát âm là "đô" cho mô hình ViTTS, đồng thời giữ nguyên chữ viết tắt `USD` trên giao diện HTML, thẻ Headline và hộp phụ đề Karaoke (nhóm `group: true` tô sáng 1-1).
      * Cập nhật quy chuẩn bắt buộc vĩnh viễn vào `AGENTS.md` (Mục 5.1).
    + **Đột phá lia ảnh toàn cảnh 9:16 (Panoramic Full-Span Pan)**:
      * Tái cấu trúc hàm `compute_pan_params` trong `core/m8_news_bridge.py`: Loại bỏ hoàn toàn giới hạn `max_drift = 120px` (nguyên nhân khiến ảnh ngang chỉ dịch chuyển một phần nhỏ ~240px và bị người dùng phản hồi "không chạy hết ảnh, chậm rì rì").
      * Cho phép camera lia quét qua toàn bộ 90-95% chiều rộng ảnh (`travel = 600 - 1350px`) với tốc độ điện ảnh 400-550 px/s, đổi chiều xen kẽ (`dir_toggle`) tạo nhịp điệu dồn dập, bám sát các pha bóng trên sân mà không bao giờ lộ viền đen.
    + **Khắc phục triệt để nhịp đọc tỷ số trong tiêu đề**:
      * Chuẩn hóa kết cấu câu dẫn tiêu đề dạng `"với tỷ số 3-0"` để ViTTS v3turbo đọc liền một mạch `"với tỷ số ba không"` với zero pause, xóa bỏ triệt để hiện tượng khựng/ngắt nhịp giữa "ba" và "không".
  - **Sản Xuất Video Short 04 — U23 Việt Nam Đại Thắng U23 Thái Lan 3-0 Tại Gia Lai VTV Cup 2026 (Bản Nâng Cấp Toàn Diện)**:
    + File: `outputs/Orther/11.11.2026/shorts/Short_U23_Viet_Nam_Dai_Thang_Thai_Lan_3_0.mp4` (63.90s / 1917 frames @ 30fps).
    + Giọng Nam: Minh Quân Pro. Tiêu đề liền mạch không khựng ("với tỷ số ba không"), câu kết đọc chuẩn tiền tệ ("chức vô địch 100000 đô").
    + Bộ sưu tập 24 ảnh hiện trường thi đấu HD Pleiku (3–4 ảnh/câu, chuyển ảnh 2.5–2.8s), lia toàn cảnh 980–1350px sống động, 100% sạch watermark stock.
    + Đầy đủ bộ ấn phẩm: Ảnh bìa 9:16 (`..._thumbnail.jpg`), Mô tả SEO 2 phần (`..._mota.txt`), QA Contact Sheet 24 ảnh (`qa/contact_scene_04.jpg`).
  - **Chẩn đoán sức khỏe hệ thống**: `core/doctor.py` đạt 100% ALL PASS (28/28 checks).

- **2026-11-10 (Nâng Cấp Cốt Lõi TTS v4.1 & Sản Xuất Trọn Bộ 3 Video Shorts 9:16 Chuyên Đề)**:
  - **Khắc Phục Triệt Để Lỗi Cắt Ngang Câu & Lặp Từ TTS (v4.1_diemdoc_nocut)**:
    + Phát hiện & xử lý 4 mắt xích lỗi:
      1. `_split_long_sentence`: Xóa bỏ nhát cắt từ theo mảng `words[i:i+max_words]`, thay bằng thuật toán ranh giới cú pháp an toàn (chấm phẩy `;`, hai chấm `: `, gạch ngang ` — `, dấu phẩy `, `, liên từ đẳng lập `đồng thời`, `và`, `nhưng`...).
      2. `build_chunks_from_text`: Sửa lỗi đếm sai số từ `len(current_chunk_words)` (đếm phần tử list thay vì số từ), giữ trọn vẹn từng câu hoàn chỉnh $\le 60$ từ.
      3. `render_chunk_vitts`: Nâng trần `max_chars = 768` (từ mức ngầm 256 phonemes) cho ViTTS v3turbo, triệt tiêu 100% tình trạng ViNeu tự động bẻ gãy câu ở ký tự ~128 và tự tiêm dấu chấm `.` giả gây ngắt nhịp và lặp từ.
      4. Bổ sung khoảng thở tự nhiên `0.25s` (`inter_sentence_pause`) giữa các câu kết thúc bằng `.!?`, loại bỏ tình trạng nối audio 0ms dồn dập.
    + Kiểm toán đối chứng bằng Whisper trên câu văn dài 51 từ về Pau Cubarsi: giọng đọc liền mạch 1 hơi 100%, không bị ngắt hạ giọng sai vị trí, không lặp từ `"trao giải"`, đọc chuẩn xác `"Đồng thời"`.
  - **Sản Xuất Hoàn Tất 3 Video Shorts 9:16 Ngày 10.11.2026 tại `outputs/Orther/10.11.2026/shorts/`**:
    + Short 01: `Short_Mourinho_Xo_Do_Ky_Luc_Guardiola.mp4` (17.1 MB, chuẩn loudnorm -14.02 LUFS).
    + Short 02: `Short_Kane_Bi_Loai_Messi_Vao_Doi_Hinh_Nam.mp4` (16.3 MB, chuẩn loudnorm -14.01 LUFS).
    + Short 03: `Short_Pau_Cubarsi_Doat_Giai_Cau_Be_Vang.mp4` (15.2 MB, 68.03s, loudnorm -14.04 LUFS, TP -3.22 dBTP).
    + Cả 3 video đều có đủ bộ 3 ấn phẩm: Video 9:16 (`.mp4`), Ảnh bìa dọc Cyber-Stadium 9:16 (`_thumbnail.jpg`), và Mô tả SEO YouTube 2 phần (`_mota.txt`).
  - **Chẩn đoán sức khỏe hệ thống**: `core/doctor.py` đạt 100% ALL PASS.

- **2026-11-09 (Sản xuất Video Bản tin Tuần 09.11.2026 & Hệ Thống 3 Loại Video Thống Nhất)**:
  - **Chuẩn hóa hệ thống 3 Loại Video Điểm Đọc**:
    + Cập nhật quy chuẩn và module xuất bản trung tâm `core/diemdoc/publisher.py` dùng chung cho cả 3 định dạng: Video Tuần 16:9 (`weekly_digest`), Video Dài Chuyên Đề 16:9 (`thematic_long`), và Video Ngắn 9:16 (`short_news`).
    + Tích hợp renderer HTML v2 tự động cho ảnh bìa ngang 16:9 (`templates/thumbnail_16x9_sports.html`) và ảnh bìa dọc 9:16 (`templates/thumbnail_9x16_sports.html`).
    + Chuẩn hóa cấu hình phát âm ViTTS: Nam (`Minh Quân Pro` spd 1.12, pch 0.93) và Nữ (`Ngọc Huyền` spd 1.12, pch 1.10).
  - **Viết lại Mô tả SEO Video Dài 16:9** (`outputs/09.11.2026/mota.txt`):
    + Tinh gọn cấu trúc 2 phần theo đúng quy định: Phần 1 gồm 3 tùy chọn Tiêu đề YouTube chuẩn Sentence Case $\le 100$ ký tự; Phần 2 gồm Lời dẫn, Điểm nhấn, 25 Mốc thời gian (Chapters) chi tiết từng giây, Nguồn tin và CTA.
  - **Sản xuất Video Tin Nhanh 25 Tin — Song Song Nam Nữ** (`outputs/09.11.2026/shorts/Short_Tin_Nhanh_25_Tin_Nam_Nu.mp4`):
    + Thời lượng 178.07s (5342 frames @ 30fps), dẫn luân phiên qua 2 giọng đọc Nam (tin lẻ) và Nữ (tin chẵn), tạo cảm giác đối thoại truyền hình nhịp độ cao.
    + Đi kèm Ảnh bìa dọc 9:16 chuẩn Cyber-Stadium Electric Cyan (`Short_Tin_Nhanh_25_Tin_Nam_Nu_thumbnail.jpg`) và mô tả SEO (`Short_Tin_Nhanh_25_Tin_Nam_Nu_mota.txt`).
    + Bảo lưu 100% bản đơn giọng cũ (`Short_Tin_Nhanh_25_Tin_The_Thao.mp4`) trong thư mục để Chủ kênh đối chiếu.
    + Kiểm toán âm thanh: Integrated Loudness `-14.42 LUFS`, True Peak `-1.36 dBTP`, Video-Audio Drift `0.7 ms` (<= 33.3 ms).
  - **Sản xuất Video Focus Short 01 — Ronaldo Giã Từ ĐTQG** (`outputs/09.11.2026/shorts/Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG.mp4`):
    + Focus Short gộp Tin 01 + Tin 02, thời lượng 80.13s (2404 frames @ 30fps), nhấn mạnh góc nhìn "Tin nóng tuần qua".
    + Header cố định `#fixed-headline-bar` cập nhật động, Lower-Third 2 góc (`📰 NGUỒN: RECORD / A BOLA` & `📷 ẢNH: REUTERS / AFP` chuyển mượt mà theo từng ảnh).
    + Ảnh bìa 9:16 (`Short_01_Tin_Nong_Ronaldo_Gia_Tu_DTQG_thumbnail.jpg`) và mô tả SEO có mốc chapters từng tin.
    + Kiểm toán âm thanh: Integrated Loudness `-14.04 LUFS`, True Peak `-3.69 dBTP`, Video-Audio Drift `21.7 ms` (<= 33.3 ms).
  - **Sản xuất Trọn Bộ 4 Video Focus Shorts Tiếp Theo (Short 2, 3, 4, 5)**:
    + **Short 2** (`Short_02_Tin_Nong_Dia_Chan_Ngoai_Hang_Anh.mp4` — 102.97s): Gộp Tin 07, 08, 10 (Nottingham 3-1 Man City, MU hòa 4-4 rơi đèn đỏ, Chelsea thua sốc). Loudness `-14.06 LUFS`, TP `-2.61 dBTP`, drift `0.7 ms`.
    + **Short 3** (`Short_03_Tin_Nong_Champions_League_Dien_Ro.mp4` — 103.37s): Gộp Tin 03, 04, 05 (Como thắng 9-1 kỷ lục C1, Valverde phút 92 cứu Real, Haaland 62 bàn). Loudness `-14.06 LUFS`, TP `-3.83 dBTP`, drift `0.7 ms`.
    + **Short 4** (`Short_04_Tin_Nong_Doi_Tuyen_Viet_Nam.mp4` — 71.97s): Gộp Tin 16, 18, 21 (Tuyển Việt Nam gọi Olaha Mạnh Đức, Công Phượng nổ súng, tạm biệt sân Long An). Loudness `-14.06 LUFS`, TP `-3.42 dBTP`, drift `0.7 ms`.
    + **Short 5** (`Short_05_Tin_Nong_Bi_Kich_San_Co.mp4` — 64.07s): Gộp Tin 12, 13 (Bi kịch Jesús de Miguel qua đời và tai nạn lịch sử, hiệu ứng Memorial Grayscale tưởng niệm). Loudness `-14.06 LUFS`, TP `-4.47 dBTP`, drift `0.7 ms`.
    + Cả 4 video đều có đủ bộ 3 ấn phẩm: Video 9:16 (`.mp4`), Ảnh bìa 9:16 (`_thumbnail.jpg`), và Mô tả SEO 2 phần (`_mota.txt`).
  - **Chuẩn Hóa Toàn Diện Tiêu Đề & Mô Tả Toàn Bộ Video Shorts (09.11.2026)**:
    + Rà soát và viết lại 100% file `_mota.txt` cho cả 7 video Short trong `outputs/09.11.2026/shorts/`.
    + Định danh chuẩn xác tính chất **TIN TUẦN** ("Tin nóng thể thao tuần qua" / "Tin nhanh thể thao tuần qua"), loại bỏ triệt để ngày tháng đơn lẻ "09/11".
    + Xóa bỏ hoàn toàn các ghi chú kỹ thuật nội bộ ("qua 2 giọng đọc Nam Nữ", nhãn `[Nam]` / `[Nữ]` trong chapters).
    + Render lại ảnh bìa 9:16 `Short_Tin_Nhanh_25_Tin_Nam_Nu_thumbnail.jpg` tập trung 100% vào sự kiện thể thao chấn động tuần qua.
  - **Sản xuất Tuần Tự Bộ 4 Video Shorts Kịch Bản Thống Nhất (Short 6, 7, 8, 10 — 10.11.2026)**:
    + Đổi mới quy trình: Thay vì chắp ghép thô các bản tin, mỗi video được viết lại một kịch bản dẫn chuyện liền mạch (Unified Script, ~120-160 từ, 30-38s), sinh giọng đọc ViTTS Minh Quân Pro mới 100%, đồng bộ Karaoke 1-1, phân bổ ảnh động theo ngữ cảnh và Lower-Third 2 góc (`📰 NGUỒN` + `📷 ẢNH`).
    + Chạy tuần tự từng video một để đảm bảo chất lượng kiểm toán tối đa:
      * **Short 6** (`Short_06_Tin_Nong_Chuyen_La_The_Thao_The_Gioi.mp4` — 37.83s / 1135 frames): Kỷ lục thế giới 51 thẻ đỏ tại Brazil & Giải vô địch bóng đá trên xe đạp Cycle-ball tại Đức. Loudness `-14.03 LUFS`, TP `-2.45 dBTP`, drift `0.3 ms`.
      * **Short 7** (`Short_07_Tin_Nong_Tam_Chan_V_League.mp4` — 29.90s / 897 frames): Nam Định giữ đỉnh bảng, HAGL thoát đáy, Công Phượng nổ súng cho Đồng Nai, Viettel hòa Thanh Hóa 1-1. Loudness `-14.03 LUFS`, TP `-2.79 dBTP`, drift `0.0 ms`.
      * **Short 8** (`Short_08_Tin_Nong_Tu_Hao_The_Thao_Viet_Nam.mp4` — 31.17s / 935 frames): Quyết Chiến đè bẹp số 1 thế giới 50-23 tại World Cup Billiards, Thanh Thúy về nước, CLB nữ TP.HCM tại Cúp C1. Loudness `-14.03 LUFS`, TP `-1.66 dBTP`, drift `0.7 ms`.
      * **Short 10** (`Short_10_Tin_Nong_Sieu_Sao_Toa_Sang.mp4` — 32.30s / 969 frames): Haaland lập kỷ lục 62 bàn C1 siêu tốc, Alcaraz vô địch Paris Masters, Lando Norris đăng quang F1 Brazil. Loudness `-14.08 LUFS`, TP `-2.13 dBTP`, drift `0.0 ms`.
    + Đầy đủ bộ 3 ấn phẩm: Video MP4 (`.mp4`), Ảnh bìa 9:16 (`_thumbnail.jpg`), và Mô tả SEO 2 phần (`_mota.txt`) chuẩn Sentence Case $\le 100$ ký tự.
  - **Chẩn đoán sức khỏe hệ thống**: `core/doctor.py` đạt 100% ALL PASS.

- **2026-11-05 (Sản xuất Video Bản -3 / `v3` Bar Chart Race 16:9 "Cuộc đua ghi bàn 1990–2026")**:
  - Hoàn thiện toàn diện video Bản -3 (`v3`) tại `outputs/05.11.2026/output/Cuoc_dua_ghi_ban_1990_2026_v3.mp4` (`1920x1080 @ 30fps`, 7m46s, 87.2 MB) và phụ đề `Cuoc_dua_ghi_ban_1990_2026_v3.srt` (41 cues).
  - Tái cấu trúc phân bổ giọng đọc kép tự nhiên và chiều sâu:
    + Mở đầu (Ngọc Huyền - 6 câu, 37.27s / 1118 frames): Khôi phục bối cảnh 35 cầu thủ thi đấu từ 1990 (IFFHS/RSSSF/Transfermarkt) và Roberto Dinamite (675 bàn).
    + Phần đua biểu đồ (Minh Quân Pro - 27 câu bình luận đánh giá, 330.33s / 9910 frames): Giọng nam bình luận đánh giá chiều sâu lịch sử 27 mốc phát triển thay vì đọc banner đơn điệu, đồng thời 82 banner Cyber-Stadium vẫn xuất hiện tự động.
    + Phần kết (92.58s / 2778 frames): Chia thành 2 phân đoạn rõ ràng: 3A (Ngọc Huyền tổng kết 4 câu, header `"TỔNG KẾT BẢNG XẾP HẠNG — ĐIỂM ĐỌC"`, Ronaldo 985 & Messi 937, Romário 772 & Lewandowski 743) và 3B (Minh Quân Pro đánh giá chuyên sâu 4 câu, header `"BÌNH LUẬN & ĐÁNH GIÁ — ĐIỂM ĐỌC"`, 3 kỷ nguyên dẫn đầu, di sản >900 bàn, triển vọng 2035).
  - Khôi phục 100% hiệu ứng thị giác v1: Ken Burns ngược chiều, crossfade chuyển cảnh 0.3s, quét gạch chân vàng keyword line 0.25s, đếm số tăng dần count-up 0.8s.
  - Sửa triệt để layout T5 bên trái: Khung chứa snapshot biểu đồ chốt 11/2026 chuẩn 16:9 `contain` trên nền tối `#0E1522`, hiển thị trọn vẹn thứ hạng 1-10, cờ, họ tên cầu thủ và nhãn năm tháng không bị cắt chữ.
  - Kiểm duyệt thị giác 100% (Contact Sheet QA): Thu thập 35 ảnh thi đấu và sân bóng chính thức (2–3 ảnh/câu), loại bỏ triệt để ảnh stock, tượng đồng, bảo tàng hay tranh vẽ.
  - Nghiệm thu đồng bộ tuyệt đối: 27/27 mốc sự kiện PASS 100%, độ trễ cực đại chỉ 0.033s (<= 1 frame). Xuất bản tài liệu `mota_v3.txt`, `decisions_v3.md`, `credits_v3.json`.

- **2026-11-05 (Sản xuất Video Bar Chart Race 16:9 "Cuộc đua ghi bàn 1990–2026")**:
  - Hoàn thiện toàn diện video Bar Chart Race 16:9 (`1920x1080 @ 30fps`, thời lượng 6m20s, dung lượng 46.2 MB) tại `outputs/05.11.2026/output/Cuoc_dua_ghi_ban_1990_2026.mp4`.
  - Khắc phục triệt để lỗi hiển thị trắng trang: chuyển sang nhúng trực tiếp font Base64 (`Barlow Condensed Bold/SemiBold` & `Roboto`), bảo toàn 100% CSS theme Cyber-Stadium chuẩn (`#0E1522`).
  - Tích hợp Logo kênh Điểm Đọc (`diem-doc-logo-1.png`) bên trái tiêu đề chính (x=64px, y=22px, kích thước 96x96px), căn chỉnh thẳng hàng và loại bỏ khung giữ chỗ bottom-right theo đúng quy chuẩn.
  - Thiết lập khoảng dừng 3.0 giây đầu cuộc đua (90 frames tĩnh ở Tháng 1/1990) kèm câu dẫn mở đầu của giọng đọc ViTTS Ngọc Huyền ("Tháng 1 năm 1990, cuộc đua chính thức bắt đầu.") và banner `XUẤT PHÁT`.
  - Đồng bộ 42 sự kiện âm thanh song ngữ, 83 banner động, viền highlight trắng 0.8s cho cầu thủ liên quan, và nhãn thanh màu xanh thép `#5A6E96` cho cầu thủ đã giải nghệ.
  - Chuẩn hóa âm thanh master EBU R128 đạt chính xác -14.2 LUFS, True Peak <= -1.0 dBTP, độ tách bạch Sidechain Ducking BGM đạt 19.8 dB (vượt chuẩn >= 18 dB).
  - Xuất bản đầy đủ phụ đề `Cuoc_dua_ghi_ban_1990_2026.srt` (56 cues), tài liệu SEO `mota.txt` kèm 7 chapters, `decisions.md` và `credits.json`.

- **2026-10-15 (Giai Đoạn 3 - Dựng Khung Tự Chứa)**:
  - Khởi tạo kiến trúc độc lập `DD-The-thao`, giải phóng sự phụ thuộc vào 4 dự án nguồn.
  - Tách thư viện tiện ích lõi `core/diemdoc/` với cơ chế chống rác Google Drive (`sys.dont_write_bytecode`).
  - Tích hợp công cụ chẩn đoán toàn diện `core/doctor.py` đạt 100% ALL PASS.
  - Tích hợp công cụ dọn dẹp an toàn `core/clean.py` hỗ trợ `--dry-run` và `--apply`.
  - Thay thế font chữ hỏng `Inter_18pt-BoldItalic.ttf` (348 KB hoàn chỉnh).
  - Tích hợp cặp Logo tròn chính thức của kênh Điểm Đọc và vector wordmark.
