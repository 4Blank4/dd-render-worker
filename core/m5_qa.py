#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

"""
m5 — QA (Visual + Layout + Content) ★ MODULE MỚI HOÀN TOÀN ★
==============================================================
Hệ thống cũ chỉ validate TEXT (số từ, mật độ thẻ) — nó KHÔNG BAO GIỜ nhìn
thấy kết quả. Với một hệ thống mà Agent tự sinh bố cục, đó là lỗ hổng chí mạng:
Agent không thể biết mình vừa tạo ra cái gì.

Module này cho hệ thống ĐÔI MẮT, qua 4 tầng:

  L1 — SCHEMA   : timeline có hợp lệ không (spec/schema.py)
  L2 — LAYOUT   : chữ có tràn khung? thẻ có chồng nhau? ảnh có trắng?
                  → đo bằng JS trong trình duyệt, CHÍNH XÁC, không cần vision
  L3 — VISION   : chụp 1 frame mỗi cảnh → contact sheet → Agent đọc bằng mắt
                  → phát hiện lỗi thẩm mỹ mà JS không thấy
  L4 — CONTENT  : con số trong card có khớp với lời thoại không?
                  (kênh về con số thì đây là lỗi nghiêm trọng nhất)

Cách dùng:
  python3 m5_qa.py <project>                 # chạy L1 + L2 + L4
  python3 m5_qa.py <project> --shots         # thêm L3: xuất contact sheet
  python3 m5_qa.py <project> --shots --every 2   # 1 ảnh mỗi 2 cảnh
"""

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_ROOT, "core"))
sys.path.insert(0, os.path.join(_ROOT, "spec"))

from diemdoc import paths
from diemdoc.jsonio import load_json, save_json
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import cards_of, load_timeline, scene_duration, scene_start, total_duration

import schema as S


# ==========================================================================
# L1 — SCHEMA
# ==========================================================================

def qa_schema(tl: dict) -> dict:
    errs, warns = S.validate_timeline(tl)
    real_warns = [w for w in warns if not w.startswith("__info__")]
    return {"layer": "L1-schema", "errors": errs, "warnings": real_warns,
            "info": [w for w in warns if w.startswith("__info__")]}


# ==========================================================================
# L2 — LAYOUT (đo trong trình duyệt)
# ==========================================================================

_LAYOUT_JS = r"""
() => {
  const out = { overflow: [], overlap: [], brokenImages: [], emptyCards: [], fonts: [], contrast: [] };
  const fmt = (el) => {
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) };
  };

  // 1. Tràn khung: nội dung cao/rộng hơn khung chứa
  document.querySelectorAll('.card, .cell, .row').forEach((el) => {
    const id = el.getAttribute('data-card') || el.className;
    if (el.scrollHeight > el.clientHeight + 2) {
      out.overflow.push({ el: id, axis: 'y', scroll: el.scrollHeight, client: el.clientHeight,
                          over: el.scrollHeight - el.clientHeight });
    }
    if (el.scrollWidth > el.clientWidth + 2) {
      out.overflow.push({ el: id, axis: 'x', scroll: el.scrollWidth, client: el.clientWidth,
                          over: el.scrollWidth - el.clientWidth });
    }
  });

  // 2. Chồng lấn giữa các card cùng cảnh
  //    Chỉ đo cảnh ĐANG HIỆN — cảnh ẩn có opacity 0 nên getBoundingClientRect
  //    vẫn trả toạ độ nhưng innerText rỗng, gây báo động giả.
  const scenes = document.querySelectorAll('.scene');
  scenes.forEach((sc, si) => {
    const visible = sc.style.visibility !== 'hidden' && sc.style.opacity !== '0';
    if (!visible) return;
    const cards = Array.from(sc.querySelectorAll('.card[data-card]'));
    const boxes = cards.map((c) => ({ id: c.getAttribute('data-card'), r: c.getBoundingClientRect() }));
    for (let i = 0; i < boxes.length; i++) {
      for (let j = i + 1; j < boxes.length; j++) {
        const a = boxes[i].r, b = boxes[j].r;
        const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (ox > 4 && oy > 4) {
          out.overlap.push({ scene: si + 1, a: boxes[i].id, b: boxes[j].id,
                             ox: Math.round(ox), oy: Math.round(oy) });
        }
      }
    }
    // 3. Card rỗng (không có chữ, không có ảnh)
    cards.forEach((c) => {
      const txt = (c.innerText || '').trim();
      const img = c.querySelector('img');
      if (!txt && !img) out.emptyCards.push({ scene: si + 1, card: c.getAttribute('data-card') });
    });
  });

  // 4. Ảnh hỏng / không tải được
  document.querySelectorAll('img').forEach((im) => {
    if (!im.complete || im.naturalWidth === 0) {
      out.brokenImages.push({ src: im.getAttribute('src') });
    }
    // ảnh tải được nhưng khung hiển thị bé tí
    const r = im.getBoundingClientRect();
    if (im.complete && im.naturalWidth > 0 && (r.width < 8 || r.height < 8)) {
      out.brokenImages.push({ src: im.getAttribute('src'), note: 'hiển thị quá nhỏ', w: Math.round(r.width), h: Math.round(r.height) });
    }
  });

  // 5. Font: kiểm tra font đã load chưa
  const wanted = ['Bebas Neue','Space Grotesk','Inter','DM Mono','Anton','Oswald','Montserrat','PlexMono'];
  wanted.forEach((f) => {
    try { if (document.fonts.check(`16px "${f}"`)) out.fonts.push(f); } catch (e) {}
  });

  // 6. Tương phản thô: chữ quá nhạt trên nền
  // (đo bằng cách so màu chữ với nền hiệu dụng — chỉ bắt trường hợp rõ ràng)
  document.querySelectorAll('.card').forEach((c) => {
    const cs = getComputedStyle(c);
    const col = cs.color;
    const m = col.match(/\d+/g);
    if (m) {
      const lum = (0.2126 * +m[0] + 0.7152 * +m[1] + 0.0722 * +m[2]) / 255;
      if (lum > 0.92 || lum < 0.06) out.contrast.push({ card: c.getAttribute('data-card'), color: col, lum: +lum.toFixed(3) });
    }
  });

  // 7. Kích thước & vị trí tổng thể
  out.viewport = { w: window.innerWidth, h: window.innerHeight };
  out.sceneCount = scenes.length;
  out.docHeight = document.documentElement.scrollHeight;

  // 8. Kiểm tra Chip Ngày (Bắt buộc theo chuẩn Điểm Đọc: THỨ ... · DD.MM.YYYY)
  const fullText = document.body.innerText || '';
  const dateRegex = /THỨ\s+[A-ZÀ-Ỹ]+\s*[·•\-]\s*\d{1,2}\.\d{1,2}\.\d{4}/i;
  out.hasDateChip = dateRegex.test(fullText);

  // 9. Kiểm tra Karaoke Safe Zone cho 9:16 (không vượt quá 80% chiều cao khung)
  const kBox = document.getElementById('karaoke-container') || document.getElementById('karaoke-box');
  if (kBox && window.innerHeight > window.innerWidth) {
    const kr = kBox.getBoundingClientRect();
    const maxAllowedBottom = window.innerHeight * 0.805; // 80% + margin
    if (kr.bottom > maxAllowedBottom) {
      out.karaokeViolation = {
        bottom: Math.round(kr.bottom),
        limit: Math.round(maxAllowedBottom),
        pct: +(kr.bottom / window.innerHeight * 100).toFixed(1)
      };
    }
  }

  return out;
}
"""


def _load_html_engine(modname: str):
    """Nạp engines/html/renderer.py để dùng lại inject_html mà không render video."""
    import importlib.util
    spec_path = os.path.join(_ROOT, "engines", "html", "renderer.py")
    if not os.path.exists(spec_path):
        die(f"Thiếu engine HTML: {spec_path}")
    spec = importlib.util.spec_from_file_location(modname, spec_path)
    eng = importlib.util.module_from_spec(spec)
    sys.modules[modname] = eng
    spec.loader.exec_module(eng)
    return eng


def qa_layout(project_dir: str, tl: dict) -> dict:
    """Mở trang ở frame đại diện rồi đo layout. Trả về báo cáo."""
    try:
        import playwright  # noqa: F401
    except ImportError:
        return {"layer": "L2-layout", "error": "Playwright chưa cài — bỏ qua L2."}
    return _layout_with_page(project_dir, tl)


def _layout_with_page(project_dir: str, tl: dict) -> dict:
    import importlib.util
    eng = _load_html_engine("_html_eng_qa")

    from playwright.sync_api import sync_playwright

    fmt = (tl.get("format") or "short").lower()
    vw, vh = (1920, 1080) if fmt == "long" else (1080, 1920)
    tpl = tl.get("template") or ("long_cinematic.html" if fmt == "long" else "short_swiss.html")
    tpl_path = os.path.join(paths.TEMPLATES, tpl)

    words = load_json(os.path.join(project_dir, "word_timestamps.json"), {}) or {}
    tmp_html = os.path.join(project_dir, "_qa_page.html")
    eng.inject_html(tpl_path, tl, words, project_dir, tmp_html)

    report: dict = {"layer": "L2-layout", "scenes": []}
    try:
        with sync_playwright() as p:
            br = p.chromium.launch(headless=True, args=[
                "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"])
            ctx = br.new_context(viewport={"width": vw, "height": vh})
            page = ctx.new_page()
            page.goto(paths.file_url(tmp_html), wait_until="load")
            # gọi startVideo rồi tua tới giữa mỗi cảnh để mọi card đã hiện
            page.evaluate("() => { if (window.startVideo) window.startVideo(); }")
            page.wait_for_timeout(400)

            scenes = tl.get("scenes", [])
            for i, sc in enumerate(scenes):
                mid = scene_start(sc) + scene_duration(sc) * 0.65
                page.evaluate("t => window.updateAudioTime && window.updateAudioTime(t)", mid)
                page.wait_for_timeout(60)
                try:
                    r = page.evaluate(_LAYOUT_JS)
                    r["scene_id"] = sc.get("scene_id", i + 1)
                    report["scenes"].append(r)
                except Exception as e:
                    report["scenes"].append({"scene_id": sc.get("scene_id", i + 1), "error": str(e)})
            br.close()
    finally:
        try:
            os.remove(tmp_html)
        except OSError:
            pass

    # gộp
    agg = {"overflow": [], "overlap": [], "brokenImages": [], "emptyCards": [], "fonts": [], "contrast": [], "hasDateChip": True, "karaokeViolations": []}
    for s in report["scenes"]:
        for k in ["overflow", "overlap", "brokenImages", "emptyCards", "fonts", "contrast"]:
            agg[k].extend(s.get(k, []) or [])
        if s.get("karaokeViolation"):
            agg["karaokeViolations"].append(s["karaokeViolation"])
        if not s.get("hasDateChip", False):
            agg["hasDateChip"] = False
    agg["fonts"] = sorted(set(agg["fonts"]))
    agg["emptyCards"] = _dedupe(agg["emptyCards"], ("scene", "card"))
    agg["overflow"] = _dedupe(agg["overflow"], ("el", "axis"))
    report["aggregate"] = agg
    return report


def _dedupe(items: list[dict], keys: tuple[str, ...]) -> list[dict]:
    """Khử trùng lặp giữa các cảnh (cùng lỗi xuất hiện ở nhiều frame đo)."""
    seen = set()
    out = []
    for it in items:
        sig = tuple(str(it.get(k)) for k in keys)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(it)
    return out


# ==========================================================================
# L3 — VISION (contact sheet cho Agent đọc bằng mắt)
# ==========================================================================

def qa_shots(project_dir: str, tl: dict, every: int = 1, per_scene: int = 1) -> str | None:
    """
    Chụp `per_scene` frame cho mỗi cảnh (rải đều), ghép thành contact sheet
    để Agent đọc bằng vision.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        warn("Playwright chưa cài — bỏ qua L3.")
        return None

    import importlib.util  # noqa: F401
    eng = _load_html_engine("_html_eng_shot")

    fmt = (tl.get("format") or "short").lower()
    vw, vh = (1920, 1080) if fmt == "long" else (1080, 1920)
    tpl = tl.get("template") or ("long_cinematic.html" if fmt == "long" else "short_swiss.html")
    tpl_path = os.path.join(paths.TEMPLATES, tpl)
    words = load_json(os.path.join(project_dir, "word_timestamps.json"), {}) or {}

    shots_dir = paths.ensure_dir(os.path.join(project_dir, "qa_shots"))
    tmp_html = os.path.join(project_dir, "_qa_shot.html")
    eng.inject_html(tpl_path, tl, words, project_dir, tmp_html)

    scenes = tl.get("scenes", [])
    made: list[str] = []

    with sync_playwright() as p:
        br = p.chromium.launch(headless=True, args=[
            "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage"])
        ctx = br.new_context(viewport={"width": vw, "height": vh})
        page = ctx.new_page()
        page.goto(paths.file_url(tmp_html), wait_until="load")
        page.evaluate("""async () => {
            if (document.fonts && document.fonts.ready) await document.fonts.ready;
            const imgs = Array.from(document.images);
            await Promise.all(imgs.map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
        }""")
        page.evaluate("() => { if (window.startVideo) window.startVideo(); }")
        page.wait_for_timeout(400)

        for i, sc in enumerate(scenes):
            if i % every != 0:
                continue
            sid = sc.get("scene_id", i + 1)
            s_start, s_dur = scene_start(sc), scene_duration(sc)
            for k in range(per_scene):
                frac = 0.72 if per_scene == 1 else (k + 1) / (per_scene + 1)
                t = s_start + s_dur * frac
                page.evaluate("t => window.updateAudioTime && window.updateAudioTime(t)", t)
                page.wait_for_timeout(80)
                out = os.path.join(shots_dir, f"scene_{int(sid):02d}_{k + 1}.jpg")
                page.screenshot(path=out, type="jpeg", quality=88)
                made.append(out)
        br.close()

    try:
        os.remove(tmp_html)
    except OSError:
        pass

    sheet = _contact_sheet(made, project_dir) if made else None
    return sheet


def _contact_sheet(images: list[str], project_dir: str, cols: int = 4) -> str | None:
    """Ghép ảnh thành lưới để Agent xem nhiều cảnh trong 1 lần đọc."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        warn("Pillow chưa cài — bỏ qua contact sheet (ảnh lẻ vẫn có trong qa_shots/).")
        return None

    thumbs = []
    cell_w = 480
    for p in images:
        try:
            im = Image.open(p).convert("RGB")
            ratio = cell_w / im.width
            im = im.resize((cell_w, int(im.height * ratio)), Image.LANCZOS)
            thumbs.append((os.path.basename(p), im))
        except Exception:
            continue
    if not thumbs:
        return None

    cell_h = max(t[1].height for t in thumbs) + 26
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cell_w * cols, cell_h * rows), (14, 16, 22))
    draw = ImageDraw.Draw(sheet)

    for i, (name, im) in enumerate(thumbs):
        cx = (i % cols) * cell_w
        cy = (i // cols) * cell_h
        sheet.paste(im, (cx, cy + 24))
        draw.text((cx + 8, cy + 6), name, fill=(220, 225, 240))
        draw.rectangle([cx, cy, cx + cell_w - 1, cy + cell_h - 1], outline=(60, 70, 90))

    out = os.path.join(project_dir, "qa_contact_sheet.jpg")
    sheet.save(out, "JPEG", quality=90)
    return out


# ==========================================================================
# L4 — CONTENT (con số phải khớp lời thoại)
# ==========================================================================

_NUM_RE = re.compile(r"\b\d[\d,]*(?:\.\d+)?%?\b")

# Nhãn cấu trúc — không phải dữ liệu, không cần khớp lời thoại.
_STRUCTURAL_KEYS = ("step", "rank", "chunk_index", "id", "hint")
_STRUCTURAL_RE = re.compile(r"^(step|part|phase|stage|chapter|scene|s|\d{1,2})$", re.IGNORECASE)


def qa_content(tl: dict) -> dict:
    """
    Với kênh về con số, lỗi nghiêm trọng nhất là con số trên màn hình
    KHÔNG xuất hiện trong lời thoại. Kiểm tra điều đó.

    Bỏ qua nhãn cấu trúc ("STEP 01", "RANK 3") vì chúng là cách trình bày,
    không phải dữ liệu cần đọc lên.
    """
    issues: list[str] = []
    checked = 0

    for sc in tl.get("scenes", []):
        sid = sc.get("scene_id")
        script = (sc.get("script_text") or "").lower()
        script_nums = {_canon(n) for n in _NUM_RE.findall(script)}
        script_flat = script.replace(",", "")

        for c in cards_of(sc):
            for field, text in _data_strings(c):
                if field in _STRUCTURAL_KEYS:
                    continue
                for num in _NUM_RE.findall(text):
                    cn = _canon(num)
                    if not cn or len(cn) < 2:
                        continue
                    # bỏ qua số thứ tự cấu trúc (01, 02, 1, 2 trong nhãn STEP 01)
                    if _STRUCTURAL_RE.match(cn) and _is_ordinal_context(text, num):
                        continue
                    checked += 1
                    if cn not in script_nums and cn not in script_flat:
                        issues.append(
                            f"Scene {sid}, card '{c.get('id')}': số “{num}” có trên màn hình "
                            f"nhưng KHÔNG có trong lời thoại."
                        )
    return {"layer": "L4-content", "checked": checked, "issues": issues}


def _data_strings(card: dict, prefix: str = "") -> list[tuple[str, str]]:
    """Duyệt card, trả về [(tên_trường, chuỗi)] cho mọi chuỗi chứa số."""
    out: list[tuple[str, str]] = []
    for k, v in card.items():
        if k.startswith("_") or k in ("reveal_time", "local_delay", "sfx", "type", "engine"):
            continue
        if isinstance(v, str):
            out.append((k, v))
        elif isinstance(v, dict):
            out.extend(_data_strings(v, k))
        elif isinstance(v, list):
            for it in v:
                if isinstance(it, dict):
                    out.extend(_data_strings(it, k))
                elif isinstance(it, str):
                    out.append((k, it))
    return out


def _is_ordinal_context(text: str, num: str) -> bool:
    """'STEP 01' / 'PART 2' → số là thứ tự, không phải dữ liệu."""
    before = text[:text.find(num)].strip().lower()
    return bool(re.search(r"(step|part|phase|stage|no|number)\s*$", before))


def _canon(n: str) -> str:
    return n.replace(",", "").rstrip("%").strip()


# ==========================================================================
# REPORT
# ==========================================================================

def report(project_dir: str, tl: dict, results: dict, sheet: str | None) -> int:
    banner("BÁO CÁO QA", os.path.basename(project_dir))
    n_err = n_warn = 0

    # L1
    r1 = results.get("L1", {})
    step("L1 — SCHEMA")
    for e in r1.get("errors", []):
        from diemdoc.log import err as _e
        _e("  " + e); n_err += 1
    for w in r1.get("warnings", []):
        warn("  " + w); n_warn += 1
    for i in r1.get("info", []):
        log("  " + i.replace("__info__ ", ""))
    if not r1.get("errors") and not r1.get("warnings"):
        ok("  Timeline hợp lệ.")

    # L2
    r2 = results.get("L2")
    if r2:
        step("L2 — LAYOUT")
        if r2.get("error"):
            warn("  " + r2["error"])
        else:
            agg = r2.get("aggregate", {})
            fonts = agg.get("fonts", [])
            log(f"  Font đã load: {', '.join(fonts) if fonts else '(không nhận diện được)'}")
            if agg.get("overflow"):
                for o in agg["overflow"][:12]:
                    warn(f"  TRÀN KHUNG [{o.get('axis')}] {o.get('el')}: vượt {o.get('over')}px"); n_warn += 1
            else:
                ok("  Không có card nào tràn khung.")
            if agg.get("overlap"):
                for o in agg["overlap"][:12]:
                    warn(f"  CHỒNG LẤN cảnh {o.get('scene')}: {o.get('a')} ↔ {o.get('b')}"); n_warn += 1
            else:
                ok("  Không có card nào chồng lấn.")
            if agg.get("brokenImages"):
                for b in agg["brokenImages"][:12]:
                    warn(f"  ẢNH LỖI: {b.get('src')} {b.get('note', '')}"); n_warn += 1
            else:
                ok("  Mọi ảnh tải được.")
            if agg.get("emptyCards"):
                for e in agg["emptyCards"][:12]:
                    warn(f"  CARD RỖNG cảnh {e.get('scene')}: {e.get('card')}"); n_warn += 1
            if not agg.get("hasDateChip", False):
                warn("  CHIP NGÀY: Thiếu chip ngày định dạng chuẩn 'THỨ ... · DD.MM.YYYY'!"); n_warn += 1
            else:
                ok("  Đã có chip ngày định dạng chuẩn 'THỨ ... · DD.MM.YYYY'.")
            if agg.get("karaokeViolations"):
                for kv in agg["karaokeViolations"]:
                    warn(f"  KARAOKE SAFE ZONE: Hộp phụ đề vượt ngưỡng 80% (bottom={kv.get('bottom')}px / {kv.get('pct')}%, max={kv.get('limit')}px)!"); n_warn += 1
            else:
                ok("  Karaoke Safe Zone: Hộp phụ đề nằm hoàn toàn trong vùng an toàn <= 80% chiều cao.")

    # L3
    step("L3 — VISION")
    if sheet:
        ok(f"  Contact sheet: {paths.rel_to_root(sheet)}")
        log("  → AGENT: hãy ĐỌC ảnh này bằng vision để đánh giá thẩm mỹ,")
        log("    kiểm tra chữ có bị cắt, ảnh có bị crop mất mặt, bố cục có cân không.")
    else:
        log("  (chưa chạy — thêm --shots)")

    # L4
    r4 = results.get("L4", {})
    step("L4 — CONTENT")
    if r4.get("issues"):
        for i in r4["issues"][:20]:
            warn("  " + i); n_warn += 1
    else:
        ok(f"  {r4.get('checked', 0)} con số khớp với lời thoại.")
    if r4.get("checked") == 0:
        warn("  Không kiểm tra được con số nào — timeline có thể thiếu dữ liệu.")

    print()
    if n_err:
        log(f"KẾT LUẬN: {n_err} LỖI, {n_warn} cảnh báo.")
    elif n_warn:
        ok(f"KẾT LUẬN: hợp lệ, {n_warn} cảnh báo cần xem.")
    else:
        ok("KẾT LUẬN: sạch.")
    return 1 if n_err else 0


def main() -> None:
    ap = argparse.ArgumentParser(description="m5 — QA đa tầng (schema/layout/vision/content)")
    ap.add_argument("project")
    ap.add_argument("--shots", action="store_true", help="Chạy L3: xuất contact sheet")
    ap.add_argument("--every", type=int, default=1, help="Chụp 1 ảnh mỗi N cảnh")
    ap.add_argument("--per-scene", type=int, default=1, help="Số frame mỗi cảnh")
    ap.add_argument("--json", metavar="FILE", help="Xuất báo cáo JSON")
    args = ap.parse_args()

    pdir = paths.project_dir(args.project)
    tl = load_timeline(pdir)

    results = {"L1": qa_schema(tl)}
    results["L2"] = qa_layout(pdir, tl)
    results["L4"] = qa_content(tl)

    sheet = None
    if args.shots:
        sheet = qa_shots(pdir, tl, every=args.every, per_scene=args.per_scene)

    code = report(pdir, tl, results, sheet)
    if args.json:
        save_json(args.json, {"results": results, "contact_sheet": sheet})
        log(f"Đã lưu báo cáo JSON: {args.json}")
    sys.exit(code)


if __name__ == "__main__":
    main()