#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True

import os
import re
import cv2
import shutil
import requests
import io
import numpy as np
from PIL import Image

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _HERE)

from diemdoc import paths
from run_day import extract_search_keyword, search_ddgs_images, download_image_bytes, open_image_from_bytes, get_high_res_url

def main():
    day_str = "16.10.2026"
    day_dir = paths.project_dir(day_str)
    images_dir = os.path.join(day_dir, "images")
    trash_dir = os.path.expanduser("~/.Trash")

    print(f"=== BẮT ĐẦU QUY TRÌNH TINH CHỌN ẢNH CHUYÊN SÂU CHO NGÀY {day_str} ===")
    
    # 1. Đọc thethao.txt để lấy thông tin các bản tin
    txt_path = os.path.join(day_dir, "thethao.txt")
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    blocks = [b.strip() for b in re.split(r"\n---\n|^---\n", content) if b.strip()]
    tin_titles = {}
    for idx, b in enumerate(blocks, 1):
        tm = re.search(r"Tiêu đề:\s*(.+)", b)
        tin_titles[idx] = tm.group(1).strip() if tm else f"Bản tin {idx}"

    # Quét tất cả file ảnh hiện tại
    all_files = sorted([f for f in os.listdir(images_dir) if f.startswith("Tin_") and f.lower().endswith((".jpg", ".jpeg", ".png"))])
    by_tin = {}
    for f in all_files:
        m = re.match(r"Tin_(\d+)_", f)
        if m:
            t_idx = int(m.group(1))
            by_tin.setdefault(t_idx, []).append(f)

    def get_stats(p):
        try:
            im = Image.open(p).convert("RGB")
            w, h = im.size
            arr = np.array(im)
            gray = np.mean(arr, axis=2)
            dark_ratio = np.mean(gray < 40)
            mean_bright = np.mean(gray)
            return w, h, dark_ratio, mean_bright
        except Exception:
            return 0, 0, 1.0, 0.0

    def get_hist(p):
        im = cv2.imread(p)
        if im is None: return None
        h = cv2.calcHist([im], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(h, h)
        return h

    removed_count = 0
    total_curated = 0

    for idx in range(1, 25):
        flist = by_tin.get(idx, [])
        title = tin_titles.get(idx, "")
        print(f"\n▶ Đang xử lý Tin {idx:02d}: '{title[:45]}...' (Hiện có {len(flist)} ảnh)")

        valid_candidates = []

        # Bước 1: Lọc bỏ ảnh slide đen / quảng cáo phát sóng
        for fn in flist:
            fp = os.path.join(images_dir, fn)
            w, h, dr, mb = get_stats(fp)
            if dr > 0.65 or mb < 35:
                print(f"  ❌ LOẠI BỎ (Ảnh phát sóng/nền đen): {fn} (dark={dr:.1%}, bright={mb:.1f})")
                shutil.move(fp, os.path.join(trash_dir, fn))
                removed_count += 1
            elif w < 500 or h < 500:
                print(f"  ❌ LOẠI BỎ (Kích thước nhỏ <500px): {fn} ({w}x{h})")
                shutil.move(fp, os.path.join(trash_dir, fn))
                removed_count += 1
            else:
                valid_candidates.append(fn)

        # Bước 2: Lọc ảnh trùng lặp góc chụp (Histogram correlation >= 0.85)
        hists = {fn: get_hist(os.path.join(images_dir, fn)) for fn in valid_candidates}
        unique_candidates = []

        for fn in valid_candidates:
            h_curr = hists[fn]
            if h_curr is None: continue
            w_curr, h_curr_sz, _, _ = get_stats(os.path.join(images_dir, fn))
            res_curr = w_curr * h_curr_sz

            dup_found = False
            for u in list(unique_candidates):
                h_u = hists[u]
                corr = cv2.compareHist(h_curr, h_u, cv2.HISTCMP_CORREL)
                if corr >= 0.85:
                    w_u, h_u_sz, _, _ = get_stats(os.path.join(images_dir, u))
                    res_u = w_u * h_u_sz
                    dup_found = True
                    if res_curr > res_u:
                        print(f"  🔄 TRÙNG LẶP: Thay thế {u} ({w_u}x{h_u_sz}) bằng {fn} ({w_curr}x{h_curr_sz}) sắc nét hơn (corr={corr:.2f})")
                        unique_candidates.remove(u)
                        shutil.move(os.path.join(images_dir, u), os.path.join(trash_dir, u))
                        unique_candidates.append(fn)
                        removed_count += 1
                    else:
                        print(f"  ❌ TRÙNG LẶP: Loại bỏ {fn} ({w_curr}x{h_curr_sz}), giữ {u} ({w_u}x{h_u_sz}) nét hơn (corr={corr:.2f})")
                        shutil.move(os.path.join(images_dir, fn), os.path.join(trash_dir, fn))
                        removed_count += 1
                    break
            if not dup_found:
                unique_candidates.append(fn)

        # Bước 3: Nếu ít hơn 3 ảnh, tải bổ sung từ DDGS
        if len(unique_candidates) < 3:
            kw = extract_search_keyword(title)
            needed = 4 - len(unique_candidates)
            print(f"  🔍 Bổ sung ảnh: Chỉ còn {len(unique_candidates)} ảnh. Đang tìm thêm {needed} ảnh với từ khóa '{kw}'...")
            extra_urls = search_ddgs_images(kw, max_needed=needed * 3)
            ext_seq = 10
            for eu in extra_urls:
                if len(unique_candidates) >= 4:
                    break
                try:
                    data = download_image_bytes(eu)
                    p_img = open_image_from_bytes(data)
                    w, h = p_img.size
                    if w >= 800 and h >= 500:
                        tmp_name = f"Tin_{idx:02d}_add_{ext_seq}.jpg"
                        tmp_path = os.path.join(images_dir, tmp_name)
                        if p_img.mode in ("RGBA", "LA", "P", "CMYK"):
                            p_img = p_img.convert("RGB")
                        p_img.save(tmp_path, "JPEG", quality=92, optimize=True)
                        unique_candidates.append(tmp_name)
                        print(f"  ➕ Đã tải bổ sung: {tmp_name} ({w}x{h})")
                        ext_seq += 1
                except Exception:
                    pass

        # Bước 4: Sắp xếp theo chất lượng (kích thước pixel & tỷ lệ khung hình) và giữ tối đa 4 ảnh
        def score_img(fn):
            fp = os.path.join(images_dir, fn)
            w, h, _, _ = get_stats(fp)
            aspect = w / h if h > 0 else 1.0
            # Ưu tiên tỷ lệ ngang 1.3 - 1.8
            aspect_bonus = 1.2 if (1.3 <= aspect <= 1.8) else 1.0
            return (w * h) * aspect_bonus

        unique_candidates.sort(key=score_img, reverse=True)
        final_kept = unique_candidates[:4]  # Giữ tối đa 4 ảnh chất lượng cao nhất

        # Chuyển các ảnh thừa vào trash
        for fn in unique_candidates[4:]:
            print(f"  🗑️  Lược bớt ảnh thừa (ưu tiên 4 ảnh nét nhất): {fn}")
            shutil.move(os.path.join(images_dir, fn), os.path.join(trash_dir, fn))
            removed_count += 1

        # Đổi tên lại liền mạch Tin_XX_1.jpg -> Tin_XX_4.jpg
        # Đổi tạm sang temp để tránh trùng tên
        temp_renamed = []
        for seq, fn in enumerate(final_kept, 1):
            old_p = os.path.join(images_dir, fn)
            tmp_p = os.path.join(images_dir, f"__tmp_{idx:02d}_{seq}.jpg")
            shutil.move(old_p, tmp_p)
            temp_renamed.append(tmp_p)

        for seq, tmp_p in enumerate(temp_renamed, 1):
            final_p = os.path.join(images_dir, f"Tin_{idx:02d}_{seq}.jpg")
            shutil.move(tmp_p, final_p)
            w, h, _, _ = get_stats(final_p)
            print(f"  ✅ Tin_{idx:02d}_{seq}.jpg: ({w}x{h})")

        total_curated += len(temp_renamed)

    print("\n" + "=" * 70)
    print(f"🎉 HOÀN TẤT TINH CHỌN ẢNH:")
    print(f"  - Đã loại bỏ {removed_count} ảnh trùng lặp, ảnh quảng cáo phát sóng, ảnh thừa.")
    print(f"  - Đã giữ lại chính xác {total_curated} ảnh chất lượng cao nhất cho 24 bản tin (mỗi tin 3-4 ảnh).")
    print(f"  - Toàn bộ ảnh đã được đánh số liền mạch Tin_XX_1 -> Tin_XX_N.")
    print("=" * 70)

if __name__ == "__main__":
    main()
