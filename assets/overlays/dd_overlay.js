/**
 * dd_overlay.js — Lớp phủ hiệu ứng thị giác dùng chung (Điểm Đọc)
 * ================================================================
 * Tự chứa 100%, không phụ thuộc thư viện ngoài.
 * Kết xuất hạt lấp lánh (sparkles), bụi sáng (embers), quét sáng (light sweep),
 * và vignette bảo vệ vùng nhìn, phủ TRÊN ảnh và DƯỚI chữ với 'lighter' blend.
 * 
 * Tính định trước (Deterministic):
 * - PRNG mulberry32 có seed.
 * - Vị trí và độ mờ của hạt là hàm toán học của thời gian toàn video t_global.
 * - Hỗ trợ global_offset_sec để hạt chuyển động liền mạch qua điểm cắt video.
 */

(function(global) {
  'use strict';

  function mulberry32(a) {
    return function() {
      var t = a += 0x6D2B79F5;
      t = Math.imul(t ^ t >>> 15, t | 1);
      t ^= t + Math.imul(t ^ t >>> 7, t | 61);
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function createParticleSprite(color, size, isSparkle) {
    const sCanvas = document.createElement("canvas");
    sCanvas.width = size * 2;
    sCanvas.height = size * 2;
    const sCtx = sCanvas.getContext("2d");
    const center = size;

    if (isSparkle) {
      const grad = sCtx.createRadialGradient(center, center, 0, center, center, size);
      grad.addColorStop(0, "#FFFFFF");
      grad.addColorStop(0.35, color);
      grad.addColorStop(1, "rgba(0,0,0,0)");
      sCtx.fillStyle = grad;
      sCtx.beginPath();
      sCtx.arc(center, center, size, 0, Math.PI * 2);
      sCtx.fill();

      // 4-point star spike
      sCtx.strokeStyle = "rgba(255,255,255,0.85)";
      sCtx.lineWidth = 1.2;
      sCtx.beginPath();
      sCtx.moveTo(center - size * 0.75, center);
      sCtx.lineTo(center + size * 0.75, center);
      sCtx.moveTo(center, center - size * 0.75);
      sCtx.lineTo(center, center + size * 0.75);
      sCtx.stroke();
    } else {
      const grad = sCtx.createRadialGradient(center, center, 0, center, center, size);
      grad.addColorStop(0, "#FFFFFF");
      grad.addColorStop(0.3, color);
      grad.addColorStop(0.7, color);
      grad.addColorStop(1, "rgba(0,0,0,0)");
      sCtx.fillStyle = grad;
      sCtx.beginPath();
      sCtx.arc(center, center, size, 0, Math.PI * 2);
      sCtx.fill();
    }
    return sCanvas;
  }

  function initOverlay(canvas, cfgOrOpts, maybeOpts) {
    if (!canvas) return null;
    const ctx = canvas.getContext("2d");
    const CW = canvas.width;
    const CH = canvas.height;
    
    let cfg = cfgOrOpts || {};
    let opts = maybeOpts || {};
    if (cfgOrOpts && (cfgOrOpts.config || cfgOrOpts.seed)) {
      cfg = cfgOrOpts.config || cfgOrOpts;
      opts = cfgOrOpts;
    }

    let seedVal = 77777;
    const seedStr = String(opts.seed || "diemdoc_fx");
    for (let i = 0; i < seedStr.length; i++) {
      seedVal = ((seedVal << 5) - seedVal) + seedStr.charCodeAt(i);
      seedVal |= 0;
    }
    const rand = mulberry32(Math.abs(seedVal));

    const spCfg = (cfg && cfg.sparkles) || {};
    const emCfg = (cfg && cfg.embers) || {};
    const swCfg = (cfg && cfg.light_sweep) || {};
    const gridCfg = (cfg && cfg.grid_lines) || {};

    const SPARKLE_COUNT = spCfg.count !== undefined ? spCfg.count : 24;
    const EMBER_COUNT = emCfg.count !== undefined ? emCfg.count : 20;
    const SPARKLE_SPEED = spCfg.speed || 1.0;
    const EMBER_SPEED_Y = emCfg.speed_y || -22.0;

    const spMin = (spCfg.size_range && spCfg.size_range[0]) || 6.0;
    const spMax = (spCfg.size_range && spCfg.size_range[1]) || 12.0;
    const emMin = (emCfg.size_range && emCfg.size_range[0]) || 7.0;
    const emMax = (emCfg.size_range && emCfg.size_range[1]) || 15.0;

    // Sprite to hơn (size=26) để không bị cắt xén
    const spriteGoldSparkle = createParticleSprite("#F59E0B", 26, true);
    const spriteCyanSparkle = createParticleSprite("#06B6D4", 26, true);
    const spriteWhiteSparkle = createParticleSprite("#FFFFFF", 24, true);
    const spriteGoldEmber = createParticleSprite("#F59E0B", 24, false);
    const spriteCyanEmber = createParticleSprite("#06B6D4", 24, false);

    // Static particle definitions
    const sparkles = [];
    for (let i = 0; i < SPARKLE_COUNT; i++) {
      const cType = i % 3;
      sparkles.push({
        x0: rand() * CW,
        y0: rand() * CH,
        vx: (rand() - 0.5) * 12 * SPARKLE_SPEED,
        vy: (rand() - 0.5) * 8 * SPARKLE_SPEED,
        size: spMin + rand() * (spMax - spMin),
        freq: 1.5 + rand() * 2.5,
        phase: rand() * Math.PI * 2,
        sprite: cType === 0 ? spriteGoldSparkle : (cType === 1 ? spriteCyanSparkle : spriteWhiteSparkle)
      });
    }

    const embers = [];
    for (let i = 0; i < EMBER_COUNT; i++) {
      const cType = i % 2;
      embers.push({
        x0: rand() * CW,
        y0: rand() * CH,
        vx: (rand() - 0.5) * 10,
        vy: EMBER_SPEED_Y + (rand() - 0.5) * 8,
        wobbleAmp: 12 + rand() * 16,
        wobbleFreq: 0.8 + rand() * 1.5,
        wobblePhase: rand() * Math.PI * 2,
        size: emMin + rand() * (emMax - emMin),
        sprite: cType === 0 ? spriteGoldEmber : spriteCyanEmber
      });
    }

    const bursts = [];

    // Center area protection coordinates (where player faces usually appear)
    const centerX = CW * 0.5;
    const centerY = CH * (CW > CH ? 0.46 : 0.48);
    const radX = CW * 0.36;
    const radY = CH * (CW > CH ? 0.32 : 0.28);

    function getCenterAttenuation(x, y) {
      // Calculate normalized elliptical distance from center
      const dx = (x - centerX) / radX;
      const dy = (y - centerY) / radY;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 1.0) {
        // Smooth ease: darker at center (0.28), ramping up to 1.0 at border
        return 0.28 + 0.72 * (dist * dist);
      }
      return 1.0;
    }

    return {
      update(sec, globalOffsetSec) {
        const t = sec + (globalOffsetSec || 0.0);
        ctx.clearRect(0, 0, CW, CH);

        // Cyber grid subtle lines
        if (gridCfg.enabled !== false) {
          ctx.save();
          ctx.strokeStyle = "rgba(6, 182, 212, 0.08)";
          ctx.lineWidth = 1;
          const gridSpd = gridCfg.speed || 6.0;
          const stepY = CW > CH ? 60 : 70;
          const yOffset = (t * gridSpd) % stepY;
          ctx.beginPath();
          for (let y = yOffset; y < CH; y += stepY) {
            ctx.moveTo(0, y);
            ctx.lineTo(CW, y);
          }
          ctx.stroke();
          ctx.restore();
        }

        // Light sweep
        if (swCfg.enabled !== false) {
          const sweepInterval = swCfg.interval_sec || 7.0;
          const sweepDur = swCfg.duration_sec || 1.8;
          const cycleT = t % sweepInterval;
          if (cycleT < sweepDur) {
            const p = cycleT / sweepDur;
            const sweepX = -CW * 0.3 + p * (CW * 1.6);
            ctx.save();
            ctx.translate(sweepX, CH / 2);
            ctx.rotate((swCfg.angle_deg || 35) * Math.PI / 180);
            const sweepGrad = ctx.createLinearGradient(-120, 0, 120, 0);
            sweepGrad.addColorStop(0, "rgba(245, 158, 11, 0)");
            sweepGrad.addColorStop(0.5, swCfg.color || "rgba(245, 158, 11, 0.10)");
            sweepGrad.addColorStop(1, "rgba(245, 158, 11, 0)");
            ctx.fillStyle = sweepGrad;
            ctx.fillRect(-120, -CH * 1.5, 240, CH * 3);
            ctx.restore();
          }
        }

        // Composite mode: lighter so particles glow over photos
        ctx.save();
        ctx.globalCompositeOperation = "lighter";

        // Embers
        if (emCfg.enabled !== false) {
          for (let i = 0; i < embers.length; i++) {
            const eb = embers[i];
            let x = (eb.x0 + eb.vx * t + eb.wobbleAmp * Math.sin(eb.wobbleFreq * t + eb.wobblePhase)) % CW;
            if (x < 0) x += CW;
            let y = (eb.y0 + eb.vy * t) % CH;
            if (y < 0) y += CH;

            const atten = getCenterAttenuation(x, y);
            const baseAlpha = (emCfg.opacity || 0.75) * (0.4 + 0.6 * (Math.sin(1.2 * t + eb.wobblePhase) * 0.5 + 0.5));
            ctx.globalAlpha = baseAlpha * atten;
            ctx.drawImage(eb.sprite, x - eb.size / 2, y - eb.size / 2, eb.size, eb.size);
          }
        }

        // Sparkles
        if (spCfg.enabled !== false) {
          for (let i = 0; i < sparkles.length; i++) {
            const sp = sparkles[i];
            let x = (sp.x0 + sp.vx * t) % CW;
            if (x < 0) x += CW;
            let y = (sp.y0 + sp.vy * t) % CH;
            if (y < 0) y += CH;

            const atten = getCenterAttenuation(x, y);
            const sinVal = Math.sin(sp.freq * t + sp.phase);
            const baseAlpha = (spCfg.opacity || 0.85) * (0.2 + 0.8 * (sinVal * 0.5 + 0.5));
            ctx.globalAlpha = baseAlpha * atten;
            ctx.drawImage(sp.sprite, x - sp.size / 2, y - sp.size / 2, sp.size, sp.size);
          }
        }

        // Keyword Burst Sparkles
        for (let b = 0; b < bursts.length; b++) {
          const bt = bursts[b].time;
          const delta = sec - bt;
          if (delta >= 0 && delta <= 0.65) {
            const burstProg = delta / 0.65;
            const bAlpha = (1.0 - burstProg) * 0.95;
            ctx.globalAlpha = bAlpha;
            const ox = bursts[b].x || (CW / 2);
            const oy = bursts[b].y || (CW > CH ? CH - 70 : CH - 240);
            const count = 8;
            for (let k = 0; k < count; k++) {
              const ang = (k / count) * Math.PI * 2;
              const dist = 25 + burstProg * 130;
              const bx = ox + Math.cos(ang) * dist;
              const by = oy + Math.sin(ang) * dist * 0.6;
              ctx.drawImage(spriteGoldSparkle, bx - 8, by - 8, 16, 16);
            }
          }
        }

        ctx.restore();
      },

      addBurst(time, x, y) {
        bursts.push({ time, x, y });
      }
    };
  }

  let activeInstance = null;

  global.DDOverlay = {
    init: function(canvas, cfgOrOpts, maybeOpts) {
      activeInstance = initOverlay(canvas, cfgOrOpts, maybeOpts);
      return activeInstance;
    },
    update: function(sec, offset) {
      if (activeInstance) activeInstance.update(sec, offset);
    },
    addBurst: function(time, x, y) {
      if (activeInstance) activeInstance.addBurst(time, x, y);
    }
  };

})(typeof window !== 'undefined' ? window : this);
