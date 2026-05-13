/* ============================================================
   Natal Numbers — Canvas Visualizations
   1. drawOrbitalDiagram(canvasId)   — hero orbital mechanics diagram
   2. drawDonut(canvasId, segments)  — influence distribution donut
   3. drawEclipticRing(canvasId, planets) — ecliptic position ring
============================================================ */

(function () {
  'use strict';

  var BLUE        = '#1a4fd6';
  var BLUE_MUTED  = '#6b8de3';
  var BLUE_LIGHT  = '#2d63f5';
  var BLUE_TINT   = '#eef2fd';
  var BORDER      = '#e2e5ea';
  var TEXT        = '#1a1d23';
  var TEXT_3      = '#7a8394';

  /* ──────────────────────────────────────────────
     1. ORBITAL DIAGRAM
     Blueprint-style: concentric rings, planet nodes,
     axis lines, central polygon, formula labels.
  ────────────────────────────────────────────── */
  function drawOrbitalDiagram(canvasId) {
    var canvas = document.getElementById(canvasId);
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var W = canvas.width;
    var H = canvas.height;
    var cx = W / 2;
    var cy = H / 2;

    ctx.clearRect(0, 0, W, H);

    // ── Radial gradient background ──
    var bgGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, W * 0.72);
    bgGrad.addColorStop(0, '#ffffff');
    bgGrad.addColorStop(1, '#f0f2f7');
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, W, H);

    // ── Blueprint axis lines ──
    ctx.save();
    ctx.setLineDash([4, 6]);
    ctx.strokeStyle = BORDER;
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, H); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(W, cy); ctx.stroke();
    ctx.setLineDash([3, 8]);
    ctx.strokeStyle = '#d4d8e2';
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(W, H); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(W, 0); ctx.lineTo(0, H); ctx.stroke();
    ctx.restore();

    // ── Concentric orbit rings ──
    var radii = [62, 104, 148, 192, 228];
    radii.forEach(function (r, i) {
      var isOuter = i === radii.length - 1;
      ctx.save();
      ctx.strokeStyle = isOuter ? BLUE_MUTED : BORDER;
      ctx.lineWidth   = isOuter ? 1.5 : 1;
      ctx.globalAlpha = isOuter ? 0.45 : 0.7;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    });

    // ── Zodiac tick marks on outermost ring ──
    ctx.save();
    ctx.strokeStyle = BLUE_MUTED;
    ctx.lineWidth = 1;
    ctx.globalAlpha = 0.35;
    for (var i = 0; i < 12; i++) {
      var angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(angle) * 228, cy + Math.sin(angle) * 228);
      ctx.lineTo(cx + Math.cos(angle) * 242, cy + Math.sin(angle) * 242);
      ctx.stroke();
    }
    ctx.restore();

    // ── Central hexagonal polygons ──
    drawPolygon(ctx, cx, cy, 6, 48, BLUE, 0.18, 1.2);
    drawPolygon(ctx, cx, cy, 6, 32, BLUE, 0.10, 0.9);

    // ── Sun center ──
    ctx.save();
    var sunGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 16);
    sunGrad.addColorStop(0, '#fffbe6');
    sunGrad.addColorStop(0.6, '#f5c842');
    sunGrad.addColorStop(1, '#e0a800');
    ctx.fillStyle = sunGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, 12, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#c98a00';
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.restore();

    // ── Planet nodes (no connector lines) ──
    var planets = [
      { r: 62,  angle: -0.8,  label: '☿', color: '#8a8a9a', size: 8  },
      { r: 104, angle: 0.6,   label: '♀', color: '#c48a3a', size: 9  },
      { r: 148, angle: -2.1,  label: '♂', color: '#c04040', size: 8  },
      { r: 192, angle: 1.4,   label: '♃', color: '#6b7fd4', size: 11 },
      { r: 228, angle: -1.0,  label: '♄', color: '#5c6e7a', size: 10 },
    ];

    planets.forEach(function (p) {
      var px = cx + Math.cos(p.angle) * p.r;
      var py = cy + Math.sin(p.angle) * p.r;

      // node with soft shadow ring
      ctx.save();
      ctx.beginPath();
      ctx.arc(px, py, p.size + 3, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.globalAlpha = 0.15;
      ctx.fill();
      ctx.restore();

      ctx.save();
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(px, py, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.restore();

      // symbol label -- offset outward along the planet's own angle
      var labelDist = p.r + p.size + 14;
      var lx = cx + Math.cos(p.angle) * labelDist;
      var ly = cy + Math.sin(p.angle) * labelDist;
      // keep label inside canvas bounds
      lx = Math.max(14, Math.min(W - 14, lx));
      ly = Math.max(14, Math.min(H - 14, ly));
      ctx.save();
      ctx.font = 'bold 12px sans-serif';
      ctx.fillStyle = TEXT;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(p.label, lx, ly);
      ctx.restore();
    });

    // ── Two styled formula pills (top-left, bottom-right) ──
    var formulas = [
      { x: 0.05, y: 0.10, text: 'θ = 360° × d / 2πr' },
      { x: 0.50, y: 0.91, text: 'T = 2π√(a³/GM)'     },
    ];

    formulas.forEach(function (f) {
      var fx = f.x * W;
      var fy = f.y * H;
      ctx.save();
      ctx.font = '500 10px Menlo, Consolas, monospace';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      var tw = ctx.measureText(f.text).width;
      var pad = 7;
      var ph = 18;
      roundRect(ctx, fx, fy - ph / 2, tw + pad * 2, ph, 5);
      ctx.fillStyle = BLUE_TINT;
      ctx.fill();
      ctx.strokeStyle = BLUE_MUTED;
      ctx.globalAlpha = 0.5;
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.globalAlpha = 1;
      ctx.fillStyle = BLUE;
      ctx.fillText(f.text, fx + pad, fy);
      ctx.restore();
    });

    // ── Annotation chips ──
    var chips = [
      { x: 0.60, y: 0.33, text: 'Orbital Mechanics'   },
      { x: 0.04, y: 0.50, text: 'Harmonic Ratio'       },
      { x: 0.58, y: 0.64, text: 'Degrees of Influence' },
    ];

    chips.forEach(function (c) {
      var chipX = c.x * W;
      var chipY = c.y * H;
      ctx.save();
      ctx.font = '600 10px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      var tw = ctx.measureText(c.text).width;
      var pad = 8;
      var ph = 20;
      roundRect(ctx, chipX, chipY - ph / 2, tw + pad * 2, ph, 5);
      ctx.fillStyle = '#fff';
      ctx.fill();
      ctx.strokeStyle = BORDER;
      ctx.lineWidth = 1;
      ctx.stroke();
      ctx.fillStyle = TEXT_3;
      ctx.fillText(c.text, chipX + pad, chipY);
      ctx.restore();
    });

    stabilizeCanvasDisplay(canvas, 'Orbital mechanics diagram');
  }

  /* ──────────────────────────────────────────────
     2. DONUT CHART
  ────────────────────────────────────────────── */
  function drawDonut(canvasId, segments) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || typeof canvas.getContext !== 'function') return;
    var ctx = canvas.getContext('2d');
    var W = canvas.width;
    var H = canvas.height;
    var cx = W / 2;
    var cy = H / 2;
    var outerR = Math.min(W, H) / 2 - 8;
    var innerR = outerR * 0.56;

    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#fff';
    ctx.fillRect(0, 0, W, H);

    var validSegments = (segments || []).map(function (seg) {
      return {
        label: seg.label,
        value: Number(seg.value),
        color: seg.color || BLUE
      };
    }).filter(function (seg) {
      return Number.isFinite(seg.value) && seg.value > 0;
    });

    var total = validSegments.reduce(function (s, seg) { return s + seg.value; }, 0);
    if (total === 0) return;

    var startAngle = -Math.PI / 2;
    var gap = 0.03;

    validSegments.forEach(function (seg) {
      var sweep = (seg.value / total) * Math.PI * 2 - gap;
      ctx.save();
      ctx.fillStyle = seg.color;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(startAngle + gap / 2) * innerR,
                 cy + Math.sin(startAngle + gap / 2) * innerR);
      ctx.arc(cx, cy, outerR, startAngle + gap / 2, startAngle + sweep + gap / 2);
      ctx.arc(cx, cy, innerR, startAngle + sweep + gap / 2, startAngle + gap / 2, true);
      ctx.closePath();
      ctx.fill();
      ctx.restore();
      startAngle += sweep + gap;
    });

    // Center label
    ctx.save();
    ctx.font = 'bold 13px Inter, sans-serif';
    ctx.fillStyle = TEXT;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(validSegments.length + ' Planets', cx, cy - 7);
    ctx.font = '10px Inter, sans-serif';
    ctx.fillStyle = TEXT_3;
    ctx.fillText('analyzed', cx, cy + 9);
    ctx.restore();

    stabilizeCanvasDisplay(canvas, 'Influence distribution chart');
  }

  /* ──────────────────────────────────────────────
     3. ECLIPTIC RING (report page)
     Shows planet positions on the 360° ecliptic.
  ────────────────────────────────────────────── */
  function drawEclipticRing(canvasId, planets) {
    var canvas = document.getElementById(canvasId);
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var W = canvas.width;
    var H = canvas.height;
    var cx = W / 2;
    var cy = H / 2;
    var outerR = Math.min(W, H) / 2 - 12;
    var innerR = outerR - 18;

    ctx.clearRect(0, 0, W, H);

    // Zodiac band
    var signs = ['♈','♉','♊','♋','♌','♍','♎','♏','♐','♑','♒','♓'];
    for (var i = 0; i < 12; i++) {
      var a1 = (i / 12) * Math.PI * 2 - Math.PI / 2;
      var a2 = ((i + 1) / 12) * Math.PI * 2 - Math.PI / 2;
      ctx.save();
      ctx.fillStyle = i % 2 === 0 ? '#f5f6f8' : '#eef0f4';
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, outerR, a1, a2);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      // divider tick
      ctx.save();
      ctx.strokeStyle = BORDER;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a1) * innerR, cy + Math.sin(a1) * innerR);
      ctx.lineTo(cx + Math.cos(a1) * outerR, cy + Math.sin(a1) * outerR);
      ctx.stroke();
      ctx.restore();

      // sign glyph
      var midAngle = ((i + 0.5) / 12) * Math.PI * 2 - Math.PI / 2;
      var glyphR = (innerR + outerR) / 2;
      ctx.save();
      ctx.font = '10px sans-serif';
      ctx.fillStyle = TEXT_3;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(signs[i], cx + Math.cos(midAngle) * glyphR, cy + Math.sin(midAngle) * glyphR);
      ctx.restore();
    }

    // Inner circle (black background)
    ctx.save();
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(cx, cy, innerR, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = BORDER;
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.restore();

    // Planet markers
    (planets || []).forEach(function (p) {
      var lam = typeof p.lam === 'number'
        ? p.lam
        : parseFloat(String(p.longitude || '0').replace('°', '')) || 0;
      var angle = (lam / 360) * Math.PI * 2 - Math.PI / 2;
      var markerR = (innerR + outerR) / 2;

      ctx.save();
      ctx.fillStyle = p.color || BLUE;
      ctx.beginPath();
      ctx.arc(
        cx + Math.cos(angle) * markerR,
        cy + Math.sin(angle) * markerR,
        6, 0, Math.PI * 2
      );
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.restore();

      // Label inside
      ctx.save();
      ctx.font = 'bold 8px Inter, sans-serif';
      ctx.fillStyle = '#fff';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(p.glyph || (p.name ? p.name[0] : '?'),
        cx + Math.cos(angle) * markerR,
        cy + Math.sin(angle) * markerR);
      ctx.restore();
    });

    // Center text
    ctx.save();
    ctx.font = 'bold 11px Inter, sans-serif';
    ctx.fillStyle = TEXT;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Ecliptic', cx, cy - 7);
    ctx.font = '9px Inter, sans-serif';
    ctx.fillStyle = TEXT_3;
    ctx.fillText('360°', cx, cy + 8);
    ctx.restore();

    stabilizeCanvasDisplay(canvas, 'Ecliptic position chart');
  }

  /* ──────────────────────────────────────────────
     Helpers
  ────────────────────────────────────────────── */
  function drawPolygon(ctx, cx, cy, sides, r, color, alpha, lw) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = lw;
    ctx.globalAlpha = alpha;
    ctx.beginPath();
    for (var i = 0; i < sides; i++) {
      var angle = (i / sides) * Math.PI * 2 - Math.PI / 2;
      if (i === 0) ctx.moveTo(cx + Math.cos(angle) * r, cy + Math.sin(angle) * r);
      else         ctx.lineTo(cx + Math.cos(angle) * r, cy + Math.sin(angle) * r);
    }
    ctx.closePath();
    ctx.stroke();
    ctx.restore();
  }

  function roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.arcTo(x + w, y, x + w, y + r, r);
    ctx.lineTo(x + w, y + h - r);
    ctx.arcTo(x + w, y + h, x + w - r, y + h, r);
    ctx.lineTo(x + r, y + h);
    ctx.arcTo(x, y + h, x, y + h - r, r);
    ctx.lineTo(x, y + r);
    ctx.arcTo(x, y, x + r, y, r);
    ctx.closePath();
  }

  function stabilizeCanvasDisplay(canvas, altText) {
    var parent = canvas.parentNode;
    if (!parent) return;

    var img = document.createElement('img');
    img.src = canvas.toDataURL('image/png');
    img.alt = canvas.getAttribute('aria-label') || altText || 'Chart';
    img.className = canvas.className;
    img.id = canvas.id;
    img.style.display = 'block';
    img.style.width = '100%';
    img.style.height = 'auto';

    parent.replaceChild(img, canvas);
  }

  // Expose to global scope
  window.drawOrbitalDiagram = drawOrbitalDiagram;
  window.drawDonut          = drawDonut;
  window.drawEclipticRing   = drawEclipticRing;

}());
