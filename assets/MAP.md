# MAP — `assets/` (Tài nguyên)

> **Agent: đọc file này để biết có gì, dùng cái nào. Không cần liệt kê thư mục.**

Mọi tài nguyên đều **offline, bản địa, miễn phí**. Không phụ thuộc API hay mạng.

---

## Tổng quan

| Thư mục | Số lượng | Nội dung | README gốc |
|---|---|---|---|
| `fonts/` | 229 file TTF | 13 bộ font chữ (bổ sung Barlow & Be Vietnam Pro) | `fonts/README_FONTS.md` |
| `vendor/` | 2 file JS | Thư viện tự chứa (GSAP 3.15.0 + CustomEase) | `vendor/VENDOR_INFO.md` |
| `overlays/` | 1 file JS | Lớp phủ hiệu ứng hạt, ánh sáng & Cyber-Stadium tự chứa (`dd_overlay.js`) | `overlays/MAP.md` |
| `sfx/` | 28 file MP3 | Hiệu ứng âm thanh | `sfx/README_SFX.md` |
| `bgm/` | 36 file MP3 | Nhạc nền | `bgm/README_BGM.md` |
| `icons/` | 58 SVG | Icon vector | `icons/README_ICONS.md` |
| `logo/` | PNG + SVG | Logo nhận diện kênh Điểm Đọc (video Intro & Outro nằm tại thư mục gốc `logo/`) | `logo/README_LOGO.md` |
| `voices/` | 2 giọng (M4A+WAV) | 2 bộ giọng chuẩn kênh: Nam chính (Minh Quân Pro) & Nữ thứ hai (Ngọc Huyền) | `voices/README.md` |

---

## `fonts/` — 13 bộ

Đường dẫn dùng trong template: `__ASSETS__/fonts/<Family>/<file>.ttf`
(`__ASSETS__` được renderer thay bằng đường dẫn tuyệt đối).

| Font | Vai trò | File chính |
|---|---|---|
| **Barlow Condensed** | Heading / Tiêu đề tin tức v2 | `Barlow_Condensed/BarlowCondensed-Bold.ttf` |
| **Be Vietnam Pro** | Body / Phụ đề Karaoke v2 | `Be_Vietnam_Pro/BeVietnamPro-SemiBold.ttf` |
| **Anton** | Hero number (brand tối) | `Anton/Anton-Regular.ttf` |
| **Bebas Neue** | Hero number (brand sáng) | `Bebas_Neue/BebasNeue-Regular.ttf` |
| **Oswald** | Heading (brand tối) | `Oswald/static/Oswald-Bold.ttf` |
| **Space Grotesk** | Heading (brand sáng) | `Space_Grotesk/static/SpaceGrotesk-Bold.ttf` |
| **Montserrat** | Body (brand tối) | `Montserrat/static/Montserrat-Medium.ttf` |
| **Inter** | Body (brand sáng) | `Inter/static/Inter_24pt-Medium.ttf` |
| **IBM Plex Mono** | Mono (brand tối) | `IBM_Plex_Mono/IBMPlexMono-Bold.ttf` |
| **DM Mono** | Mono (brand sáng) | `DM_Mono/DMMono-Medium.ttf` |
| **JetBrains Mono** | Mono dự phòng | `JetBrains_Mono/static/...` |
| **Plus Jakarta Sans** | Body dự phòng | `Plus_Jakarta_Sans/static/...` |
| **Roboto** | Body dự phòng | `Roboto/static/...` |

**Font nào cho brand nào** xem `design/brands/*.json` → khối `fontFiles`.
Chi tiết đầy đủ: `fonts/README_FONTS.md`.

---

## `sfx/` — 28 hiệu ứng

Ánh xạ **tự động theo loại card** (khai báo trong `spec/schema.py` → `COMPONENTS[].sfx`):

| Nhóm | File tiêu biểu | Dùng khi |
|---|---|---|
| **Sub-bass / Impact** | `sub_drop_boom.mp3`, `sub_drop_long_hit.mp3`, `glass_shatter_record.mp3` | Thẻ hook, kỷ lục chấn động |
| **UI Click / Pop** | `pop_card.mp3` (mặc định), `click_classic_ui.mp3`, `switch_toggle_on.mp3` | Thẻ bento, biểu đồ |
| **Whoosh / Slide** | `whoosh_page.mp3` (mặc định chuyển cảnh), `paper_slide_page.mp3` | Chuyển cảnh |
| **Counter / Tick** | `tick_counter.mp3`, `beep_retro_digital.mp3` | Số đang đếm |
| **Bell / Chime** | `chimes_reveal.mp3`, `bell_ping_highlight.mp3` | Tiết lộ chân dung, trích dẫn |
| **Strike** | `strike_line.mp3` | Bảng xếp hạng, gạch bỏ |

**Override:** đặt `"sfx": "ten_file.mp3"` trong card.
Chi tiết: `sfx/README_SFX.md`.

---

## `bgm/` — 36 nhạc nền

Chọn qua `"bgm": "<tên file>"` trong timeline. Mặc định `bgm_editorial_5_minimal_loop.mp3`.
Volume mặc định 0.08 (rất nhỏ — đây là bed, không phải nhạc chính).

| Nhóm | File tiêu biểu | Hợp với |
|---|---|---|
| **Editorial** | `bgm_editorial.mp3`, `_2_momentum`, `_3_warm_pad`, `_4_investigative`, `_5_minimal_loop` ★ | Video khoa học, điều tra |
| **Minimal / Ambient** | `bgm_minimal_ambient.mp3`, `bgm_minimal_techno.mp3`, `bgm_soft_clean_pad.mp3` | Nền trung tính |
| **Pulse / Tension** | `bgm_pulse_dark_full.mp3`, `bgm_ticking_against_clock.mp3`, `bgm_tension_ready_result.mp3`, `bgm_countdown_dramatic.mp3` | Đếm ngược, cao trào |
| **Lo-fi** | `bgm_lofi_vibes.mp3`, `bgm_lofi_chill_full.mp3`, `bgm_lofi_driving_home.mp3` | Kể chuyện nhẹ |
| **Cinematic** | `bgm_cinematic_moody_36s.mp3`, `bgm_ambient_shiny_star.mp3` | Mở đầu điện ảnh |
| **Industrial / Tech** | `bgm_industrial*.mp3`, `bgm_tech_*.mp3`, `bgm_electronic_driver.mp3` | Nội dung kỹ thuật |
| **Upbeat** | `bgm_upbeat_blaze.mp3`, `bgm_upbeat_1_future_bass.mp3` | Năng lượng cao |
| **Intro ngắn** | `bgm_intro_light_logo_22s.mp3`, `bgm_upbeat_3_intro_7s.mp3` | Logo/intro |

Chi tiết: `bgm/README_BGM.md`.

---

## `icons/` — 58 SVG

Icon vector 1 dòng, dùng trong card `three-pillars` (trường `icon`) hoặc chèn thủ công.

Phân loại: kinh doanh (bánh răng, tiền tệ, hộp thư), công nghệ (vi mạch, wifi, lập
trình), xây dựng (nhà, tòa nhà, bản vẽ), giáo dục (bóng đèn ý tưởng, bút chì),
thời gian (đồng hồ, lịch), danh hiệu (cúp, huy chương, sao).

Chi tiết: `icons/README_ICONS.md`.

---

## `logo/` — Logo Kênh

| File | Dùng cho |
|---|---|
| `diem-doc-logo-1.png` | ★ Logo tròn Điểm Đọc chính thức |
| `diem-doc-logo-2.png` | Logo tròn biến thể |
| `diem-doc-wordmark.svg` | Vector chữ thương hiệu Điểm Đọc |

*(Lưu ý: Hai video mở/kết `Intro.mp4` và `Outro.mp4` cùng thư mục lưu trữ `old/` được đặt tại thư mục gốc `logo/` để khớp với bộ dựng `core/run_day.py`).*

---

## `voice_samples/` — 20 mẫu giọng

WAV mẫu để nghe thử trước khi chọn. **Không dùng khi render** — Kokoro tự sinh
giọng theo mã (`am_liam`, `bm_george`...).

Đặt tên: `01_am_adam.wav` … `20_bf_isabella.wav`.

Danh mục đầy đủ + mô tả: `python3 spec/voices.py` hoặc `voice_samples/README_VOICES.md`.

---

## Cách tài nguyên được tham chiếu

| Ngữ cảnh | Cách viết | Ai thay thế |
|---|---|---|
| Template HTML/CSS | `__ASSETS__/fonts/...` | `engines/html/renderer.py` → `inject_html()` |
| Template HTML (logo) | `__LOGO__` | `inject_html()` |
| Timeline (bgm) | `"bgm": "bgm_editorial.mp3"` | `btnum.paths.BGM` |
| Timeline (sfx) | `"sfx": "pop_card.mp3"` | `btnum.paths.SFX` |
| Card (ảnh) | `"images_ready/anh.jpg"` | tương đối trong project, không được dùng URL tuyệt đối |

**Quy tắc:** ảnh trong card phải là đường dẫn **tương đối trong project**.
Validator sẽ báo lỗi nếu dùng `http://`, `https://`, hoặc `/`.

---

## `voices/` — 2 bộ giọng đọc chuẩn (Nam & Nữ)

Lưu trữ cấu hình manifest và file mẫu đã nghe duyệt:
- `assets/voices/voices.json`: Manifest định nghĩa 2 giọng chuẩn của hệ thống.
- `assets/voices/male/`:
  - Giọng: **Minh Quân Pro** (Mẫu 15, ViTTS v3turbo, Bắc)
  - Tham số: `speed=1.12`, `pitch=0.93`, `temperature=0.6`
  - Audio: `sample_15_Minh_Quan_Pro_var15_spd1.12_pch0.93.m4a` & `.wav`
- `assets/voices/female/`:
  - Giọng: **Ngọc Huyền** (Mẫu 14, ViTTS v3turbo, Bắc)
  - Tham số: `speed=1.12`, `pitch=1.10`, `temperature=0.5`
  - Audio: `sample_14_Ngoc_Huyen_var14_spd1.12_pch1.10.m4a` & `.wav`

---

## Xem thêm

- Brand dùng font/màu nào: `design/MAP.md`
- SFX tự động theo card: `spec/MAP.md`
- Đường dẫn trong code: `core/btnum/paths.py`