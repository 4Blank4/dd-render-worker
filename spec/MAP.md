# MAP — `spec/` (Nguồn Chân Lý Dữ Liệu "Điểm Đọc")

> **Agent: đọc file này trước khi viết bất kỳ timeline nào.** Đây là nơi định
> nghĩa mọi thứ hợp lệ trong hệ thống. Không đoán — tra ở đây.

---

## Vì sao thư mục này quan trọng nhất

Toàn hệ thống xoay quanh **một file JSON** (`video_timeline.json`). `spec/` định
nghĩa file đó được phép chứa gì. Validator, builder, render router, template —
tất cả đều đọc từ đây. Sửa `spec/` là sửa luật của cả hệ thống.

**Nguyên tắc:** nếu tài liệu (kể cả file này) lệch với `spec/schema.py` thì
**code đúng** — và bạn phải sửa tài liệu.

---

## Các file

| File | Nội dung | Khi nào đọc |
|---|---|---|
| `schema.py` | ★ Định nghĩa timeline + registry 21 component + 3 engine (`html`, `gsap`, `d3`) | Trước khi viết timeline; khi thêm component |
| `timeline_template.json` | Khung khởi đầu cho project mới | Khi bắt đầu project mới |

---

## `schema.py` — Cấu trúc bên trong

| Khối | Chứa gì |
|---|---|
| `SCHEMA_VERSION` | Phiên bản contract hiện tại (`1.0.0`) |
| `FORMATS` | `short` (1080x1920) · `long` (1920x1080) |
| `ENGINES` | `html` · `gsap` · `d3` (đã loại bỏ `manim`) |
| `ROLES` | `hook · setup · evidence · turn · payoff · outro · connective` |
| `COMPONENTS` | ★ Registry 21 component — mỗi cái có fields/required/engine/sfx/slot |
| `TIMELINE_SCHEMA` | Cấu trúc timeline |
| `SCENE_SCHEMA` | Cấu trúc scene |
| `CARD_SCHEMA` | Cấu trúc card |
| `validate_card()` / `validate_timeline()` | Hàm kiểm tra tính hợp lệ |
| `to_json_schema()` | Xuất JSON Schema để kiểm duyệt dữ liệu |

**Lệnh tra cứu nhanh:**

```bash
python3 spec/schema.py              # tổng quan
python3 spec/schema.py --list       # 21 component theo engine, kèm slot/density
python3 spec/schema.py --json-schema # JSON Schema đầy đủ
```

---

## Cấu trúc timeline (tóm tắt)

```jsonc
{
  "schema_version": "1.0.0",
  "format": "long",                   // long (1920x1080) | short (1080x1920)
  "template": "long_cinematic.html",  // file trong templates/
  "brand": "cinematic-dark",          // file trong design/brands/ (Cyber-Stadium)
  "output_filename": "diem_doc_tin_chinh.mp4",
  "scenes": [
    {
      "scene_id": 1,
      "role": "hook",
      "script_text": "Chào mừng các bạn đến với Điểm Đọc Thể Thao...",
      "cards": [
        {
          "id": "c1",
          "type": "title-banner",
          "trigger_word": "Điểm",
          "title": "ĐIỂM ĐỌC THỂ THAO",
          "tag": "24H"
        }
      ]
    }
  ]
}
```