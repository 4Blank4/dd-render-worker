/* ============================================================================
   Điểm Đọc — DIRECTOR
   Bộ máy dựng cảnh: đọc timeline → dựng DOM → điều khiển reveal/transition/karaoke.
   Phụ thuộc: _runtime.js (window.BTN)
   ============================================================================
   Khác biệt so với hệ thống cũ:
     - Không biết gì về từng loại card cụ thể. Nó gọi BTN.RENDERERS[type].
       → Thêm card mới chỉ cần đăng ký renderer, KHÔNG sửa director.
     - Mọi chuyển động đi qua BTN.Anim (tua được) → deterministic.
     - Bố cục dùng grid 12 cột có row-span thật (hệ thống cũ không có).
   ========================================================================== */
(function () {
  "use strict";
  const B = window.BTN;

  const Director = {
    tl: null,
    words: null,
    sceneEls: [],       // DOM của từng cảnh (dựng trước toàn bộ)
    scenes: [],
    curIdx: -1,
    counted: new WeakSet(),
    anim: null,
    domain: null,       // {vw, vh, format}

    // ── KHỞI TẠO ──────────────────────────────────────────────────────────
    init(timelineData, wordTimestamps, domain) {
      this.tl = timelineData || {};
      this.words = wordTimestamps || {};
      this.domain = domain || { vw: 1080, vh: 1920, format: "short" };
      this.scenes = this.tl.scenes || [];
      this.anim = new B.Anim();

      this._renderChrome();
      this._buildAllScenes();
      this._renderSubtitleBox();

      // expose cho renderer
      window.updateAudioTime = (t) => this.update(t);
      window.loadTimelineData = (d) => { this.tl = d; };
    },

    // ── CHROME (header, logo, chapter ribbon, scene counter) ──────────────
    _renderChrome() {
      const t = this.tl;
      const q = (s) => document.querySelector(s);
      if (t.channel_name) {
        const el = q("#channel-title");
        if (el) el.innerHTML = String(t.channel_name).replace(/\bNUMBERS\b/, "<b>NUMBERS</b>");
      }
      const ribbon = q("#chapter-ribbon");
      if (ribbon && Array.isArray(t.chapter_ribbon) && t.chapter_ribbon.length) {
        ribbon.innerHTML = t.chapter_ribbon.map((ch, i) =>
          `<div class="chap-pill" data-chap="${ch.chap_id || i + 1}">
             <span>${B.esc(ch.name)}</span><span class="chap-badge">${B.esc(ch.number)}</span>
           </div>`).join("");
      }
      this._updateCounter(0);
    },

    _updateCounter(idx) {
      const el = document.querySelector("#scene-indicator");
      if (!el) return;
      const sc = this.scenes[idx] || {};
      const sid = sc.scene_id || idx + 1;
      const total = this.tl.total_scenes_count || this.scenes.length;
      el.textContent = `SCENE ${String(sid).padStart(2, "0")} / ${String(total).padStart(2, "0")}`;
    },

    _updateChapter(scene) {
      const active = scene.chapter_id || 0;
      document.querySelectorAll(".chap-pill").forEach((p) => {
        const c = parseInt(p.getAttribute("data-chap"), 10);
        p.classList.remove("active", "done");
        if (c === active) p.classList.add("active");
        else if (active > 0 && c < active) p.classList.add("done");
      });
    },

    // ── DỰNG TẤT CẢ CẢNH TRƯỚC ────────────────────────────────────────────
    // Dựng hết ngay từ đầu (ẩn) để: ảnh preload, font ổn định, đo layout chính xác.
    _buildAllScenes() {
      const layer = document.getElementById("scene-layer");
      if (!layer) return;
      layer.innerHTML = this.scenes.map((sc, i) => this._sceneHTML(sc, i)).join("");
      this.sceneEls = Array.from(layer.children);
    },

    _sceneHTML(scene, idx) {
      const portraitHTML = this._portraitHTML(scene);
      const cards = scene.cards || [];
      const bannerIdx = cards.findIndex((c) => c.type === "title-banner");
      const banner = bannerIdx >= 0 ? cards[bannerIdx] : null;

      // bố cục: banner chiếm toàn chiều ngang trên cùng, phần còn lại vào grid
      const gridCards = cards.filter((_, i) => i !== bannerIdx);
      const rows = this._layoutRows(gridCards);

      const gridHTML = rows.map((row) => {
        const rowCls = `row row-${row.length}`;
        return `<div class="${rowCls}">` + row.map(({ card, span, rowSpan }) =>
          `<div class="cell" style="grid-column:span ${span};${rowSpan > 1 ? `grid-row:span ${rowSpan};` : ""}">${
            this._cardHTML(card, idx)
          }</div>`).join("") + `</div>`;
      }).join("");

      const bannerHTML = banner
        ? `<div class="banner-slot">${this._cardHTML(banner, idx)}</div>`
        : "";

      return `<section class="scene" data-scene="${idx}" style="opacity:0;visibility:hidden">
        ${bannerHTML}
        <div class="scene-grid" style="--row-count:${Math.max(1, rows.length)}">${gridHTML}</div>
        ${portraitHTML}
      </section>`;
    },

    /**
     * Xếp card vào lưới 12 cột.
     * Card có slot="full" (span 12) chiếm trọn một hàng.
     * Các card còn lại gom lại cho tới khi đủ 12 cột.
     * Trả về [[{card, span, rowSpan}]]
     */
    _layoutRows(cards) {
      const rows = [];
      let cur = [];
      let used = 0;

      const spanOf = (c) => {
        if (c.span) return c.span;
        const slot = (B.SLOTS && B.SLOTS[c.type]) || "half";
        return { full: 12, half: 6, third: 4, any: 6 }[slot] || 6;
      };

      for (const c of cards) {
        let span = spanOf(c);
        if (span >= 12) {
          if (cur.length) { rows.push(cur); cur = []; used = 0; }
          rows.push([{ card: c, span: 12, rowSpan: 1 }]);
          continue;
        }
        if (used + span > 12) { rows.push(cur); cur = []; used = 0; }
        cur.push({ card: c, span, rowSpan: 1 });
        used += span;
        if (used === 12) { rows.push(cur); cur = []; used = 0; }
      }
      if (cur.length) rows.push(cur);

      // nếu hàng lẻ chỉ có 1 card → cho nó span đầy để không bị hụt
      rows.forEach((r) => {
        if (r.length === 1) r[0].span = 12;
      });
      return rows;
    },

    _cardHTML(card, sceneIdx) {
      const fn = B.RENDERERS[card.type];
      const accent = card.accent || "accent";
      const role = card.role || "";
      const attrs = `data-card="${B.esc(card.id)}" data-type="${B.esc(card.type)}" data-role="${role}"`;

      if (!fn) {
        // Không có renderer → hiện thông báo rõ ràng thay vì im lặng (hệ thống cũ im lặng)
        return `<div class="card card-missing accent-${accent}" ${attrs}>
          <div class="miss-title">⚠ Chưa có renderer cho type “${B.esc(card.type)}”</div>
          <div class="miss-hint">Template này chưa hỗ trợ card này. Đổi type trong timeline hoặc thêm renderer.</div>
        </div>`;
      }
      return fn(card, { sceneIdx, accent, esc: B.esc, hl: B.hl, fmtNum: B.fmtNum });
    },

    _portraitHTML(scene) {
      const p = scene.portrait;
      if (!p || !p.image) return "";
      return `<aside class="portrait-col">${B.RENDERERS["portrait-hero-card"]
        ? B.RENDERERS["portrait-hero-card"](p, { esc: B.esc, hl: B.hl })
        : ""}</aside>`;
    },

    _renderSubtitleBox() {
      if (document.getElementById("subtitle-text")) return;
      const wrap = document.createElement("div");
      wrap.className = "subtitle-container";
      wrap.innerHTML = `<div id="subtitle-text"></div>`;
      document.body.appendChild(wrap);
    },

    // ── VÒNG LẶP CHÍNH: gọi mỗi frame với thời gian tuyệt đối ────────────
    update(sec) {
      if (!this.scenes.length) return;
      const idx = this._sceneAt(sec);

      if (idx !== this.curIdx) {
        if (this.curIdx >= 0) this._hideScene(this.curIdx);
        this.curIdx = idx;
        this._showScene(idx, sec);
      }

      const scene = this.scenes[idx];
      const scStart = parseFloat(scene.start_time || scene._start_time || 0);
      const local = sec - scStart;

      this._driveCards(scene, local, sec);
      this._driveAmbient(sec);
      this._driveTransition(scene, sec);
      this._driveKaraoke(sec);
    },

    _sceneAt(sec) {
      const scenes = this.scenes;
      for (let i = 0; i < scenes.length; i++) {
        const s = scenes[i];
        const start = parseFloat(s.start_time || s._start_time || 0);
        const dur = parseFloat(s.duration || s._duration || 8);
        if (sec >= start && sec < start + dur) return i;
      }
      return scenes.length - 1;
    },

    _showScene(idx, sec) {
      const el = this.sceneEls[idx];
      if (!el) return;
      el.style.visibility = "visible";
      el.style.opacity = 1;
      this._updateCounter(idx);
      this._updateChapter(this.scenes[idx]);
      this.counted = new WeakSet(); // reset bộ đếm cho cảnh mới
    },

    _hideScene(idx) {
      const el = this.sceneEls[idx];
      if (el) { el.style.opacity = 0; el.style.visibility = "hidden"; }
    },

    // ── ĐIỀU KHIỂN REVEAL TỪNG CARD ──────────────────────────────────────
    _driveCards(scene, local, absSec) {
      const el = this.sceneEls[this.curIdx];
      if (!el) return;
      const nodes = el.querySelectorAll(".card[data-card]");
      const byId = {};
      nodes.forEach((n) => { byId[n.getAttribute("data-card")] = n; });

      (scene.cards || []).forEach((card) => {
        const node = byId[card.id];
        if (!node) return;

        // thời điểm reveal tương đối trong cảnh
        const rv = card.reveal_time !== undefined
          ? parseFloat(card.reveal_time) - parseFloat(scene.start_time || scene._start_time || 0)
          : parseFloat(card.local_delay || 0.3);

        const local_ = local;
        const revealed = local_ >= rv;

        if (revealed && !node.classList.contains("visible")) {
          node.classList.add("visible");
          // animation vào
          const a = new B.Anim();
          a.add(node, { opacity: [0, 1], y: [26, 0], scale: [0.985, 1] },
                { at: 0, dur: 0.5, ease: "easeOut" });
          // đếm số bên trong
          if (!this.counted.has(node)) {
            this.counted.add(node);
            node.querySelectorAll("[data-count-target]").forEach((n) => {
              B.animateNumber(n, n.getAttribute("data-count-target"), 650);
            });
          }
          node._anim = a;
        }

        // áp dụng animation theo thời gian (tua được)
        if (node._anim) node._anim.setTime(Math.max(0, local_ - rv));

        // glow khi vừa hiện
        const sinceReveal = local_ - rv;
        if (node.classList.contains("visible")) {
          if (sinceReveal >= 0 && sinceReveal < 1.1) node.classList.add("just-revealed");
          else node.classList.remove("just-revealed");
        }
        // ẩn trước khi tới thời điểm reveal
        if (!revealed) node.classList.remove("visible");
      });
    },

    // ── NỀN ĐỘNG ─────────────────────────────────────────────────────────
    _driveAmbient(sec) {
      const a = document.getElementById("blob-a");
      const b = document.getElementById("blob-b");
      const g = document.getElementById("bg-grid");
      if (a) a.style.transform = `translate(${1250 + Math.sin(sec / 7) * 170}px,${-200 + Math.cos(sec / 9) * 100}px)`;
      if (b) b.style.transform = `translate(${-220 + Math.cos(sec / 8) * 160}px,${540 + Math.sin(sec / 6) * 110}px)`;
      if (g) g.style.transform = `translate(${(-sec * 7) % 152}px,${(-sec * 4) % 152}px)`;
    },

    // ── CHUYỂN CẢNH ──────────────────────────────────────────────────────
    _driveTransition(scene, sec) {
      const tr = scene.transition || "wipe";
      const wipe = document.getElementById("wipe");
      const flash = document.getElementById("flash");
      const slit = document.getElementById("slit");
      const iris = document.getElementById("iris");
      if (!wipe) return;

      [wipe, slit, iris].forEach((e) => { if (e) e.style.display = "none"; });
      if (flash) flash.style.opacity = 0;

      const scStart = parseFloat(scene.start_time || scene._start_time || 0);
      const scDur = parseFloat(scene.duration || scene._duration || 8);
      const isFirst = this.curIdx === 0;
      const isLast = this.curIdx === this.scenes.length - 1;
      const el = sec - scStart;
      const elOut = scStart + scDur - sec;

      const smooth = (p) => p * p * (3 - 2 * p); // smoothstep
      const IN = { wipe: 0.55, slit: 0.5, iris: 0.55, fade: 0.35, glitch: 0.55 }[tr] || 0.5;
      const OUT = { wipe: 0.42, slit: 0.4, iris: 0.45, fade: 0.3, glitch: 0.42 }[tr] || 0.4;

      if (tr === "none") return;

      if (tr === "wipe" || tr === "glitch") {
        let x1 = null, x2 = null;
        if (el < IN && !isFirst) { const e = smooth(el / IN); x1 = Math.min(1, e * 1.25) * 100; x2 = e * 100; }
        else if (elOut < OUT && !isLast) { const e = smooth(1 - elOut / OUT); x1 = -100 + Math.min(1, e * 1.25) * 100; x2 = -100 + e * 100; }
        if (x1 !== null) {
          wipe.style.display = "block";
          wipe.querySelector(".w1").style.transform = `translateX(${x1}%)`;
          wipe.querySelector(".w2").style.transform = `translateX(${x2}%)`;
          const lbl = document.getElementById("wipe-label");
          if (lbl) lbl.textContent = scene.wipe_label || "";
        }
      } else if (tr === "slit" && slit) {
        let p = null;
        if (el < IN && !isFirst) p = el / IN;
        else if (elOut < OUT && !isLast) p = 1 - elOut / OUT;
        if (p !== null) {
          const half = smooth(p) * 100;
          slit.style.display = "block";
          slit.querySelector(".sl").style.transform = `translateX(${half - 100}%)`;
          slit.querySelector(".sr").style.transform = `translateX(${100 - half}%)`;
        }
      } else if (tr === "iris" && iris) {
        let p = null;
        if (el < IN && !isFirst) p = el / IN;
        else if (elOut < OUT && !isLast) p = 1 - elOut / OUT;
        if (p !== null) {
          const rad = (1 - smooth(p)) * 78;
          iris.style.display = "block";
          iris.style.background = `radial-gradient(circle at 50% 46%, transparent ${rad}%, #05070C ${rad + 8}%)`;
        }
      } else if (tr === "fade" && flash) {
        if (el < IN && !isFirst) flash.style.opacity = 1 - el / IN;
        else if (elOut < OUT && !isLast) flash.style.opacity = 1 - elOut / OUT;
      }
    },

    // ── KARAOKE ──────────────────────────────────────────────────────────
    _driveKaraoke(sec) {
      const box = document.getElementById("subtitle-text");
      if (!box) return;
      const scene = this.scenes[this.curIdx] || {};
      const chunks = (this.words && this.words.karaoke_chunks) || [];
      const subs = scene.subtitles || (chunks.length ? chunks : (this.tl.subtitles || []));

      let active = null;
      for (let i = 0; i < subs.length; i++) {
        const s = subs[i];
        if (sec >= (s.start - 0.06) && sec <= (s.end + 0.18)) { active = s; break; }
      }
      if (!active) { box.innerHTML = ""; return; }

      if (active.words && active.words.length) {
        box.innerHTML = active.words.map((w) => {
          let cls = "sub-word";
          if (/\d/.test(w.word)) cls += " is-number";
          if (sec >= w.start - 0.04 && sec <= w.end + 0.08) cls += " active";
          else if (sec > w.end) cls += " spoken";
          return `<span class="${cls}">${B.esc(w.word)}</span>`;
        }).join("");
      } else {
        box.textContent = active.text || "";
      }
    }
  };

  // ── BOOTSTRAP ───────────────────────────────────────────────────────────
  window.startVideo = function () {
    if (!window.VIDEO_DATA) return;
    const domain = window.VIDEO_DOMAIN || { vw: 1080, vh: 1920, format: "short" };
    Director.init(window.VIDEO_DATA, window.WORD_TIMESTAMPS, domain);
    const t0 = performance.now();
    (function loop() {
      Director.update((performance.now() - t0) / 1000.0);
      requestAnimationFrame(loop);
    })();
  };

  window.BTN.Director = Director;
})();