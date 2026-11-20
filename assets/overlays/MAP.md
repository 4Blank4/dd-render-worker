# MAP — `assets/overlays/` (Lớp Phủ Hiệu Ứng Thị Giác Dùng Chung)

> Thư viện Javascript tự chứa, chuyên biệt để tạo lớp phủ hiệu ứng hạt, ánh sáng và lưới toạ độ Cyber-Stadium cho hệ thống video Điểm Đọc.

---

## 1. Danh Sách Tệp

| Tệp | Vai Trò | Kiến Trúc & API |
|---|---|---|
| `dd_overlay.js` | ★ Bộ kết xuất hạt lấp lánh (sparkles), bụi sáng (embers), quét sáng (light sweep), và lưới toạ độ | Tự chứa 100%, không phụ thuộc thư viện ngoài. API: `DDOverlay.init(canvas, cfg, { seed, width, height })`. Hỗ trợ `update(sec, globalOffsetSec)` và `addBurst(time, x, y)`. |

---

## 2. Đặc Tính Kỹ Thuật

- **Tính định trước (Deterministic)**: Sử dụng PRNG `mulberry32` có seed trích từ `item_id + title`. Mọi toạ độ hạt là hàm toán học của thời gian $t$, bảo đảm tua tới frame bất kỳ đều cho kết quả giống hệt nhau.
- **Bảo vệ vùng mặt cầu thủ**: Tự động giảm độ sáng hạt ở vùng trung tâm ($dx^2 + dy^2 < 1.0$) và tăng dần ra 4 rìa khung hình.
- **Phủ TRÊN ảnh và DƯỚI chữ**: Đặt trên Canvas 2D với `globalCompositeOperation = 'lighter'` để hạt phát sáng trên ảnh chụp thực tế.
- **Tối ưu tốc độ**: Pre-render sprite hạt bằng offscreen canvas radial gradient, không chạy bộ lọc blur trên từng frame.
