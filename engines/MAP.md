# MAP — `engines/` (Động cơ render)

> **Agent: đọc file này để biết engine nào làm được gì, và cách thêm engine mới.**
> Không cần đọc code trừ khi đang sửa chính engine đó.

---

## Engine là gì

Mỗi **card** trong timeline có trường `engine`. `core/m4_render.py` đọc trường đó,
nhóm card theo engine, rồi gọi engine tương ứng. Nhờ vậy có thể **lai**: phần lớn
video dựng bằng HTML, cảnh toán học dựng bằng Manim.

Hai nhóm:

| Nhóm | Engine | Cách xử lý |
|---|---|---|
| **Global** | `html`, `gsap`, `d3` | Render trực tiếp trong engine HTML (cùng một trang bằng Virtual Clock) |
| *(Ghi chú)* | `manim` | *Đã loại bỏ hoàn toàn trong Điểm Đọc (không phù hợp nội dung thể thao).* |

---

## `html/` — engine mặc định

**File:** `renderer.py`

### Nguyên lý: đồng hồ ảo (điểm kỹ thuật cốt lõi)

Đây là tài sản kỹ thuật quan trọng nhất, giữ nguyên từ hệ thống cũ.

**Vấn đề:** nếu quay màn hình thời gian thực, video phụ thuộc hiệu năng máy. Máy
lag → mất frame → animation giật → render không lặp lại được.

**Giải pháp:** trước khi script template chạy, tiêm một shim ghi đè **toàn bộ
nguồn thời gian của trình duyệt**:

- `performance.now()`, `Date.now()` → đồng hồ ảo `vnow`
- `requestAnimationFrame` → hàng đợi thủ công
- `setTimeout` / `setInterval` → timer ảo có `due`
- `document.getAnimations()` → pause + gán `currentTime` (seek CSS animation)

Rồi vòng lặp render gọi `advanceTo(t)` cho từng frame: đốt hết timer đến hạn, chạy
hết RAF queue, seek mọi animation về đúng thời điểm, chụp ảnh JPEG Q95 → pipe vào
FFmpeg.

**Kết quả:**
- Không bao giờ rớt frame (30fps luôn là 30fps)
- **Deterministic** — render 10 lần ra file y hệt
- Máy chậm chỉ render lâu hơn, không làm video xấu đi

### Hàm chính

| Hàm | Làm gì |
|---|---|
| `render_html_engine()` | Điều phối toàn bộ: inject → render frame → mix audio |
| `inject_html()` | Thay `__ASSETS__`, `__LOGO__`, chèn `VIDEO_DATA` + `WORD_TIMESTAMPS` |
| `image_paths()` | Quét đệ quy mọi đường dẫn ảnh trong timeline (để preload) |
| `_scene_scope()` / `_full_scope()` | Chuẩn bị phạm vi render (1 cảnh vs toàn video) |
| `_build_sfx()` | Thu thập SFX event → track |
| `_content_hash()` | Hash để cache (bỏ qua render nếu không đổi) |

### Chi tiết đáng biết

- **Preload ảnh:** quét `VIDEO_DATA` tìm mọi URL ảnh và `await` load hết trước
  frame đầu. Nếu không, thẻ hiện ở giây 40 sẽ trắng vì ảnh chưa tải.
- **Cache:** hash gồm timeline + template + `_base.css` + `_runtime.js` + `_cards.js`
  + `_director.js` + độ phân giải. Đổi nhạc → không render lại hình.
- **SFX:** pre-mix bằng pydub thành 1 track (không giới hạn số lượng như cách dùng
  `amix` nhiều input của FFmpeg).
- **Âm thanh:** trộn voice (1.6) + bgm (0.08) + sfx, rồi **chuẩn hóa EBU R128** về
  −16 LUFS (không phải peak như hệ cũ).

---

## `manim/` — đồ họa toán học ★

**Files:** `renderer.py` (điều phối) + `scenes.py` (thư viện hoạt cảnh)

### Vì sao có engine này

Đây là kênh về con số/toán học (6174, 1729, 142857, Planck, 1/137). Manim sinh ra
để vẽ toán — biến đổi công thức, đồ thị, hình học, LaTeX. Nó vượt trần của CSS:
CSS chỉ làm được opacity/transform/color, không morph hình, không vẽ đường động.

### Cách hoạt động

1. Card có `engine: "manim"` và `scene_class: "TenClass"`.
2. `renderer.py` chạy `manim render scenes.py TenClass --transparent`.
3. Clip lưu ở `<project>/clips/<card_id>.mp4` + ghi `manifest.json`.
4. `m6_compose.py` overlay clip lên video HTML đúng khung thời gian.

**Nếu Manim chưa cài:** hệ thống tự bỏ qua, video vẫn render bình thường. Kiểm tra
bằng `python3 engines/manim/renderer.py --status`.

### 7 khuôn hoạt cảnh có sẵn (`scenes.py`)

| Class | Dùng cho | params |
|---|---|---|
| `KaprekarCollapse` | 6174 — sự sụp đổ Kaprekar | `{"start": 3524}` |
| `Taxicab1729` | 1729 — tổng hai lập phương | `{"target": 1729}` |
| `CyclicRotation` | 142857 — số xoay vòng | `{"base": 142857, "max": 6}` |
| `PowerLadder` | Thang bậc 10 | `{"exponents": [...]}` |
| `FineStructure` | Hằng số 1/137 | `{"denominator": 137.036}` |
| `NumberCompare` | So sánh hai con số | `{"left": {...}, "right": {...}}` |
| `CustomFormula` | Công thức LaTeX tùy ý | `{"latex": "E=mc^2", "caption": "..."}` |

Tất cả kế thừa `BTNScene` — đọc params qua `self.btn_params`, nền trong suốt, màu
đồng bộ brand Cinematic Dark.

### Thêm hoạt cảnh mới

1. Viết class trong `scenes.py`, kế thừa `BTNScene`.
2. Đọc tham số qua `self.btn_params`.
3. Trong timeline: `{"engine":"manim", "type":"math-derivation", "scene_class":"TenClass", "params":{...}}`

---

## `gsap/` và `d3/` — không có thư mục riêng

Hai engine này **không cần thư mục riêng** vì chúng chạy trong cùng engine HTML:

- **gsap**: card `kinetic-statement` dùng. Nếu GSAP được nạp, `_runtime.js` sẽ
  nhường quyền điều khiển animation cho nó (GSAP timeline có `.seek(t)` — hợp hoàn
  hảo với đồng hồ ảo). Không có GSAP thì dùng engine animation tự viết trong
  `_runtime.js`.
- **d3**: card `bar-chart` / `line-chart` dùng. Hiện render bằng SVG thuần trong
  `_cards.js`; cắm D3 thật vào là việc mở rộng đã hoạch định.

Cả hai đều khai báo trong `spec/schema.py` → `ENGINES` và nằm trong
`GLOBAL_ENGINES` của `m4_render.py`.

---

## Thêm engine hoàn toàn mới

1. Khai báo trong `spec/schema.py` → `ENGINES` (thêm `desc`, `renderer`, `speed`).
2. Viết `engines/<tên>/renderer.py`.
3. Thêm tên vào `GLOBAL_ENGINES` (render cùng trang) hoặc `CLIP_ENGINES` (render
   clip riêng → composite) trong `core/m4_render.py`.
4. Nếu là clip engine: `m6_compose.composite_clips()` đã xử lý sẵn qua
   `clips/manifest.json` — chỉ cần engine ghi manifest đúng định dạng.

---

## Xem thêm

- Ai gọi engine nào: `core/MAP.md` (mục m4_render)
- Component dùng engine gì: `spec/MAP.md`
- Đồng hồ ảo hoạt động ra sao: `templates/MAP.md`