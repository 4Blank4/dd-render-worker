/* ============================================================================
   By The Numbers — CARDS
   Thư viện renderer cho mọi card type. Đăng ký vào BTN.RENDERERS.
   Mỗi renderer nhận (card, ctx) và trả về HTML string.
   Phụ thuộc: _runtime.js
   ============================================================================
   Đây là "design system primitives" — tách khỏi template để:
     - Mọi brand dùng chung một bộ component, chỉ khác CSS token.
     - Thêm card mới = thêm 1 hàm, không đụng template.
   ========================================================================== */
(function () {
  "use strict";
  const B = window.BTN;
  const R = B.register;

  const acc = (a) => `accent-${a || "accent"}`;
  const cnt = (v) => `data-count-target="${B.esc(v)}"`;

  /* ── SLOTS: gợi ý vị trí lưới cho từng type (director dùng để xếp hàng) ── */
  B.SLOTS = {
    "title-banner": "full", "kinetic-statement": "full", "stat-bento-trio": "full",
    "dual-number-clash": "full", "comparison-split": "full", "math-pipeline": "full",
    "math-equation-board": "full", "math-derivation": "full", "rank-table": "full",
    "grid-matrix": "full", "lineup-grid": "full", "three-pillars": "full",
    "giant-number-spotlight": "half", "stat-callout": "half", "portrait-hero-card": "half",
    "photo-card": "half", "fact-list": "half", "quote-card": "half",
    "bar-chart": "half", "line-chart": "half", "scale-ladder": "half",
    "progress-ring": "third"
  };

  /* ══════════════════ KHUNG & NHỊP ══════════════════ */

  R("title-banner", (c, ctx) => `
    <div class="card card-banner ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="title-banner">
      <div class="bn-kicker">${B.esc(c.tag || c.kicker || "BY THE NUMBERS")}</div>
      <div class="bn-headline">${B.hl(c.title)}</div>
      ${c.pill_number ? `<div class="bn-pill">${B.esc(c.pill_number)}</div>` : ""}
    </div>`);

  R("kinetic-statement", (c, ctx) => {
    const lines = (c.lines || []).map((ln, i) =>
      `<div class="ks-line" data-line="${i}">${B.hl(ln)}</div>`).join("");
    return `<div class="card card-kinetic ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="kinetic-statement">
      <div class="ks-wrap">${lines}${c.sub ? `<div class="ks-sub">${B.hl(c.sub)}</div>` : ""}</div>
    </div>`;
  });

  /* ══════════════════ CON SỐ ══════════════════ */

  R("giant-number-spotlight", (c, ctx) => {
    const val = c.value !== undefined ? c.value : c.number;
    // Số càng dài thì cỡ chữ càng nhỏ, để không tràn khung.
    const len = String(val || "").length;
    const size = len <= 3 ? 130 : len <= 5 ? 110 : len <= 8 ? 84 : len <= 12 ? 62 : 46;
    return `<div class="card card-giant ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="giant-number-spotlight">
      <div class="gt-kicker">${B.esc(c.kicker || "")}${c.badge ? `<span class="gt-badge">${B.esc(c.badge)}</span>` : ""}</div>
      <div class="gt-row">
        <div class="gt-num" style="font-size:${size}px" ${cnt(val)}>${B.esc(val)}</div>
        ${c.unit ? `<div class="gt-unit">${B.esc(c.unit)}</div>` : ""}
      </div>
      <div class="gt-bar"></div>
      ${c.description ? `<div class="gt-desc">${B.hl(c.description)}</div>` : ""}
    </div>`;
  });

  R("stat-callout", (c, ctx) => {
    const len = String(c.value || "").length;
    const size = len <= 3 ? 132 : len <= 5 ? 108 : len <= 8 ? 78 : len <= 12 ? 58 : 44;
    return `<div class="card card-callout ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="stat-callout">
      ${c.badge ? `<div class="co-badge">${B.esc(c.badge)}</div>` : ""}
      <div class="co-num" style="font-size:${size}px" ${cnt(c.value)}>${B.esc(c.value)}</div>
      ${c.unit ? `<div class="co-unit">${B.esc(c.unit)}</div>` : ""}
      ${c.subtitle ? `<div class="co-sub">${B.hl(c.subtitle)}</div>` : ""}
    </div>`;
  });

  R("stat-bento-trio", (c, ctx) => {
    const items = (c.items || []).map((it, i) => {
      const a = it.accent || ["accent", "accent2", "accent3"][i] || "accent";
      return `<div class="trio-cell ${acc(a)}">
        <div class="trio-num" ${cnt(it.value)}>${B.esc(it.value)}</div>
        <div class="trio-title">${B.esc(it.title)}</div>
        ${it.sub ? `<div class="trio-sub">${B.hl(it.sub)}</div>` : ""}
      </div>`;
    }).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="stat-bento-trio">
      <div class="trio">${items}</div></div>`;
  });

  const sideHTML = (s) => `
    <div class="cmp-side ${s.highlight ? "is-hi" : ""} ${s.valid_green ? "is-ok" : ""}">
      <div class="cmp-label">${B.esc(s.label)}</div>
      <div class="cmp-val" ${cnt(s.value)}>${B.esc(s.value)}</div>
      ${s.sub ? `<div class="cmp-sub">${B.hl(s.sub)}</div>` : ""}
    </div>`;

  R("dual-number-clash", (c, ctx) => `
    <div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="dual-number-clash">
      <div class="cmp-grid">${sideHTML(c.left || {})}
        ${c.verdict ? `<div class="cmp-verdict">${B.esc(c.verdict)}</div>` : `<div class="cmp-vs">VS</div>`}
        ${sideHTML(c.right || {})}</div>
    </div>`);

  R("comparison-split", (c, ctx) => `
    <div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="comparison-split">
      <div class="cmp-grid">${sideHTML(c.left || {})}<div class="cmp-vs">→</div>${sideHTML(c.right || {})}</div>
    </div>`);

  /* ══════════════════ TOÁN HỌC ══════════════════ */

  R("math-pipeline", (c, ctx) => {
    const rows = (c.rows || []).map((r, i) => `
      <div class="mp-row ${r.final ? "is-final" : ""}" data-row="${i}">
        <div class="mp-step">${B.esc(r.step || "")}</div>
        <div class="mp-eq">${B.esc(r.equation)}</div>
        <div class="mp-res">${B.esc(r.result)}</div>
      </div>`).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="math-pipeline">
      ${c.title ? `<div class="card-title">${B.esc(c.title)}</div>` : ""}
      <div class="mp-list">${rows}</div></div>`;
  });

  R("math-equation-board", (c, ctx) => {
    const body = (c.parts || []).map((p) => {
      if (typeof p === "string") return `<div class="me-line">${B.esc(p)}</div>`;
      return `<div class="me-line">${B.esc(p.lhs || "")} <span class="me-op">${B.esc(p.op || "=")}</span> ${B.esc(p.rhs || "")}</div>`;
    }).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="math-equation-board">
      <div class="me-board">${body}</div>
      ${c.description ? `<div class="gt-desc">${B.hl(c.description)}</div>` : ""}</div>`;
  });

  // Manim cards render ra khung trống — engine manim chồng clip lên sau.
  R("math-derivation", (c, ctx) => `
    <div class="card card-manim ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="math-derivation">
      <div class="manim-slot" data-manim="${B.esc(c.scene_class || "")}"></div>
      ${c.title ? `<div class="manim-title">${B.esc(c.title)}</div>` : ""}
    </div>`);

  /* ══════════════════ BIỂU ĐỒ (SVG — engine d3 hoặc html đều dùng) ═══════ */

  R("bar-chart", (c, ctx) => {
    const bars = c.bars || [];
    const max = Math.max(1, ...bars.map((b) => parseFloat(b.value) || 0));
    const rows = bars.map((b, i) => {
      const pct = ((parseFloat(b.value) || 0) / max) * 100;
      return `<div class="bc-row ${b.highlight ? "is-hi" : ""}">
        <div class="bc-label">${B.esc(b.label)}</div>
        <div class="bc-track"><div class="bc-fill" data-w="${pct}" style="width:0%"></div></div>
        <div class="bc-val" ${cnt(b.value)}>${B.esc(b.value)}</div>
      </div>`;
    }).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="bar-chart">
      ${c.title ? `<div class="card-title">${B.esc(c.title)}</div>` : ""}
      <div class="bc-list">${rows}</div>
      ${c.unit ? `<div class="chart-unit">${B.esc(c.unit)}</div>` : ""}</div>`;
  });

  R("line-chart", (c, ctx) => {
    const pts = (c.points || []).map((p) => ({ x: parseFloat(p.x) || 0, y: parseFloat(p.y) || 0, label: p.label }));
    if (!pts.length) return `<div class="card" data-card="${B.esc(c.id)}" data-type="line-chart"></div>`;
    const maxX = Math.max(...pts.map((p) => p.x)) || 1;
    const maxY = Math.max(...pts.map((p) => p.y)) || 1;
    const W = 100, H = 60;
    const path = pts.map((p, i) => `${i ? "L" : "M"}${(p.x / maxX) * W},${H - (p.y / maxY) * H}`).join(" ");
    const dots = pts.map((p) =>
      `<circle cx="${(p.x / maxX) * W}" cy="${H - (p.y / maxY) * H}" r="1.3" class="lc-dot"/>`).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="line-chart">
      ${c.title ? `<div class="card-title">${B.esc(c.title)}</div>` : ""}
      <svg class="lc-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">
        <path d="${path}" class="lc-path" fill="none"/>
        ${dots}
      </svg>
      ${c.unit ? `<div class="chart-unit">${B.esc(c.unit)}</div>` : ""}</div>`;
  });

  R("scale-ladder", (c, ctx) => {
    const rungs = (c.rungs || []).map((r, i) => `
      <div class="sl-rung ${r.active ? "is-active" : ""}">
        <span class="sl-label">${B.esc(r.label)}</span>
        <span class="sl-val">${B.esc(r.value)}</span>
      </div>`).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="scale-ladder">
      <div class="sl-list">${rungs}</div></div>`;
  });

  R("progress-ring", (c, ctx) => {
    const pct = Math.max(0, Math.min(100, parseFloat(c.percent) || 0));
    const dash = (pct / 100) * 251.2;
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="progress-ring">
      <svg class="pr-svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" class="pr-track"/>
        <circle cx="50" cy="50" r="40" class="pr-fill" style="stroke-dasharray:${dash} 251.2"/>
      </svg>
      <div class="pr-center">${B.esc(c.value || pct + "%")}</div>
      ${c.label ? `<div class="pr-label">${B.esc(c.label)}</div>` : ""}</div>`;
  });

  /* ══════════════════ SO SÁNH / XẾP HẠNG ══════════════════ */

  R("rank-table", (c, ctx) => {
    const rows = (c.rows || []).map((r) => `
      <div class="rt-row ${r.highlight ? "is-hi" : ""}">
        <div class="rt-rank">${B.esc(r.rank)}</div>
        <div class="rt-name">${B.esc(r.name)}</div>
        <div class="rt-val" ${cnt(r.value)}>${B.esc(r.value)}</div>
      </div>`).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="rank-table">
      ${c.title ? `<div class="card-title">${B.esc(c.title)}</div>` : ""}
      <div class="rt-list">${rows}</div></div>`;
  });

  R("grid-matrix", (c, ctx) => {
    const items = (c.items || []).map((it, i) => `
      <div class="gm-cell" data-cell="${i}">
        <div class="gm-val">${B.esc(it.value)}</div>
        ${it.hint ? `<div class="gm-hint">${B.esc(it.hint)}</div>` : ""}
        ${it.label ? `<div class="gm-label">${B.esc(it.label)}</div>` : ""}
      </div>`).join("");
    const len = (c.items || []).length;
    const cols = len === 4 ? 2 : Math.min(3, Math.max(2, len));
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="grid-matrix">
      <div class="gm-grid" style="grid-template-columns:repeat(${cols},1fr)">${items}</div></div>`;
  });

  R("lineup-grid", (c, ctx) => {
    const items = (c.heroes || []).map((h) => `
      <div class="lu-card">
        ${h.image ? `<div class="lu-img"><img src="${B.esc(h.image)}" alt=""></div>` : ""}
        <div class="lu-meta">
          <div class="lu-num" ${cnt(h.number)}>${B.esc(h.number)}</div>
          <div class="lu-name">${B.esc(h.name)}</div>
          ${h.role ? `<div class="lu-role">${B.esc(h.role)}</div>` : ""}
        </div>
      </div>`).join("");
    const cols = Math.min(4, Math.max(2, (c.heroes || []).length));
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="lineup-grid">
      ${c.kicker ? `<div class="card-title">${B.esc(c.kicker)}</div>` : ""}
      <div class="lu-grid" style="grid-template-columns:repeat(${cols},1fr)">${items}</div></div>`;
  });

  /* ══════════════════ NHÂN VẬT ══════════════════ */

  R("portrait-hero-card", (c, ctx) => `
    <div class="card card-portrait ${acc(c.accent)}" data-card="${B.esc(c.id || "portrait")}" data-type="portrait-hero-card">
      <div class="pt-imgbox">
        <img src="${B.esc(c.image)}" alt="">
        ${c.caption_tag ? `<div class="pt-tag">${B.esc(c.caption_tag)}</div>` : ""}
        ${c.stamp_number ? `<div class="pt-stamp">
          <div class="pt-stamp-label">${B.esc(c.stamp_label || "ICONIC NUMBER")}</div>
          <div class="pt-stamp-val" ${cnt(c.stamp_number)}>${B.esc(c.stamp_number)}</div></div>` : ""}
      </div>
      <div class="pt-meta">
        ${c.kicker ? `<div class="pt-kicker">${B.esc(c.kicker)}</div>` : ""}
        <div class="pt-name">${B.esc(c.name)}</div>
        ${c.subtitle ? `<div class="pt-sub">${B.hl(c.subtitle)}</div>` : ""}
        ${(c.footer_left || c.footer_right) ? `<div class="pt-bar">
          <span>${B.esc(c.footer_left || "")}</span><span>${B.esc(c.footer_right || "")}</span></div>` : ""}
      </div>
    </div>`);

  R("photo-card", (c, ctx) => `
    <div class="card card-photo ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="photo-card">
      <div class="ph-img"><img src="${B.esc(c.image)}" alt=""></div>
      <div class="ph-meta">
        ${c.kicker ? `<div class="ph-kicker">${B.esc(c.kicker)}</div>` : ""}
        ${c.title ? `<div class="ph-title">${B.esc(c.title)}</div>` : ""}
        ${c.number ? `<div class="ph-num" ${cnt(c.number)}>${B.esc(c.number)}</div>` : ""}
        ${c.caption ? `<div class="ph-cap">${B.hl(c.caption)}</div>` : ""}
        ${c.credit ? `<div class="ph-credit">${B.esc(c.credit)}</div>` : ""}
      </div></div>`);

  /* ══════════════════ VĂN BẢN ══════════════════ */

  R("fact-list", (c, ctx) => {
    const items = (c.items || []).map((it) => {
      const text = typeof it === "string" ? it : (it.text || "");
      const hi = typeof it === "object" && it.highlight;
      return `<li class="${hi ? "is-hi" : ""}">${B.hl(text)}</li>`;
    }).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="fact-list">
      ${c.title ? `<div class="card-title">${B.esc(c.title)}</div>` : ""}
      <ul class="fl-list">${items}</ul></div>`;
  });

  R("quote-card", (c, ctx) => `
    <div class="card card-quote ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="quote-card">
      <div class="qt-mark">“</div>
      <div class="qt-text">${B.hl(c.quote || c.text)}</div>
      ${c.author ? `<div class="qt-author">${B.esc(c.author)}${c.role ? ` <span class="qt-role">— ${B.esc(c.role)}</span>` : ""}</div>` : ""}
    </div>`);

  R("three-pillars", (c, ctx) => {
    const items = (c.pillars || []).map((p, i) => `
      <div class="tp-cell ${acc(["accent", "accent2", "accent3"][i] || "accent")}">
        ${p.icon ? `<div class="tp-icon">${B.esc(p.icon)}</div>` : ""}
        <div class="tp-title">${B.esc(p.title)}</div>
        ${p.sub ? `<div class="tp-sub">${B.hl(p.sub)}</div>` : ""}
      </div>`).join("");
    return `<div class="card ${acc(c.accent)}" data-card="${B.esc(c.id)}" data-type="three-pillars">
      <div class="tp-grid">${items}</div></div>`;
  });

  /* ── Hiệu ứng phụ trợ: bar-chart fill theo thời gian ── */
  // Director gọi sau khi card revealed; ở đây dùng CSS transition + set width.
  document.addEventListener("DOMContentLoaded", () => {});
  const _origUpdate = null;
})();