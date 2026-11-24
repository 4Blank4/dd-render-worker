# AGENTS.md — Luật Vận Hành Cho Agent (Kênh "Điểm Đọc" — DD-The-thao)

Tài liệu này là bộ quy tắc cốt lõi bắt buộc cho mọi AI Agent thao tác trong hệ thống sản xuất video thể thao tự động **Điểm Đọc** (`DD-The-thao`). Hệ thống hoàn toàn tự chứa (self-contained), độc lập và không phụ thuộc vào các dự án bên ngoài.

---

## 0. Quy Tắc Tra Cứu Nhanh & Duy Trì `SYSTEM_MAP.md`

- **Bắt đầu phiên mới & Trước mỗi yêu cầu mới**:
  1. Agent **chỉ đọc 2 file**: `AGENTS.md` (file này) + `SYSTEM_MAP.md`. Tuyệt đối không quét thư mục tràn lan.
  2. **★ BẮT BUỘC DỌN SẠCH CACHE TẠM TRƯỚC KHI LÀM VIỆC**: Mỗi ngày hoặc ngay khi nhận được yêu cầu mới từ Chủ kênh, Agent **bắt buộc kiểm tra và dọn dẹp toàn bộ dữ liệu lưu tạm** trong `~/Library/Caches/DiemDoc/` (chạy `python3 -B core/clean.py --all --apply` để chuyển vào `~/.Trash`, không cần chờ 2 ngày hay 14 ngày) nhằm giải phóng dung lượng ổ cứng trước khi chạy tác vụ mới.
- **★ Đọc MAP trước khi mở code**: Mỗi thư mục con đều có file `MAP.md` mô tả từng file bên trong. Hãy đọc `MAP.md` thay vì mở trực tiếp mã nguồn để tiết kiệm ngữ cảnh:
  - `spec/MAP.md`: Timeline schema, component cards, hợp đồng dữ liệu.
  - `core/MAP.md`: Bộ công cụ pipeline (`m0` đến `m7`), run, doctor, clean.
  - `templates/MAP.md`: Cấu trúc template HTML, JS runtime, virtual clock director.
  - `design/MAP.md`: Bảng màu Cyber-Stadium, design tokens, preset thương hiệu.
  - `assets/MAP.md`: Danh mục fonts, sfx, bgm, svg icons, logos.
  - `data/MAP.md`: Dữ liệu phát âm thể thao và cấu hình nguồn tin.
  - `projects/MAP.md`: Cấu trúc các dự án video con.
  - `_ref/MAP.md`: Tài nguyên tham chiếu từ các dự án nguồn.
- **Cập nhật bắt buộc sau mỗi nhiệm vụ**: Khi hoàn thành video mới, bổ sung component, hoặc cập nhật tính năng:
  1. Cập nhật `SYSTEM_MAP.md` (bản đồ kỹ thuật + nhật ký nâng cấp).
  2. Cập nhật `MAP.md` của thư mục bị ảnh hưởng nếu có thêm/sửa file.
- **Nguồn chân lý là code**: `spec/schema.py` quyết định toàn bộ component và trường dữ liệu.

---

## 1. Ranh Giới & An Toàn Dữ Liệu

- **Độc lập 100%**: Mọi thao tác (đọc, ghi, render) CHỈ ĐƯỢC PHÉP diễn ra bên trong `DD-The-thao/` và thư mục tạm `~/Library/Caches/DiemDoc`.
- **4 Dự Án Nguồn Là Bất Khả Xâm Phạm**: Tuyệt đối **không sửa, không xóa, không tạo file** trong `Video-Thethao`, `Video-TienDuy`, `By-The-Numbers`, `Man-nhan` hoặc các thư mục anh em (`TTS`, `Tin-Tuc`).
- **Safe Trash Policy**: Tuyệt đối không dùng lệnh xóa vĩnh viễn (`rm -rf`). Mọi file rác, cache cũ hoặc file cần xóa phải di chuyển vào `~/.Trash/` (sử dụng `core/clean.py` hoặc thư viện `shutil.move`).

---

## 2. Quy Tắc Bắt Buộc Khi Chạy Trên Google Drive

- **Không sinh rác trên Drive**:
  - Tuyệt đối cấm tạo file nhị phân `.pyc` và thư mục `__pycache__` trên Google Drive. Mọi script/entrypoint phải thiết lập `sys.dont_write_bytecode = True` ngay đầu file (hoặc chạy với cờ `python3 -B`).
  - Thư mục làm việc tạm (`WORK`), file render JPEG, video tạm thời bắt buộc đặt ngoài Google Drive: mặc định tại `~/Library/Caches/DiemDoc`. Chỉ file sản phẩm cuối cùng mới xuất vào `outputs/`.
  - **Dọn dẹp tức thì trước & sau mỗi tác vụ**: Agent bắt buộc chạy `python3 -B core/clean.py --all --apply` ngay khi nhận yêu cầu mới và tự động dọn sạch các file video chunk trung gian trong `~/Library/Caches/DiemDoc` ngay sau khi ghép xong video thành phẩm vào `outputs/`.
- **An toàn đường dẫn tiếng Việt & khoảng trắng**:
  - Thư mục gốc nằm trong đường dẫn có dấu tiếng Việt và khoảng trắng (`Drive của tôi`). Mọi URL nạp vào Playwright phải qua hàm `paths.file_url()` (đã percent-encode qua `pathname2url`).
  - Mọi lệnh gọi `subprocess` bắt buộc truyền mảng tham số (`list`), tuyệt đối không nối chuỗi `shell=True`.

---

## 3. Hợp Đồng Dữ Liệu — `video_timeline.json`

Toàn bộ quy trình dựng video xoay quanh file kịch bản thời gian `video_timeline.json` định nghĩa tại `spec/schema.py`.
- Mỗi **scene** có: `scene_id`, `script_text`, `cards`.
- Mỗi **card** có: `id`, `type`, `trigger_word` (hoặc `lock_timing: true`).
- `trigger_word` bắt buộc xuất hiện nguyên văn trong `script_text` của cảnh đó để làm neo thời gian.
- Chuẩn hóa và kiểm tra timeline:
  ```bash
  python3 core/m2_timeline_builder.py <project> --normalize
  python3 core/m0_validate.py <project>
  ```

---

## 4. Chuẩn Đầu Ra Kênh "Điểm Đọc" — Hệ Thống 3 Loại Video Thống Nhất (Cập nhật 09.11.2026)

> **★ LƯU Ý VỀ ENGINE RENDER & MODULE XUẤT BẢN TRUNG TÂM (`core/diemdoc/publisher.py`):**
> - **Engine chính:** **HTML v2 (Playwright + GSAP)** (`core/run_day.py build --engine html` & `engines/html/renderer.py`), xoay vòng 5 layout điện ảnh, Karaoke phụ đề theo khoảng lặng âm thanh thực tế, hiệu ứng hạt DDOverlay và **Lower-Third 2 góc động** đồng bộ trên cả 3 template (`long_sports_news_v2.html`, `short_news_v2.html`, `short_digest_v2.html`).
> - **Module xuất bản dùng chung:** `core/diemdoc/publisher.py` chuẩn hóa 100% Giọng đọc (`config/voice.json`), **Hệ thống 3 kiểu Thumbnail đồng bộ 16:9 & 9:16** (`cyber_split`, `magazine_bento`, `clash_diagonal`), và Mô tả SEO 2 phần (`mota.txt`).

Hệ thống sản xuất thống nhất **3 Loại Video chính thức**:

1. **Loại 1 — Video Tổng Hợp Thông Tin Hằng Ngày / Hằng Tuần (`daily_digest` / `weekly_digest` — 16:9)**:
   - **Lưu trữ**: `outputs/<DD.MM.YYYY>/` (VD: `outputs/21.11.2026/`, `outputs/22.11.2026/`).
   - **Định dạng & Quy mô (ĐỘNG — KHÔNG CỐ ĐỊNH SỐ TIN)**: `1920x1080 @ 30fps`, chuẩn âm lượng loudnorm `-14 LUFS` ($\text{TP} \le -1.0\text{ dBTP}$). **Số lượng bản tin hoàn toàn linh hoạt theo mật độ sự kiện thực tế** trong khung thời gian (tuyệt đối KHÔNG ép đủ hoặc cắt bớt về một con số lối mòn như 18, 19, 20, 24 hay 25 bài). Ngày ít tin chỉ cần 8–14 tin chất lượng; ngày cuối tuần/cao điểm đa giải đấu có thể 22–30+ tin; tuyệt đối không nhồi tin phong trào vặt cho đủ số và không bỏ sót tin lớn vì chạm trần.
   - **Trình bày giao diện**: Template `templates/long_sports_news_v2.html`, **BẬT Chip Thứ Ngày** (`date-chip`), Lower-Third 2 góc (`📰 NGUỒN` góc trái + `📷 ẢNH` góc phải đổi động theo từng ảnh), Ticker tin tiếp theo ở đáy.
   - **Ấn phẩm đi kèm**:
     + **3 ảnh bìa ngang 16:9 dùng ĐỦ CẢ 3 KIỂU** (`thumbnail_A.jpg`: `cyber_split` kiểu ban đầu từ `thumbnail_16x9_sports.html`; `thumbnail_B.jpg`: `magazine_bento` Tạp chí Gold/Navy 3 khung từ `thumbnail_16x9_magazine.html`; `thumbnail_C.jpg`: `clash_diagonal` Đối đầu đường chéo Đỏ/Trắng/Carbon từ `thumbnail_16x9_clash.html` + `thumbnail.jpg`).
     + **Mô tả SEO 2 phần** `mota.txt` (`=== TIÊU ĐỀ YOUTUBE ===` 3 Options A/B/C Sentence Case $\le 100$ ký tự + `=== MÔ TẢ VIDEO ===` gồm lời dẫn, điểm nhấn, `⏱️ MỐC THỜI GIAN (CHAPTERS):`, nguồn báo, lời kêu gọi đăng ký và dòng `#DiemDoc...` cuối).
     + **Bảng kiểm duyệt thị giác**: `outputs/<DD.MM.YYYY>/qa/` (`contact_overview.jpg` + `contact_scene_XX.jpg`).

2. **Loại 2 — Video Dài Theo Chủ Đề / Thông Tin Yêu Cầu Riêng (`thematic_long` — 16:9, ~4–12 phút)**:
   - **Lưu trữ**: `outputs/<DD.MM.YYYY>/` kèm cờ đánh dấu `no_date` / `special_topic` (như chuyên đề Ronaldo `25.10.2026`, Messi `30.10.2026`), hoặc `outputs/Orther/<DD.MM.YYYY>/` (như các video thống kê dữ liệu / Bar Chart Race `05.11`, `07.11`, `08.11`).
   - **Trình bày giao diện**: Template `templates/long_sports_news_v2.html` hoặc template đồ thị chuyên biệt (`bar_chart_race_16x9.html`), **ẨN hoàn toàn Chip Thứ Ngày** (`hide_date_chip: true`), giữ nguyên nhận diện Cyber-Stadium Electric Cyan (`#00E5FF`) và Lower-Third 2 góc động.
   - **Ấn phẩm đi kèm**: Đồng bộ 100% với Loại 1 gồm **3 ảnh bìa ngang 16:9 dùng ĐỦ CẢ 3 KIỂU** (`thumbnail_A.jpg` `cyber_split`, `thumbnail_B.jpg` `magazine_bento`, `thumbnail_C.jpg` `clash_diagonal`), **Mô tả SEO 2 phần** `mota.txt` (không dùng cụm từ phi thời sự như "thước phim phân tích"), và **Bảng ảnh QA** `qa/`.

3. **Loại 3 — Video Ngắn Dạng Tin Tức Hằng Ngày / Ý Tưởng Riêng (`short_news` — 9:16, ~45s–175s)**:
   - **Lưu trữ**:
     + Tin ngắn đột xuất / ý tưởng riêng hằng ngày: `outputs/Orther/<DD.MM.YYYY>/shorts/`.
     + Các video Short trích xuất từ bản tin ngày/tuần (Focus Short gộp 2–5 tin hoặc Digest Short điểm nhanh theo số tin thực tế `< 180s`): `outputs/<DD.MM.YYYY>/shorts/`.
   - **Trình bày giao diện**:
     + **Đơn tin (1 tin) hoặc Focus Short (gộp 2–5 tin)**: Dùng `templates/short_news_v2.html`. Đầu mỗi bản tin hiển thị `Hero Title` lớn kèm đọc tiêu đề (`is_title: true`), khi vào nội dung tự động thu lên thanh tiêu đề cố định `#fixed-headline-bar` và cập nhật động `#cat-pill`, `#lt-news-source` (`📰 NGUỒN`), `#lt-photo-credit` (`📷 ẢNH`) theo đúng từng bản tin/câu!
     + **Digest Short (đọc nhanh các tin trong ngày/tuần)**: Dùng `templates/short_digest_v2.html` với bộ đếm `TIN XX/N` (động theo tổng số tin thực tế), thanh tiêu đề cố định và Lower-Third 2 góc động.
   - **Ấn phẩm đi kèm**:
     + **1 ảnh bìa dọc 9:16** (`<tên_short>_thumbnail.jpg` hoặc `thumbnail.jpg`, `1080x1920`): qua `publisher.render_thumbnail_9x16()`, **mặc định chọn NGẪU NHIÊN 1 trong 3 kiểu** (`cyber_split` `thumbnail_9x16_sports.html`, `magazine_bento` `thumbnail_9x16_magazine.html`, `clash_diagonal` `thumbnail_9x16_clash.html`).
     + **Mô tả SEO 2 phần** (`<tên_short>_mota.txt`): Phần 1 `=== TIÊU ĐỀ YOUTUBE ===` (1 tiêu đề Sentence Case $\le 100$ ký tự kèm `#Shorts`) + Phần 2 `=== MÔ TẢ VIDEO ===` (tóm tắt + `⏱️ MỐC THỜI GIAN (CHAPTERS):` nếu gộp nhiều tin + nguồn tin + lời kêu gọi + dòng `#Shorts #DiemDoc...`).

---

## 5. Quy Trình Vận Hành & Bất Biến Kỹ Thuật (Giai Đoạn 4)

### 5.1. Quy ước Chữ Hiển Thị (Display) & Giọng Đọc TTS (Cập nhật 24.10.2026 & 30.10.2026)
- **★ KHÔNG TỰ Ý PHIÊN ÂM (Giữ Nguyên Bản Từ Gốc)**:
  - Giữ nguyên tên gốc chuẩn quốc tế và thuật ngữ trên giao diện HTML, hộp phụ đề Karaoke VÀ CẢ TRONG CHUỖI ĐỌC TTS (ví dụ: `Erling Haaland`, `Kylian Mbappé`, `Lionel Messi`, `Harry Kane`, `Real Madrid`, `Barcelona`, `Champions League`, `Palladium`...).
  - Mô hình **ViTTS v3turbo Minh Quân Pro** đọc trực tiếp văn bản song ngữ/tiếng Anh rất chuẩn xác, mượt mà và tự nhiên hơn nhiều so với việc bẻ vụn thành âm tiết tiếng Việt.
  - **TUYỆT ĐỐI KHÔNG tự ý phiên âm** bất kỳ tên riêng, câu lạc bộ, giải đấu hoặc từ ngoại quốc nào nữa.
  - Phụ đề Karaoke và từ đọc đạt tỷ lệ khớp 1-1 hoàn hảo từng từ (`cumulative drift = 0`).
- **Trường hợp duy nhất được phép phiên âm**:
  - Chỉ phiên âm khi Chủ kênh (USER) nghe lại video bản nháp và **yêu cầu đích danh cho từ cụ thể** đó (thông qua `manual_overrides`). Khi không có yêu cầu từ Chủ kênh, mặc định giữ nguyên 100% từ gốc.
- **★ QUY CHUẨN SỐ VIỆT NAM (Bắt buộc vĩnh viễn)**:
  - Mọi con số hàng nghìn phải viết liền mạch dạng `1400`, `1180`, `1402`, `2026`...
  - **TUYỆT ĐỐI KHÔNG viết có dấu chấm hàng nghìn như `1.400` hay `1.180`**: ViTTS sẽ nhận nhầm thành số thập phân ("một chấm bốn trăm") hoặc ngắt câu sai lệch, gây vỡ nhịp phụ đề Karaoke.
- **★ QUY CHUẨN CHỮ VIẾT TẮT THỂ THAO & THỜI SỰ (`data/abbreviations_map.json`)**:
  - Các từ viết tắt phổ biến (VĐQG, ĐTQG, Cúp QG, CAHN, SLNA, BXH, TTCN, HCV, HCB, HCĐ, KO...) được định nghĩa trong `data/abbreviations_map.json`.
  - Hàm `prepare()` trong `core/diemdoc/tts_text.py` tự động chuyển đổi từ viết tắt sang chuỗi phát âm chuẩn ("vô địch quốc gia", "đội tuyển quốc gia"...) cho mô hình ViTTS đọc, trong khi giao diện hiển thị HTML và thẻ Karaoke vẫn giữ nguyên từ viết tắt gọn gàng và tô sáng đồng bộ (nhóm `group: true`).
- **★ QUY CHUẨN ĐƠN VỊ TIỀN TỆ USD (Bắt buộc vĩnh viễn — Cập nhật 11.11.2026)**:
  - Mọi từ viết tắt đơn vị tiền tệ **USD** quy chuẩn đọc phát âm thành **"đô"** (ví dụ: `100000 USD` đọc là `100000 đô`, `50 triệu USD` đọc là `50 triệu đô`).
  - Trên màn hình hiển thị HTML, thẻ Headline, và hộp phụ đề Karaoke vẫn giữ nguyên chữ viết tắt **`USD`** chuẩn mực quốc tế và tô sáng đồng bộ (nhóm `group: true`).
  - Tuyệt đối không đọc thành "u-ét-đê" hay "đô la mỹ".
- **★ QUY CHUẨN ĐỊA DANH "TP. HCM" / "TP HCM" (Bắt buộc vĩnh viễn — Cập nhật 17.11.2026)**:
  - Mọi từ viết tắt địa danh **TP. HCM**, **TP.HCM** hoặc **TP HCM** quy chuẩn đọc phát âm thành **"thành phố Hồ Chí Minh"** liên tiếp, dấu chấm ở đây chỉ có tác dụng ký hiệu viết tắt, tuyệt đối không ngắt nghỉ hay tạo khoảng lặng giữa TP và HCM.
  - Trên màn hình hiển thị HTML, thẻ Headline, và hộp phụ đề Karaoke vẫn giữ nguyên định dạng viết tắt gọn gàng và tô sáng đồng bộ (nhóm `group: true`).
- **★ QUY CHUẨN VIẾT HOA TIẾNG VIỆT (Sentence Case — Bắt buộc)**:
  - Mọi tiêu đề video YouTube, tiêu đề cảnh, tên nhóm và mô tả phải tuân thủ chuẩn chính tả tiếng Việt (Sentence Case): chỉ viết hoa chữ cái đầu câu, danh từ riêng (tên người, câu lạc bộ, giải đấu, quốc gia) và từ viết tắt (CLB, VĐQG, VAR, CAHN...).
  - Tuyệt đối cấm viết hoa chữ cái đầu mọi từ theo kiểu tiếng Anh (Title Case / "In Đậm Ký Tự Đầu").
- **★ QUY CHUẨN TIÊU ĐỀ & MÔ TẢ ĐA NỀN TẢNG (`mota.txt` & `*_mota.txt` — Cập nhật 20.11.2026)**:
  - Độ dài tiêu đề bắt buộc $\le 100$ ký tự (chuẩn tối ưu 75–95 ký tự), tuân thủ Sentence Case.
  - **1. Đối với Video Dài 16:9 (`mota.txt` — Mặc định chỉ đăng YouTube)**:
    + Gồm 2 phần: `=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===` (3 phương án Option A/B/C) và `=== MÔ TẢ VIDEO ===` (Lời dẫn + Điểm nhấn + `⏱️ MỐC THỜI GIAN (CHAPTERS):` + Nguồn báo + Lời kêu gọi đăng ký + Dòng hashtag `#DiemDoc...` cuối).
    + **Thống nhất hậu tố thương hiệu (Brand Suffix) ở cuối cả 3 Option tiêu đề**:
      * Bản tin hằng ngày (`daily_digest`): `<Tiêu đề chính> | Điểm Đọc DD/MM` (VD: `... | Điểm Đọc 20/11`).
      * Bản tin tổng hợp tuần (`weekly_digest`): `<Tiêu đề chính> | Điểm Đọc Tuần`.
      * Video chuyên đề / dữ liệu (`thematic_long`): `<Tiêu đề chính> | Điểm Đọc`.
  - **2. Đối với Video Short 9:16 (`*_mota.txt` — Đăng cả YouTube Shorts, Facebook Reels và TikTok)**:
    + Chỉ dùng **1 tiêu đề duy nhất** trong mục `=== TIÊU ĐỀ YOUTUBE (ĐỘ DÀI CHUẨN <= 100 KÝ TỰ) ===` có hậu tố `| Điểm Đọc #Shorts`.
    + Phần `=== MÔ TẢ VIDEO ===` bắt buộc tách sẵn **3 khối nội dung cho 3 mạng xã hội** để copy-paste trực tiếp:
      * `[1. YOUTUBE SHORTS — MÔ TẢ]`: Tóm tắt + `⏱️ MỐC THỜI GIAN (CHAPTERS):` (nếu gộp nhiều tin) + Nguồn + CTA Đăng ký YouTube + `#Shorts #DiemDoc...`.
      * `[2. FACEBOOK REELS — CHỈ MÔ TẢ / CAPTION]`: Dòng Hook nổi bật + Tóm tắt / gạch đầu dòng nội dung (không dùng mốc giờ `00:00`) + Nguồn + CTA Theo dõi fanpage + `#DiemDoc... #Reels` (không gắn `#Shorts`).
      * `[3. TIKTOK — CHỈ MÔ TẢ / CAPTION]`: Tóm tắt ngắn gọn 1–2 câu chuẩn SEO tìm kiếm + Câu hỏi gợi bình luận tương tác + `#DiemDoc #TinTheThao #BongDa #TheThao247 #XuHuong...` (không gắn `#Shorts`).
  - **CẤM TUYỆT ĐỐI dữ liệu "rác" kỹ thuật nội bộ** xuất hiện trong tiêu đề, lời mô tả hoặc danh sách chapters công khai: không ghi `[Nam]`, `[Nữ]`, `[Nu]`, `[TIN 01]`, `[01]`, `(Mẫu 14)`, `(Mẫu 15)`, tên giọng đọc TTS (`Minh Quân Pro`, `Ngọc Huyền`), chú thích giọng đọc hậu trường, cụm phi thời sự `"thước phim phân tích"` hay phần thừa `=== HASHTAGS ===`. Mọi hàm xuất bản đều phải qua lớp lọc `sanitize_chapter_label()` & `sanitize_public_text()` trong `core/diemdoc/publisher.py`.
- **★ QUY CHUẨN NGÔN TỪ BÁO CHÍ TỰ NHIÊN (Cấm ngôn từ máy móc & hậu trường — Bắt buộc vĩnh viễn, cập nhật 19.11.2026)**:
  - Tuyệt đối **KHÔNG đưa các từ, cụm từ hoặc chi tiết mang tính "máy móc", kỹ thuật sản xuất hay hậu trường** vào lời thoại video, chữ trên thumbnail, tiêu đề và mô tả (`mota.txt` / `*_mota.txt`):
    + Cấm nhắc tới quy trình/công cụ sản xuất: `"giọng đọc"`, `"giọng nam"`, `"giọng nữ"`, `"cảnh quay"`, `"khung hình"`, `"hiệu ứng hiển thị"`, `"hiệu ứng hình ảnh"`, `"render"`, `"thời gian tạo video"`, `"lưu trữ"`, `"TTS"`, `"AI"`, `"lồng tiếng"`.
    + Cấm đưa mốc thời gian kỹ thuật cào tin nội bộ ra nội dung công khai (ví dụ: tuyệt đối **KHÔNG** viết `"cập nhật từ 12 giờ"`, `"từ 12h trưa hôm qua đến sáng nay"`, `"từ 00:01..."` trong lời dẫn hay mô tả vì vô nghĩa với khán giả và thiếu chuyên nghiệp).
  - Luôn diễn đạt theo văn phong **báo chí truyền hình tự nhiên, đi thẳng vào tin tức thể thao** (chỉ giữ mốc thời gian sự kiện thể thao thực tế như *"tối 18/11"*, *"hôm nay 19/11"*, *"rạng sáng mai"*).

### 5.2. Bất Biến Đồng Bộ Video–Audio (Cut Concat — KHÔNG XFADE)
- **TUYỆT ĐỐI KHÔNG DÙNG XFADE VIDEO**: Khi có voiceover liên tục, xfade làm ngắn video khiến âm thanh và hình ảnh bị lệch dần theo thời gian.
- **Mặc định là "Cut Concat"**: Nối các cảnh video bằng ffmpeg concat demuxer (`-c copy`). Hiệu ứng chuyển cảnh thị giác nằm hoàn toàn bên trong HTML template.
- **Âm thanh Master dựng MỘT LẦN**: Toàn bộ âm thanh nền BGM (acrossfade 3s), hiệu ứng SFX (track đơn lọc min_gap >= 0.25s) và Ducking (sidechaincompress hạ BGM khi có giọng, separation $\ge 18$ dB) được dựng trực tiếp trên `voiceover.wav` liên tục.
- **Nghiệm thu đồng bộ**: Độ lệch giữa video và audio thành phẩm bắt buộc $\le 1$ frame (33.3 ms).

### 5.3. Quy Chuẩn Màu Sắc Cyber-Stadium (Cập nhật 30.10.2026)
- **Màu chủ đạo mới**: Chuyển vĩnh viễn từ màu Cam sang tone **Xanh dương điện ảnh / Electric Cyan** (`#00E5FF`, `#06B6D4`, `#38BDF8`).
- Giao diện mát mắt, hiện đại, thể thao đỉnh cao và tương phản cực tốt trên nền đen `#060911` / `#070B14`.
- Áp dụng đồng bộ cho CSS tokens: `--accent-primary: #00E5FF`, box-shadow cyan neon glow, border và highlight Karaoke.

### 5.4. Quy Chuẩn Video Chuyên Đề (Không Đề Cập Ngày)
- Đối với video dạng chuyên đề nhân vật/sự kiện (như Messi, Ronaldo...) không nhắc đến ngày tháng trong lời dẫn:
  - **Bỏ hoàn toàn Chip Thứ Ngày** (`date-chip`) khỏi Header và giao diện video.
  - Chỉ hiển thị Chip Thứ Ngày đối với video Bản tin thời sự hằng ngày (Daily News Digest).

### 5.5. Quy Trình Bắt Buộc: Bảng Ảnh Đối Chứng & Kiểm Duyệt Thị Giác (Contact Sheet QA) (Cập nhật 02.11.2026)
- **Bắt buộc tự động sinh Contact Sheet**: Sau khi thu thập ảnh, hệ thống bắt buộc tự động tạo các bảng ảnh Thumbnail Grid (mỗi thumbnail kèm tên file rõ nét và caption mô tả đối chứng) lưu tại `outputs/<ngày>/qa/` (gồm bảng từng cảnh `contact_scene_XX.jpg` và bảng tổng hợp overview).
- **Đối chứng thị giác & Diệt rác e-commerce**:
  - Tuyệt đối loại bỏ các ảnh nhận nhầm từ khóa sang sản phẩm thương mại điện tử (ví dụ: "Bao" thành bao bột mì, "coach" thành túi xách thời trang, "table" thành bàn ghế bán hàng, "medal" thành sản phẩm kỷ niệm chương...).
  - Chặn triệt để ảnh dính watermark stock (Alamy, Getty, Shutterstock, iStock, Dreamstime...) và ảnh nền trắng sản phẩm e-commerce.
  - Chỉ khi toàn bộ ảnh được đối chứng chính xác với ngữ cảnh câu nói trong kịch bản mới được chuyển sang bước render.

### 5.6. Quy Chuẩn Video Shorts 9:16 Chuyên Đề Riêng Lẻ & Nguồn Lower-Third Động (Cập nhật 04.11.2026)
- **Cấu trúc lưu trữ tách biệt**: Mọi video chuyên đề riêng lẻ / tin tức đột xuất không nằm trong bản tin dài hằng ngày được tổ chức lưu trữ độc lập tại: `outputs/Orther/<DD.MM.YYYY>/` (gồm `thethao.json`, `image_credits.json`, `image_plan.json`, `images/`, `audio/`, `audio-title/`, `shorts/`, `qa/`).
- **Quy chuẩn hiển thị Lower-Third 2 góc màn hình**:
  - **Góc dưới bên trái**: Hiển thị cố định nhãn nguồn bài viết / nguồn tin tức báo chí: `📰 NGUỒN: <TÊN BÁO>` (ví dụ: `📰 NGUỒN: VNEXPRESS / BÁO CHÍ TÂY BAN NHA`, `📰 NGUỒN: GLOBO ESPORTE`...), màu Cyan `#38BDF8`.
  - **Góc dưới bên phải**: Hiển thị nhãn nguồn ảnh `📷 ẢNH: <TÊN NGUỒN ẢNH>` (ví dụ: `📷 ẢNH: REUTERS`, `📷 ẢNH: GETTY IMAGES`, `📷 ẢNH: WIKIMEDIA COMMONS`...). **Bắt buộc**: Mỗi lần khung hình đổi sang ảnh mới, nhãn này phải tự động đổi ngay lập tức theo đúng nguồn của ảnh đó qua GSAP timeline.
- **Quy chuẩn lập kế hoạch & phân bổ hình ảnh theo câu (Semantic Image Planning)**:
  - Mỗi câu trong kịch bản phải được gắn ít nhất 1–2 ảnh tư liệu bám sát trực tiếp ngữ cảnh lời dẫn.
  - **Quy tắc ảnh chính xen kẽ**: Đối với các ảnh hiện trường quan trọng và chính xác nhất, được phép lặp lại 2–3 lần nhưng bắt buộc dùng xen kẽ với các góc chụp hoặc tư liệu bổ trợ, không lặp lại 2 ảnh giống hệt nhau liên tiếp.
- **Kỹ thuật hiệu ứng tưởng niệm (Memorial Grayscale)**:
  - Khi sản xuất video về cầu thủ/nhân vật thể thao qua đời: Áp dụng kỹ thuật chuyển màu ảnh sang thang xám (Grayscale / B&W qua Pillow hoặc CSS filter) cho các ảnh chân dung/tưởng niệm để thể hiện sự trang nghiêm và tiếc thương.

### 5.7. Quy Chuẩn Phạm Vi Thời Gian Tổng Hợp Tin & Nguồn Ảnh HD Sạch Logo (Cập nhật 23.11.2026)
1. **Video Tuần / Nửa Tuần / Nhiều Ngày**:
   - **Video Tuần** (thường yêu cầu vào Thứ Hai hằng tuần): Khung thời gian **BẮT BUỘC** luôn tính trọn vẹn **00:01 Thứ Hai tuần trước đến 23:59 Chủ Nhật tuần trước** (`--period weekly` trong `core/m1_scraper.py` & `core/run_day.py prepare`). Khi xuất bản vào ngày Thứ Hai cập nhật (VD `23.11.2026`), ghi rõ tuần được tổng hợp là tuần trước (VD **`16–22/11`**, `TUẦN 16–22.11 · CN 23.11.2026`) và ngày cập nhật là `23/11/2026`; **TUYỆT ĐỐI KHÔNG** bắt đầu tuần từ Thứ Ba/Thứ Tư hoặc gộp ngày Thứ Hai cập nhật vào khoảng tuần (như `18–23/11`).
   - **Quy tắc kiểm toán dữ liệu ngày có sẵn & bổ sung từ Internet (`core/diemdoc/weekly_coverage.py`)**: Trước khi lên kế hoạch Video Tuần, bắt buộc chạy `python3 -B core/diemdoc/weekly_coverage.py --day Weekly-<DD.MM.YYYY>` để kiểm tra các ngày đã có trong `outputs/`. Riêng bản tin ngày gần nhất được tạo từ `12:00 trưa Chủ Nhật` đến `sáng Thứ Hai` (lưu tại `outputs/<ngày Thứ Hai>/`, VD `outputs/23.11.2026/`) **được chấp nhận hợp lệ là dữ liệu cho ngày Chủ Nhật tuần trước**. Bất kỳ ngày/khoảng giờ nào trong 7 ngày (`Thứ Hai` → `Chủ Nhật`) còn thiếu (VD Thứ Hai `16/11` và sáng Thứ Ba `17/11`) **bắt buộc phải tìm kiếm/cào bổ sung từ Internet (Báo Việt Nam + Thế Giới)** thay vì chỉ ghép các ngày sẵn có.
   - **Video Nửa Tuần hoặc Nhiều Ngày**: Tính trọn từ **00:01 ngày bắt đầu đến 23:59 ngày kết thúc** (hoặc đến thời điểm hiện tại nếu kéo dài sang ngày hôm nay) qua `--since` & `--until`.
2. **Video Ngày Hôm Qua / Bản Tin Hằng Ngày**:
   - Khi yêu cầu tạo video cho **ngày hôm qua**: Nội dung được tổng hợp từ **trưa – chiều hôm qua (~12:00 – 18:00 ICT) đến thời điểm hiện tại** (`--period yesterday` mặc định từ `12:00` trưa hôm qua trở về sau).
3. **Chuẩn Hình Ảnh Không Logo & Khổ Lớn HD (Mặc định bắt buộc)**:
   - Mặc định chỉ sử dụng **ảnh sạch hoàn toàn không logo, không watermark, không chữ góc báo chí** (chặn triệt để `wm1-` VnExpress, Getty, Alamy, Shutterstock, iStock, Dreamstime, nền trắng e-commerce...) và **ảnh khổ lớn chuẩn HD** (`W >= 800`, `H >= 450`, ưu tiên ảnh gốc `1020px–2560px`, tỷ lệ ngang `W/H >= 1.18` cho khung ảnh ngang) để tránh vi phạm bản quyền, vỡ ảnh hoặc làm giảm chất lượng video.

### 5.8. Quy Chuẩn Tìm Kiếm Song Hành Báo Việt Nam & Thế Giới + Tách Bạch Từng Tin + Chống Lối Mòn Số Lượng Tin (Cập nhật 24.11.2026)
1. **Tuyệt đối không cố định số lượng bài/tin (Anti-Quota Rule)**:
   - Không có bất kỳ hạn mức cứng nào kiểu `18 tin`, `19 tin`, `20 tin`, `24 tin` hay `25 tin`.
   - Số lượng tin trong kế hoạch và video **100% phụ thuộc vào lượng sự kiện thể thao thực sự đáng chú ý** trong khung thời gian yêu cầu.
   - Nghiêm cấm cắt bỏ tin quan trọng (nhất là tin thể thao thế giới) chỉ vì "đã đủ số bài", và nghiêm cấm nhồi tin phong trào cấp xã/phường hay tin lặt vặt để "cho tròn 18–20 bài".
2. **★ BẮT BUỘC Tách Bạch 1 Vấn Đề / 1 Tin — Cấm Gộp Chéo Tin (Anti-Bundling Rule, cập nhật 24.11.2026)**:
   - **Trừ những thông tin thực sự liên quan trực tiếp cùng một diễn biến**, tuyệt đối **KHÔNG gộp** nhiều sự kiện, nhiều trận đấu, nhiều môn thể thao hoặc nhiều giải đấu khác nhau vào chung một tin.
   - Tin có thể viết ngắn gọn, súc tích (**3–5 câu/tin**), không cần kéo dài gượng ép.
   - Với **tin lớn / trận đấu lớn** có nhiều lớp thông tin đáng chú ý, chủ động **chia thành nhiều tin riêng biệt** theo từng góc nhìn (ví dụ: 1 tin diễn biến & kết quả trận đấu, 1 tin phản ứng/phát biểu & đánh giá sau trận, 1 tin cục diện bảng xếp hạng & kịch bản đi tiếp).
   - Các kết quả phụ hoặc tin bên lề ít chi tiết mới đưa có hệ thống vào mục tổng hợp cuối bản tin **`CÁC TIN THỂ THAO KHÁC`** (`voice_preset: "secondary"`, 100% giọng Nữ Ngọc Huyền).
3. **Bắt buộc quét song song Báo Việt Nam & Báo Thể Thao Thế Giới (`config/sources.json`)**:
   - Mọi tác vụ tìm kiếm & lên kế hoạch tin tức **bắt buộc** khai thác đồng thời cả **báo Việt Nam** (`Thanh Niên`, `VnExpress`, `Tuổi Trẻ`, `Dân Trí`...) VÀ **báo Thể thao Thế giới** (`BBC Sport`, `BBC Football`, `ESPN`, `Sky Sports`, `The Guardian Sport`, kết hợp tìm kiếm bổ sung cho F1, MotoGP, UFC/Boxing, NBA, ATP/WTA, Golf, Rugby, Cricket, BWF...).
   - Khi tổng hợp số liệu/tỷ số từ web search, **bắt buộc đối chứng chéo** với bài báo gốc quốc tế (`BBC Sport` / `ESPN` / `The Guardian` / `Sky Sports`) để bảo đảm 100% chính xác tỷ số, người ghi bàn và bối cảnh trước khi trình Chủ kênh.

### 5.9. Quy Tắc Mặc Định Thực Thi Sản Xuất (Bắt Buộc — Không Hỏi Lại, cập nhật 24.11.2026)
1. **Mặc định chạy bằng GitHub Cloud (`core/cloud_runner.py`)**:
   - Mọi tác vụ dựng/render video mặc định chạy trên **GitHub Actions Matrix** (`python3 -B core/cloud_runner.py --day <DD.MM.YYYY> --mode daily_long --shards 8` hoặc `--skip-extras` khi không cần giữ `.wav` thô).
   - **Tuyệt đối không hỏi lại** chọn GitHub hay local; chỉ chạy local trên máy Mac (`daily_runner.py`) khi Chủ kênh yêu cầu trực tiếp.
2. **Mặc định chỉ thực hiện Video 16:9 chính (Không tự làm Short)**:
   - Khi Chủ kênh yêu cầu lên kế hoạch hoặc làm video Ngày / Tuần / Chuyên đề, **chỉ thực hiện Video chính 16:9** (kèm 3 Thumbnail A/B/C + `mota.txt` + kiểm duyệt QA).
   - **Tuyệt đối không tự ý làm thêm và không hỏi gợi ý làm thêm Video Short 9:16**, trừ khi Chủ kênh ra lệnh đích danh yêu cầu làm Short.

### 5.10. Quy Tắc Đồng Nhất Tiêu Đề SEO & Ảnh Thumbnail (Bắt Buộc — Cập nhật 24.11.2026)
- **Tiêu đề SEO (`mota.txt` Option A/B/C) và Ảnh + Chữ trên Thumbnail (`thumbnail_A/B/C.jpg`) bắt buộc phải đồng nhất chủ thể**:
  - Tuyệt đối **KHÔNG** để một Option tiêu đề (hoặc Short SEO title) nêu tên một sự kiện/nhân vật tâm điểm (ví dụ U17 Việt Nam) trong khi hình ảnh trên Thumbnail lại **không hề có** sự kiện/nhân vật đó.
  - Khi trong ngày có tin cực nóng, **cho phép và khuyến khích** tiêu đề (thậm chí cả 3 Option) và hình ảnh/chữ trên bộ 3 Thumbnail trùng khớp xoay quanh tin nóng đó (không cần cố né trùng giữa 3 thumbnail nếu tin đó là tâm điểm hút người xem nhất).
  - Với mỗi Option tiêu đề, phải đối chiếu trực tiếp với bộ thumbnail tương ứng bảo đảm khán giả nhìn ảnh + đọc tiêu đề thấy **khớp 100% câu chuyện**.


---

## 6. Lệnh Thường Dùng & Chẩn Đoán

```bash
# Kiểm tra sức khỏe toàn diện hệ thống (bắt buộc ALL PASS trước khi làm việc)
python3 core/doctor.py

# Dọn dẹp toàn bộ cache bộ nhớ đệm an toàn vào Trash (bắt buộc chạy trước mỗi yêu cầu mới)
python3 -B core/clean.py --dry-run
python3 -B core/clean.py --all --apply

# 1. Soạn thảo & chuẩn hoá timeline
python3 core/m2_timeline_builder.py <project> --normalize
python3 core/m0_validate.py <project>

# 2. Sinh giọng đọc ViTTS Minh Quân Pro (lưu trong WORK/<project>/)
python3 core/m3_voice.py <project>
python3 core/m3_voice.py <project> --units units.json   # cho video phụ 9:16

# 3. Đồng bộ phụ đề & cue-points card
python3 core/m5_sync.py <project> --sync whisper-small --check
python3 core/m5_sync.py <project> --sync syllabic       # siêu tốc <0.1s

# 4. Render cảnh (cache hash) & Kiểm duyệt QA
python3 core/m4_render.py <project>
python3 core/m4_render.py <project> --preview
python3 core/m5_qa.py <project> --shots

# 5. Ghép video (cut-concat), master audio & kiểm toán
python3 core/m6_compose.py <project>
python3 core/audio_check.py <project>

# 6. Đóng gói xuất bản
python3 core/m7_publish.py <project>
```


---

## 7. Kho Thư Viện Nâng Cấp Dùng Chung Trong `node_modules/` & `.agents/skills/` (Cập nhật 02.11.2026)

Hệ thống `DD-The-thao` đã được gắn liên kết `node_modules/` dùng chung (`/Users/phamminhtrieu/Documents/Trieu/Numbers_Modules/node_modules`) và tích hợp bộ 3 Agent Skills tại `.agents/skills/`. Agent **CÓ THỂ KHAI THÁC NGAY** các năng lực mới sau cho cả Video 16:9 chính và 3 Video Shorts 9:16:

1. **Motionmaxxing (`node_modules/motionmaxxing/` & `.agents/skills/motionmaxxing/`) — Chuyển động Điện ảnh & 12 Đường cong Gia tốc Thực nghiệm:**
   - Tương thích 100% với cơ chế Playwright Virtual Clock + GSAP của `DD-The-thao`.
   - Cung cấp `runtime/motion.js` với 12 đường cong gia tốc đo từ 53 phim chuyên nghiệp (`snapSettle`, `softLand`, `whip`, `crashIn`, `popOver`, `bounceHard`...), hệ thống điều khiển camera/cursor/stagger theo frame 30fps, thư viện 3D `hero3d/` (`Three.js` + `UnrealBloomPass`), cùng kho 4.300 chuyển động mẫu tra cứu bằng `python3 node_modules/motionmaxxing/scripts/precedent.py`.
2. **VideoShotcraft 2.0 (`node_modules/video-shotcraft/` & `.agents/skills/video-shotcraft-recipes/`) — Kho 124 Thẻ Công Thức Góc Máy & Nhịp Điệu Thể Thao:**
   - Cung cấp 124 kịch bản góc máy chi tiết từng frame ở 30fps (`node_modules/video-shotcraft/references/shots/`): lia camera đa tầng chiều sâu (`camera/depth-layer-moves.md`, `camera/crash-zoom-punch.md`), nhịp cắt dồn dập kiểu trailer thể thao (`rhythm/trailer-grammar-moves.md`, `rhythm/beat-cut-moves.md`, `rhythm/speed-ramp-freeze.md`), bảng thống kê cầu thủ/trận đấu xuất hiện tuần tự (`ui-entrance/product-card-progressive-assemble.md`, `data/chart-live-moves.md`), và hiệu ứng quét HUD phân tích chiến thuật (`effects/scanline-annotate-focus.md`, `effects/spotlight-sweep-moves.md`).
3. **DataViz (`node_modules/dataviz/` & `.agents/skills/dataviz/`) — Đồ Thị Thống Kê Bóng Đá / Thể Thao Chuẩn Mực:**
   - Quy trình chọn biểu đồ so sánh phong độ, bàn thắng, tỷ lệ kiểm soát bóng (`references/choosing-a-form.md`, `marks-and-anatomy.md`) và kiểm tra độ tương phản màu Cyber-Stadium tự động qua `python3 node_modules/dataviz/scripts/validate_palette.py`.
4. **Antigravity Animation (`node_modules/antigravity-animation/`) — Lớp Phủ Hạt Hình Học GPU 60fps:**
   - Cung cấp mã nguồn Canvas 2D tối ưu GPU (`antigravity-basic.html` & `antigravity-pattern.html`) tạo các hạt hình học trôi nổi hoặc tự động hội tụ thành đội hình trên nền tối Cyber-Stadium mà không gây nặng CPU.
