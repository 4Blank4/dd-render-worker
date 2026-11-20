# Điểm Đọc (DD-The-thao) — Hệ Thống Sản Xuất Video Tin Tức Thể Thao Tự Động

Hệ thống độc lập tự chứa sản xuất video tin tức thể thao tiếng Việt cho kênh **Điểm Đọc** (1 video chính 16:9 + 3 video phụ 9:16 mỗi ngày).

---

## 🚀 Quy Trình Sản Xuất Hằng Ngày (2 Bước Chuẩn)

Toàn bộ quy trình sản xuất hằng ngày được điều phối tự động qua công cụ `core/run_day.py`:

```
┌────────────────────────────────────────────────────────────────────────┐
│  BƯỚC 1: BIÊN SOẠN & DUYỆT NỘI DUNG (PREPARE)                         │
│  python3 core/run_day.py prepare [--test]                              │
│                                                                        │
│  m1_scraper (Cào tin) ──> Lọc tin ──> m1b_llm_writer (Biên kịch LLM)   │
│                          │                                             │
│                          ├──> video_timeline.json (16:9 ~10 phút)      │
│                          ├──> shorts_units.json (3x 9:16 ~1-2 phút)    │
│                          └──> goi_duyet_noi_dung.md (Sổ Chứng Cứ)      │
│                                       │                                │
│                                       ▼                                │
│                     [CHỦ KÊNH DUYỆT NỘI DUNG TRONG 5 PHÚT]             │
└────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────┐
│  BƯỚC 2: SẢN XUẤT TỰ ĐỘNG TOÀN DIỆN (BUILD)                           │
│  python3 core/run_day.py build [--engine pil|html]                     │
│                                                                        │
│  • Luồng chạy chính (Mặc định: --engine pil):                          │
│    Engine PIL + FFmpeg (1-169.py & 1-916.py) tối ưu tốc độ & ổn định   │
│  • Luồng nâng cấp thử nghiệm (--engine html, tùy chọn):                │
│    Engine HTML Playwright (templates v2, GSAP, 3 layout đa dạng)       │
│                                                                        │
│  m3_voice (ViTTS Minh Quân Pro) ──> m5_sync (Đồng bộ Whisper / Syllabic)│
│       ──> m6_compose (Master Audio, Ducking, -14 LUFS)                 │
│       ──> m7_publish (3 Thumbnail A/B/C + SEO Metadata + Subtitles)    │
│                                                                        │
│  🎉 THÀNH PHẨM XUẤT BẢN TRONG: outputs/DD.MM.YYYY/                     │
│     • 1 Video Chính 16:9 (kèm 3 thumbnail A/B/C + mota.txt)            │
│     • 3 Video Phụ 9:16 (Shorts 1, 2, 3 kèm thumbnail + mota.txt)       │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Bước 1 — Thu thập tin tức & Lập Sổ Chứng Cứ
```bash
# Chạy cào tin thật từ RSS báo chí:
python3 core/run_day.py prepare

# Hoặc chạy kiểm thử nhanh với dữ liệu mẫu (tiết kiệm quota/offline):
python3 core/run_day.py prepare --test
```
👉 **Hệ thống sẽ dừng lại tại đây**. Chủ kênh mở file `~/Library/Caches/DiemDoc/goi_duyet_noi_dung.md` (hoặc `WORK/goi_duyet_noi_dung.md`) để kiểm chứng sự thật, đối chiếu trích đoạn nguồn gốc báo chí và phê duyệt kịch bản.

### 2. Bước 2 — Sản xuất trọn gói Video & Thumbnail
```bash
# Sản xuất thực tế (render hình ảnh Playwright + Master Audio Loudnorm):
python3 core/run_day.py build

# Hoặc kiểm thử siêu tốc luồng nối file & audio (bỏ qua render Playwright):
python3 core/run_day.py build --mock-render

# Nếu bị gián đoạn giữa chừng (mất mạng, hết pin):
python3 core/run_day.py build   # Tự động tiếp tục từ bước dở dang (Resume an toàn)

# Chạy lại toàn bộ từ đầu:
python3 core/run_day.py build --force
```

---

## 📁 Cấu Trúc Thành Phẩm Xuất Bản (`outputs/`)

Sau khi chạy lệnh `build`, toàn bộ thành phẩm sẽ được đóng gói sẵn sàng đăng tải tại `outputs/_tin_trong_ngay/`:

```
outputs/_tin_trong_ngay/
├── Tin-The-Thao-Trong-Ngay.mp4        # Video chính 16:9 chuẩn YouTube 1080p, -14 LUFS
├── thumbnail_A.jpg                    # Thumbnail A: Góc Kịch tính (Dramatic)
├── thumbnail_B.jpg                    # Thumbnail B: Góc Ngôi sao & Sự kiện (Star/Event)
├── thumbnail_C.jpg                    # Thumbnail C: Góc Phân tích chuyên sâu (Analysis)
├── thumbnail.jpg                      # Thumbnail mặc định
├── mota.txt                           # Tiêu đề A/B/C, mô tả SEO, Chapters, Tags, Hashtags
├── sub_tieng_viet.txt                 # Phụ đề kịch bản tiếng Việt
└── shorts/                            # 3 Video phụ 9:16 cho TikTok / Shorts / Reels
    ├── short_1/                       # Short 1: Quick Digest tổng hợp tin vắn nóng
    │   ├── Short-01-Quick-Digest.mp4  # Video dọc 1080x1920 @ 30fps
    │   ├── thumbnail.jpg              # Thumbnail dọc 9:16
    │   ├── mota.txt                   # Caption ngắn gọn kèm hashtag
    │   └── sub_tieng_viet.txt
    ├── short_2/                       # Short 2: Tiêu điểm phân tích sâu 1
    │   ├── Short-02-Vinicius-Mourinho.mp4
    │   ├── thumbnail.jpg
    │   ├── mota.txt
    │   └── sub_tieng_viet.txt
    └── short_3/                       # Short 3: Tiêu điểm phân tích sâu 2
        ├── Short-03-Tam-Hung-Thien-Truong.mp4
        ├── thumbnail.jpg
        ├── mota.txt
        └── sub_tieng_viet.txt
```

---

## 🛠️ Công Cụ Kiểm Tra & Bảo Trì Hệ Thống

```bash
# 1. Kiểm tra sức khỏe toàn diện môi trường (13/13 tiêu chí bắt buộc ALL PASS)
python3 core/doctor.py

# 2. Dọn dẹp cache rác an toàn vào ~/.Trash/ (Safe Trash)
python3 core/clean.py --dry-run   # Xem trước dung lượng dọn
python3 core/clean.py --apply     # Thực hiện dọn dẹp

# 3. Kiểm toán âm lượng & độ phân tách giọng nói/nhạc nền
python3 core/audio_check.py _tin_trong_ngay

# 4. Quét tên riêng/thuật ngữ thể thao mới trong kịch bản
python3 core/diemdoc/unknown_names.py
```

Chi tiết kiến trúc và các module thành phần xem thêm tại [AGENTS.md](AGENTS.md) và [SYSTEM_MAP.md](SYSTEM_MAP.md).
