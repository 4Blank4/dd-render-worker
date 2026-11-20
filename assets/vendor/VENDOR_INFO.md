# VENDOR_INFO.md — Thông Tin Thư Viện Vendored (DD-The-thao)

Thư mục này chứa các thư viện JavaScript client-side được đóng gói trực tiếp (self-contained) vào dự án, phục vụ render video qua Virtual Clock Playwright mà không phụ thuộc vào `node_modules` hay mạng internet bên ngoài.

---

## 1. Danh Sách Thư Viện (`assets/vendor/js/`)

| Tên thư viện | Phiên bản | Tệp đính kèm | Giấy phép | Mục đích sử dụng |
|---|---|---|---|---|
| **GSAP (GreenSock Animation Platform)** | `3.15.0` | `gsap.min.js` (72.9 KB) | Standard GreenSock License | Điều khiển animation theo đồng hồ ảo `window.__vt` (timeline paused, deterministic) |
| **GSAP CustomEase Plugin** | `3.15.0` | `CustomEase.min.js` (7.1 KB) | GreenSock License | Easing chuyển động mượt mà cho hiệu ứng chuyển ảnh/thẻ |

---

## 2. Quy Tắc Sử Dụng
- Thư viện được nạp vào template HTML bằng đường dẫn tương đối:
  `<script src="../assets/vendor/js/gsap.min.js"></script>`
  `<script src="../assets/vendor/js/CustomEase.min.js"></script>`
- **QUY TẮC ĐỒNG HỒ ẢO:** Tuyệt đối không để GSAP tự động chạy ticker (`requestAnimationFrame` / `Date.now`).
  Mọi animation phải tạo trong `gsap.timeline({ paused: true })` và mỗi frame tua theo thời gian ảo:
  `tl.time(window.__vt.now() / 1000)` để đảm bảo tính xác định 100% (deterministic) giữa mọi lần render.
