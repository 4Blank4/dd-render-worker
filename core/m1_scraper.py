#!/usr/bin/env python3
"""
m1_scraper.py — Bộ cào và lọc tin tức thể thao tự động cho "Điểm Đọc"
=====================================================================
Chức năng:
1. Đọc danh sách và thứ tự ưu tiên các nguồn báo thể thao từ `config/sources.json`.
2. Hỗ trợ cào tin qua luồng RSS (`feedparser`) hoặc danh sách URL trực tiếp.
3. Lọc bỏ các bài đăng quá 36 giờ (theo múi giờ Việt Nam ICT UTC+7).
4. Bóc tách nội dung văn bản sạch bằng `trafilatura` (loại bỏ menu, quảng cáo, rác).
5. Trích xuất ảnh bìa chất lượng cao (ưu tiên og:image/ảnh lớn) và ghi chú/nguồn ảnh (credit) bằng `BeautifulSoup`.
6. Bộ lọc từ khóa chặt chẽ:
   - Drop ngay các bài chứa: "trực tiếp", "diễn biến", "tường thuật", "tin đồn", "cập nhật".
   - Luật "Chống tin sai": Loại bỏ hoàn toàn các tin đồn chuyển nhượng (chỉ nhận khi có Official / "Here we go" / công bố chính thức).
7. Xuất kết quả vào `WORK/temp_raw_news.json` (ngoài Google Drive) qua `paths.work_file`.
8. Tự động quét từ lạ / tên riêng chưa có trong từ điển bằng `unknown_names.py`.
"""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import os
import re
import json
import time
import argparse
import urllib.request
import calendar
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from typing import List, Dict, Any, Tuple, Optional

# Thêm core vào sys.path để import diemdoc
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from diemdoc import paths
from diemdoc.unknown_names import scan_unknown_names

# Thư viện ngoài bắt buộc
import feedparser
import trafilatura
from bs4 import BeautifulSoup

ICT = timezone(timedelta(hours=7))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

# 1. Bộ từ khóa cấm bắt buộc loại bỏ ngay lập tức
FORBIDDEN_KEYWORDS = [
    "trực tiếp",
    "diễn biến",
    "tường thuật",
    "tin đồn",
    "cập nhật"
]

# 2. Quy tắc chống tin sai — Chuyển nhượng
TRANSFER_KEYWORDS = [
    "chuyển nhượng",
    "chiêu mộ",
    "gia nhập",
    "cập bến",
    "sang thi đấu cho",
    "mua cầu thủ",
    "bán cầu thủ",
    "hợp đồng mới",
    "đàm phán",
    "rời clb",
    "rời đội",
    "nhắm mua",
    "để mắt"
]

RUMOR_INDICATORS = [
    "tin đồn",
    "đồn đoán",
    "nghi vấn",
    "nguồn tin cho rằng",
    "nguồn tin cho biết",
    "truyền thông loan tin",
    "được cho là",
    "rục rịch",
    "bắn tin",
    "có thể gia nhập",
    "chuẩn bị hỏi mua"
]

OFFICIAL_CONFIRMATIONS = [
    "chính thức",
    "official",
    "here we go",
    "xác nhận",
    "công bố",
    "hoàn tất hợp đồng",
    "ký kết hợp đồng",
    "ra mắt"
]

# Mẫu URL test mặc định cho nghiệm thu GĐ5a
TEST_SAMPLE_URLS = [
    "https://vnexpress.net/mourinho-chat-van-thoi-diem-cong-bo-an-phat-vinicius-5132437.html",
    "https://vnexpress.net/bong-ro-tre-vnexpress-cup-ziaja-harmony-phan-dinh-phung-lua-moi-5132110.html",
    "https://thanhnien.vn/lo-dien-gio-dau-chinh-thuc-3-tran-giai-giao-huu-tai-san-thien-truong-viet-nam-da-ngay-nao-18526101514242116.htm",
    "https://thanhnien.vn/doi-tuyen-viet-nam-van-chuan-bi-tot-nhat-truoc-khi-asian-cup-nguy-co-bi-dung-vi-xung-dot-185261012152533223.htm"
]


def load_source_configs() -> List[Dict[str, Any]]:
    """Đọc cấu hình nguồn tin từ config/sources.json và sắp xếp theo priority."""
    cfg_file = os.path.join(paths.CONFIG, "sources.json")
    if not os.path.exists(cfg_file):
        return []
    with open(cfg_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    sources = data.get("sources", [])
    sources.sort(key=lambda s: s.get("priority", 999))
    return sources


def parse_date_to_ict(val: Any) -> Optional[datetime]:
    """Chuyển đổi đa định dạng thời gian thành datetime có timezone ICT (UTC+7)."""
    if not val:
        return None
    if isinstance(val, time.struct_time):
        ts = calendar.timegm(val)
        return datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(ICT)
    if isinstance(val, datetime):
        if val.tzinfo is None:
            return val.replace(tzinfo=ICT)
        return val.astimezone(ICT)

    s = str(val).strip()
    # 1. Thử ISO format
    try:
        clean_iso = s.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean_iso)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ICT)
        return dt.astimezone(ICT)
    except Exception:
        pass

    # 2. Thử RFC 2822
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ICT)
        return dt.astimezone(ICT)
    except Exception:
        pass

    # 3. Thử các định dạng ngày giờ phổ biến của báo VN
    date_patterns = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y %H:%M",
        "%m/%d/%Y %I:%M:%S %p",
        "%m/%d/%Y %I:%M %p"
    ]
    for fmt in date_patterns:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.replace(tzinfo=ICT)
        except Exception:
            pass

    return None


def check_forbidden_keywords(title: str, description: str, tags: List[str]) -> Tuple[bool, str]:
    """Kiểm tra sự xuất hiện của từ khóa cấm trong tiêu đề, mô tả và tag."""
    combined_texts = [
        ("tiêu đề", title.lower()),
        ("mô tả", description.lower()),
        ("tag", " ".join(tags).lower())
    ]
    for field, text in combined_texts:
        for kw in FORBIDDEN_KEYWORDS:
            if kw in text:
                return True, f"Chứa từ khóa cấm '{kw}' trong {field}"
    return False, ""


def check_transfer_rumor(title: str, description: str, content: str) -> Tuple[bool, str]:
    """
    Quy tắc chống tin sai:
    Nếu bài viết thuộc chủ đề chuyển nhượng, loại bỏ hoàn toàn các tin đồn
    (chỉ chấp nhận khi có Official / Here we go / công bố chính thức).
    """
    text_check = (title + " " + description).lower()
    is_transfer = any(kw in text_check for kw in TRANSFER_KEYWORDS)
    if not is_transfer:
        return False, ""

    has_official = any(kw in text_check for kw in OFFICIAL_CONFIRMATIONS)
    has_rumor = any(kw in text_check for kw in RUMOR_INDICATORS)

    if has_rumor or not has_official:
        return True, "Loại bỏ tin đồn chuyển nhượng chưa có xác nhận chính thức (Official/Here we go)"

    return False, ""


def extract_credit_from_text(text: str) -> str:
    """Bóc tách chuỗi credit/nguồn ảnh từ chú thích (ví dụ: 'Ảnh: AS', 'ẢNH: VFF', 'Nguồn: AP')."""
    if not text:
        return ""
    m = re.search(r'((?:Ảnh|ẢNH|Nguồn|NGUỒN|Photo|PHOTO|Theo|THEO)\s*:\s*[^,\.;\n\r]+)', text)
    if m:
        c = m.group(1).strip()
        # Loại bỏ các đoạn văn bản dài bị dính liền
        if len(c) < 60:
            return c
    return ""


_BAD_IMAGE_PATTERNS = (
    "logo", "icon", "avatar", "cacnguon", "placeholder", "blank.gif",
    "wm1-", "watermark", "gettyimages", "alamy", "shutterstock", "istock", "dreamstime", "123rf",
)


def is_clean_large_image_url(src: str) -> bool:
    """Loại bỏ URL chứa logo, watermark báo chí (wm1-) hoặc stock có bản quyền."""
    low = (src or "").lower()
    if not low or "data:image" in low:
        return False
    return not any(b in low for b in _BAD_IMAGE_PATTERNS)


def extract_article_from_html(html: str, url: str, source_name: str = "") -> Dict[str, Any]:
    """Trích xuất toàn bộ dữ liệu bài viết sạch từ HTML."""
    soup = BeautifulSoup(html, "html.parser")

    # 1. Tiêu đề
    og_title = soup.find("meta", property="og:title")
    tw_title = soup.find("meta", attrs={"name": "twitter:title"})
    h1 = soup.find("h1")
    title = ""
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    elif tw_title and tw_title.get("content"):
        title = tw_title["content"].strip()
    elif h1:
        title = h1.get_text().strip()
    elif soup.title:
        title = soup.title.get_text().strip()

    import html as html_lib
    title = html_lib.unescape(title)

    # Làm sạch đuôi tên báo trong tiêu đề
    title = re.sub(r'\s*[-|–]\s*(Báo\s*)?(Thanh Niên|VnExpress|Tuổi Trẻ|Dân Trí|Bóng đá).*$', '', title, flags=re.I).strip()

    # 2. Mô tả (Sapo / Lead)
    og_desc = soup.find("meta", property="og:description")
    meta_desc = soup.find("meta", attrs={"name": "description"})
    desc = ""
    if og_desc and og_desc.get("content"):
        desc = og_desc["content"].strip()
    elif meta_desc and meta_desc.get("content"):
        desc = meta_desc["content"].strip()
    desc = html_lib.unescape(desc)

    # 3. Ngày đăng
    pub_date_raw = None
    for sel in [
        ("meta", {"property": "article:published_time"}),
        ("meta", {"name": "pubdate"}),
        ("meta", {"name": "its_tag_pubdate"}),
        ("meta", {"itemprop": "datePublished"}),
        ("time", {})
    ]:
        tag = soup.find(sel[0], sel[1])
        if tag:
            pub_date_raw = tag.get("content") or tag.get("datetime") or tag.get_text()
            if pub_date_raw:
                break

    pub_date_ict = parse_date_to_ict(pub_date_raw)

    # 4. Tags
    tags: List[str] = []
    for tag_el in soup.find_all("meta", property="article:tag"):
        if tag_el.get("content"):
            tags.append(tag_el["content"].strip())
    keywords_meta = soup.find("meta", attrs={"name": "keywords"})
    if keywords_meta and keywords_meta.get("content"):
        for kw in keywords_meta["content"].split(","):
            if kw.strip():
                tags.append(kw.strip())

    # 5. Nội dung văn bản sạch qua trafilatura
    clean_text = trafilatura.extract(html, include_comments=False, include_tables=False) or ""

    # 6. Bóc tách ảnh và credit ảnh (ưu tiên ảnh lớn sạch không logo/watermark)
    og_img = soup.find("meta", property="og:image")
    cover_url = og_img["content"].strip() if (og_img and og_img.get("content")) else ""
    if cover_url and not is_clean_large_image_url(cover_url):
        cover_url = ""

    # Quét toàn bộ credit trong bài viết (figcaption, author, credit tags)
    all_credits: List[str] = []
    for fc in soup.find_all("figcaption"):
        c = extract_credit_from_text(fc.get_text().strip())
        if c and c not in all_credits:
            all_credits.append(c)

    for el in soup.find_all(["p", "div", "span"], class_=re.compile(r'caption|description|author|source|credit', re.I)):
        c_text = el.get_text().strip()
        c = extract_credit_from_text(c_text)
        if c and c not in all_credits:
            all_credits.append(c)

    # Quét danh sách ảnh trong bài
    article_images: List[Dict[str, str]] = []
    seen_img_urls = set()
    # Tìm tất cả thẻ figure hoặc div media/photo
    raw_figures = soup.find_all("figure") + soup.find_all("div", class_=re.compile(r'photo|image|figure|picture|media|tplCaption', re.I))
    
    for fig in raw_figures:
        img = fig.find("img")
        if not img:
            continue
        src = img.get("data-src") or img.get("src") or img.get("data-original") or ""
        if not src or "data:image" in src:
            srcset = img.get("srcset")
            if srcset:
                src = srcset.split(",")[-1].strip().split(" ")[0]
        if not src or "data:image" in src:
            continue
        if src.startswith("//"):
            src = "https:" + src

        # Bỏ qua icon, logo, badge rác, wm1- VnExpress và stock watermark
        if not is_clean_large_image_url(src):
            continue
        if "thanhnien.vn/thumb_w/" in src:
            src = re.sub(r"/thumb_w/\d+/", "/", src)

        if src in seen_img_urls:
            continue
        seen_img_urls.add(src)

        fc = fig.find("figcaption")
        if not fc:
            fc = fig.find(["p", "div", "span"], class_=re.compile(r'caption|desc', re.I))
        fc_text = fc.get_text().strip() if fc else ""
        img_credit = extract_credit_from_text(fc_text)
        if not img_credit and all_credits:
            img_credit = all_credits[0]

        article_images.append({
            "url": src,
            "caption": fc_text,
            "credit": img_credit
        })

    # Nếu chưa có cover image, lấy ảnh đầu tiên trong bài
    if not cover_url and article_images:
        cover_url = article_images[0]["url"]

    # Cover image credit & caption
    cover_caption = ""
    cover_credit = ""
    for ai in article_images:
        if ai.get("caption") and not cover_caption:
            cover_caption = ai["caption"]
        if ai.get("credit") and not cover_credit:
            cover_credit = ai["credit"]
        if cover_caption and cover_credit:
            break

    if not cover_caption:
        cover_caption = desc[:120] + "..." if len(desc) > 120 else desc

    if not cover_credit:
        cover_credit = all_credits[0] if all_credits else (f"Ảnh: {source_name}" if source_name else "Ảnh: Thông tấn xã")

    return {
        "url": url,
        "title": title,
        "description": desc,
        "published_at_raw": pub_date_raw,
        "published_at": pub_date_ict.isoformat() if pub_date_ict else None,
        "published_dt": pub_date_ict,
        "tags": tags,
        "clean_text": clean_text,
        "word_count": len(clean_text.split()),
        "cover_image": {
            "url": cover_url,
            "caption": cover_caption,
            "credit": cover_credit
        },
        "images": article_images
    }


def fetch_url_html(url: str, timeout: int = 12) -> Optional[str]:
    """Tải mã HTML của URL với header tiêu chuẩn."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        sys.stderr.write(f"[LỖI TẢI] Không thể tải {url}: {e}\n")
        return None


def parse_since_argument(val: Optional[str], default_end_of_day: bool = False) -> Optional[datetime]:
    """Chuyển đổi tham số --since / --until thành datetime có timezone ICT (UTC+7)."""
    if not val:
        return None
    val = val.strip()
    date_only_fmts = {"%Y-%m-%d", "%d/%m/%Y"}
    fmts = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d/%m/%Y",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(val, fmt)
            if fmt in date_only_fmts:
                if default_end_of_day:
                    dt = dt.replace(hour=23, minute=59, second=59)
                else:
                    dt = dt.replace(hour=0, minute=1, second=0)
            return dt.replace(tzinfo=ICT)
        except ValueError:
            pass
    return parse_date_to_ict(val)


def resolve_time_window(
    period: Optional[str] = None,
    since_str: Optional[str] = None,
    until_str: Optional[str] = None,
    now_ict: Optional[datetime] = None,
) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Tính toán cửa sổ thời gian chuẩn theo quy chuẩn kênh Điểm Đọc (ICT UTC+7):
    - `weekly`: 00:01 Thứ Hai tuần trước -> 23:59:59 Chủ Nhật tuần trước.
    - `yesterday`: 12:00 trưa hôm qua -> hiện tại (None).
    - Tham số `--since` / `--until` tường minh luôn được ưu tiên ghi đè nếu truyền vào.
    """
    if now_ict is None:
        now_ict = datetime.now(ICT)

    auto_since: Optional[datetime] = None
    auto_until: Optional[datetime] = None
    p = (period or "").strip().lower()

    if p == "weekly":
        today_0 = now_ict.replace(hour=0, minute=0, second=0, microsecond=0)
        last_mon = today_0 - timedelta(days=today_0.weekday() + 7)
        auto_since = last_mon.replace(hour=0, minute=1, second=0)
        auto_until = (last_mon + timedelta(days=6)).replace(hour=23, minute=59, second=59)
    elif p == "yesterday":
        yest = (now_ict - timedelta(days=1)).replace(hour=12, minute=0, second=0, microsecond=0)
        auto_since = yest
        auto_until = None

    since_dt = parse_since_argument(since_str, default_end_of_day=False) if since_str else auto_since
    until_dt = parse_since_argument(until_str, default_end_of_day=True) if until_str else auto_until
    return since_dt, until_dt


def evaluate_and_filter_article(
    article_data: Dict[str, Any],
    now_ict: Optional[datetime] = None,
    since_dt: Optional[datetime] = None,
    until_dt: Optional[datetime] = None,
) -> Tuple[bool, str]:
    """
    Áp dụng các lớp kiểm duyệt nghiêm ngặt:
    1. Kiểm tra thời gian: Nếu có --since / --until, loại bỏ tin ngoài cửa sổ (chuẩn UTC+7).
    2. Kiểm tra từ khóa cấm: "trực tiếp", "diễn biến", "tường thuật", "tin đồn", "cập nhật" -> Drop.
    3. Kiểm tra chuyển nhượng (Chống tin sai): Tin đồn / chưa xác nhận -> Drop.
    4. Kiểm tra độ dài nội dung: < 150 ký tự -> Drop.
    """
    if now_ict is None:
        now_ict = datetime.now(ICT)

    pub_dt = article_data.get("published_dt")
    title = article_data.get("title", "")
    desc = article_data.get("description", "")
    tags = article_data.get("tags", [])
    clean_text = article_data.get("clean_text", "")

    # 1. Lọc thời gian (theo --since / --until nếu có, KHÔNG DROP THEO 36H)
    if pub_dt:
        age_seconds = (now_ict - pub_dt).total_seconds()
        age_hours = age_seconds / 3600.0
        article_data["age_hours"] = round(age_hours, 2)
        if since_dt and pub_dt < since_dt:
            return False, f"TRƯỚC_MỐC_THỜI_GIAN (đăng lúc {pub_dt.strftime('%Y-%m-%d %H:%M')}, trước mốc {since_dt.strftime('%Y-%m-%d %H:%M')})"
        if until_dt and pub_dt > until_dt:
            return False, f"SAU_MỐC_KẾT_THÚC (đăng lúc {pub_dt.strftime('%Y-%m-%d %H:%M')}, sau mốc {until_dt.strftime('%Y-%m-%d %H:%M')})"
    else:
        article_data["age_hours"] = None
        if since_dt or until_dt:
            return False, "KHÔNG_CÓ_THỜI_GIAN_ĐĂNG"

    # 2. Lọc từ khóa cấm
    has_forbidden, forbidden_reason = check_forbidden_keywords(title, desc, tags)
    if has_forbidden:
        return False, f"TỪ_KHÓA_BỊ_CẤM ({forbidden_reason})"

    # 3. Lọc tin đồn chuyển nhượng (Chống tin sai)
    is_rumor, rumor_reason = check_transfer_rumor(title, desc, clean_text)
    if is_rumor:
        return False, f"TIN_ĐỒN_CHUYỂN_NHƯỢNG ({rumor_reason})"

    # 4. Kiểm tra độ dài nội dung
    if len(clean_text) < 150:
        return False, f"NỘI_DUNG_QUÁ_NGẮN ({len(clean_text)} ký tự < 150)"

    return True, "HỢP LỆ"


def scrape_single_url(
    url: str,
    source_name: str = "",
    priority: int = 99,
    since_dt: Optional[datetime] = None,
    until_dt: Optional[datetime] = None,
) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """Cào và kiểm duyệt một bài viết đơn lẻ từ URL."""
    html = fetch_url_html(url)
    if not html:
        return False, None, "LỖI_MẠNG_HOẶC_KHÔNG_THỂ_TRUY_CẬP"

    data = extract_article_from_html(html, url, source_name=source_name)
    data["source"] = source_name or (url.split("//")[-1].split("/")[0])
    data["source_priority"] = priority

    passed, reason = evaluate_and_filter_article(data, since_dt=since_dt, until_dt=until_dt)
    return passed, data, reason


def crawl_rss_sources(
    limit_per_source: Optional[int] = None,
    max_total: Optional[int] = 50,
    since_dt: Optional[datetime] = None,
    until_dt: Optional[datetime] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Cào các nguồn RSS theo thứ tự ưu tiên trong config/sources.json.
    - Nếu có since_dt / until_dt: Lấy bài viết có since_dt <= published_at <= until_dt (chuẩn UTC+7).
    - Nếu không có giới hạn thời gian: Lấy mặc định tối đa 50 tin mới nhất từ RSS.
    Trả về (accepted_articles, dropped_reports).
    """
    sources = load_source_configs()
    now_ict = datetime.now(ICT)

    accepted: List[Dict[str, Any]] = []
    dropped: List[Dict[str, Any]] = []
    seen_urls = set()

    if since_dt and until_dt:
        m_str = f"từ {since_dt.strftime('%Y-%m-%d %H:%M')} đến {until_dt.strftime('%Y-%m-%d %H:%M')}"
    elif since_dt:
        m_str = f"từ mốc {since_dt.strftime('%Y-%m-%d %H:%M')}"
    else:
        m_str = f"tối đa {max_total or 50} tin mới nhất"
    print(f"\n[M1_SCRAPER] Bắt đầu quét RSS ({m_str}) từ {len(sources)} nguồn được cấu hình...")

    for src in sources:
        if max_total and len(accepted) >= max_total:
            break

        name = src.get("name", "Nguồn")
        rss_url = src.get("rss", "")
        priority = src.get("priority", 99)
        if not rss_url:
            continue

        print(f"\n-> Đang đọc luồng RSS: {name} (Ưu tiên {priority}): {rss_url}")
        feed = None
        try:
            req = urllib.request.Request(rss_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                feed = feedparser.parse(resp.read())
        except Exception as e:
            try:
                feed = feedparser.parse(rss_url)
            except Exception as e2:
                sys.stderr.write(f"   [CẢNH BÁO] Không đọc được RSS {rss_url}: {e2}\n")
                continue

        if not feed or not feed.entries:
            print(f"   (0 tin hoặc luồng không khả dụng)")
            continue

        print(f"   Đã tìm thấy {len(feed.entries)} bài trong luồng RSS.")
        src_accepted = 0

        for entry in feed.entries:
            if max_total and len(accepted) >= max_total:
                break
            if limit_per_source and src_accepted >= limit_per_source:
                break

            import html as html_lib
            entry_title = html_lib.unescape(entry.get("title", "").strip())
            entry_url = entry.get("link", "").strip()
            entry_desc = html_lib.unescape(entry.get("summary", "").strip())

            if not entry_url or entry_url in seen_urls:
                continue
            seen_urls.add(entry_url)

            # 1. Kiểm tra sơ bộ từ khóa cấm từ RSS để tiết kiệm request
            has_forbidden, forbidden_reason = check_forbidden_keywords(entry_title, entry_desc, [])
            if has_forbidden:
                dropped.append({
                    "url": entry_url,
                    "title": entry_title,
                    "source": name,
                    "reason": f"TỪ_KHÓA_BỊ_CẤM ({forbidden_reason})"
                })
                continue

            # 2. Kiểm tra sơ bộ tin đồn chuyển nhượng từ RSS
            is_rumor, rumor_reason = check_transfer_rumor(entry_title, entry_desc, "")
            if is_rumor:
                dropped.append({
                    "url": entry_url,
                    "title": entry_title,
                    "source": name,
                    "reason": f"TIN_ĐỒN_CHUYỂN_NHƯỢNG ({rumor_reason})"
                })
                continue

            # 3. Kiểm tra sơ bộ ngày đăng từ RSS (nếu có mốc since_dt / until_dt)
            pub_raw = entry.get("published_parsed") or entry.get("published")
            pub_dt = parse_date_to_ict(pub_raw)
            if pub_dt and since_dt and pub_dt < since_dt:
                dropped.append({
                    "url": entry_url,
                    "title": entry_title,
                    "source": name,
                    "reason": f"TRƯỚC_MỐC_THỜI_GIAN ({pub_dt.strftime('%Y-%m-%d %H:%M')} < {since_dt.strftime('%Y-%m-%d %H:%M')})"
                })
                continue
            if pub_dt and until_dt and pub_dt > until_dt:
                dropped.append({
                    "url": entry_url,
                    "title": entry_title,
                    "source": name,
                    "reason": f"SAU_MỐC_KẾT_THÚC ({pub_dt.strftime('%Y-%m-%d %H:%M')} > {until_dt.strftime('%Y-%m-%d %H:%M')})"
                })
                continue

            # 4. Cào toàn văn bài viết và thẩm định chi tiết
            passed, data, reason = scrape_single_url(entry_url, source_name=name, priority=priority, since_dt=since_dt, until_dt=until_dt)
            if passed and data:
                data.pop("published_dt", None)
                data["id"] = f"art_{len(accepted) + 1:02d}"
                accepted.append(data)
                src_accepted += 1
                pub_display = data.get("published_at", "")[:16]
                print(f"   [NHẬN #{len(accepted)}] [{pub_display}] {entry_title[:65]}...")
            else:
                dropped.append({
                    "url": entry_url,
                    "title": entry_title,
                    "source": name,
                    "reason": reason
                })

    return accepted, dropped


def run_test_sample_urls(since_dt: Optional[datetime] = None, until_dt: Optional[datetime] = None) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Chạy kiểm thử trên 4 URL báo mẫu theo đúng yêu cầu nghiệm thu GĐ5a."""
    print("=" * 80)
    print("CHẠY KIỂM THỬ ĐỘC LẬP NGHIỆM THU GĐ5a (4 URL BÁO MẪU)")
    print("=" * 80)

    accepted: List[Dict[str, Any]] = []
    dropped: List[Dict[str, Any]] = []

    for i, url in enumerate(TEST_SAMPLE_URLS, 1):
        source_name = "VnExpress" if "vnexpress" in url else ("Thanh Niên" if "thanhnien" in url else "Báo thể thao")
        priority = 1 if "thanhnien" in url else 2
        print(f"\n[{i}/4] Đang cào URL: {url}")

        passed, data, reason = scrape_single_url(url, source_name=source_name, priority=priority, since_dt=since_dt, until_dt=until_dt)
        if passed and data:
            data.pop("published_dt", None)
            data["id"] = f"art_{len(accepted) + 1:02d}"
            accepted.append(data)
            print(f"   -> KẾT QUẢ: [NHẬN] (Độ dài text: {len(data['clean_text'])} ký tự, Tuổi tin: {data.get('age_hours')}h)")
        else:
            title_sample = data.get("title") if data else "Không rõ tiêu đề"
            dropped.append({
                "url": url,
                "title": title_sample,
                "source": source_name,
                "reason": reason
            })
            print(f"   -> KẾT QUẢ: [BỎ QUA / DROP] Lý do: {reason}")

    return accepted, dropped


def save_and_report_results(accepted: List[Dict[str, Any]], dropped: List[Dict[str, Any]], output_file: Optional[str] = None):
    """Lưu kết quả ra WORK/temp_raw_news.json và quét unknown names."""
    if output_file is None:
        output_file = paths.work_file("temp_raw_news.json")

    now_ict = datetime.now(ICT)
    payload = {
        "metadata": {
            "channel": "Điểm Đọc - Thể Thao",
            "generated_at": now_ict.isoformat(),
            "total_scraped": len(accepted) + len(dropped),
            "total_accepted": len(accepted),
            "total_dropped": len(dropped)
        },
        "dropped_details": dropped,
        "articles": accepted
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"\n[LƯU FILE] Đã lưu kết quả cào tin vào: {output_file}")

    # Quét tên riêng chưa có trong từ điển
    all_text = ""
    for art in accepted:
        all_text += f"{art['title']}. {art['description']}. {art['clean_text']}\n\n"

    print("\n" + "=" * 80)
    print("QUÉT TÊN RIÊNG & TỪ LẠ CHƯA CÓ TRONG TỪ ĐIỂN PHÁT ÂM (unknown_names.py)")
    print("=" * 80)
    unknowns = scan_unknown_names(all_text)
    print(f"Tổng số từ/tên riêng cần rà soát: {len(unknowns)}")
    for item in unknowns[:25]:
        print(f"  - {item['name']}: {item['reason']}")
    if len(unknowns) > 25:
        print(f"  ... và {len(unknowns) - 25} từ khác.")

    return payload


def main():
    parser = argparse.ArgumentParser(description="Bộ cào và lọc tin thể thao tự động - Kênh Điểm Đọc")
    parser.add_argument("--period", choices=["weekly", "yesterday"], default=None, help="Cửa sổ chuẩn: weekly (00:01 T2 tuần trước -> 23:59 CN tuần trước) hoặc yesterday (12:00 trưa hôm qua -> nay)")
    parser.add_argument("--since", type=str, default=None, help="Chỉ lấy tin từ mốc thời gian này trở đi (VD: '2026-10-15 00:01')")
    parser.add_argument("--until", type=str, default=None, help="Chỉ lấy tin đến mốc thời gian này trở về trước (VD: '2026-10-21 23:59')")
    parser.add_argument("--test", action="store_true", help="Chạy kiểm thử trên 4 URL báo mẫu")
    parser.add_argument("--rss", action="store_true", help="Cào tin tự động từ các luồng RSS nguồn")
    parser.add_argument("--urls", nargs="+", help="Danh sách URL cần cào trực tiếp")
    parser.add_argument("--limit", type=int, default=None, help="Giới hạn số tin mỗi nguồn (khi cào RSS)")
    parser.add_argument("--max-total", type=int, default=50, help="Giới hạn tổng số tin (mặc định 50 nếu không có --since)")
    parser.add_argument("--output", type=str, default=None, help="Đường dẫn file JSON đầu ra")

    args = parser.parse_args()

    since_dt, until_dt = resolve_time_window(period=args.period, since_str=args.since, until_str=args.until)
    if args.since and not since_dt:
        sys.stderr.write(f"[CẢNH BÁO] Không thể phân tích cú pháp --since: {args.since}\n")
    if args.until and not until_dt:
        sys.stderr.write(f"[CẢNH BÁO] Không thể phân tích cú pháp --until: {args.until}\n")
    if since_dt or until_dt:
        s_txt = since_dt.strftime("%Y-%m-%d %H:%M:%S") if since_dt else "đầu lịch sử"
        u_txt = until_dt.strftime("%Y-%m-%d %H:%M:%S") if until_dt else "hiện tại"
        print(f"[M1_SCRAPER] Lọc thời gian (UTC+7): {s_txt} -> {u_txt}")

    if args.urls:
        accepted = []
        dropped = []
        for u in args.urls:
            passed, data, reason = scrape_single_url(u, since_dt=since_dt, until_dt=until_dt)
            if passed and data:
                data.pop("published_dt", None)
                data["id"] = f"art_{len(accepted) + 1:02d}"
                accepted.append(data)
            else:
                dropped.append({"url": u, "reason": reason})
    elif args.test:
        accepted, dropped = run_test_sample_urls(since_dt=since_dt, until_dt=until_dt)
    else:
        # Mặc định hoặc khi có --rss / --since / --period: cào tin từ luồng RSS
        max_total = None if (since_dt or until_dt) else args.max_total
        accepted, dropped = crawl_rss_sources(limit_per_source=args.limit, max_total=max_total, since_dt=since_dt, until_dt=until_dt)

    save_and_report_results(accepted, dropped, args.output)


if __name__ == "__main__":
    main()
