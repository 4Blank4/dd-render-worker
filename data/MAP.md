# data/MAP.md — Chỉ Mục Dữ Liệu Tĩnh & Từ Điển Kênh "Điểm Đọc"

Thư mục này chứa các tệp dữ liệu tĩnh, từ điển chuẩn hóa phát âm thể thao, và cấu hình danh mục.

## Danh Sách Tệp

| Tệp | Định dạng | Mục đích |
|---|---|---|
| `pronunciation_sports.json` | JSON | Từ điển phát âm tên riêng thể thao (~230 mục chia theo nhóm đối tượng) giúp ViTTS đọc chuẩn xác ngữ điệu tiếng Việt và hỗ trợ gom cụm Karaoke. Bổ sung trọn bộ nhân vật và giải thưởng Ballon d'Or 2026. |
| `abbreviations_map.json` | JSON | Từ điển chuẩn hoá phát âm từ viết tắt thể thao & thời sự (VĐQG, ĐTQG, Cúp QG, CAHN, SLNA, BXH, TTCN, HCV, HCB, HCĐ, KO, Man Utd, Man United, MU, CĐV, HLV, VĐV, BTC, USD, CLB, VFF...). Quy chuẩn đơn vị tiền tệ USD đọc thành "đô", CLB đọc thành "câu lạc bộ", VFF đọc thành "vê ép ép". Tự động nạp vào `core/diemdoc/tts_text.py` để ViTTS đọc thành tiếng rõ ràng và nhóm Karaoke đồng bộ, trong khi giao diện HTML vẫn giữ nguyên dạng viết tắt gọn gàng. |

## Cấu Trúc `pronunciation_sports.json`

File có cấu trúc phân cấp theo các nhóm đối tượng (categories):
- `clubs`: Danh sách câu lạc bộ (45 mục).
- `players`: Danh sách cầu thủ (72 mục).
- `coaches`: Danh sách huấn luyện viên (19 mục).
- `competitions`: Danh sách giải đấu (21 mục).
- `terms`: Thuật ngữ chuyên môn bóng đá (13 mục).
- `general`: Từ viết tắt & thuật ngữ chung (24 mục).

Mỗi mục trong từng danh sách tuân thủ cấu trúc hợp đồng dữ liệu:
```json
{
  "display": "Erling Haaland",
  "say": "E-lin Ha-lan",
  "group": true,
  "status": "đã duyệt"
}
```
- `display`: Chuỗi hiển thị nguyên bản trên giao diện HTML và phụ đề Karaoke. Hỗ trợ cơ chế khớp không phân biệt dấu phụ (accent-insensitive matching: ví dụ `Kylian Mbappe` khớp cả `Kylian Mbappé`, `Martin Odegaard` khớp cả `Martin Ødegaard`, `Darwin Nunez` khớp cả `Darwin Núñez`).
- `say`: Chuỗi phiên âm tiếng Việt tự nhiên có dấu để ViTTS v3turbo phát âm chuẩn xác ngữ điệu thể thao.
- `group`: `true` nếu là tên riêng hoặc cụm từ bất khả phân ly (giữ nguyên cả cụm từ khi highlight Karaoke và căn chỉnh thời gian).
- `status`: Trạng thái thẩm định chất lượng âm thanh (`chưa nghe`, `đã duyệt`, `chờ nghe xác nhận`).

## Quy Trình Bổ Sung Từ Điển Hằng Ngày
1. Trước khi sinh giọng đọc, Agent chạy `core/diemdoc/unknown_names.py` để quét kịch bản.
2. Các tên riêng thể thao nước ngoài hoặc thuật ngữ viết tắt chưa có trong từ điển sẽ được phát hiện và cảnh báo.
3. Bổ sung mục mới vào đúng nhóm đối tượng trong `data/pronunciation_sports.json` với phiên âm tiếng Việt tự nhiên.
4. Chạy `python3 core/pron_test.py` để kiểm tra chất lượng phát âm mẫu nếu cần.
