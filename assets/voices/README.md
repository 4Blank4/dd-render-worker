# assets/voices/ — Kho Tài Nguyên Giọng Đọc Chuẩn Kênh Điểm Đọc

Thư mục này lưu trữ các mẫu giọng đọc bản quyền đã được Chủ kênh thẩm định, nghe duyệt và phê duyệt chính thức cho hệ thống sản xuất video tự động **Điểm Đọc** (`DD-The-thao`).

---

## 1. Giọng Nam Chính (Primary Voice) — Minh Quân Pro (Mẫu 15)
- **Thư mục:** `assets/voices/male/`
- **File mẫu:**
  - `sample_15_Minh_Quan_Pro_var15_spd1.12_pch0.93.m4a`
  - `sample_15_Minh_Quan_Pro_var15_spd1.12_pch0.93.wav`
- **Cấu hình tối ưu:**
  - `voice`: `"Minh Quân Pro"`
  - `speed`: `1.12`
  - `pitch`: `0.93` (Hạ -7% tạo độ dày trầm điện ảnh, nam tính)
  - `temperature`: `0.6` (Nhấn nhá biểu cảm kịch tính)
- **Vai trò:** Giọng đọc tin tức thể thao chính 16:9, phim tài liệu kỷ lục, phân tích chuyên sâu.

---

## 2. Giọng Nữ Thứ Hai (Secondary Voice) — Ngọc Huyền (Mẫu 14)
- **Thư mục:** `assets/voices/female/`
- **File mẫu:**
  - `sample_14_Ngoc_Huyen_var14_spd1.12_pch1.10.m4a`
  - `sample_14_Ngoc_Huyen_var14_spd1.12_pch1.10.wav`
- **Cấu hình tối ưu:**
  - `voice`: `"Ngọc Huyền"`
  - `speed`: `1.12`
  - `pitch`: `1.10` (Nâng +10% tạo âm sắc thanh cao, trong trẻo, nữ tính rõ rệt mà không méo tiếng)
  - `temperature`: `0.5` (Cân bằng, phát âm chuẩn xác, mượt mà)
- **Vai trò:** Giọng đọc mảng nội dung mới, chuyên đề phái nữ/thể thao nữ, podcast đời sống, review, video ngắn Shorts 9:16 cần năng lượng tươi sáng.

---

## 3. Cách Sử Dụng Trong Hệ Thống

### Lệnh chạy CLI:
```bash
# Mặc định sử dụng Giọng Nam (Minh Quân Pro):
python3 core/m3_voice.py <project>

# Kích hoạt Giọng Nữ Thứ Hai (Ngọc Huyền):
python3 core/m3_voice.py <project> --voice female
# hoặc:
python3 core/m3_voice.py <project> --voice 14
# hoặc:
python3 core/m3_voice.py <project> --voice "Ngọc Huyền"
```

### Cấu hình trong `video_timeline.json`:
```json
{
  "voice_config": {
    "preset": "female"
  }
}
```
hoặc cấu hình trực tiếp trong `projects/<project>/voice.json`.
