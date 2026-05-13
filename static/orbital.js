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

    // Background
    ctx.fillStyle = '#f8f9fb';
    ctx.fillRect(0, 0, W, H);

    // ── Blueprint axis lines ──
    ctx.save();
    ctx.setLineDash([4, 6]);
    ctx.strokeStyle = BORDER;
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, H); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(W, cy); ctx.stroke();
    // diagonal guides
    ctx.setLineDash([3, 8]);
    ctx.strokeStyle = '#d4d8e2';
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(W, H); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(W, 0); ctx.lineTo(0, H); ctx.stroke();
    ctx.restore();

    // ── Concentric orbit rings ──
    var radii = [62, 104, 148, 192, 228];
    radii.forEach(function (r, i) {
      ctx.save();
      ctx.strokeStyle = i === 2 ? BLUE_MUTED : BORDER;
      ctx.lineWidth = i === 2 ? 1.2 : 0.8;
      ctx.globalAlpha = i === 2 ? 0.5 : 0.6;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    });

    // ── Zodiac tick marks on outermost ring ──
    ctx.save();
    ctx.strokeStyle = BORDER;
    ctx.lineWidth = 0.8;
    for (var i = 0; i < 12; i++) {
      var angle = (i / 12) * Math.PI * 2 - Math.PI / 2;
      var innerR = 228;
      var outerR = 240;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(angle) * innerR, cy + Math.sin(angle) * innerR);
      ctx.lineTo(cx + Math.cos(angle) * outerR, cy + Math.sin(angle) * outerR);
      ctx.stroke();
    }
    ctx.restore();

    // ── Central hexagonal polygon ──
    drawPolygon(ctx, cx, cy, 6, 48, BLUE, 0.18, 1.2);
    drawPolygon(ctx, cx, cy, 6, 32, BLUE, 0.10, 0.9);

    // ── Sun center ──
    ctx.save();
    var sunGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 14);
    sunGrad.addColorStop(0, '#fffbe6');
    sunGrad.addColorStop(1, '#f5c842');
    ctx.fillStyle = sunGrad;
    ctx.beginPath();
    ctx.arc(cx, cy, 10, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#e0a800';
    ctx.lineWidth = 1;
    ctx.stroke();
    ctx.restore();

    // ── Planet nodes ──
    var planets = [
      { r: 62,  angle: -0.8,  label: '☿', color: '#9b9b9b', size: 5 },
      { r: 104, angle: 0.6,   label: '♀', color: '#c48a3a', size: 6 },
      { r: 148, angle: -2.1,  label: '♂', color: '#c04040', size: 5 },
      { r: 192, angle: 1.4,   label: '♃', color: '#7a5c2e', size: 8 },
      { r: 228, angle: -1.0,  label: '♄', color: '#5c6e7a', size: 7 },
    ];

    planets.forEach(function (p) {
      var px = cx + Math.cos(p.angle) * p.r;
      var py = cy + Math.sin(p.angle) * p.r;

      // orbit-to-node connector line
      ctx.save();
      ctx.strokeStyle = BORDER;
      ctx.lineWidth = 0.6;
      ctx.setLineDash([2, 5]);
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(px, py);
      ctx.stroke();
      ctx.restore();

      // node
      ctx.save();
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(px, py, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.restore();

      // symbol label
      ctx.save();
      ctx.font = 'bold 11px sans-serif';
      ctx.fillStyle = TEXT;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(p.label, px + (px > cx ? 14 : -14), py + (py > cy ? 14 : -14));
      ctx.restore();
    });

    // ── Floating formula labels ──
    var formulas = [
      { x: 0.08, y: 0.12, text: 'θ = 360° × d / 2πr' },
      { x: 0.54, y: 0.08, text: 'T = 2π√(a³ / GM)' },
      { x: 0.06, y: 0.82, text: 'R = a/b = Φ ≈ 1.618' },
      { x: 0.52, y: 0.88, text: 'V = Σ digits / n' },
    ];

    formulas.forEach(function (f) {
      var fx = f.x * W;
      var fy = f.y * H;
      ctx.save();
      ctx.font = '10px Menlo, Consolas, monospace';
      ctx.fillStyle = BLUE;
      ctx.globalAlpha = 0.65;
      ctx.fillText(f.text, fx, fy);
      ctx.restore();
    });

    // ── Annotation chips ──
    var chips = [
      { x: 0.60, y: 0.35, text: 'Orbital Mechanics' },
      { x: 0.05, y: 0.50, text: 'Harmonic Ratio' },
      { x: 0.60, y: 0.62, text: 'Degrees of Influence' },
    ];

    chips.forEach(function (c) {
      var chipX = c.x * W;
      var chipY = c.y * H;
      ctx.save();
      ctx.font = '600 9px Inter, sans-serif';
      ctx.fillStyle = TEXT_3;
      var metrics = ctx.measureText(c.text);
      var pad = 6;
      // pill background
      ctx.fillStyle = '#fff';
      ctx.strokeStyle = BORDER;
      ctx.lineWidth = 1;
      roundRect(ctx, chipX - pad, chipY - 9, metrics.width + pad * 2, 16, 4);
      ctx.fill(); ctx.stroke();
      ctx.fillStyle = TEXT_3;
      ctx.font = '600 9px Inter, sans-serif';
      ctx.textBaseline = 'middle';
      ctx.fillText(c.text, chipX, chipY - 1);
      ctx.restore();
    });

    // ── Degree scale arc label ──
    ctx.save();
    ctx.font = '9px Menlo, Consolas, monospace';
    ctx.fillStyle = BLUE_MUTED;
    ctx.globalAlpha = 0.6;
    var labelAngle = -Math.PI * 0.25;
    ctx.fillText('λ →', cx + Math.cos(labelAngle) * 108, cy + Math.sin(labelAngle) * 108);
    ctx.restore();
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
    img.width = canvas.width;
    img.height = canvas.height;
    img.alt = canvas.getAttribute('aria-label') || altText || 'Chart';
    img.className = canvas.className;
    img.id = canvas.id;
    img.style.display = 'block';
    img.style.maxWidth = '100%';

    parent.replaceChild(img, canvas);
  }

  // Expose to global scope
  window.drawOrbitalDiagram = drawOrbitalDiagram;
  window.drawDonut          = drawDonut;
  window.drawEclipticRing   = drawEclipticRing;

}());
