/* ============================================================================
   By The Numbers — RUNTIME
   Đồng hồ ảo + bộ máy dựng cảnh + engine animation.
   Được nhúng vào MỌI template. Template chỉ cần khai báo bố cục (CSS/HTML).
   ============================================================================
   Nguyên lý cốt lõi (giữ từ hệ thống cũ, đã được kiểm chứng):
     Toàn bộ nguồn thời gian của trình duyệt bị ghi đè bằng một đồng hồ ảo.
     Renderer tua đồng hồ tới đúng t = frame/fps rồi chụp ảnh.
     → Không rớt frame, deterministic, máy chậm chỉ render lâu hơn.
   ========================================================================== */
(function () {
  "use strict";

  // ── 1. VIRTUAL TIME SHIM ────────────────────────────────────────────────
  // Phải chạy TRƯỚC mọi script khác (renderer tiêm qua add_init_script).
  if (!window.__vt) {
    (function () {
      let vnow = 0;
      const dateBase = Date.now();
      const _RealDate = Date;
      performance.now = () => vnow;
      Date.now = () => dateBase + vnow;

      let rafId = 0;
      let rafQ = new Map();
      window.requestAnimationFrame = (cb) => { const id = ++rafId; rafQ.set(id, cb); return id; };
      window.cancelAnimationFrame = (id) => { rafQ.delete(id); };

      let tId = 0;
      const timers = new Map();
      window.setTimeout = (cb, ms, ...a) => {
        const id = ++tId; timers.set(id, { cb, due: vnow + Math.max(0, +ms || 0), args: a, iv: 0 }); return id;
      };
      window.setInterval = (cb, ms, ...a) => {
        const id = ++tId; const iv = Math.max(1, +ms || 0);
        timers.set(id, { cb, due: vnow + iv, args: a, iv }); return id;
      };
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
            for (const [id, t] of timers) {
              if (t.due <= ms && (!next || t.due < next.due)) { next = t; nid = id; }
            }
            if (!next) break;
            vnow = next.due;
            if (next.iv) next.due += next.iv; else timers.delete(nid);
            try { typeof next.cb === "function" ? next.cb(...next.args) : (0, eval)(String(next.cb)); }
            catch (e) { console.error(e); }
          }
          vnow = ms;
          const q = rafQ; rafQ = new Map();
          for (const cb of q.values()) { try { cb(vnow); } catch (e) { console.error(e); } }
          seekAnimations();
          seekAnimations(); // animations created by the callbacks above
          return vnow;
        }
      };
    })();
  }

  // ── 2. UTILITIES ────────────────────────────────────────────────────────
  const esc = (s) => (s === undefined || s === null) ? "" : String(s);

  // *highlight* → <b>
  const hl = (t) => esc(t).replace(/\*([^*]+)\*/g, '<b class="hl">$1</b>');

  // Định dạng số: 1234567 → "1,234,567"
  function fmtNum(n) {
    const parts = String(n).split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
  }

  // Đếm số từ giá trị chuỗi, giữ tiền tố/hậu tố ("$1,200", "27.8%", "10¹⁰⁰")
  function animateNumber(el, raw, dur) {
    if (!el || raw === undefined || raw === null) return;
    const str = String(raw);
    // bắt: prefix | số | suffix ; chấp nhận số mũ unicode ở suffix
    const m = str.match(/^([^0-9+\-]*?)(-?\d+(?:,\d{3})*(?:\.\d+)?)(.*)$/);
    if (!m) { el.textContent = str; return; }
    const pre = m[1], numPart = m[2], suf = m[3];

    // Biểu thức toán học hoặc chứa toán tử → đứng yên, không đếm để tránh làm sai nghĩa
    if (/(=|[+×÷/^&|⟩]|\.\.\.)/.test(str)) { el.textContent = str; return; }

    // Số đặc biệt tạo tương phản tức thì
    if (str === "1,000,000,000" || str === "000,000,000") { el.textContent = str; return; }

    // Năm 4 chữ số trong khoảng hợp lý → đứng yên, không đếm
    if (/^\d{4}$/.test(numPart) && +numPart > 1500 && +numPart < 2200) { el.textContent = str; return; }

    const hasComma = numPart.indexOf(",") >= 0;
    const dec = (numPart.split(".")[1] || "").length;
    const target = parseFloat(numPart.replace(/,/g, ""));
    // Số <= 1 hoặc = 0 → không đếm từ 0, giữ nguyên để hiển thị số 1 ngay lập tức
    if (isNaN(target) || Math.abs(target) <= 1) { el.textContent = str; return; }

    const t0 = performance.now();
    (function tick(now) {
      const p = Math.min(1, (now - t0) / dur);
      const e = 1 - Math.pow(1 - p, 3); // easeOutCubic
      let f = (target * e).toFixed(dec);
      if (hasComma) f = fmtNum(f);
      el.textContent = pre + f + suf;
      if (p < 1) requestAnimationFrame(tick);
      else el.textContent = str; // kết thúc chính xác bằng giá trị gốc
    })(t0);
  }

  // ── 3. ANIMATION ENGINE ─────────────────────────────────────────────────
  // Một timeline animation tự viết, TUA ĐƯỢC (seekable) — thay cho GSAP ở chế độ
  // no-dep, và là lớp nền để GSAP (nếu có) ghi đè.
  //
  // Mỗi "clip" là { el, from, to, start, dur, ease, prop, onUpdate }
  // setTime(t) áp dụng mọi clip tại thời điểm t → hoàn toàn deterministic.
  function makeEase(name) {
    switch (name) {
      case "linear":   return (x) => x;
      case "easeIn":   return (x) => x * x;
      case "easeOut":  return (x) => 1 - Math.pow(1 - x, 3);
      case "easeInOut":return (x) => x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
      case "backOut":  return (x) => 1 + 2.7 * Math.pow(x - 1, 3) + 1.7 * Math.pow(x - 1, 2);
      case "expo":     return (x) => x === 1 ? 1 : 1 - Math.pow(2, -10 * x);
      case "overshoot":return (x) => {
        const c = 1.70158 * 1.525, c3 = c + 1;
        return 1 + c3 * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2);
      };
      default:         return (x) => 1 - Math.pow(1 - x, 3);
    }
  }

  class Anim {
    constructor() { this.clips = []; this.duration = 0; }

    /** Thêm clip hoạt hoá. props: {opacity:[0,1], y:[24,0], scale:[.96,1], blur:[8,0]} */
    add(el, props, opts) {
      if (!el) return this;
      const o = opts || {};
      const start = o.at || 0;
      const dur = o.dur || 0.5;
      const ease = makeEase(o.ease || "easeOut");
      for (const k in props) {
        this.clips.push({ el, prop: k, from: props[k][0], to: props[k][1], start, dur, ease });
      }
      this.duration = Math.max(this.duration, start + dur);
      return this;
    }

    /** Clip tuỳ ý: onUpdate(p, el) */
    addFn(el, dur, ease, onUpdate, at) {
      this.clips.push({ el, prop: "__fn", from: 0, to: 1, start: at || 0,
                        dur: dur || 0.5, ease: makeEase(ease || "easeOut"), onUpdate });
      this.duration = Math.max(this.duration, (at || 0) + (dur || 0.5));
      return this;
    }

    /** Stagger nhiều element */
    stagger(els, props, opts) {
      const o = opts || {};
      const step = o.each || 0.09;
      Array.from(els).forEach((el, i) => {
        this.add(el, props, Object.assign({}, o, { at: (o.at || 0) + i * step }));
      });
      return this;
    }

    /** Áp dụng trạng thái tại thời điểm t (giây). Đây là hàm thuần của t. */
    setTime(t) {
      for (const c of this.clips) {
        const raw = c.dur <= 0 ? 1 : Math.max(0, Math.min(1, (t - c.start) / c.dur));
        const p = c.ease(raw);
        const v = c.from + (c.to - c.from) * p;
        const el = c.el;
        if (!el) continue;
        if (c.prop === "__fn") { c.onUpdate(p, el); continue; }
        switch (c.prop) {
          case "opacity": el.style.opacity = v; break;
          case "y":       el.style.transform = (el.style.transform.replace(/translateY\([^)]*\)\s*/, "") + ` translateY(${v}px)`).trim(); break;
          case "x":       el.style.transform = (el.style.transform.replace(/translateX\([^)]*\)\s*/, "") + ` translateX(${v}px)`).trim(); break;
          case "scale":   el.style.transform = (el.style.transform.replace(/scale\([^)]*\)\s*/, "") + ` scale(${v})`).trim(); break;
          case "blur":    el.style.filter = `blur(${v}px)`; break;
          case "clip":    el.style.clipPath = `inset(0 ${100 - v * 100}% 0 0)`; break;
          case "wipe":    el.style.clipPath = `inset(0 0 ${100 - v * 100}% 0)`; break;
          case "width":   el.style.width = v + "%"; break;
          case "height":  el.style.height = v + "%"; break;
          case "rotate":  el.style.transform = (el.style.transform.replace(/rotate\([^)]*\)\s*/, "") + ` rotate(${v}deg)`).trim(); break;
        }
      }
    }
  }

  // ── 4. TEMPLATE REGISTRY ────────────────────────────────────────────────
  // Template đăng ký renderer cho từng card type tại đây.
  // Registry này là cầu nối duy nhất giữa spec/component và DOM thật.
  const RENDERERS = {};

  function register(type, fn) { RENDERERS[type] = fn; }

  // ── 5. SFX / TRANSITION tables ──────────────────────────────────────────
  const TRANSITIONS = ["wipe", "slit", "iris", "fade", "glitch", "none"];

  // ── 6. EXPORT ───────────────────────────────────────────────────────────
  window.BTN = {
    esc, hl, fmtNum, animateNumber,
    Anim, makeEase,
    RENDERERS, register,
    TRANSITIONS,
    version: "2.0.0"
  };
})();