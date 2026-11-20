#!/usr/bin/env python3
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

"""
ENGINE: HTML — Renderer khung-hình-theo-khung-hình (deterministic)
===================================================================
Đây là engine mặc định. Nguyên lý (giữ từ hệ thống cũ, đã kiểm chứng):

  Tiêm một ĐỒNG HỒ ẢO vào trang trước khi script template chạy, ghi đè
  performance.now / Date.now / requestAnimationFrame / setTimeout / setInterval
  và toàn bộ CSS/WAAPI animation. Với mỗi frame: tua đồng hồ tới đúng
  t = frame/fps, chụp ảnh JPEG Q95, đẩy thẳng vào FFmpeg.

  → Không rớt frame. Deterministic (render 10 lần ra file y hệt).
  → Máy chậm chỉ render lâu hơn, không làm video xấu đi.

Cải tiến so với hệ thống cũ:
  - Chờ font + ảnh + preload mọi ảnh trong timeline trước frame đầu.
  - Cảnh báo rõ khi JS lỗi (không im lặng).
  - Cache theo hash nội dung cảnh (bỏ qua render nếu không đổi).
  - Âm thanh chuẩn hóa EBU R128 thay vì chỉ peak.
  - Trả exit code rõ ràng để pipeline biết thất bại.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
sys.path.insert(0, os.path.join(_ROOT, "core"))

from diemdoc import paths
from diemdoc.audio import build_sfx_track, mix_audio
from diemdoc.jsonio import hash_obj, load_json, save_json
from diemdoc.log import banner, die, log, ok, step, warn
from diemdoc.timeline import cards_of, load_timeline, total_duration

# Shim đồng hồ ảo — đọc từ _runtime.js để có MỘT nguồn chân lý duy nhất.
# (runtime.js chứa cùng đoạn shim; ở đây ta đọc trực tiếp để không lệch nhau.)
VIRTUAL_TIME_SHIM = r"""
(() => {
  if (window.__vt) return;
  let vnow = 0;
  const dateBase = Date.now();
  performance.now = () => vnow;
  Date.now = () => dateBase + vnow;
  let rafId = 0; let rafQ = new Map();
  window.requestAnimationFrame = (cb) => { const id = ++rafId; rafQ.set(id, cb); return id; };
  window.cancelAnimationFrame = (id) => { rafQ.delete(id); };
  let tId = 0; const timers = new Map();
  window.setTimeout = (cb, ms, ...a) => { const id = ++tId; timers.set(id, {cb, due: vnow + Math.max(0, +ms||0), args:a, iv:0}); return id; };
  window.setInterval = (cb, ms, ...a) => { const id = ++tId; const iv = Math.max(1, +ms||0); timers.set(id, {cb, due: vnow+iv, args:a, iv}); return id; };
  window.clearTimeout = (id) => timers.delete(id);
  window.clearInterval = (id) => timers.delete(id);
  const animStart = new WeakMap();
  function seekAnimations() {
    for (const a of document.getAnimations()) {
      if (!animStart.has(a)) animStart.set(a, vnow);
      try { a.pause(); a.currentTime = Math.max(0, vnow - animStart.get(a)); } catch (e) {}
    }
  }
  window.__vt = {
    now: () => vnow,
    advanceTo(ms) {
      let guard = 0;
      while (guard++ < 20000) {
        let next = null, nid = null;
        for (const [id, t] of timers) if (t.due <= ms && (!next || t.due < next.due)) { next = t; nid = id; }
        if (!next) break;
        vnow = next.due;
        if (next.iv) next.due += next.iv; else timers.delete(nid);
        try { typeof next.cb === 'function' ? next.cb(...next.args) : (0, eval)(String(next.cb)); } catch (e) { console.error(e); }
      }
      vnow = ms;
      const q = rafQ; rafQ = new Map();
      for (const cb of q.values()) { try { cb(vnow); } catch (e) { console.error(e); } }
      seekAnimations(); seekAnimations();
      return vnow;
    }
  };
})();
"""


# ==========================================================================
# Chuẩn bị HTML
# ==========================================================================

def _normalize_image_paths(obj, project_dir: str):
    """Chuyển các đường dẫn ảnh tương đối trong project thành file:// URL hợp lệ."""
    if isinstance(obj, dict):
        new_d = {}
        for k, v in obj.items():
            if k in ("image", "bg_image", "hero_image", "src", "path", "file_url", "avatar", "left_avatar") and isinstance(v, str):
                if not v.startswith(("http://", "https://", "file://", "data:")):
                    full_p = os.path.join(project_dir, v)
                    work_p = paths.work_project_file(os.path.basename(project_dir), v)
                    root_p = os.path.join(_ROOT, v)
                    if os.path.exists(full_p):
                        new_d[k] = paths.file_url(full_p)
                    elif os.path.exists(work_p):
                        new_d[k] = paths.file_url(work_p)
                    elif os.path.exists(root_p):
                        new_d[k] = paths.file_url(root_p)
                    elif os.path.isabs(v) and os.path.exists(v):
                        new_d[k] = paths.file_url(v)
                    else:
                        new_d[k] = v
                else:
                    new_d[k] = v
            else:
                new_d[k] = _normalize_image_paths(v, project_dir)
        return new_d
    elif isinstance(obj, list):
        return [_normalize_image_paths(x, project_dir) for x in obj]
    return obj


def inject_html(template_path: str, timeline: dict, words: dict, project_dir: str,
                out_path: str) -> str:
    """
    Đọc template, thay placeholder, ghi ra file HTML tạm trong project.
    Dùng đường dẫn TƯƠNG ĐỐI để template có thể tham chiếu _base.css/_runtime.js
    nằm cạnh nó trong templates/.
    """
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("__ASSETS__", paths.file_url(paths.ASSETS))
    # Ưu tiên logo từ channel.json hoặc diem-doc-logo-1.png
    logo_file = "diem-doc-logo-1.png"
    cfg_channel = os.path.join(paths.CONFIG, "channel.json")
    if os.path.exists(cfg_channel):
        try:
            with open(cfg_channel, "r", encoding="utf-8") as f:
                cdata = json.load(f)
                logo_file = cdata.get("logo", {}).get("primary", logo_file)
        except Exception:
            pass
    html = html.replace("__LOGO__", paths.file_url(os.path.join(paths.LOGO, logo_file)))

    # Chuẩn hóa đường dẫn ảnh trong project thành file_url để không bị lệch do <base href>
    norm_timeline = _normalize_image_paths(timeline, project_dir)

    inject = (
        f"window.VIDEO_DATA = {_json(norm_timeline)};\n"
        f"window.WORD_TIMESTAMPS = {_json(words)};\n"
        f"window.RENDER_MODE = 'frames';"
    )
    if "// __INJECT_JSON_HERE__" not in html:
        die(f"Template {os.path.basename(template_path)} thiếu marker '// __INJECT_JSON_HERE__'")
    html = html.replace("// __INJECT_JSON_HERE__", inject)

    # các asset tương đối (_base.css, _runtime.js...) nằm trong templates/
    html = html.replace("<head>", f'<head>\n<base href="{paths.file_url(paths.TEMPLATES)}/">', 1)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path


def _json(obj) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False)


def image_paths(timeline: dict) -> list[str]:
    """Quét đệ quy mọi đường dẫn ảnh trong timeline."""
    import re
    found: list[str] = []
    rx = re.compile(r"\.(png|jpe?g|webp|gif|svg)$", re.IGNORECASE)

    def walk(o):
        if isinstance(o, str):
            if rx.search(o):
                found.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(timeline)
    return found


# ==========================================================================
# Render
# ==========================================================================

_HW_ENCODER_CHECKED: bool | None = None


def _has_videotoolbox() -> bool:
    """Kiểm tra một lần xem FFmpeg có hỗ trợ mã hóa phần cứng h264_videotoolbox (macOS) không."""
    global _HW_ENCODER_CHECKED
    if _HW_ENCODER_CHECKED is not None:
        return _HW_ENCODER_CHECKED
    try:
        out = subprocess.check_output(["ffmpeg", "-hide_banner", "-encoders"], text=True, stderr=subprocess.DEVNULL)
        _HW_ENCODER_CHECKED = ("h264_videotoolbox" in out)
    except Exception:
        _HW_ENCODER_CHECKED = False
    return _HW_ENCODER_CHECKED


def render_html_engine(project_dir: str, template: str | None, scene_number: int | None,
                       fps: int = 30, preview: bool = False,
                       use_cache: bool = True, force: bool = False,
                       format_override: str | None = None,
                       video_only_output: bool = False,
                       jpeg_quality: int = 88,
                       hw_encode: bool = True) -> str | None:
    import base64
    from playwright.sync_api import sync_playwright

    project_dir = os.path.abspath(project_dir)
    tl = load_timeline(project_dir)
    fmt = (format_override or tl.get("format") or "short").lower()
    vw, vh = (1920, 1080) if fmt == "long" else (1080, 1920)

    template = template or tl.get("template") or ("long_cinematic.html" if fmt == "long" else "short_swiss.html")
    tpl_path = os.path.join(paths.TEMPLATES, template)
    if not os.path.exists(tpl_path):
        die(f"Không tìm thấy template: {tpl_path}")

    # ---- chế độ cảnh đơn lẻ: rebase về t=0 ----
    if scene_number is not None:
        active, duration, out_mp4, html_path, voice, words_path, out_dir = _scene_scope(tl, project_dir, scene_number, preview)
    else:
        active, duration, out_mp4, html_path, voice, words_path, out_dir = _full_scope(tl, project_dir, preview)

    # ---- cache theo nội dung ----
    cache_file = os.path.join(out_dir, f".cache_{os.path.basename(out_mp4)}.json")
    if use_cache and not force and os.path.exists(out_mp4):
        prev = load_json(cache_file, {})
        if prev.get("hash") == _content_hash(active, tpl_path, vw, vh, fps):
            ok(f"Cache hit — bỏ qua render: {os.path.basename(out_mp4)}")
            return out_mp4

    words = load_json(words_path, {}) or {}
    if not words.get("karaoke_chunks"):
        warn(f"Không có karaoke_chunks trong {os.path.basename(words_path)} — phụ đề sẽ trống.")

    html = inject_html(tpl_path, active, words, project_dir, html_path)

    if preview:
        fps = 15
    scale = 0.5 if preview else 1.0
    import math
    if not preview and "_n_frames" in active:
        n_frames = int(active["_n_frames"])
    else:
        n_frames = int(round(duration * fps))
    exact = n_frames / fps
    out_w, out_h = int(vw * scale) // 2 * 2, int(vh * scale) // 2 * 2

    log(f"{vw}x{vh} @ {fps}fps | {template} | {exact:.2f}s | {n_frames} frames", tag="html")
    log(f"→ {paths.rel_to_root(out_mp4)}", tag="html")

    tmp = paths.ensure_dir(os.path.join(out_dir, f"_tmp_{os.getpid()}"))
    video_only = os.path.join(tmp, "video_only.mp4")

    # Kiểm tra xem có video_only.mp4 hoàn chỉnh từ phiên render vừa xong không (chỉ tái sử dụng khi không bật force)
    reused_video = False
    if not force:
        for entry in os.listdir(out_dir):
            if entry.startswith("_tmp_") and entry != f"_tmp_{os.getpid()}":
                cand = os.path.join(out_dir, entry, "video_only.mp4")
                if os.path.exists(cand) and os.path.getsize(cand) > 1024 * 1024:
                    try:
                        probe_dur = float(subprocess.check_output([
                            "ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", cand
                        ], text=True).strip())
                        if abs(probe_dur - duration) <= 0.5:
                            shutil.copy2(cand, video_only)
                            reused_video = True
                            ok(f"Tái sử dụng video_only.mp4 đã render hoàn tất từ {entry} ({probe_dur:.2f}s).")
                            break
                    except Exception:
                        pass
    else:
        # Khi force=True, dọn sạch mọi _tmp_ cũ để đảm bảo render mới 100%
        for entry in os.listdir(out_dir):
            if entry.startswith("_tmp_") and entry != f"_tmp_{os.getpid()}":
                old_tmp = os.path.join(out_dir, entry)
                try: shutil.rmtree(old_tmp, ignore_errors=True)
                except Exception: pass

    t0 = time.time()
    js_errors: list[str] = []

    if not reused_video:
        use_hw = bool(hw_encode and not preview and _has_videotoolbox())
        if use_hw:
            enc_codec = ["-c:v", "h264_videotoolbox", "-q:v", "68", "-pix_fmt", "yuv420p"]
        else:
            enc_codec = ["-c:v", "libx264", "-preset", "fast", "-crf", "26" if preview else "18", "-pix_fmt", "yuv420p"]

        enc = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error",
             "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
             "-vf", f"scale={out_w}:{out_h}:flags=lanczos" if scale != 1.0 else "null",
             *enc_codec,
             "-r", str(fps), "-movflags", "+faststart", video_only],
            stdin=subprocess.PIPE)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, args=[
                    "--no-sandbox", "--allow-file-access-from-files", "--disable-dev-shm-usage",
                    "--hide-scrollbars", "--force-device-scale-factor=1", "--font-render-hinting=none"])
                ctx = browser.new_context(viewport={"width": vw, "height": vh}, device_scale_factor=1)
                ctx.add_init_script(VIRTUAL_TIME_SHIM)
                page = ctx.new_page()
                page.on("pageerror", lambda e: js_errors.append(str(e)))
                page.goto(paths.file_url(html), wait_until="load", timeout=90000)

                # chờ font + ảnh tĩnh
                page.evaluate("""async () => {
                    if (document.fonts && document.fonts.ready) await document.fonts.ready;
                    const imgs = Array.from(document.images);
                    await Promise.all(imgs.map(i => i.complete ? 1 : new Promise(r => { i.onload = i.onerror = r; })));
                }""")
                page.evaluate("() => { if (window.startVideo) window.startVideo(); }")

                # preload ảnh tham chiếu trong timeline (ảnh của card chưa hiện)
                imgs = image_paths(active)
                if imgs:
                    page.evaluate("""async (urls) => {
                        await Promise.all(urls.map(u => new Promise(r => {
                            const im = new Image(); im.onload = im.onerror = r; im.src = u; })));
                    }""", imgs)

                # Dùng CDP Page.captureScreenshot trực tiếp (nhanh hơn page.screenshot do bỏ vòng kiểm tra ổn định layout)
                cdp = None
                try:
                    cdp = ctx.new_cdp_session(page)
                except Exception:
                    cdp = None

                q_val = max(75, min(95, int(jpeg_quality)))
                for i in range(n_frames):
                    page.evaluate("ms => window.__vt.advanceTo(ms)", i * 1000.0 / fps)
                    if cdp is not None:
                        try:
                            res_cdp = cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": q_val})
                            buf = base64.b64decode(res_cdp["data"])
                        except Exception:
                            cdp = None
                            buf = page.screenshot(type="jpeg", quality=q_val, animations="allow", caret="hide")
                    else:
                        buf = page.screenshot(type="jpeg", quality=q_val, animations="allow", caret="hide")
                    enc.stdin.write(buf)
                    if i and i % (fps * 5) == 0:
                        el = time.time() - t0
                        eta = el / i * (n_frames - i)
                        log(f"  frame {i}/{n_frames}  ({el:.0f}s, ETA {eta:.0f}s)", tag="html")
                browser.close()
        except Exception as e:
            enc.kill()
            die(f"Lỗi Playwright: {e}")

        enc.stdin.close()
        if enc.wait() != 0:
            die("FFmpeg encoder thất bại.")

    if js_errors:
        warn(f"{len(js_errors)} lỗi JS trong template. Đầu tiên: {js_errors[0][:300]}")

    # ---- âm thanh (bỏ qua nếu video_only_output=True để tránh mix/loudnorm thừa ở từng chunk nhỏ) ----
    if video_only_output:
        shutil.copy2(video_only, out_mp4)
    else:
        sfx_wav = _build_sfx(active, exact, tmp)
        bgm = _pick_bgm(active) if scene_number is None else None

        if not mix_audio(video_only, out_mp4, exact,
                         voice=voice, bgm=bgm,
                         bgm_gain=float(active.get("bgm_volume", 0.08)),
                         sfx=sfx_wav, loudness_normalize=not preview):
            die("Trộn âm thanh thất bại.")

    # ---- dọn dẹp ----
    _archive_html(project_dir, html_path)
    try:
        shutil.move(tmp, os.path.expanduser(f"~/.Trash/{os.path.basename(tmp)}_{int(time.time())}"))
    except Exception:
        shutil.rmtree(tmp, ignore_errors=True)

    save_json(cache_file, {"hash": _content_hash(active, tpl_path, vw, vh, fps)})
    ok(f"RENDER XONG: {paths.rel_to_root(out_mp4)} ({exact:.2f}s, {time.time() - t0:.0f}s)")
    return out_mp4


# ==========================================================================
# Scope helpers
# ==========================================================================

def _scene_scope(tl: dict, project_dir: str, scene_number: int, preview: bool):
    import copy
    scenes = tl.get("scenes", [])
    target = next((s for s in scenes if int(s.get("scene_id", 0)) == scene_number), None)
    if target is None and 1 <= scene_number <= len(scenes):
        target = scenes[scene_number - 1]
    if target is None:
        die(f"Không tìm thấy cảnh {scene_number}.")

    sc = copy.deepcopy(target)
    start = float(sc.get("_start_time", sc.get("start_time", 0)) or 0)
    sc["_start_time"] = sc["start_time"] = 0.0
    for c in cards_of(sc):
        rv = c.get("_reveal_time", c.get("reveal_time"))
        local = (float(rv) - start) if rv is not None else float(c.get("local_delay", 0.2))
        local = max(0.0, round(local, 3))
        c["_reveal_time"] = c["reveal_time"] = local
        c["local_delay"] = local

    active = dict(tl)
    active["scenes"] = [sc]
    active["subtitles"] = sc.get("subtitles_local") or sc.get("subtitles") or []
    dur = float(sc.get("_duration", sc.get("duration", 10)) or 10)
    active["total_duration"] = dur

    out_dir = paths.ensure_dir(os.path.join(project_dir, "scenes_out"))
    pfx = f"scene_{scene_number:02d}"
    return (active, dur,
            os.path.join(out_dir, f"{pfx}{'_preview' if preview else ''}.mp4"),
            os.path.join(project_dir, f"render_{pfx}.html"),
            os.path.join(out_dir, f"{pfx}.wav"),
            os.path.join(out_dir, f"{pfx}_words.json"),
            out_dir)


def _full_scope(tl: dict, project_dir: str, preview: bool):
    name = tl.get("output_filename") or "final_video.mp4"
    if not name.endswith(".mp4"):
        name += ".mp4"
    if preview:
        name = name[:-4] + "_preview.mp4"
    proj_name = os.path.basename(project_dir.rstrip("/"))
    voice_wav = paths.work_project_file(proj_name, "voiceover.wav")
    if not os.path.exists(voice_wav):
        voice_wav = os.path.join(project_dir, "voiceover.wav")
    return (tl, total_duration(tl),
            os.path.join(project_dir, name),
            os.path.join(project_dir, "render.html"),
            voice_wav,
            os.path.join(project_dir, "word_timestamps.json"),
            project_dir)


def _content_hash(active: dict, tpl_path: str, vw: int, vh: int, fps: int) -> str:
    from diemdoc.jsonio import hash_file
    return hash_obj({"tl": active, "tpl": hash_file(tpl_path),
                     "base": hash_file(os.path.join(paths.TEMPLATES, "_base.css")),
                     "runtime": hash_file(os.path.join(paths.TEMPLATES, "_runtime.js")),
                     "cards": hash_file(os.path.join(paths.TEMPLATES, "_cards.js")),
                     "director": hash_file(os.path.join(paths.TEMPLATES, "_director.js")),
                     "dom": [vw, vh, fps]})


def _pick_bgm(active: dict) -> str | None:
    name = active.get("bgm") or "bgm_editorial.mp3"
    p = os.path.join(paths.BGM, name)
    if os.path.exists(p):
        return p
    # Fallback sang các BGM có sẵn trong assets
    for cand in ["bgm_editorial.mp3", "bgm_countdown_dramatic.mp3", "bgm_pulse_dark_full.mp3", "bgm_default.mp3"]:
        cp = os.path.join(paths.BGM, cand)
        if os.path.exists(cp):
            return cp
    warn(f"Không thấy BGM '{name}' — render không nhạc nền.")
    return None


def _build_sfx(active: dict, duration: float, tmp: str) -> str | None:
    """Thu thập & trộn mọi SFX event thành 1 track."""
    events: list[dict] = []
    scenes = active.get("scenes", [])
    enable_scene_whoosh = active.get("enable_sfx", True)

    for ev in active.get("sfx_events", []):
        f = ev.get("file")
        if not f and ev.get("sfx"):
            f = os.path.join(paths.SFX, ev["sfx"])
        if f and os.path.exists(f):
            t_ms = int(max(0, float(ev.get("time_ms", ev.get("time", 0) * 1000))))
            events.append({"file": f, "time_ms": t_ms, "volume": float(ev.get("volume", 0.22))})

    for si, sc in enumerate(scenes):
        sc_start = float(sc.get("_start_time", sc.get("start_time", 0)) or 0)
        default_page = "whoosh_page.mp3" if (si > 0 and enable_scene_whoosh) else ""
        page_sfx = sc.get("sfx", default_page)
        if page_sfx:
            f = os.path.join(paths.SFX, page_sfx)
            if os.path.exists(f):
                events.append({"file": f, "time_ms": int(max(0, sc_start * 1000)), "volume": 0.25})

        for c in cards_of(sc):
            ctype = c.get("type", "card")
            sfx = c.get("sfx")
            if not sfx:
                continue
            f = os.path.join(paths.SFX, sfx)
            if not os.path.exists(f):
                f = os.path.join(paths.SFX, "pop_card.mp3")
                if not os.path.exists(f):
                    continue
            rv = c.get("_reveal_time", c.get("reveal_time"))
            if rv is None:
                rv = sc_start + float(c.get("local_delay", 0.3))
            events.append({"file": f, "time_ms": int(max(0, float(rv) * 1000)), "volume": 0.24})

    if not events:
        return None
    res = build_sfx_track(events, duration, os.path.join(tmp, "sfx.wav"))
    if isinstance(res, tuple):
        out_wav, num_sfx = res
        return out_wav if num_sfx > 0 else None
    return res


def _archive_html(project_dir: str, html_path: str) -> None:
    if not os.path.exists(html_path):
        return
    arch = paths.ensure_dir(os.path.join(project_dir, "render_html"))
    try:
        shutil.move(html_path, os.path.join(arch, os.path.basename(html_path)))
    except Exception:
        pass


# ==========================================================================
# CLI
# ==========================================================================

def main() -> None:
    ap = argparse.ArgumentParser(description="Engine HTML — render deterministic frame-by-frame")
    ap.add_argument("project")
    ap.add_argument("--scene", type=int, default=None)
    ap.add_argument("--template", default=None)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--preview", action="store_true", help="15fps, 50% scale — duyệt nhanh")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--force", action="store_true", help="Bỏ qua cache, render lại")
    args = ap.parse_args()

    banner("ENGINE HTML — DETERMINISTIC RENDER", "By The Numbers")
    pdir = paths.project_dir(args.project)
    render_html_engine(pdir, args.template, args.scene, fps=args.fps,
                       preview=args.preview, use_cache=not args.no_cache, force=args.force)


if __name__ == "__main__":
    main()