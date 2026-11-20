# MAP — `design/` (Bản sắc thị giác)

> **Agent: đọc file này khi cần đổi màu/font, hoặc thêm brand mới.**

---

## Vì sao tách riêng

Hệ thống cũ nhúng mọi màu/font trực tiếp vào từng file template (4000+ dòng).
Muốn đổi tông màu phải sửa HTML — dễ sai, dễ lệch.

Ở đây bản sắc được **tách thành dữ liệu**: `design/` định nghĩa, template chỉ đọc.

---

## Các file

| File | Nội dung |
|---|---|
| `tokens.json` | Thang chữ, khoảng cách, bo góc, chuyển động, bố cục, biểu đồ |
| `brands/swiss-light.json` | Brand nền sáng (dùng cho short) |
| `brands/cinematic-dark.json` | Brand nền tối (dùng cho long) |

---

## `tokens.json`

Giá trị **dùng chung cho mọi brand** — thứ không đổi khi đổi bản sắc.

| Khối | Nội dung |
|---|---|
| `typography.scale` | 8 bậc: `hero` (112px) → `micro` (11px), kèm weight/line/tracking |
| `space` | Thang 0–10 (0, 4, 8, 12, 16, 22, 26, 34, 44, 56, 72) |
| `radius` | sm 8 → xl 22, pill 999 |
| `motion.ease` | out / inOut / snap (cubic-bezier) |
| `motion.duration` | micro 0.18 → cinematic 1.4 (giây) |
| `motion.stagger` | tight 0.06 / base 0.11 / loose 0.2 |
| `motion.reveal` | offsetY 26, scale 0.985 |
| `motion.countUp` | hero 900ms / stat 650ms / inline 420ms |
| `layout` | safeMargin, headerHeight, subtitleBottom, gridGap, gridColumns |
| `chart` | barMinWidth, axisLabelSize, seriesColors |

---

## Brand — cấu trúc chung

Mỗi brand JSON có 6 khối:

| Khối | Nội dung |
|---|---|
| `id` / `name` / `defaultFormat` | Định danh |
| `color` | bg, surface, ink (4 mức), border, accent ×4, accentSoft, subtitle |
| `font` | hero / heading / body / mono (tên family) |
| `fontFiles` | Đường dẫn file TTF + weight cho từng family |
| `effects` | shadow, border, grain, gridPaper / ambientBlobs, gradientNumber |
| `chrome` | topHeader, chapterRibbon, sceneCounter, vignette, portraitColumn |

### So sánh hai brand

| | `swiss-light` | `cinematic-dark` |
|---|---|---|
| **Dùng cho** | short 9:16 | long 16:9 |
| **Nền** | `#F6F5F0` giấy ấm | `#05070C` navy đen |
| **Mực** | `#121418` đen | `#F3F6FF` trắng ngà |
| **Nhấn 0** | `#FF3B00` vermilion | `#FFC24D` gold |
| **Nhấn 1** | `#1D4ED8` cobalt | `#28E0D0` teal |
| **Nhấn 2** | `#059669` emerald | `#FF6B4A` ember |
| **Font hero** | Bebas Neue | Anton |
| **Font heading** | Space Grotesk | Oswald |
| **Font body** | Inter | Montserrat |
| **Font mono** | DM Mono | IBM Plex Mono |
| **Hiệu ứng** | lưới chấm, viền mực, đổ bóng cứng | blob neon, vignette, gradient số |
| **Cột chân dung** | không | có (452px) |

---

## Cách brand đi vào CSS

1. Template HTML khai báo `:root { --accent-0: #FF3B00; ... }`.
2. `_base.css` dùng các biến đó cho mọi component.
3. Card có `accent: "accent2"` → class `.accent2` → ánh xạ sang `--accent-1`.

Chuỗi ánh xạ:
```
card.accent = "accent2"
  → class .accent2  (trong _base.css)
  → --accent: var(--accent-1)
  → --accent-1: brand color
```

---

## Thêm brand mới

1. Sao chép một brand JSON, sửa `id`, `name`, `color`, `font`, `fontFiles`.
2. Tạo template HTML trong `templates/` khai báo `:root { --... }` tương ứng,
   trỏ tới cùng `_base.css` và các file `_*.js`.
3. Trong timeline: `"template": "ten_brand.html"`, `"brand": "ten-brand"`.

**Không cần sửa `_base.css`, `_cards.js`, `_director.js`** — chúng brand-agnostic.

---

## Xem thêm

- Template dùng token thế nào: `templates/MAP.md`
- Font thật nằm ở: `assets/fonts/` (xem `assets/MAP.md`)