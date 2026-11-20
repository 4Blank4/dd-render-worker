# MAP — `templates/` (Giao diện & bộ máy dựng cảnh)

> **Agent: đọc file này để biết template nào dùng khi nào, và cách thêm component.**
> Phần lớn trường hợp chỉ cần file này, không cần mở code.

---

## Kiến trúc: tách cấu trúc khỏi bản sắc

Đây là điểm khác biệt lớn nhất so với hệ thống cũ (nơi mỗi template là một file
4000+ dòng chứa mọi thứ).

```
_base.css      ← CẤU TRÚC: bố cục, thành phần, hành vi. Brand-agnostic.
_runtime.js    ← ĐỒNG HỒ ẢO + engine animation tua được
_cards.js      ← 22 RENDERER component
_director.js   ← BỘ MÁY dựng cảnh (không biết type cụ thể)
      ↑
      │ được chia sẻ bởi
      │
short_swiss.html      ← CHỈ khai báo bản sắc (màu, font, chi tiết trang trí)
long_cinematic.html   ← CHỈ khai báo bản sắc
```

**Hệ quả:** đổi brand = sửa ~150 dòng khai báo token, không đụng 4000 dòng. Thêm
component = thêm 1 hàm, không đụng template.

---

## Các file

| File | Vai trò | Khi nào đọc |
|---|---|---|
| `_runtime.js` | Đồng hồ ảo + `BTN.Anim` (animation tua được) + utils | Khi sửa animation |
| `_cards.js` | ★ 22 renderer component | Khi thêm/sửa component |
| `_director.js` | Dựng DOM từ timeline, điều khiển reveal/transition/karaoke | Khi sửa hành vi chung |
| `_base.css` | CSS cấu trúc cho mọi component | Khi sửa bố cục |
| `short_swiss.html` | Brand **Swiss Editorial Light** (9:16) | Khi chọn template short nền sáng |
| `short_cinematic.html` | Brand **Cinematic Neon Dark** (9:16) | Khi chọn template short thể thao nền tối |
| `long_cinematic.html` | Brand **Cinematic Neon Dark** (16:9) | Khi chọn template long video chính |
| `long_sports_news.html` | ★ Template bản tin thể thao 16:9 chuyên dụng Điểm Đọc (Cyber-Stadium, Ken Burns, Credit badge) | Template mặc định cho video chính Điểm Đọc |
| `long_sports_news_v2.html` | ★ Template v2 16:9 chuẩn thống nhất cho **Loại 1 (Bản tin tuần)** & **Loại 2 (Chuyên đề dài)**: GSAP deterministic, **9 layouts** (`full`, `split`, `polaroid`, `cinema`, `triptych`, `hero_mosaic`, `filmstrip_carousel`, `spotlight_sequence`, `bento_grid`) tận dụng trọn vẹn 1–5 ảnh/câu, 4 chuyển cảnh xoay vòng (`fade`, `wipe_left`, `slide_up`, `zoom_in`), **Broadcast Stat Callout HUD** góc trên phải (`sent.stat_badge`), lớp phủ `dd_overlay.js` ở z-index 45, tiêu đề nguyên văn co font DOM tự động, chip ngày tiếng Việt (tự ẩn khi `hide_date_chip: true`), **Lower-Third 2 góc động** (`#lt-news-source` góc trái `📰 NGUỒN` + `#lt-photo-credit` góc phải `📷 ẢNH` đổi theo từng ảnh), ticker TIN TIẾP THEO | Kích hoạt khi chạy `run_day.py build --engine html` hoặc `daily_runner.py` |
| `short_news_v2.html` | ★ Template v2 9:16 chuẩn thống nhất cho **Loại 3 (Tin ngắn hằng ngày 1 tin & Focus Short gộp 2–5 tin)**: GSAP deterministic, hỗ trợ chuyển đổi động giữa `Hero Title` (khi `sent.is_title === true` ở đầu mỗi bản tin) và thanh tiêu đề cố định `#fixed-headline-bar`, tự động cập nhật `#cat-pill`, `#lt-news-source` (`📰 NGUỒN`) và `#lt-photo-credit` (`📷 ẢNH` / `📊 ĐỒ HỌA`) theo từng bản tin/ảnh/câu, phụ đề Karaoke 48px; hỗ trợ **Opening Hook 3 giây đầu (`sent.hook`)** (Crash-Zoom, Micro-Shake, Flash, Scanline, Shockwave Rings, HUD đếm số `Score-Slam`, Tactical Pills & cắt nhanh `fast_cut`); tích hợp sân khấu đồ thị dữ liệu động Cyber-Stadium DataViz (`grouped_race`, `duel_stack`, `trophy_race`) chạy thanh đua ngang, đếm số GSAP & cờ quốc gia SVG nội tuyến (`ES`, `AR`, `PT`, `VN`, `US`, `RU`, `IN`, `DE`, `HU`, `FIDE`, `NL`, `NO`, `GB`, `SG`, `QA`, `GR`, `CN`, `HK`, `MY`, `UY`, `BE`, `IT`, `ENG`) | Kích hoạt cho Shorts 9:16 đơn tin và Focus Short |
| `short_digest_v2.html` | ★ Template v2 9:16 Digest Short ("Đọc nhanh 25 tin"): Lướt nhanh nhiều tin (6-8s/tin), 1 ảnh nét nhất + tiêu đề cố định + bộ đếm `TIN XX/25` + **Lower-Third 2 góc động** (`📰 NGUỒN` + `📷 ẢNH`), karaoke nhảy từng từ | Kích hoạt khi chạy `run_day.py build --engine html --shorts digest` |
| `thumbnail_16x9_sports.html` | ★ Template thumbnail ngang (`1920x1080` — 16:9) A/B/C testing chuẩn Cyber-Stadium Electric Cyan (`#00E5FF`) | Dùng cho mọi video 16:9 (Loại 1 & Loại 2) qua `core/diemdoc/publisher.py` |
| `thumbnail_9x16_sports.html` | ★ Template thumbnail dọc (`1080x1920` — 9:16) chuẩn Cyber-Stadium Electric Cyan (`#00E5FF`), đồng bộ 100% nhận diện với `thumbnail_16x9_sports.html` | Dùng cho mọi video Shorts 9:16 (Loại 3) qua `core/diemdoc/publisher.py` |
| `thumbnail_cinematic_split.html` | Bí danh đồng bộ 100% với `thumbnail_9x16_sports.html` | Tương thích ngược cho các script cũ |
| `short_outro_1_cyber_pulse.html` | ★ Outro Short 9:16 Mẫu 1 (`6.50s`) — Cyber Pulse & Interactive Tap (Logo Điểm Đọc + "Cảm ơn bạn đã xem video!" + nút 1 Like / Đăng ký kênh có con trỏ bấm chuyển sang "Đã đăng ký") | Dựng qua `core/build_short_outros.py` |
| `short_outro_2_tactical_broadcast.html` | ★ Outro Short 9:16 Mẫu 2 (`6.00s`) — Tactical Broadcast Scoreboard (Match-card "Còn nhiều tin nóng phía sau!", Ticker 24/7, Equalizer 5 thanh, CTA "Đăng ký + Bật chuông") | Dựng qua `core/build_short_outros.py` |
| `short_outro_3_kinetic_slam.html` | ★ Outro Short 9:16 Mẫu 3 (`5.40s`) — Kinetic Slam & Fast Loop (Chữ lớn Anton đập nhịp "Thấy hay? -> Thả tim! -> Bấm theo dõi -> Điểm Đọc") | Dựng qua `core/build_short_outros.py` |

---

## `_runtime.js` — nền tảng

| Thành phần | Làm gì |
|---|---|
| **Virtual time shim** | Ghi đè `performance.now`, `Date.now`, `rAF`, `setTimeout`, `setInterval`, `getAnimations()` |
| `BTN.Anim` | Timeline animation **tua được** — `add()`, `stagger()`, `setTime(t)` |
| `BTN.makeEase()` | linear, easeIn/Out/InOut, backOut, expo, overshoot |
| `BTN.animateNumber()` | Đếm số, giữ tiền tố/hậu tố (`$1,200`, `27.8%`), bỏ qua năm 4 chữ số |
| `BTN.hl()` | `*text*` → `<b class="hl">text</b>` |
| `BTN.SLOTS` | Gợi ý vị trí lưới cho từng card type |
| `BTN.register()` | Đăng ký renderer component |
| `BTN.esc()` | Escape HTML |

**Vì sao `BTN.Anim` thay vì CSS transition:** CSS transition không tua được. Đồng
hồ ảo cần mọi thứ là **hàm thuần của t**. `Anim.setTime(t)` áp mọi clip tại t →
deterministic.

---

## `_cards.js` — thư viện component

Đăng ký renderer cho 22 type. Mỗi renderer nhận `(card, ctx)` → trả về HTML string.

```js
BTN.register("giant-number-spotlight", (card, ctx) => `
  <div class="card card-giant">...</div>`);
```

**Điểm thông minh:**
- `giant-number-spotlight` và `stat-callout` **tự thu cỡ chữ theo độ dài số** —
  "6174" cỡ 130px, "1.62×10⁻³⁵" cỡ nhỏ hơn, không bao giờ tràn khung.
- Không có renderer cho type → hiện thông báo rõ ràng (`⚠ Chưa có renderer`) thay
  vì im lặng như hệ cũ.

### Thêm component mới

1. Khai báo trong `spec/schema.py` → `COMPONENTS`.
2. Thêm `R("tên-type", (c, ctx) => ...)` vào `_cards.js`.
3. Thêm CSS vào `_base.css`.
4. **Không sửa `_director.js`** — nó gọi `BTN.RENDERERS[type]`, tự nhận.

---

## `_director.js` — bộ máy

Đọc timeline → dựng DOM → điều khiển mọi thứ theo thời gian.

| Hàm | Làm gì |
|---|---|
| `init()` | Khởi tạo, dựng chrome + toàn bộ scene |
| `_buildAllScenes()` | Dựng **hết** scene ngay từ đầu (ẩn) để ảnh preload, font ổn định |
| `_layoutRows()` | Xếp card vào lưới 12 cột, gộp hàng, card lẻ span đầy |
| `_cardHTML()` | Gọi `BTN.RENDERERS[type]`, fallback thông báo nếu thiếu |
| `update(sec)` | **Vòng lặp chính** — gọi mỗi frame |
| `_driveCards()` | Reveal card theo `reveal_time`, chạy `Anim` |
| `_driveTransition()` | wipe / slit / iris / fade / glitch |
| `_driveKaraoke()` | Phụ đề từng từ |
| `_driveAmbient()` | Nền động (blob, grid) |

**Điểm quan trọng:** Director **không biết** gì về từng loại card cụ thể. Nó chỉ
gọi renderer. Đây là lý do thêm card mới không cần sửa director.

---

## `_base.css` — cấu trúc

Brand-agnostic. Mọi màu/font đến từ CSS variables do template đặt.

| Nhóm | Nội dung |
|---|---|
| `#bg-grid`, `.bg-blob`, `#vignette` | Nền ambient |
| `.top-header`, `.brand-*`, `.chap-pill`, `.scene-counter-pill` | Chrome trên |
| `#scene-layer`, `.scene`, `.scene-grid`, `.row`, `.cell` | Lưới cảnh |
| `.card` + `.accent`/`.accent2/3/4` | Thẻ nền tảng |
| `.card-giant`, `.card-callout`, `.trio`, `.cmp-*`, `.mp-*`, `.rt-*`, `.lu-*`, `.pt-*`, `.ph-*`, `.fl-*`, `.qt-*`, `.tp-*` | Từng component |
| `#subtitle-text`, `.sub-word` | Phụ đề karaoke |
| `#wipe`, `#slit`, `#iris`, `#flash` | Chuyển cảnh |

**Lưu ý kỹ thuật:** `.gt-num` dùng `line-height:1.15` + padding dọc. Với
`background-clip:text`, line-height quá sát sẽ **cắt chân chữ số** — đây là lỗi đã
gặp và đã sửa.

---

## Hai template brand

| | `short_swiss.html` | `long_cinematic.html` |
|---|---|---|
| Định dạng | 1080x1920 (9:16) | 1920x1080 (16:9) |
| Phong cách | Swiss Editorial Light | Cinematic Neon Dark |
| Nền | Giấy ấm `#F6F5F0` + lưới chấm | Đen navy `#05070C` + blob + vignette |
| Màu nhấn | Vermilion / Cobalt / Emerald | Gold / Teal / Ember |
| Font | Bebas Neue / Space Grotesk / Inter / DM Mono | Anton / Oswald / Montserrat / IBM Plex Mono |
| Cột chân dung | không | có (452px) |

Mỗi file chỉ chứa `@font-face` + `:root { --tokens }` + vài quy tắc đặc trưng.
Toàn bộ cấu trúc đến từ `_base.css`.

**Đổi sang brand mới:** tạo file HTML khai báo token mới, trỏ tới cùng `_base.css`.
Không cần viết lại component.

---

## `thumbnail_cinematic_split.html`

Style 3 "Cinematic Split": nửa trên ảnh chân dung fade to black, nửa dưới con số
khổng lồ trên nền đen.

Placeholder được điền tự động bởi `core/m7_publish.py` → `_scaffold_thumbnail()`:
`__THUMB_IMAGE__`, `__THUMB_KICKER__`, `__THUMB_HERO__`, `__THUMB_HERO_SIZE__`,
`__THUMB_SUBTITLE__`, `__THUMB_TAG_A/B__`.

Cỡ số tự tính theo độ dài chuỗi để không tràn khung.

---

## Luồng render một frame

```
m4_render (Python)
  └─ inject_html(): thay __ASSETS__, __LOGO__, chèn VIDEO_DATA + WORD_TIMESTAMPS
  └─ Playwright mở trang, add_init_script(VIRTUAL_TIME_SHIM)
  └─ chờ font + ảnh tĩnh + preload ảnh trong timeline
  └─ gọi window.startVideo()
  └─ với mỗi frame: advanceTo(t) → screenshot → pipe vào FFmpeg
```

Trong trang:
```
_runtime.js  → dựng đồng hồ ảo + BTN.*
_cards.js    → đăng ký 22 renderer
_director.js → startVideo() → Director.init() → vòng lặp update(t) mỗi frame
```

---

## Xem thêm

- Component & trường dữ liệu: `spec/MAP.md`
- Engine HTML (chi tiết đồng hồ ảo): `engines/MAP.md`
- Bản sắc thị giác: `design/tokens.json` + `design/brands/*.json`
- **Thư viện chuyển động & công thức góc máy nâng cấp (`node_modules/` & `.agents/skills/`):**
  - `node_modules/motionmaxxing/runtime/motion.js`: 12 đường cong gia tốc thực nghiệm (`snapSettle`, `softLand`, `whip`, `crashIn`...) và điều phối keyframe 30fps.
  - `node_modules/video-shotcraft/references/shots/`: 124 thẻ công thức góc máy (nhịp cắt trailer thể thao `rhythm/trailer-grammar-moves.md`, `camera/crash-zoom-punch.md`, quét HUD `effects/scanline-annotate-focus.md`, biểu đồ động `data/chart-live-moves.md`).
  - `node_modules/dataviz/`: Quy tắc thiết kế biểu đồ thống kê và kiểm tra độ tương phản màu (`scripts/validate_palette.py`).
  - `node_modules/antigravity-animation/`: Hạt hình học không trọng lực & xếp đội hình tối ưu GPU (`antigravity-basic.html`, `antigravity-pattern.html`).
