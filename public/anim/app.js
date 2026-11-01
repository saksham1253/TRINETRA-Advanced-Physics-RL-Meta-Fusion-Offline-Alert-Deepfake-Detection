/* TRINETRA Live Flow: timeline engine + scenes + explore mode. Plain JS, SVG, no dependencies, works offline.
   Every number is drawn from window.ANIM_DATA (built by TRINETRA/ANIM/tools/extract_animation_data.py) and carries an
   origin badge. Scenario replays are SIMULATED (seeded) and ribboned. Fusion maths mirrors ws5_fusion_rl exactly. */
'use strict';
const D = window.ANIM_DATA || {}, SCRIPT = window.ANIM_SCRIPT || {scenes: []};
const Q = new URLSearchParams(location.search);
const RECORD = Q.get('record') === '1';
const C = {bg: '#0B1238', bg2: '#101A4A', panel: '#16205A', panel2: '#1C2868', line: '#2E3D85', text: '#F4F1EA', dim: '#B9C2E3',
  ember: '#FF6B35', amber: '#FFB703', saffron: '#F57C1F', teal: '#2EC4B6', blue: '#5B8DEF', green: '#3DDC97', violet: '#A78BFA', gold: '#F2B705', red: '#F0533F'};
const ORIGIN = {REAL_RESULT: ['REAL RESULT', C.teal, ''], REAL_CONFIG: ['REAL CONFIG', C.blue, ''], PAPER: ['PUBLIC REPORT', '#FFFFFF', ''],
  ILLUSTRATIVE: ['ILLUSTRATIVE', C.amber, '6 4'], SIM: ['SIMULATED REPLAY', C.amber, '6 4'], WORKED: ['WORKED EXAMPLE', C.green, '']};
const S = {showSrc: false, reduced: matchMedia('(prefers-reduced-motion: reduce)').matches, lang: 'hi', lowfx: Q.get('safe') === '1'};

/* ---------------- utils */
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eo = x => 1 - Math.pow(1 - clamp(x), 3);
const eio = x => (x = clamp(x), x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const lerp = (a, b, x) => a + (b - a) * x;
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const fmt = (x, n = 2) => (x == null || isNaN(x)) ? '–' : Number(x).toFixed(n);
function rng(seed) { let s = seed >>> 0 || 1; return () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296; }
function noise(seed, t) { const r = rng(seed * 9973 + Math.floor(t)), a = r(), r2 = rng(seed * 9973 + Math.floor(t) + 1), b = r2(); const f = t - Math.floor(t); return lerp(a, b, f * f * (3 - 2 * f)); }
const h = (tag, a = {}, inner = '') => `<${tag} ${Object.entries(a).filter(([, v]) => v !== undefined && v !== null && v !== false).map(([k, v]) => `${k}="${esc(v)}"`).join(' ')}>${inner}</${tag}>`;
const T = (x, y, s, o = {}) => h('text', {x, y, fill: o.fill || C.text, 'font-size': o.size || 22, 'font-weight': o.w || 400, 'text-anchor': o.anchor || 'start',
  'font-family': o.mono ? 'JetBrains Mono, IBM Plex Mono, Consolas, monospace' : (o.math ? 'STIX Two Text, Cambria Math, Times New Roman, serif' : undefined), opacity: o.op, 'letter-spacing': o.ls}, esc(s));
const R = (x, y, w, hh, o = {}) => h('rect', {x, y, width: Math.max(0, w), height: Math.max(0, hh), rx: o.rx ?? 14, fill: o.fill || C.panel, stroke: o.stroke || C.line, 'stroke-width': o.sw || 1.5, opacity: o.op, 'stroke-dasharray': o.dash});
const L = (x1, y1, x2, y2, o = {}) => h('line', {x1, y1, x2, y2, stroke: o.stroke || C.dim, 'stroke-width': o.sw || 2, opacity: o.op, 'stroke-dasharray': o.dash, 'marker-end': o.arrow ? 'url(#ar)' : undefined});
const G = (inner, o = {}) => h('g', {transform: o.tr, opacity: o.op}, inner);
function wrap(text, max) { const out = []; let cur = ''; for (const w of String(text).split(' ')) { if ((cur + ' ' + w).trim().length > max) { out.push(cur.trim()); cur = w; } else cur += ' ' + w; } if (cur.trim()) out.push(cur.trim()); return out; }
function TW(x, y, s, max, o = {}) { return wrap(s, max).map((ln, i) => T(x, y + i * (o.lh || (o.size || 22) * 1.3), ln, o)).join(''); }

/* data-origin badge; with "Sources" on it also prints the file path */
function badge(x, y, origin, src, o = {}) {
  const [lab, col, dash] = ORIGIN[origin] || ORIGIN.ILLUSTRATIVE;
  const w = lab.length * 8.2 + 20;
  let s = R(x, y, w, 24, {rx: 12, fill: 'rgba(7,12,40,.85)', stroke: col, sw: 1.6, dash: dash || undefined}) + T(x + w / 2, y + 17, lab, {fill: col, size: 13, w: 700, anchor: 'middle', ls: .5});
  if (S.showSrc && src) s += T(x + (o.srcRight ? w + 8 : 0), y + (o.srcRight ? 17 : 40), src, {fill: C.dim, size: 13, mono: true});
  return s;
}
function ribbon(x, y, w, hh, label = 'ILLUSTRATIVE') {
  const id = 'rb' + Math.round(x + y * 7 + w);
  return h('clipPath', {id}, R(x, y, w, hh, {rx: 14})) + G(R(x + w - 210, y + 22, 300, 28, {rx: 0, fill: 'rgba(255,183,3,.92)', stroke: 'none'}) +
    T(x + w - 60, y + 42, label, {fill: '#1A1200', size: 14, w: 800, anchor: 'middle', ls: 1}), {tr: `rotate(30 ${x + w - 60} ${y + 36})`}).replace('<g ', `<g clip-path="url(#${id})" `);
}
function chip(x, y, label, bg, fg = '#0B1238') { const w = label.length * 8.6 + 18; return R(x, y, w, 24, {rx: 12, fill: bg, stroke: 'none'}) + T(x + w / 2, y + 17, label, {fill: fg, size: 13, w: 800, anchor: 'middle'}); }
const LADDER = {C0: ['C0', '#5C6370', C.text], C1: ['C1 DESIGN', '#E3E6F3', '#101A4A'], C2: ['C2 BUILT', C.blue, '#0B1238'], C3: ['C3 MEASURED', C.teal, '#0B1238'], C4: ['C4 MATCHED SOTA', C.gold, '#0B1238']};
const ladder = (x, y, k) => { const [l, bg, fg] = LADDER[k] || LADDER.C1; return chip(x, y, l, bg, fg); };
const CLS = {A: ['A ESTABLISHED', C.blue], B: ['B DERIVED', C.green], C: ['C HYPOTHESIS', C.violet]};
const clsChip = (x, y, k) => chip(x, y, CLS[k][0], CLS[k][1]);
const pending = (x, y) => chip(x, y, 'RESULT PENDING', '#FDE68A', '#5A3A00');

/* ---------------- fusion maths (mirrors ws5_fusion_rl: nf.effective_weight, fusion_models.fm1, nf3, decision.conformal_level) */
const F = D.fusion || {};
const TAU = (F.tau || {}).value ?? 0.5, LAM = (F.lambda || {}).value ?? 0.3, CFA = (F.C_FA || {}).value ?? 5, CMISS = (F.C_miss || {}).value ?? 100;
const PSTAR = CFA / (CFA + CMISS);
const CAPS = ((F.trust_caps || {}).value) || {};
const h2 = p => { p = clamp(p, 1e-6, 1 - 1e-6); return -(p * Math.log2(p) + (1 - p) * Math.log2(1 - p)); };
const nf1 = (p, phi, sigma = .25) => Math.exp(-Math.pow(Math.max(p - phi, 0), 2) / (2 * (sigma * sigma + 1e-6)));
function fuse(ex) {
  const a = ex.filter(e => e.avail !== false);
  if (!a.length) return {p: 0, u: 1, w: [], uncertain: true, level: 'GREEN'};
  const w = a.map(e => e.r * (e.c ?? 1) * Math.exp(-e.u / TAU)); const sw = w.reduce((s, v) => s + v, 0) || 1;
  const p = a.reduce((s, e, i) => s + w[i] * e.p, 0) / sw; const wn = w.map(v => v / sw);
  const base = a.reduce((s, e, i) => s + wn[i] * e.u, 0); const disp = Math.sqrt(a.reduce((s, e, i) => s + wn[i] * (e.p - p) ** 2, 0));
  const u = clamp(base + LAM * disp);
  return {p, u, w, uncertain: u > .6, level: level(p)};
}
const level = p => p >= 10 * PSTAR ? 'RED' : p >= 4 * PSTAR ? 'ORANGE' : p >= PSTAR ? 'YELLOW' : 'GREEN';
const LV = {GREEN: '#3DDC97', YELLOW: '#FFE066', ORANGE: '#FF9F43', RED: '#F0533F'};
const RULES = {
  'plain mean': ex => ex.reduce((s, e) => s + e.p, 0) / ex.length,
  'median': ex => { const v = ex.map(e => e.p).sort((a, b) => a - b), n = v.length; return n % 2 ? v[(n - 1) / 2] : (v[n / 2 - 1] + v[n / 2]) / 2; },
  'max': ex => Math.max(...ex.map(e => e.p)),
  'inverse-variance': ex => { const w = ex.map(e => 1 / Math.max(e.u, .05) ** 2); return ex.reduce((s, e, i) => s + w[i] * e.p, 0) / w.reduce((a, b) => a + b, 0); },
  'log-linear pool': ex => { const w = ex.map(e => e.r), sw = w.reduce((a, b) => a + b, 0); const z = ex.reduce((s, e, i) => s + w[i] / sw * Math.log(clamp(e.p, 1e-4, 1 - 1e-4) / (1 - clamp(e.p, 1e-4, 1 - 1e-4))), 0); return 1 / (1 + Math.exp(-z)); },
  'FM-1 (code default)': ex => fuse(ex).p,
};

/* ---------------- simulated replay generator (seeded; the ONLY non-repo inputs in the film, always ribboned) */
const SC = {
  steam: {name: 'Steam from a kitchen', truth: 'no fire', growth: 'saturates', flick: .35},
  fire: {name: 'Real fire, early smoke', truth: 'fire', growth: 't²', flick: 2.0},
  fog: {name: 'Morning fog on a hillside', truth: 'no fire', growth: 'flat', flick: .1},
  night: {name: 'Headlights at night', truth: 'no fire', growth: 'flat', flick: 6.0},
  fake: {name: 'Viral "fire" video (synthetic placeholder)', truth: 'fake', growth: 'n/a', flick: 0},
};
function replay(kind, x) { // x in [0,1] along the scenario
  const n = (s, a = .04) => (noise(s, x * 30) - .5) * 2 * a;
  let cnn, zs, phys, anom, media = null, pfake = 0, obs, exp_ = x * x;
  if (kind === 'fire') { cnn = .25 + .7 * eo(seg(x, .1, .8)) + n(1); zs = .3 + .6 * eo(seg(x, .2, .85)) + n(2); phys = .12 + .8 * eo(seg(x, .3, .8)) + n(3, .02); anom = .2 + .65 * eo(seg(x, .25, .8)) + n(4); obs = exp_ + n(5, .03); }
  else if (kind === 'steam') { cnn = .3 + .45 * eo(seg(x, .05, .5)) + n(1, .05); zs = .45 + .1 * Math.sin(x * 18) + n(2); phys = .04 + n(3, .01); anom = .06 + n(4, .02); obs = .35 * eo(seg(x, 0, .45)); }
  else if (kind === 'fog') { cnn = .2 + .15 * eo(seg(x, .1, .6)) + n(1); zs = .3 + n(2); phys = .03; anom = .05; obs = .15 * x; }
  else if (kind === 'night') { cnn = .35 + .2 * Math.abs(Math.sin(x * 12)) + n(1); zs = .25 + n(2); phys = .03; anom = .08; obs = .05; }
  else { cnn = .05 + n(1, .02); zs = .08; phys = .03; anom = .06; media = .95; pfake = .1 + .8 * eo(seg(x, .2, .6)); obs = 0; }
  const phi = clamp(phys);
  const ex = [
    {k: 'fire_cnn', name: 'Fire CNN', p: clamp(cnn), r: CAPS.fire_cnn?.default_r ?? .8},
    {k: 'zeroshot', name: 'Zero-shot CLIP', p: clamp(zs), r: CAPS.zeroshot?.default_r ?? .4},
    {k: 'fire_phys', name: 'Fire physics', p: phi, r: CAPS.fire_phys?.default_r ?? 1, physics: true},
    {k: 'anomaly', name: 'Anomaly (site normal?)', p: clamp(anom), r: CAPS.anomaly?.default_r ?? .7},
  ];
  if (media != null) ex.push({k: 'media', name: 'Viral video (media)', p: media, r: (CAPS.zeroshot?.default_r ?? .4) * (1 - pfake), media: true});
  ex.forEach(e => { e.u = .5 * h2(e.p); e.c = e.physics ? 1 : nf1(e.p, phi); });
  const f = fuse(ex);
  return {ex, f, phi, obs, exp: exp_, pfake, flick: SC[kind].flick, kind};
}

/* ======================================================================= scene helpers */
const LAYERS = ['DATA', 'PERCEPTION', 'PHYSICS', 'FUSION', 'DECISION', 'HUMAN'];
function minimap(active) {
  let s = '';
  LAYERS.forEach((l, i) => {
    const on = active.includes(i), x = 1560 + i * 0, y = 30 + i * 24;
    s += R(1600, y, 280, 20, {rx: 6, fill: on ? 'rgba(245,124,31,.9)' : 'rgba(22,32,90,.85)', stroke: on ? C.saffron : C.line, sw: 1}) +
      T(1614, y + 15, `${i + 1} ${l}`, {size: 13, w: on ? 800 : 500, fill: on ? '#0B1238' : C.dim, mono: true});
  });
  return s;
}
function header(id, name, active) { return T(60, 58, `${id} · ${name}`, {fill: C.gold, size: 20, w: 700, mono: true, ls: 1}) + minimap(active); }
function title(x, y, s, o = {}) { return T(x, y, s, {size: o.size || 44, w: 800, ...o}); }
function eye(cx, cy, w, open, o = {}) {
  const hh = w * .32 * open;
  return h('path', {d: `M${cx - w / 2},${cy} Q${cx},${cy - hh * 2} ${cx + w / 2},${cy} Q${cx},${cy + hh * 2} ${cx - w / 2},${cy} Z`, fill: o.fill || 'rgba(255,248,236,.06)', stroke: o.stroke || C.saffron, 'stroke-width': 4}) +
    (open > .25 ? h('circle', {cx, cy, r: w * .15 * Math.min(1, open * 1.3), fill: 'none', stroke: o.iris || C.teal, 'stroke-width': 4}) + h('circle', {cx, cy, r: w * .06 * open, fill: C.gold}) : '');
}
function particle(x1, y1, x2, y2, t, col, k = 3, speed = .35, phase = 0) {
  if (S.reduced || S.lowfx) return '';
  let s = '';
  for (let i = 0; i < k; i++) { const f = ((t * speed + i / k + phase) % 1 + 1) % 1; s += h('circle', {cx: lerp(x1, x2, f), cy: lerp(y1, y2, f), r: 5, fill: col, opacity: .9 * Math.sin(f * Math.PI)}); }
  return s;
}
const ds = q => (D.datasets || []).find(d => q.test(d.name)) || null;
const res = k => (D.results || {})[k] || null;
const cur = k => (D.curves || {})[k] || null;

/* ======================================================================= S0 cold open */
function S0(t) {
  let s = '';
  const eyes = [[660, 'SEE', 'cameras, satellites, weather, media'], [960, 'REASON', 'physics + calibrated fusion'], [1260, 'RESPOND', 'tiered alerts, human approves']];
  eyes.forEach(([x, l, d], i) => {
    const o = eo(seg(t, .6 + i * 1.4, 1.8 + i * 1.4));
    s += eye(x, 470, 230, o) + G(T(x, 610, l, {size: 34, w: 800, anchor: 'middle', ls: 4}) + T(x, 645, d, {size: 18, fill: C.dim, anchor: 'middle'}), {op: seg(t, 1.2 + i * 1.4, 2 + i * 1.4)});
  });
  const a = eo(seg(t, 5.5, 7.5));
  s += G(T(960, 250, 'TRINETRA', {size: 150, w: 900, anchor: 'middle', ls: 14}) + T(960, 312, 'See. Reason. Respond.', {size: 34, fill: C.gold, anchor: 'middle', ls: 3}), {op: a, tr: `translate(0 ${(1 - a) * 20})`});
  const pd = eo(seg(t, 9, 14)), xs = LAYERS.map((_, i) => 360 + i * 240);
  s += h('polyline', {points: xs.map(x => `${x},770`).join(' '), fill: 'none', stroke: C.saffron, 'stroke-width': 3, 'stroke-dasharray': 1200, 'stroke-dashoffset': 1200 * (1 - pd)});
  LAYERS.forEach((l, i) => { const o = seg(pd, i / 6, (i + 1) / 6); s += G(h('circle', {cx: xs[i], cy: 770, r: 10, fill: C.saffron}) + T(xs[i], 812, l, {size: 17, anchor: 'middle', fill: C.dim, mono: true}), {op: o}); });
  return s;
}

/* ======================================================================= S1 why warnings fail: surveys + 14 patterns */
function S1(t) {
  let s = header('S1', 'Why warnings fail', []);
  if (t < 16.5) {
    s += G(title(60, 130, 'What surveys and public reports say') + T(60, 170, 'cost of disasters in India and the measured value of early warning', {size: 22, fill: C.dim}), {op: eo(seg(t, 0, 1))});
    (D.surveys || []).forEach((v, i) => {
      const c = i % 3, r = Math.floor(i / 3), x = 60 + c * 610, y = 205 + r * 205, o = eo(seg(t, .6 + i * .55, 1.4 + i * .55));
      s += G(R(x, y, 580, 185, {fill: C.panel}) + T(x + 22, y + 62, v.value, {size: 46, w: 800, fill: v.id === 'rumour' ? C.red : C.gold}) +
        TW(x + 22, y + 98, v.label, 52, {size: 19}) + TW(x + 22, y + 156, v.source.split(' (via')[0], 44, {size: 13, fill: C.dim, lh: 16}) +
        badge(x + 420, y + 146, 'PAPER', v.source) + chip(x + 420 - 92, y + 146, `CONF ${v.confidence}`, v.confidence === 'A' ? C.teal : C.amber), {op: o, tr: `translate(0 ${(1 - o) * 18})`});
    });
    s += G(T(60, 845, 'Confidence A = widely published; B = approximate, verify before quoting (docs/26).', {size: 17, fill: C.dim}), {op: seg(t, 6, 7)});
  } else {
    const lt = t - 16.5;
    s += G(title(60, 130, 'Warning systems fail in 14 documented ways') + T(60, 170, 'category-level patterns from the literature (docs/17), each mapped to a TRINETRA design answer', {size: 22, fill: C.dim}), {op: eo(seg(lt, 0, 1))});
    (D.failure_patterns || []).forEach((p, i) => {
      const c = i % 7, r = Math.floor(i / 7), x = 60 + c * 262, y = 215 + r * 300, on = seg(lt, .3 + i * .3, .8 + i * .3);
      const fl = seg(lt, 8.5 + i * .3, 9.1 + i * .3), back = fl > .5, sx = Math.abs(Math.cos(fl * Math.PI));
      const face = back
        ? R(0, 0, 246, 280, {fill: '#13305A', stroke: C.teal}) + T(14, 32, p.id, {fill: C.teal, size: 18, w: 800, mono: true}) + TW(14, 72, p.answer, 21, {size: 18, w: 600}) + ladder(14, 236, p.ladder)
        : R(0, 0, 246, 280, {fill: `rgba(240,83,63,${.12 + .25 * on})`, stroke: C.red}) + T(14, 32, p.id, {fill: C.red, size: 18, w: 800, mono: true}) + TW(14, 72, p.pattern, 20, {size: 18, w: 600}) + TW(14, 190, p.hinglish, 30, {size: 14, fill: C.dim, lh: 17});
      s += G(face, {op: on, tr: `translate(${x + 123 * (1 - sx)} ${y}) scale(${Math.max(sx, .02)} 1)`});
    });
    s += G(T(60, 845, 'Chips: C1 design only · C2 built, untested on real data · C3 built and measured by us. No C4 (matched SOTA) claim yet.', {size: 17, fill: C.dim}) + badge(1480, 826, 'REAL_CONFIG', 'TRINETRA/docs/17_EXISTING_SYSTEMS_AND_FAILURES.md'), {op: seg(lt, 9, 10)});
  }
  return s;
}

/* ======================================================================= S2 data journey */
function S2(t) {
  let s = header('S2', 'The data journey', [0]);
  const picks = [/D-Fire/, /CIFAKE/i, /Landslide4Sense/i, /Sen1Floods11/i, /FireSense/i, /DeepFire/i].map(ds).filter(Boolean);
  if (t < 19) {
    s += G(title(60, 130, t < 9 ? 'The originals are huge' : 'So we draw small, seeded, stratified subsets') +
      T(60, 170, t < 9 ? 'real full sizes from the dataset register (docs/09b)' : 'stratified by class, site and time · seed 0 · every subset recorded', {size: 22, fill: C.dim}), {op: eo(seg(t % 9.5, 0, 1))});
    picks.forEach((d, i) => {
      const mb = parseFloat(String(d.size_full).replace(/,/g, '')) * (/GB/i.test(d.size_full) ? 1024 : 1) || 50;
      const side = 60 + 40 * Math.log10(mb + 1), x = 120 + i * 290, y = 560 - side, o = eo(seg(t, .4 + i * .5, 1.4 + i * .5));
      s += G(h('polygon', {points: `${x},${y} ${x + side},${y} ${x + side + 40},${y - 30} ${x + 40},${y - 30}`, fill: 'rgba(91,141,239,.10)', stroke: C.blue, 'stroke-dasharray': '6 5'}) +
        h('polygon', {points: `${x + side},${y} ${x + side + 40},${y - 30} ${x + side + 40},${y + side - 30} ${x + side},${y + side}`, fill: 'rgba(91,141,239,.06)', stroke: C.blue, 'stroke-dasharray': '6 5'}) +
        R(x, y, side, side, {rx: 2, fill: 'rgba(91,141,239,.08)', stroke: C.blue, dash: '6 5'}) +
        TW(x, 610, d.name.split('(')[0].trim(), 24, {size: 17, w: 700}) + T(x, 662, `full: ${d.size_full}`, {size: 16, fill: C.dim, mono: true}), {op: o});
      const so = eo(seg(t, 9.5 + i * .5, 11 + i * .5));
      if (so > 0) s += G(R(x + side / 2 - 22, lerp(y + side / 2, 700, so), 44, 44, {rx: 6, fill: C.saffron, stroke: 'none'}) +
        TW(x, 790, `subset: ${d.size_subset}`, 26, {size: 15, fill: C.gold, mono: true, lh: 18}), {op: so});
    });
    s += G(T(60, 880, '"Too big for a 36-hour prototype": we keep the protocol, not the terabytes.', {size: 20, fill: C.dim}) + badge(1480, 862, 'REAL_CONFIG', 'TRINETRA/docs/09b_dataset_links.csv'), {op: seg(t, 3, 4)});
  } else if (t < 30) {
    const lt = t - 19, cv = (D.conversion || {}).tpd || {};
    s += G(title(60, 130, 'Tables mapped to one schema: TPD-0.1') + T(60, 170, 'landslide pack: NASA catalog + NASA POWER rain + Copernicus DEM → one leakage-safe index', {size: 22, fill: C.dim}), {op: eo(seg(lt, 0, 1))});
    const cols = ['event_id', 'lat', 'lon', 'day', 'rain_1d…30d', 'slope_p90', 'caine_ratio', 'dfs', 'label'];
    for (let r = 0; r < 9; r++) { const o = eo(seg(lt, .5 + r * .25, 1.2 + r * .25)), y = 230 + r * 46;
      s += G(R(lerp(-700, 60, o), y, 720, 38, {rx: 6, fill: r % 2 ? C.panel : C.panel2}) + T(lerp(-680, 80, o), y + 26, r === 0 ? cols.join(' · ') : `row ${r} → mapped, units checked, group = 0.1° block`, {size: r === 0 ? 13 : 15, mono: r === 0, fill: r === 0 ? C.gold : C.text}), {op: o}); }
    const k = [['input rows', cv.input_rows], ['output rows', cv.output_rows], ['dropped', cv.dropped_rows], ['landslide days', cv.positives], ['control days', cv.controls], ['spatial groups', cv.spatial_groups]];
    k.forEach(([l, v], i) => { const x = 880 + (i % 3) * 330, y = 250 + Math.floor(i / 3) * 190, o = eo(seg(lt, 3 + i * .4, 4 + i * .4));
      const val = v ? Math.round(v.value * eo(seg(lt, 3 + i * .4, 5 + i * .4))) : '–';
      s += G(R(x, y, 300, 160) + T(x + 22, y + 82, String(val), {size: 62, w: 800, fill: l === 'dropped' ? C.teal : C.gold}) + T(x + 22, y + 122, l, {size: 20}) + (v ? badge(x + 160, y + 14, v.origin, v.source) : ''), {op: o}); });
    s += G(chip(880, 650, 'SOURCE + DERIVED', C.blue) + chip(1060, 650, 'SYNTHETIC 0', '#E3E6F3') + chip(1190, 650, 'OWN-CAPTURED 0', '#E3E6F3') +
      T(880, 712, (cv.split || {}).value || '', {size: 18, fill: C.dim}) + T(880, 742, 'controls share sites, other monsoon days: base rate is artificial (case-control)', {size: 18, fill: C.dim}), {op: seg(lt, 6, 7)});
  } else if (t < 43) {
    const lt = t - 30, R1 = rng(7), vids = 8, cols = ['#FF6B35', '#FFB703', '#2EC4B6', '#5B8DEF', '#3DDC97', '#A78BFA', '#F472B6', '#F4F1EA'];
    s += G(title(60, 130, 'The leakage trap') + T(60, 170, 'frames of one video are near-copies: if they land on both sides, the test is a memory test', {size: 22, fill: C.dim}), {op: eo(seg(lt, 0, 1))});
    s += R(60, 210, 870, 610, {fill: 'rgba(240,83,63,.07)', stroke: C.red}) + T(90, 255, 'Random split', {size: 30, w: 800, fill: C.red}) + T(90, 290, 'train', {size: 18, fill: C.dim}) + T(640, 290, 'test', {size: 18, fill: C.dim});
    s += R(990, 210, 870, 610, {fill: 'rgba(46,196,182,.07)', stroke: C.teal}) + T(1020, 255, 'Grouped split (TRINETRA)', {size: 30, w: 800, fill: C.teal}) + T(1020, 290, 'train', {size: 18, fill: C.dim}) + T(1500, 290, 'test', {size: 18, fill: C.dim});
    const pts = []; for (let v = 0; v < vids; v++) for (let f = 0; f < 5; f++) pts.push({v, side: R1() < .7 ? 0 : 1, jx: R1(), jy: R1()});
    const o = eo(seg(lt, 1, 3));
    pts.forEach((p, i) => { const x = (p.side ? 640 : 110) + p.jx * 240, y = 320 + p.jy * 420; s += h('circle', {cx: x, cy: y, r: 11 * o, fill: cols[p.v]}); p.x = x; p.y = y; });
    if (lt > 3) pts.forEach((a, i) => pts.forEach((b, j) => { if (j > i && a.v === b.v && a.side !== b.side) s += L(a.x, a.y, b.x, b.y, {stroke: C.red, sw: 1.6, op: .65 * seg(lt, 3, 4.5)}); }));
    if (lt > 4.5) s += G(T(500, 560, '99%', {size: 110, w: 900, fill: C.red, anchor: 'middle', op: .9}) + T(500, 600, 'looks great, means nothing', {size: 20, anchor: 'middle', fill: C.text}) + ribbon(60, 210, 870, 610), {op: seg(lt, 4.5, 5.5)});
    const g2 = eo(seg(lt, 6, 8));
    for (let v = 0; v < vids; v++) { const side = v < 6 ? 0 : 1, cx = (side ? 1560 : 1060) + (v % 3) * 110, cy = 360 + Math.floor((v % 6) / 3) * 150;
      for (let f = 0; f < 5; f++) { const a = f / 5 * Math.PI * 2; s += h('circle', {cx: cx + 30 * Math.cos(a) * g2, cy: cy + 30 * Math.sin(a) * g2, r: 10 * g2, fill: cols[v]}); } }
    const fp = (D.conversion || {}).fire_pack || {};
    if (lt > 8.5) s += G(R(1500, 640, 330, 150, {fill: '#0E1A3F', stroke: C.gold, sw: 2.5}) + T(1525, 680, 'VAULT · held-out', {size: 20, w: 800, fill: C.gold}) +
      T(1525, 716, `DeepFire, deduped · n = ${fp.heldout_rows ? fp.heldout_rows.value.toLocaleString('en-IN') : '–'}`, {size: 18}) + T(1525, 744, `fire pack OOF rows: ${fp.oof_rows ? fp.oof_rows.value.toLocaleString('en-IN') : '–'}`, {size: 18}) +
      (fp.heldout_rows ? badge(1525, 756, 'REAL_RESULT', fp.heldout_rows.source) : ''), {op: seg(lt, 8.5, 9.5)});
  } else {
    const lt = t - 43;
    s += G(title(60, 130, 'Every split goes where it is needed') + T(60, 170, 'role per module: train · validation · held-out (other source) · stress (look-alikes)', {size: 22, fill: C.dim}), {op: eo(seg(lt, 0, 1))});
    const L1 = [['train + val', 'D-Fire · CIFAKE · L4S · Sen1Floods11', C.blue], ['held-out', 'DeepFire · FIRE · StyleGAN faces · Bolivia', C.gold], ['stress', 'weather · candles · scenes · AI art', C.amber], ['real geo table', '736 rows · 101 blocks', C.teal]];
    const M2 = [['Fire CNN', 'train · held-out · stress'], ['Zero-shot CLIP', 'held-out · stress (no training)'], ['Media authenticity', 'train · held-out'], ['EO heads', 'train · Bolivia held-out'], ['Physics + Geo-PINN', 'real geo table'], ['Fusion calibration', 'out-of-fold scores only'], ['RL environment', 'real rain seasons (simulator)']];
    L1.forEach(([a, b, col], i) => { const y = 250 + i * 150; s += G(R(80, y, 520, 110, {stroke: col, sw: 2}) + T(104, y + 46, a, {size: 26, w: 800, fill: col}) + T(104, y + 82, b, {size: 17, fill: C.dim}), {op: eo(seg(lt, .3 + i * .3, 1 + i * .3))}); });
    M2.forEach(([a, b], i) => { const y = 225 + i * 88; s += G(R(1180, y, 660, 72) + T(1204, y + 32, a, {size: 22, w: 700}) + T(1204, y + 58, b, {size: 15, fill: C.dim}), {op: eo(seg(lt, 1 + i * .25, 1.7 + i * .25))}); });
    const E = [[0, 0], [1, 0], [2, 0], [0, 1], [1, 1], [2, 1], [0, 2], [1, 2], [0, 3], [3, 4], [0, 5], [3, 6]];
    E.forEach(([a, b], i) => { const y1 = 305 + a * 150, y2 = 261 + b * 88, o = seg(lt, 2.5, 3.5); s += L(600, y1, 1180, y2, {stroke: L1[a][2], sw: 1.6, op: .5 * o}) + (o > .5 ? particle(600, y1, 1180, y2, lt, L1[a][2], 2, .45, i * .13) : ''); });
  }
  return s;
}

/* ======================================================================= shared replay layout (S3, S4, S5, explore) */
function frameStrip(kind, x, X0, Y0) {
  let s = R(X0, Y0, 480, 600, {fill: C.panel}) + T(X0 + 20, Y0 + 36, 'Camera frames', {size: 22, w: 700});
  for (let i = 0; i < 4; i++) {
    const fx = clamp(x - (3 - i) * .06), y = Y0 + 60 + i * 132;
    s += R(X0 + 20, y, 440, 118, {rx: 8, fill: '#0A1030', stroke: C.line});
    const r2 = rng(i + 3);
    if (kind === 'steam' || kind === 'fog') for (let k = 0; k < 9; k++) s += h('ellipse', {cx: X0 + 110 + r2() * 260, cy: y + 100 - fx * 70 * r2(), rx: 18 + fx * 40 * r2(), ry: 10 + fx * 18, fill: '#E8ECF8', opacity: .12 + .25 * fx});
    if (kind === 'fire') { const sz = .2 + .8 * eo(fx); for (let k = 0; k < 7; k++) s += h('path', {d: `M${X0 + 200 + k * 9},${y + 108} q${-12 * sz},${-40 * sz} ${4},${-70 * sz * (.6 + r2() * .5)} q${14 * sz},${30 * sz} ${6},${70 * sz}z`, fill: k % 2 ? C.amber : C.ember, opacity: .5 + .4 * sz});
      s += h('ellipse', {cx: X0 + 240, cy: y + 40 - sz * 20, rx: 40 + 80 * sz, ry: 12 + 18 * sz, fill: '#6B6F80', opacity: .15 + .3 * sz}); }
    if (kind === 'night') for (let k = 0; k < 2; k++) s += h('circle', {cx: X0 + 180 + k * 70, cy: y + 70, r: 10, fill: '#FFF5C2', opacity: .5 + .5 * Math.abs(Math.sin(x * 20 + k))});
    if (kind === 'fake') s += h('rect', {x: X0 + 30, y: y + 10, width: 420, height: 98, fill: '#0A1030'}) + T(X0 + 240, y + 66, 'camera: no fire seen', {size: 16, anchor: 'middle', fill: C.dim});
    s += T(X0 + 30, y + 22, `t-${3 - i}`, {size: 13, fill: C.dim, mono: true});
  }
  return s + ribbon(X0, Y0, 480, 600, 'SIMULATED REPLAY');
}
function expertsPanel(st, X0, Y0, wmax) {
  let s = R(X0, Y0, 560, 600, {fill: C.panel}) + T(X0 + 20, Y0 + 36, 'Experts: risk p · uncertainty halo · weight', {size: 22, w: 700});
  const sw = st.f.w.reduce((a, b) => a + b, 0) || 1;
  st.ex.forEach((e, i) => {
    const y = Y0 + 80 + i * 100, bw = 330 * e.p, halo = 330 * e.u * .6;
    s += T(X0 + 20, y, e.name, {size: 19, w: 600}) + T(X0 + 540, y, `w ${fmt(st.f.w[i] / sw, 2)}`, {size: 16, anchor: 'end', mono: true, fill: C.dim});
    s += R(X0 + 20, y + 14, 330, 22, {rx: 11, fill: '#0A1030', stroke: C.line});
    s += R(X0 + 20 + Math.max(0, bw - halo), y + 8, Math.min(330, 2 * halo), 34, {rx: 17, fill: 'rgba(255,183,3,.18)', stroke: 'none'});
    s += R(X0 + 20, y + 14, bw, 22, {rx: 11, fill: e.media ? C.violet : e.physics ? C.blue : C.ember, stroke: 'none', op: .4 + .6 * (st.f.w[i] / sw) / Math.max(.25, wmax)});
    s += T(X0 + 365, y + 32, `p ${fmt(e.p)}`, {size: 16, mono: true}) + T(X0 + 450, y + 32, e.physics ? 'physics' : `c ${fmt(e.c)}`, {size: 16, mono: true, fill: e.c < .5 ? C.red : C.dim});
  });
  return s + T(X0 + 20, Y0 + 585, 'c = physics consistency (NF-1): more alarm than physics allows ⇒ less weight', {size: 14, fill: C.dim});
}
function physicsPanel(st, X0, Y0) {
  let s = R(X0, Y0, 380, 600, {fill: C.panel}) + T(X0 + 20, Y0 + 36, 'Physics check', {size: 22, w: 700});
  const px = X0 + 40, py = Y0 + 300, pw = 300, ph = 220;
  s += L(px, py, px + pw, py, {stroke: C.line}) + L(px, py, px, py - ph, {stroke: C.line}) + T(px, py + 24, 'time →', {size: 14, fill: C.dim}) + T(px + 6, py - ph + 14, 'flame/plume area', {size: 14, fill: C.dim});
  let pe = '', po = '';
  for (let i = 0; i <= 40; i++) { const xx = i / 40; pe += `${px + xx * pw},${py - xx * xx * ph} `; }
  const nObs = Math.max(2, Math.round(40 * st.x));
  for (let i = 0; i <= nObs; i++) { const xx = i / 40, ob = replay(st.kind, xx).obs; po += `${px + xx * pw},${py - clamp(ob) * ph} `; }
  s += h('polyline', {points: pe, fill: 'none', stroke: C.blue, 'stroke-width': 3, 'stroke-dasharray': '8 6'}) + h('polyline', {points: po, fill: 'none', stroke: st.kind === 'fire' ? C.teal : C.red, 'stroke-width': 4});
  s += T(px + pw, py - ph - 8, 'expected (t² growth)', {size: 14, fill: C.blue, anchor: 'end'}) + T(px + pw, py + 44, 'observed', {size: 14, fill: st.kind === 'fire' ? C.teal : C.red, anchor: 'end'});
  const D0 = .5, f0 = 1.5 / Math.sqrt(D0), lo = f0 * .7, hi = f0 * 1.3, bx = X0 + 40, by = Y0 + 410, bw = 300, fmax = 7;
  s += T(bx, by - 14, `flicker f ≈ 1.5·D^(−1/2) = ${fmt(f0, 1)} Hz, D ${D0} m`, {size: 15}) + R(bx, by, bw, 18, {rx: 9, fill: '#0A1030'}) + R(bx + lo / fmax * bw, by, (hi - lo) / fmax * bw, 18, {rx: 9, fill: 'rgba(91,141,239,.55)', stroke: 'none'});
  if (st.flick > 0) { const inb = st.flick >= lo && st.flick <= hi; s += h('circle', {cx: bx + clamp(st.flick / fmax) * bw, cy: by + 9, r: 10, fill: inb ? C.teal : C.red}) + T(bx, by + 46, `observed ${fmt(st.flick, 1)} Hz: ${inb ? 'inside band' : 'outside band'}`, {size: 16, fill: inb ? C.teal : C.red, w: 700}); }
  s += badge(X0 + 20, Y0 + 490, 'REAL_CONFIG', 'TRINETRA/trinetra/src/trinetra/ws1a_firephys/established_ef.py:21-23') + T(X0 + 20, Y0 + 545, `physics p = ${fmt(st.phi)} · observations simulated`, {size: 15, fill: C.dim});
  return s;
}
function gauge(st, X0, Y0, valid) {
  let s = R(X0, Y0, 340, 600, {fill: C.panel}) + T(X0 + 20, Y0 + 36, 'Fused risk (FM-1)', {size: 22, w: 700});
  const gx = X0 + 26, gy = Y0 + 66, gh = 440, toY = p => gy + gh - Math.sqrt(clamp(p)) * gh;   // sqrt axis so p* is visible
  s += R(gx, gy, 40, gh, {rx: 20, fill: '#0A1030'});
  [['10p*', 10 * PSTAR, LV.RED], ['4p*', 4 * PSTAR, LV.ORANGE], ['p*', PSTAR, LV.YELLOW]].forEach(([l, v, c]) => s += L(gx - 6, toY(v), gx + 48, toY(v), {stroke: c, sw: 2}) + T(gx + 52, toY(v) + 5, l, {size: 13, fill: c, mono: true, w: 700}));
  const top = toY(st.f.p);
  s += R(gx - 5, toY(clamp(st.f.p + st.f.u * .3)), 50, Math.max(6, toY(clamp(st.f.p - st.f.u * .3)) - toY(clamp(st.f.p + st.f.u * .3))), {rx: 18, fill: 'rgba(255,183,3,.16)', stroke: 'none'});
  s += R(gx, top, 40, gy + gh - top, {rx: 20, fill: LV[st.f.level], stroke: 'none'});
  const tx = X0 + 120;
  s += T(tx, Y0 + 116, fmt(st.f.p, 2), {size: 54, w: 800, fill: LV[st.f.level]}) + chip(tx, Y0 + 132, st.f.level, LV[st.f.level]);
  s += T(tx, Y0 + 196, `U* ${fmt(st.f.u, 2)}`, {size: 18, mono: true}) + (st.f.uncertain ? T(tx, Y0 + 218, '→ human review', {size: 15, fill: C.amber}) : '');
  s += T(tx, Y0 + 250, 'p* = C_FA/(C_FA+C_miss)', {size: 13, fill: C.dim}) + T(tx, Y0 + 270, `= ${CFA}/${CFA + CMISS} = ${fmt(PSTAR, 4)}`, {size: 13, fill: C.dim, mono: true});
  s += T(tx, Y0 + 296, `cuts ${fmt(PSTAR, 3)} · ${fmt(4 * PSTAR, 3)} · ${fmt(10 * PSTAR, 3)}`, {size: 13, fill: C.dim, mono: true});
  if (valid) s += T(tx, Y0 + 336, 'detector persistence', {size: 14, fill: C.dim}) + T(tx, Y0 + 358, `${valid.support}/5 frames ≥ 0.5 ${valid.ok ? '✓' : '…'}`, {size: 14, mono: true, fill: valid.ok ? C.teal : C.amber});
  s += badge(tx, Y0 + 380, 'REAL_CONFIG', 'configs/fusion.json τ, λ · configs/default.json C_FA, C_miss · decision.py:31');
  return s;
}
function validator(kind, x) { let k = 0; for (let i = 0; i < 5; i++) if (replay(kind, clamp(x - i * .03)).ex[0].p >= .5) k++; return {support: k, ok: k >= 3}; }
function replayScene(kind, x, Y0 = 200) {
  const st = replay(kind, x); st.x = x;
  const sw = st.f.w.reduce((a, b) => a + b, 0) || 1, wmax = Math.max(...st.f.w.map(w => w / sw));
  return frameStrip(kind, x, 40, Y0) + expertsPanel(st, 540, Y0, wmax) + physicsPanel(st, 1120, Y0) + gauge(st, 1520, Y0, kind === 'fake' ? null : validator(kind, x));
}

/* ======================================================================= S3 / S4 / S5 */
function S3(t) {
  const x = seg(t, 1, 30);
  let s = header('S3', 'Incident A · the false alarm that does not fire', [1, 2, 3]) + title(60, 130, 'Steam in a kitchen') + T(60, 170, 'the fire detector climbs, but physics, zero-shot and site context do not agree', {size: 22, fill: C.dim});
  s += replayScene('steam', x);
  if (t > 29) { const st = replay('steam', 1); s += G(R(40, 820, 1820, 64, {fill: 'rgba(46,196,182,.14)', stroke: C.teal}) +
    T(70, 862, `Outcome: level ${st.f.level} (watch + log entry), no public alert. A fixed 0.5 threshold on the detector alone would have rung.`, {size: 22, w: 700}), {op: seg(t, 29, 30)}); }
  return s;
}
function S4(t) {
  const x = seg(t, 1, 27);
  let s = header('S4', 'Incident B · a real fire, early', [1, 2, 3, 4, 5]) + title(60, 130, 'A real fire, caught early') + T(60, 170, 'same layout: experts converge, physics snaps to the data, the cost line is crossed, a human approves', {size: 22, fill: C.dim});
  if (t < 28) return s + replayScene('fire', x);
  const st = replay('fire', 1), lt = t - 28, sw = st.f.w.reduce((a, b) => a + b, 0);
  const top = st.ex.map((e, i) => [e.name, st.f.w[i] / sw, e.p]).sort((a, b) => b[1] - a[1]);
  s += G(R(60, 210, 820, 600, {fill: C.panel, stroke: C.gold, sw: 2.5}) + T(90, 256, 'Operator console · SDMA control room', {size: 26, w: 800, fill: C.gold}) +
    T(90, 300, `Fused risk ${fmt(st.f.p)} · level ${st.f.level} · U* ${fmt(st.f.u)} · temporal validator confirmed`, {size: 20}) +
    T(90, 345, 'Why (top contributors by weight):', {size: 19, fill: C.dim}) + top.slice(0, 4).map((r, i) => T(110, 385 + i * 34, `${r[0]} · weight ${fmt(r[1])} · p ${fmt(r[2])}`, {size: 19, mono: true})).join('') +
    T(90, 545, 'Evidence: 4 camera frames · physics growth curve match · flicker inside band', {size: 18, fill: C.dim}) +
    R(90, 600, 340, 70, {rx: 12, fill: lt > 3 ? C.teal : C.panel2, stroke: C.teal, sw: 2}) + T(260, 645, lt > 3 ? 'APPROVED ✓' : 'Approve alert', {size: 24, w: 800, anchor: 'middle', fill: lt > 3 ? '#0B1238' : C.text}) +
    R(460, 600, 340, 70, {rx: 12, fill: C.panel2}) + T(630, 645, 'Reject / hold', {size: 22, anchor: 'middle', fill: C.dim}) +
    T(90, 720, 'CAP 1.2 alert cannot be built without the approval token (ws3_alert/cap.py)', {size: 16, fill: C.dim}) + badge(90, 740, 'REAL_CONFIG', 'TRINETRA/trinetra/src/trinetra/ws3_alert/cap.py'), {op: eo(seg(lt, 0, .8))});
  const T3 = [['Local siren (co-located only)', 'shield-bounded Tier-0 action', C.amber], ['SDMA control room', 'tiered advisory + evidence', C.saffron], ['Official channels', 'CAP feed via authorised parties only', C.teal]];
  T3.forEach(([a, b, c], i) => { const y = 260 + i * 170, o = eo(seg(lt, 4 + i * .8, 5 + i * .8));
    s += G(L(880, 440, 1180, y + 55, {stroke: c, sw: 3}) + particle(880, 440, 1180, y + 55, lt, c, 3) + R(1180, y, 640, 110, {stroke: c, sw: 2.5}) + T(1210, y + 48, a, {size: 26, w: 800, fill: c}) + T(1210, y + 84, b, {size: 18, fill: C.dim}), {op: o}); });
  s += G(T(1180, 800, 'Time-to-detection: not shown (no measured result yet).', {size: 17, fill: C.dim}) + ribbon(1180, 240, 640, 520, 'SIMULATED REPLAY'), {op: seg(lt, 5, 6)});
  return s;
}
function S5(t) {
  const x = seg(t, 1, 20), st = replay('fake', x);
  let s = header('S5', 'The fake that arrives', [1, 3]) + title(60, 130, 'A viral "fire" video') + T(60, 170, 'screened for authenticity, then cross-checked against cameras, satellite and weather', {size: 22, fill: C.dim});
  s += R(60, 210, 520, 600, {fill: C.panel}) + T(84, 250, 'Social media post', {size: 22, w: 700});
  s += R(84, 275, 470, 300, {rx: 10, fill: '#2A1406'}); for (let k = 0; k < 14; k++) s += h('path', {d: `M${130 + k * 28},560 q-20,-90 8,-${150 + (k % 4) * 40} q22,80 10,${150 + (k % 4) * 40}z`, fill: k % 2 ? C.amber : C.ember, opacity: .7});
  s += chip(96, 287, 'SYNTHETIC PLACEHOLDER', C.amber, '#1A1200') + T(84, 610, '"Huge fire near the market!! share fast"', {size: 19}) + T(84, 640, '120k shares in 1 hour (illustrative)', {size: 16, fill: C.dim});
  s += T(84, 690, `authenticity check: p_fake ${fmt(st.pfake)}`, {size: 20, w: 700, fill: st.pfake > .5 ? C.red : C.amber}) + R(84, 705, 470, 20, {rx: 10, fill: '#0A1030'}) + R(84, 705, 470 * st.pfake, 20, {rx: 10, fill: C.red, stroke: 'none'});
  s += T(84, 760, `r′ = r·(1 − p_fake) = 0.40 × ${fmt(1 - st.pfake)} = ${fmt(.4 * (1 - st.pfake))}`, {size: 19, mono: true}) + badge(84, 772, 'REAL_CONFIG', 'TRINETRA/trinetra/src/trinetra/ws5_fusion_rl/adapters.py (authenticity_adjusted_reliability)', {srcRight: true});
  s += ribbon(60, 210, 520, 600, 'SIMULATED REPLAY');
  const sw = st.f.w.reduce((a, b) => a + b, 0) || 1, wmax = Math.max(...st.f.w.map(w => w / sw));
  s += expertsPanel(st, 620, 210, wmax) + gauge(st, 1220, 210, null);
  s += G(R(1590, 210, 290, 600, {fill: C.panel}) + T(1610, 250, 'Corroboration', {size: 22, w: 700}) +
    [['CCTV nearby', 'no flame, no smoke'], ['Satellite hotspots', 'none in window'], ['Weather', 'no lightning, low wind']].map(([a, b], i) => R(1610, 280 + i * 130, 250, 110, {rx: 10, fill: C.panel2}) + T(1626, 320 + i * 130, a, {size: 19, w: 700}) + T(1626, 352 + i * 130, b, {size: 16, fill: C.dim}) + T(1626, 378 + i * 130, '✗ not corroborated', {size: 15, fill: C.red})).join('') +
    TW(1610, 700, 'Downgraded: it cannot raise the alert tier on its own.', 22, {size: 19, w: 700, fill: C.teal}), {op: seg(t, 8, 9.5)});
  return s;
}

/* ======================================================================= S6 fusion under the hood */
const CANON = [{name: 'Camera A', p: .82, u: .15, r: .9}, {name: 'Camera B (correlated with A)', p: .80, u: .16, r: .9}, {name: 'Outlier sensor', p: .10, u: .55, r: .5}, {name: 'Over-confident model', p: .99, u: .02, r: .6}];
function S6(t) {
  let s = header('S6', 'Fusion under the hood', [3, 4]) + title(60, 130, 'Fusion that knows what it does not know') + T(60, 170, 'exact rules from ws5_fusion_rl (FM-1, τ and λ from configs/fusion.json)', {size: 22, fill: C.dim});
  const steps = [['Calibrate', 'T on other folds'], ['Weight', 'w̃ = r·c·e^(−u/τ)'], ['Pool', 'FM-1: Σw̃p / Σw̃'], ['Uncertainty', 'U* = Σw̄u + λ·D'], ['Threshold', 'p*, 4p*, 10p*'], ['Tier + human', 'GREEN … RED']];
  steps.forEach(([a, b], i) => { const x = 60 + i * 305, on = seg(t, .5 + i * .9, 1.2 + i * .9); s += G(R(x, 200, 285, 92, {stroke: on > .5 ? C.saffron : C.line, sw: 2}) + T(x + 18, 238, a, {size: 22, w: 800}) + T(x + 18, 272, b, {size: 17, mono: true, fill: C.dim}), {op: .35 + .65 * on}); });
  s += badge(60, 302, 'REAL_CONFIG', `fusion.json τ=${TAU} λ=${LAM} · nf.py effective_weight · nf3_conflict_to_uncertainty`, {srcRight: true});
  // worked example (repo numbers)
  const W = ((F.worked_example || {}).value || {}).experts || [];
  const wex = W.map(([n, p, u, r]) => ({name: n, p, u, r, c: 1})), wf = fuse(wex), wsum = wf.w.reduce((a, b) => a + b, 0);
  s += G(R(60, 350, 560, 470) + T(84, 390, 'Worked example (from the code)', {size: 22, w: 700}) +
    wex.map((e, i) => T(84, 440 + i * 70, e.name, {size: 18, w: 600}) + R(84, 452 + i * 70, 280, 18, {rx: 9, fill: '#0A1030'}) + R(84, 452 + i * 70, 280 * e.p, 18, {rx: 9, fill: C.ember, stroke: 'none', op: .35 + wf.w[i] / wsum}) + T(380, 467 + i * 70, `p ${e.p} u ${e.u} r ${e.r} → w ${fmt(wf.w[i], 3)}`, {size: 15, mono: true})).join('') +
    T(84, 680, `fused p̂ = ${fmt(wf.p, 4)} → ${wf.level}`, {size: 26, w: 800, fill: LV[wf.level]}) + T(84, 716, `U* = ${fmt(wf.u, 4)} (≤ 0.6, so not "uncertain")`, {size: 18, mono: true}) +
    T(84, 750, 'the doubtful media check barely counts', {size: 17, fill: C.dim}) + badge(84, 770, 'WORKED', (F.worked_example || {}).source), {op: eo(seg(t, 6, 7.5))});
  // averaging toggle on a hard case
  const names = Object.keys(RULES), k = Math.floor(clamp((t - 16) / 2, 0, names.length - 1));
  const cex = CANON.map(e => ({...e, c: 1}));
  s += G(R(650, 350, 680, 470) + T(674, 390, 'Averaging rule on a hard case', {size: 22, w: 700}) +
    CANON.map((e, i) => T(674, 425 + i * 26, `${e.name}: p ${e.p} · u ${e.u} · r ${e.r}`, {size: 15, mono: true, fill: C.dim})).join('') +
    names.map((n, i) => { const v = RULES[n](cex), on = i === k && t > 16, dropped = RULES[n](cex.filter((_, j) => j !== 2)); const y = 548 + i * 40;
      return T(674, y + 16, n, {size: 17, w: on ? 800 : 500, fill: on ? C.gold : C.text}) + R(900, y, 260, 22, {rx: 11, fill: '#0A1030'}) + R(900, y, 260 * v, 22, {rx: 11, fill: on ? C.gold : C.blue, stroke: 'none', op: on ? 1 : .55}) +
        T(1170, y + 17, `${fmt(v)}  Δout ${fmt(Math.abs(dropped - v))}`, {size: 15, mono: true, fill: on ? C.gold : C.dim}); }).join('') +
    T(674, 805, 'Δout = change if the outlier goes missing (bounded influence check)', {size: 14, fill: C.dim}) + badge(1120, 360, 'WORKED', 'formulas in app.js RULES; FM-1 = repo rule'), {op: eo(seg(t, 14, 15.5))});
  // real reliability diagram
  const zc = cur('zeroshot_threshold'), zr = res('zeroshot');
  s += G(R(1360, 350, 500, 470) + T(1384, 390, 'Calibration on real scores', {size: 22, w: 700}) + (zc ? (() => {
    const bx = 1410, by = 760, bw = 300, bh = 300; let q = L(bx, by, bx + bw, by - bh, {stroke: C.dim, dash: '6 6'}) + L(bx, by, bx + bw, by, {stroke: C.line}) + L(bx, by, bx, by - bh, {stroke: C.line});
    zc.value.reliability.forEach(b => { q += h('circle', {cx: bx + b.conf * bw, cy: by - b.acc * bh, r: 4 + Math.sqrt(b.n) / 4, fill: C.teal, opacity: .85}); });
    return q + T(bx + bw / 2, by + 26, 'predicted p', {size: 14, anchor: 'middle', fill: C.dim}) + T(1384, 430, `zero-shot, ${zc.value.n.toLocaleString('en-IN')} OOF images`, {size: 16, fill: C.dim}) +
      (zr ? T(1384, 455, `ECE raw ${fmt(zr.value.ece_raw, 3)} → cross-fit ${fmt(zr.value.ece_cal, 3)}`, {size: 16, mono: true}) : '') + badge(1384, 470, 'REAL_RESULT', zc.source);
  })() : T(1384, 450, 'NOT FOUND IN REPO', {fill: C.amber})), {op: eo(seg(t, 24, 25.5))});
  return s;
}

/* ======================================================================= S7 physics */
function S7(t) {
  let s = header('S7', 'The physics engine', [2]) + title(60, 130, 'Physics turns rain, slope and pixels into checkable claims') + T(60, 170, 'observables → physics model → predicted state → consistency + validity → fusion', {size: 22, fill: C.dim});
  (D.physics || []).filter(p => p.id !== 'cyclone_holland').forEach((p, i) => {
    const y = 200 + i * 128, o = eo(seg(t, .5 + i * .6, 1.3 + i * .6));
    s += G(R(60, y, 640, 116) + T(80, y + 32, p.name, {size: 19, w: 700}) + clsChip(560 - (CLS[p.class][0].length - 11) * 8, y + 12, p.class) +
      T(80, y + 66, p.equation, {size: 20, math: true}) + T(80, y + 98, (p.parameters[0] ? `${p.parameters[0].note || ''} = ${p.parameters[0].value}` : p.reduction || p.regime).slice(0, 62), {size: 15, mono: true, fill: C.dim}) +
      (p.parameters[0] ? badge(520, y + 82, p.parameters[0].origin, p.parameters[0].source) : ''), {op: o});
  });
  const hc = cur('caine_hist');
  if (hc) {
    const v = hc.value, bx = 760, by = 620, bw = 560, bh = 300, n = v.events.length, mx = Math.max(...v.events.map((e, i) => Math.max(e / 184, v.controls[i] / 552)));
    let q = R(730, 200, 620, 560) + T(756, 240, 'Real data: Caine ratio I / I_thr', {size: 22, w: 700}) + T(756, 268, 'catalogued landslide days vs same-site control days (share of each)', {size: 15, fill: C.dim});
    const o = eo(seg(t, 8, 11));
    v.events.forEach((e, i) => { const x = bx + i / n * bw, w = bw / n - 3, he = e / 184 / mx * bh * o, hc2 = v.controls[i] / 552 / mx * bh * o;
      q += R(x, by - hc2, w / 2, hc2, {rx: 2, fill: C.blue, stroke: 'none', op: .8}) + R(x + w / 2, by - he, w / 2, he, {rx: 2, fill: C.ember, stroke: 'none'}); });
    const x1 = bx + (0 - v.bins_log10[0]) / (v.bins_log10[n] - v.bins_log10[0]) * bw;
    q += L(x1, by - bh - 10, x1, by + 4, {stroke: C.gold, dash: '6 5'}) + T(x1 + 6, by - bh, 'I = I_thr', {size: 14, fill: C.gold}) + L(bx, by, bx + bw, by, {stroke: C.line}) +
      T(bx, by + 26, 'log10 ratio →', {size: 14, fill: C.dim}) + R(bx, by + 44, 14, 14, {rx: 2, fill: C.ember, stroke: 'none'}) + T(bx + 22, by + 56, 'landslide days (184)', {size: 15}) + R(bx + 250, by + 44, 14, 14, {rx: 2, fill: C.blue, stroke: 'none'}) + T(bx + 272, by + 56, 'control days (552)', {size: 15}) +
      badge(756, 700, 'REAL_RESULT', hc.source) + T(900, 717, `AUC ${res('geo_caine_ratio') ? res('geo_caine_ratio').value : '–'} with zero training`, {size: 17, w: 700, fill: C.teal});
    s += G(q, {op: eo(seg(t, 7, 8))});
  }
  const lp = cur('landslide_pair');
  if (lp) {
    const e = lp.value.event, c = lp.value.control, rows = [['day', e.day, c.day], ['3-day rain mm', (+e.rain_3d).toFixed(0), (+c.rain_3d).toFixed(0)], ['7-day rain mm', (+e.rain_7d).toFixed(0), (+c.rain_7d).toFixed(0)], ['Caine ratio', (+e.caine_ratio).toFixed(2), (+c.caine_ratio).toFixed(2)], ['ΔFS', (+e.dfs).toFixed(3), (+c.dfs).toFixed(3)], ['FS (back-analysed)', (+e.fs_backcalc).toFixed(2), (+c.fs_backcalc).toFixed(2)]];
    let q = R(1380, 200, 480, 420) + T(1404, 240, `One real site: ${lp.value.lat}°N ${lp.value.lon}°E`, {size: 20, w: 700}) + T(1404, 266, `slope ${(+e.slope_p90_deg).toFixed(1)}°`, {size: 15, fill: C.dim}) +
      T(1600, 300, 'landslide', {size: 15, fill: C.ember, w: 700}) + T(1740, 300, 'control', {size: 15, fill: C.blue, w: 700});
    rows.forEach((r, i) => q += T(1404, 336 + i * 38, r[0], {size: 16}) + T(1600, 336 + i * 38, r[1], {size: 16, mono: true, fill: C.ember}) + T(1740, 336 + i * 38, r[2], {size: 16, mono: true, fill: C.blue}));
    q += badge(1404, 576, 'REAL_RESULT', lp.source);
    s += G(q, {op: eo(seg(t, 12, 13.5))});
  }
  // reduction to parent + regime meter
  const psi = 1 - eo(seg(t, 20, 27)), beta = 16.5 * Math.PI / 180, dfs = 9.81 * psi * Math.tan(32 * Math.PI / 180) / (19 * 2 * Math.sin(beta) * Math.cos(beta));
  s += G(R(1380, 640, 480, 180) + T(1404, 676, 'ΔFS reduces to its parent', {size: 19, w: 700}) + clsChip(1600, 656, 'B') +
    T(1404, 710, `ψ = ${fmt(psi, 2)} m  →  ΔFS = ${fmt(dfs, 3)}`, {size: 18, mono: true}) + R(1404, 724, 430, 14, {rx: 7, fill: '#0A1030'}) + R(1404, 724, 430 * psi, 14, {rx: 7, fill: C.green, stroke: 'none'}) +
    T(1404, 764, psi < .02 ? 'ψ → 0 ⇒ ΔFS → 0: back to static FS ✓' : 'φ′ 32°, γ 19, z 2 m, β 16.5° (real site)', {size: 15, fill: psi < .02 ? C.teal : C.dim}) +
    T(1404, 796, 'regime: shallow planar slip → inside', {size: 15, fill: C.teal}) + badge(1700, 646, 'WORKED', 'ΔFS formula from data_adapters/build_geo.py'), {op: eo(seg(t, 18, 19.5))});
  return s;
}

/* ======================================================================= S8 cyclone (planned) */
function S8(t) {
  let s = header('S8', 'Cyclone mode · PLANNED', [2, 4]) + title(60, 130, 'Where the same pipeline goes next') + T(60, 170, 'specification only (docs/13): nothing here is implemented or measured', {size: 22, fill: C.dim});
  const cx = 620, cy = 520; let v = '';
  for (let a = 0; a < 6; a++) { let p = ''; for (let i = 0; i < 80; i++) { const th = i / 12 + a * Math.PI / 3 + t * (S.reduced ? 0 : .6), r = 20 + i * 3.6; p += `${cx + r * Math.cos(th)},${cy + r * Math.sin(th) * .8} `; } v += h('polyline', {points: p, fill: 'none', stroke: C.blue, 'stroke-width': 2, opacity: .55}); }
  s += R(120, 220, 1000, 600, {fill: C.panel}) + v + h('circle', {cx, cy, r: 18, fill: C.gold}) + ribbon(120, 220, 1000, 600, 'ILLUSTRATIVE');
  const items = [['Wind profile (Holland 1980)', 'A · verify equation'], ['Public forecasts (IMD RSMC)', 'official bulletins'], ['Ground evidence', 'cameras · flood · debris'], ['Misinformation screen', 'reuse media authenticity'], ['Evacuation planner (RL)', 'advisory only'], ['Human decides', 'tiered alerts via CAP']];
  items.forEach(([a, b], i) => { const y = 230 + i * 98, o = eo(seg(t, 1 + i * .6, 1.8 + i * .6)); s += G(R(1180, y, 680, 84, {stroke: i === 5 ? C.gold : C.line, sw: 2}) + T(1204, y + 36, a, {size: 21, w: 700}) + T(1204, y + 66, b, {size: 16, fill: C.dim}) + chip(1730, y + 14, 'PLANNED', '#E3E6F3'), {op: o}); });
  return s;
}

/* ======================================================================= S9 proof, honesty */
function S9(t) {
  let s = header('S9', 'Proof · honesty · next', [5]) + title(60, 130, 'Only measured numbers. Pending stays pending.');
  const g = k => res(k) ? res(k).value : '–', zs = res('zeroshot'), rl = res('rl_env');
  const rows = [['Landslide physics, Caine, zero training', g('geo_caine_ratio'), 'C3'], ['Landslide physics, ΔFS, zero training', g('geo_dFS_iverson'), 'C3'], ['Trained rain-only model', g('geo_logit_rain'), 'C3'],
    ['Rain + physics logistic', g('geo_logit_hybrid'), 'C3'], ['Geo-PINN (not admitted)', g('geo_pinn'), 'C3'], ['Zero-shot CLIP AUC (not admitted)', zs ? zs.value.oof_auc : '–', 'C3'],
    ['RL (CQL) vs physics rule, C_miss 5000 → not deployed', rl && rl.value['5000'] ? `${rl.value['5000'].cql_learned} / ${rl.value['5000'].physics_rule}` : '–', 'C3']];
  s += R(60, 170, 1080, 520) + T(84, 210, 'Results (REAL RESULT, from results/)', {size: 22, w: 700});
  rows.forEach(([a, b, k], i) => { const o = eo(seg(t, .3 + i * .3, .9 + i * .3)); s += G(T(84, 256 + i * 52, a, {size: 19}) + T(760, 256 + i * 52, String(b), {size: 20, mono: true, w: 700, fill: C.teal}) + ladder(980, 238 + i * 52, k), {op: o}); });
  s += T(84, 640, 'Fire CNN · media · EO · fusion · landslide meta-fusion:', {size: 18}) + pending(600, 622) + badge(760, 622, 'REAL_RESULT', 'TRINETRA/results/ · docs/14_RESULTS_LOG.md', {srcRight: true});
  s += G(R(1170, 170, 690, 330) + T(1194, 210, 'What we do NOT claim', {size: 22, w: 700, fill: C.amber}) +
    ['No matched-protocol SOTA comparison yet (no C4)', 'Small prototype subsets; not full benchmarks', 'Physics beats rain: not proven (CI includes 0)', 'Simulator ≠ field; no field trial yet', 'Class C hypotheses stay OFF until validated'].map((x, i) => T(1194, 252 + i * 46, '• ' + x, {size: 18})).join(''), {op: eo(seg(t, 3, 4))});
  s += G(R(1170, 520, 690, 170, {stroke: C.teal, sw: 2}) + TW(1194, 562, 'TRINETRA complements certified fire alarms and official IMD / NDMA warnings; it never replaces them. A human approves every public alert.', 58, {size: 19, w: 600}), {op: eo(seg(t, 6, 7))});
  const close = 1 - eo(seg(t, 12, 14.5));
  [760, 960, 1160].forEach(x => s += eye(x, 800, 150, Math.max(.02, close)));
  s += G(T(960, 880, 'github.com/saksham1253/TRINETRA-CONTENT-OG · Team SANKAT MOCHAK · GEHU Dehradun', {size: 18, anchor: 'middle', fill: C.dim, mono: true}), {op: seg(t, 9, 10)});
  return s;
}

/* ---- SYSTEM · DFD L0/L1 with live packets (time-driven so it works in the play timeline, Explore and record mode) */
const DK = {bg: '#11161D', bar: '#1A2029', box: '#0D1117', ink: '#F0F3F6', sub: '#A9B1BD', edge: '#8B949E',
  blue: '#5B8DEF', orange: '#F0703A', teal: '#2EC4B6', amber: '#F2B705', violet: '#A78BFA', red: '#F0533F', grey: '#9AA4B2'};
const DFD_P = 8;                                                     // seconds per full source→alert cycle
const bz = (a, b, c, d, u) => { const v = 1 - u; return v * v * v * a + 3 * v * v * u * b + 3 * v * u * u * c + u * u * u * d; };
// edge = list of segments; each seg is [x0,y0,x1,y1] (straight) or [x0,y0,c1x,c1y,c2x,c2y,x1,y1] (cubic)
const hz = (x0, y0, x1, y1) => { const k = Math.max(30, (x1 - x0) * .45); return [x0, y0, x0 + k, y0, x1 - k, y1, x1, y1]; };
const segD = sg => sg.length === 4 ? `L${sg[2]},${sg[3]}` : `C${sg[2]},${sg[3]} ${sg[4]},${sg[5]} ${sg[6]},${sg[7]}`;
function segAt(sg, u) { if (sg.length === 4) return [lerp(sg[0], sg[2], u), lerp(sg[1], sg[3], u)]; return [bz(sg[0], sg[2], sg[4], sg[6], u), bz(sg[1], sg[3], sg[5], sg[7], u)]; }
function edgeAt(segs, u) { const n = segs.length, k = Math.min(n - 1, Math.floor(u * n)); return segAt(segs[k], u * n - k); }
function dfdScene(tm) {
  const box = (x, y, w, hh, t, sub, c, o = {}) => { const glow = o.glow || 0;
    return (glow > 0 ? `<rect x="${x - 5}" y="${y - 5}" width="${w + 10}" height="${hh + 10}" rx="14" fill="none" stroke="${c}" stroke-width="${2 + 6 * glow}" opacity="${.45 * glow}"/>` : '') +
      `<rect x="${x}" y="${y}" width="${w}" height="${hh}" rx="10" fill="${DK.box}" stroke="${c}" stroke-width="2.6"${o.dash ? ' stroke-dasharray="9 6"' : ''}/>` +
      t.map((ln, i) => `<text x="${x + 18}" y="${y + 36 + i * 27}" font-size="23" font-weight="700" fill="${DK.ink}" font-family="Inter,'IBM Plex Sans',sans-serif">${ln}</text>`).join('') +
      sub.map((ln, i) => `<text x="${x + 18}" y="${y + 40 + t.length * 27 + i * 22}" font-size="17" fill="${DK.sub}" font-family="'JetBrains Mono','IBM Plex Mono',monospace">${ln}</text>`).join(''); };
  const ph = (s, d) => { const q = (((tm - s) % DFD_P) + DFD_P) % DFD_P; return q < d ? q / d : -1; };   // −1 = no packet now
  const glowAt = s => { const q = (((tm - s) % DFD_P) + DFD_P) % DFD_P; return q < .7 ? 1 - q / .7 : 0; };
  const lab = (x, y, t, c = DK.sub, a = 'start') => `<text x="${x}" y="${y}" font-size="17" fill="${c}" text-anchor="${a}" font-family="'JetBrains Mono',monospace" style="paint-order:stroke;stroke:${DK.bg};stroke-width:5">${t}</text>`;
  let edges = '', pk = '';
  const E2 = (segs, c, s, d, tag, waves = 2, w = 2.2) => {
    edges += `<path d="M${segs[0][0]},${segs[0][1]} ${segs.map(segD).join(' ')}" fill="none" stroke="${c}" stroke-width="${w}" opacity=".75" marker-end="url(#dfA${c.slice(1)})"/>`;
    for (let k = 0; k < waves; k++) { const u = ph(s + k * DFD_P / waves, d); if (u < 0) continue;
      for (let j = 4; j >= 0; j--) { const uu = u - j * .035; if (uu < 0) continue; const [x, y] = edgeAt(segs, uu);
        pk += `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${j ? 6 - j : 7}" fill="${c}" opacity="${j ? .5 - j * .1 : 1}"${j ? '' : ' stroke="#fff" stroke-width="1.6"'}/>`; }
      if (tag) { const [x, y] = edgeAt(segs, u); pk += `<text x="${(x + 11).toFixed(1)}" y="${(y - 11).toFixed(1)}" font-size="15" font-weight="800" fill="${c}" font-family="'JetBrains Mono',monospace" style="paint-order:stroke;stroke:${DK.bg};stroke-width:5">${tag}</text>`; } } };
  // ---- layout (1920×1080)
  const SRC = [[150, ['CCTV / video'], ['frames, clips'], DK.blue], [290, ['Satellite +', 'weather'], ['S1/S2, FIRMS, POWER, DEM'], DK.blue],
    [430, ['Media + text'], ['posts (text model', 'PLANNED)'], DK.blue, 1], [570, ['Sensor streams'], ['generic numeric input'], DK.blue]];
  const EXP = [[120, ['Fire CNN + temporal'], ['fire_cnn · ws4_cctv']], [240, ['Zero-shot CLIP'], ['kaggle/eval_zeroshot']], [360, ['Media check'], ['deepfake_net, r ≤ 0.4']],
    [480, ['EO heads'], ['S1 · S2 · InSAR']], [600, ['Anomaly layer'], ['ws8_anomaly']]];
  // edges with schedule (start s, duration d inside the 8 s cycle)
  SRC.forEach(([y], i) => E2([hz(320, y + 55, 376, 430)], DK.grey, 0 + i * .12, 1, i === 0 ? 'x' : ''));
  EXP.forEach(([y], i) => E2([hz(610, 430, 676, y + 52)], DK.grey, 1.1 + i * .08, .9, i === 0 ? 'clean' : ''));
  E2([hz(1000, 172, 1056, 240)], DK.grey, 2.1, .9, '');                                   // fire → physics
  EXP.forEach(([y], i) => E2([hz(1000, y + 52, 1056, 530)], DK.teal, 2.1 + i * .08, 1.1, i === 1 ? 'pᵢ,uᵢ' : ''));
  E2([[1210, 330, 1210, 436]], DK.grey, 3.2, .7, '', 2);
  E2([hz(1360, 240, 1416, 410)], DK.grey, 3.2, .9, '');
  E2([hz(1360, 530, 1416, 410)], DK.teal, 3.6, .8, 'p̂,U*', 2, 2.6);
  E2([hz(1680, 410, 1726, 215)], DK.amber, 4.5, .7, 'level');
  E2([[1815, 280, 1815, 326]], DK.amber, 5.3, .5, 'token');
  E2([hz(1680, 410, 1726, 625)], DK.violet, 4.5, .8, 'state');
  // last mile: alert bus to the offline strip
  const bus = [[1730, 430, 1705, 430], [1705, 430, 1705, 770], [1705, 770, 160, 770], [160, 770, 160, 791]];
  E2(bus, DK.red, 5.8, 1.6, 'CAP', 1, 2.6);
  const SX = i => 30 + i * 235, SW = 215;                            // single-row strip: 8 boxes
  E2([[1705, 770, 1782, 770], [1782, 770, 1782, 791]], DK.grey, 6.1, .5, '', 1); E2([[SX(6) + 107, 770, SX(6) + 107, 791]], DK.blue, 6.4, .5, '', 1);
  for (let i = 0; i < 3; i++) E2([hz(SX(i) + SW, 833, SX(i + 1) - 4, 833)], i ? DK.teal : DK.red, 7.3 + i * .4, .4, i === 1 ? 'SF10' : '', 1);
  E2([[SX(2) + 107, 875, SX(2) + 107, 892], [SX(2) + 107, 892, SX(4) + 107, 892], [SX(4) + 107, 892, SX(4) + 107, 879]], DK.amber, 8.5, .7, '', 1);
  E2([hz(SX(4) + SW, 833, SX(5) - 4, 833)], DK.orange, 9.2, 1.2, 'walk', 1);
  // ---- nodes (glow when their packet arrives)
  let n = '';
  SRC.forEach(([y, t, sub, c, dash], i) => n += box(30, y, 290, 110, t, sub, c, {dash, glow: glowAt(-.6 + i * .12)}));
  n += box(380, 330, 230, 200, ['Adapters'], ['data_adapters/', 'group splits,', 'dedupe'], DK.grey, {glow: glowAt(1)});
  EXP.forEach(([y, t, sub], i) => n += box(680, y, 320, 104, t, sub, DK.orange, {glow: glowAt(2 + i * .08)}));
  n += box(1060, 150, 300, 180, ['Physics engine'], ['fire_gate · geo_gate:', 'FS, Iverson, Caine'], DK.blue, {glow: glowAt(3)});
  n += box(1060, 440, 300, 180, ['Meta-fusion'], ['calibrate → weight →', 'FM-1 → U*, S'], DK.teal, {glow: glowAt(3.5)});
  n += box(1420, 320, 260, 180, ['Decision'], ['decide() + shield', '(raise-only)'], DK.amber, {glow: glowAt(4.4)});
  n += box(1730, 150, 170, 130, ['Human', 'review'], ['ws3_alert/', 'operator'], DK.amber, {glow: glowAt(5.2)});
  n += box(1730, 330, 170, 130, ['Alerts'], ['cap.py · dtn', '(offline)'], DK.amber, {glow: glowAt(5.8)});
  n += box(1730, 560, 170, 130, ['RL advisory'], ['env_landslide', 'CQL + gate'], DK.violet, {glow: glowAt(5.3)});
  // strip
  n += `<text x="30" y="752" font-size="18" font-weight="800" fill="${DK.red}" font-family="'JetBrains Mono',monospace">LAST MILE · internet OFF · sab channel parallel, jo pehle pahunche · ranges = planning model</text>`;
  [['D3 queue', 'DTN · data mule', DK.red, 7.3], ['Gateway', 'battery · LoRa', DK.red, 7.7], ['Ridge relays', '865–867 MHz', DK.teal, 8.1], ['Village pager', 'buzzer · text', DK.teal, 8.5],
   ['Siren', '~1.6 km model', DK.amber, 9.2], ['Human runner', 'Aapda Mitra', DK.orange, 10.4], ['Satellite msg', 'no ground net', DK.blue, 6.9], ['Cell / FM', 'only if up', DK.grey, 6.6, 1]]
    .forEach(([t, sub, c, g, dash], i) => n += box(SX(i), 795, SW, 80, [t], [sub], c, {dash, glow: glowAt(g)}));
  // static labels like the reference
  const L = lab(1372, 200, 'FS floor') + lab(1222, 395, 'c_i') + lab(1368, 492, 'p̂, U*', DK.teal) + lab(1690, 205, 'level', DK.sub, 'start') + lab(1828, 310, 'approved') + lab(1690, 590, 'state') + lab(1010, 405, 'r↓');
  const mk = c => `<marker id="dfA${c.slice(1)}" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12z" fill="${c}"/></marker>`;
  const head = `<rect width="1920" height="1080" fill="${DK.bg}"/><rect width="1920" height="64" fill="${DK.bar}"/><rect x="24" y="17" width="8" height="30" rx="2" fill="${DK.orange}"/>` +
    `<text x="46" y="44" font-size="30" font-weight="800" fill="${DK.ink}" font-family="'JetBrains Mono',monospace" letter-spacing="1">SYSTEM · DFD L0/L1 · LIVE</text>` +
    `<text x="1890" y="42" font-size="17" fill="${DK.sub}" text-anchor="end" font-family="'JetBrains Mono',monospace">dot = data packet · dashed = planned/conditional</text>` ;
  return `<defs>${[DK.grey, DK.teal, DK.amber, DK.violet, DK.red, DK.blue, DK.orange].map(mk).join('')}</defs>` + head + edges + n + L + pk;
}
function SD(t) { return dfdScene(t); }

/* ======================================================================= engine */
const SCENES = (SCRIPT.scenes || []).map(sc => ({...sc, fn: {S0, S1, S2, SD, S3, S4, S5, S6, S7, S8, S9}[sc.id]}));
const TOTAL = SCENES.reduce((a, s) => Math.max(a, s.t0 + s.dur), 0) || 295;
const stage = document.getElementById('stage'), capEl = document.getElementById('cap');
const E = {t: 0, playing: !Q.has('paused'), speed: 1, last: performance.now(), fpsN: 0, fpsT: 0, lastSvg: ''};
const DEFS = `<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="${C.dim}"/></marker>
<radialGradient id="bgG" cx="50%" cy="40%" r="75%"><stop offset="0%" stop-color="#16236A"/><stop offset="100%" stop-color="#070C28"/></radialGradient></defs>`;
const sceneAt = t => SCENES.find(s => t >= s.t0 && t < s.t0 + s.dur) || SCENES[SCENES.length - 1];
function render(t) {
  const sc = sceneAt(t); if (!sc) return;
  const lt = t - sc.t0;
  let body = '';
  try { body = sc.fn ? sc.fn(lt) : ''; } catch (err) { body = T(80, 300, 'render error in ' + sc.id + ': ' + err.message, {fill: C.red}); console.error(err); }
  const fadeIn = seg(lt, 0, .6), fadeOut = 1 - seg(lt, sc.dur - .5, sc.dur);
  const svg = DEFS + R(0, 0, 1920, 1080, {rx: 0, fill: 'url(#bgG)', stroke: 'none'}) + h('rect', {x: 0, y: 0, width: 1920, height: 6, fill: C.saffron}) +
    G(body, {op: S.reduced ? 1 : Math.min(fadeIn, fadeOut)}) + T(1880, 1060, `${sc.id} · ${fmtT(t)}`, {size: 13, anchor: 'end', fill: '#6F7BB8', mono: true});
  if (svg !== E.lastSvg) { stage.innerHTML = svg; E.lastSvg = svg; }
  // captions
  let c = '';
  if (S.lang !== 'off') for (const k of sc.captions || []) if (lt >= k.t) c = k[S.lang] || k.en;
  if (capEl.textContent !== c) capEl.textContent = c;
  document.getElementById('time').textContent = `${fmtT(t)} / ${fmtT(TOTAL)}`;
  document.getElementById('scene').textContent = `${sc.id} ${sc.name}`;
  document.querySelector('#scrub .fill').style.width = `${t / TOTAL * 100}%`;
}
const fmtT = t => `${Math.floor(t / 60)}:${String(Math.floor(t % 60)).padStart(2, '0')}`;
function seek(t) { E.t = clamp(t, 0, TOTAL - .001); render(E.t); }
function loop(now) {
  const dt = Math.min(.1, (now - E.last) / 1000); E.last = now;
  if (E.playing && !RECORD) { E.t += dt * E.speed; if (E.t >= TOTAL) { E.t = TOTAL - .001; E.playing = false; setPlay(); if (!Q.has('noexplore')) openExplore(); } render(E.t); }
  E.fpsN++; E.fpsT += dt; if (E.fpsT > 2) { const fps = E.fpsN / E.fpsT; if (fps < 45 && !S.lowfx && E.playing) { S.lowfx = true; console.info('[anim] fps', fps.toFixed(0), '→ reduced effects'); } E.fpsN = 0; E.fpsT = 0; }
  requestAnimationFrame(loop);
}
// record mode: frame-exact, deterministic; a recorder calls window.__TRINETRA_SEEK(t) then captures the frame
window.__TRINETRA_SEEK = t => { seek(t); return true; };
window.__TRINETRA_TOTAL = TOTAL;

/* ======================================================================= controls */
const $ = id => document.getElementById(id);
function setPlay() { $('b-play').textContent = E.playing ? 'Pause' : 'Play'; }
function jump(d) { const i = SCENES.indexOf(sceneAt(E.t)); const j = clamp(i + d, 0, SCENES.length - 1); seek(SCENES[j].t0 + .01); }
function toggle(btn, key, cls) { S[key] = !S[key]; $(btn).setAttribute('aria-pressed', S[key]); if (cls) document.body.classList.toggle(cls, S[key]); E.lastSvg = ''; render(E.t); }
$('b-play').onclick = () => { if (E.t >= TOTAL - .01) E.t = 0; E.playing = !E.playing; setPlay(); };
$('b-prev').onclick = () => jump(-1); $('b-next').onclick = () => jump(1);
$('b-speed').onchange = e => E.speed = +e.target.value;
$('b-cap').onchange = e => { S.lang = e.target.value; render(E.t); };
$('b-src').onclick = () => toggle('b-src', 'showSrc');
$('b-rm').onclick = () => toggle('b-rm', 'reduced');
$('b-pres').onclick = () => toggle('b-pres', 'presenter', 'presenter');
$('b-ex').onclick = () => openExplore();
$('b-fs').onclick = () => (document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()).catch(() => {});
const scrub = $('scrub');
SCENES.forEach(sc => { const m = document.createElement('div'); m.className = 'mk'; m.style.left = `${sc.t0 / TOTAL * 100}%`; m.innerHTML = `<span>${sc.id}</span>`; m.title = sc.name; scrub.appendChild(m); });
const scrubTo = e => { const r = scrub.getBoundingClientRect(); seek(clamp((e.clientX - r.left) / r.width) * TOTAL); };
scrub.onpointerdown = e => { scrubTo(e); scrub.setPointerCapture(e.pointerId); scrub.onpointermove = scrubTo; };
scrub.onpointerup = () => scrub.onpointermove = null;
addEventListener('keydown', e => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
  const k = e.key.toLowerCase();
  if (k === ' ') { e.preventDefault(); $('b-play').click(); }
  else if (k === 'arrowright') jump(1); else if (k === 'arrowleft') jump(-1);
  else if (k === 's') $('b-src').click(); else if (k === 'm') $('b-rm').click(); else if (k === 'p') $('b-pres').click();
  else if (k === 'f') $('b-fs').click(); else if (k === 'c') { const sel = $('b-cap'); sel.selectedIndex = (sel.selectedIndex + 1) % 3; sel.onchange({target: sel}); }
  else if (k === 'e') (document.body.classList.contains('exploring') ? closeExplore() : openExplore());
  else if (k === 'escape') { closeVideo(); closeExplore(); }
});
if (RECORD) { document.body.classList.add('record'); E.playing = false; }
if (S.reduced) $('b-rm').setAttribute('aria-pressed', 'true');
if (Q.has('t')) seek(+Q.get('t')); else seek(0);
setPlay(); requestAnimationFrame(loop);

/* ======================================================================= explore mode */
const OB = (o, src) => `<span class="chip o-${o}">${(ORIGIN[o] || ORIGIN.ILLUSTRATIVE)[0]}</span>${src ? `<div class="src mono">${esc(src)}</div>` : ''}`;
const side = html => { $('ex-side').innerHTML = html; };
let __dfdStop = null;

/* ---- Last Mile: offline alert ladder (data precomputed by ws3_alert/last_mile.py via ANIM/tools/extract_last_mile.py) */
const LM = window.LAST_MILE || null;
const LM_T = {satellite: 1, cell: 0, fm: 0, fail_R1: 0, fail_R2: 0, upgrades: 0};
const LM_LABEL = {satellite: 'Satellite messaging up', cell: 'Cell towers up', fm: 'FM / community radio up', fail_R1: 'Fail ridge relay R1', fail_R2: 'Fail ridge relay R2', upgrades: 'Add 3 suggested pagers'};
const lmColor = ch => ch.startsWith('LoRa') ? C.teal : ch.startsWith('siren') ? C.amber : ch.startsWith('satellite') ? C.blue : ch.startsWith('runner') ? C.ember : ch === 'none' ? C.red : C.gold;
function renderLastMile(svg, tm) {
  const key = LM.toggles.map(k => LM_T[k]).join(''), cb = LM.combos[key], DL = LM.params.deadline_min;
  const X = x => 60 + x * 54, Y = y => 520 - y * 52, pos = {};
  LM.nodes.forEach(n => pos[n.id] = [X(n.x_km), Y(n.y_km)]); LM.villages.forEach(v => pos[v.id] = [X(v.x_km), Y(v.y_km)]);
  const clock = (tm % 14) / 12 * (DL + 2);                          // sim minutes: 0 → 12 over 12 s, then hold
  let q = DEFS + R(0, 0, 1500, 800, {rx: 0, fill: '#080E30', stroke: 'none'}) +
    T(36, 42, 'LAST MILE · INTERNET OFF · WHO HEARS THE WARNING, HOW, AND WHEN?', {size: 20, w: 800, fill: C.gold, mono: true}) +
    T(36, 70, 'Synthetic hill valley (not a real map). Each dot = a village; colour = first channel that reaches it after operator approval.', {size: 15, fill: C.dim});
  // ridge silhouette
  q += h('path', {d: 'M40,560 L180,330 L330,470 L410,300 L560,450 L760,250 L900,420 L1050,280 L1250,460 L1440,330 L1440,600 L40,600Z', fill: '#0E1747', stroke: C.line});
  // siren audible radius + Bluetooth scale reference
  LM.nodes.filter(n => n.kind === 'siren').forEach(n => { const on = !cb.mesh_unreachable.includes(n.id);
    q += h('circle', {cx: pos[n.id][0], cy: pos[n.id][1], r: LM.physics.siren_radius_m / 1000 * 54, fill: on ? 'rgba(255,176,32,.10)' : 'none', stroke: on ? C.amber : C.red, 'stroke-dasharray': '5 4'}); });
  // mesh + runner paths with moving packets
  cb.villages.forEach(v => { if (!v.path.length || v.min === null) return; const pts = v.path.map(id => pos[id]).filter(Boolean); if (pts.length < 2) return;
    const runner = v.ch.startsWith('runner'), col = lmColor(v.ch);
    q += h('polyline', {points: pts.map(p => p.join(',')).join(' '), fill: 'none', stroke: col, 'stroke-width': runner ? 2 : 2.5, 'stroke-dasharray': runner ? '3 6' : undefined, opacity: .75});
    const src = runner ? (cb.villages.find(x => x.id === v.path[0]) || {min: 0}).min || 0 : 0, f = runner ? Math.min(1, Math.max(0, (clock - src) / Math.max(.01, v.min - src))) : (tm * .6) % 1;
    const a = pts[pts.length - 2], b = pts[pts.length - 1];
    if (!runner || f < 1) q += h('circle', {cx: lerp(a[0], b[0], f), cy: lerp(a[1], b[1], f), r: runner ? 6 : 5, fill: col, stroke: '#fff', 'stroke-width': 1.2}); });
  // satellite beam
  if (LM_T.satellite) cb.villages.filter(v => v.ch.startsWith('satellite')).forEach(v => { q += L(pos[v.id][0], 95, pos[v.id][0], pos[v.id][1] - 12, {stroke: C.blue, sw: 2, dash: '2 6'}) + T(pos[v.id][0], 90, 'SAT', {size: 11, fill: C.blue, anchor: 'middle', mono: true}); });
  // nodes
  LM.nodes.forEach(n => { const [x, y] = pos[n.id], dead = (n.id === 'R1-ridge' && LM_T.fail_R1) || (n.id === 'R2-ridge' && LM_T.fail_R2), cut = cb.mesh_unreachable.includes(n.id);
    const col = dead || cut ? C.red : n.kind === 'gateway' ? C.gold : n.kind === 'relay' ? C.teal : C.amber;
    q += (n.kind === 'siren' ? h('polygon', {points: `${x},${y - 11} ${x + 10},${y + 8} ${x - 10},${y + 8}`, fill: col}) : R(x - 9, y - 9, 18, 18, {rx: 3, fill: col, stroke: '#fff'})) +
      T(x, y - 16, n.id + (dead ? ' ✕' : cut ? ' (no link)' : ''), {size: 12, w: 700, fill: col, anchor: 'middle', mono: true}); });
  // villages
  cb.villages.forEach((v, i) => { const V0 = LM.villages[i], [x, y] = pos[v.id], lit = v.min !== null && clock >= v.min, late = v.min === null || v.min > DL;
    const r = 7 + Math.sqrt(V0.population) / 4, col = lmColor(v.ch);
    q += h('circle', {cx: x, cy: y, r, fill: lit ? col : '#1C2868', stroke: late ? C.red : col, 'stroke-width': late ? 3 : 2}) +
      h('circle', {cx: x, cy: y, r: 100 / 1000 * 54 + .8, fill: 'none', stroke: '#fff', opacity: .6}) +
      T(x, y + r + 15, v.id, {size: 12, w: 700, anchor: 'middle'}) +
      T(x, y + r + 29, v.min === null ? 'unreached' : (v.min < 1 ? `${Math.round(v.min * 60)} s` : `${v.min.toFixed(0)} min`), {size: 11, anchor: 'middle', fill: late ? C.red : C.dim, mono: true}); });
  // clock + legend + scale
  q += R(36, 610, 1400, 60, {rx: 8, fill: '#101A4A', stroke: C.line}) + T(56, 646, `sim clock ${clock.toFixed(1)} min · deadline ${DL} min`, {size: 15, w: 800, fill: C.gold, mono: true});
  [['LoRa pager', C.teal], ['siren', C.amber], ['satellite msg', C.blue], ['cell / FM', C.gold], ['human runner', C.ember], ['late / unreached', C.red]].forEach(([l, c], i) =>
    q += h('circle', {cx: 470 + i * 160, cy: 641, r: 7, fill: c}) + T(484 + i * 160, 646, l, {size: 13}));
  q += L(60, 700, 60 + 54 * 5, 700, {stroke: C.dim, sw: 2}) + T(60, 722, '5 km', {size: 12, fill: C.dim, mono: true}) +
    T(360, 722, `tiny white ring = Bluetooth ~${LM.physics.bluetooth_range_m} m · dashed amber = siren ${LM.physics.siren_radius_m} m (70 dB) · LoRa hop ≤ ${LM.physics.range_km.hill_forest} km hill / ${LM.physics.range_km.valley_nlos} km valley`, {size: 12, fill: C.dim});
  svg.innerHTML = q;
}
function lastMileSide() {
  const cb = LM.combos[LM.toggles.map(k => LM_T[k]).join('')], s = cb.summary;
  side(`<h3>Alert ladder (no internet)</h3><p>Every channel is tried in parallel; the earliest wins and a human runner is always the floor.</p>` +
    LM.toggles.map(k => `<label style="display:block;margin:4px 0"><input type="checkbox" data-lm="${k}" ${LM_T[k] ? 'checked' : ''}> ${LM_LABEL[k]}</label>`).join('') +
    `<p><b>${Math.round(s.share_population_by_deadline * 100)}%</b> of ${s.population} people warned within ${LM.params.deadline_min} min (${s.reached_by_deadline}/${s.villages} villages).</p>` +
    `<p>Late / unreached: <b>${s.late_or_unreached.join(', ') || 'none'}</b></p>` +
    (cb.mesh_unreachable.length ? `<p>Mesh cannot reach: <b>${cb.mesh_unreachable.join(', ')}</b> — add a relay with line of sight.</p>` : '') +
    `<p>Single points of failure: ${Object.entries(LM.spof).map(([k, v]) => `<b>${k}</b> → ${v.join(', ')}`).join('; ')}. Fix: second gateway on another power/backhaul path.</p>` +
    `<p>Planner suggests pagers in: ${LM.upgrades.map(u => `${u.village} (+${u.population_gained})`).join(', ')}.</p>` +
    `<p class="k">LoRa SF${LM.params.sf}, ${LM.params.payload_bytes}-byte frame = ${LM.physics.airtime_ms} ms airtime. Terrain exponents are assumptions; a site survey must calibrate them. Public alerts still need operator approval.</p>` +
    OB('ILLUSTRATIVE', 'TRINETRA/trinetra/src/trinetra/ws3_alert/last_mile.py · results/last_mile_demo.json'));
  $('ex-side').querySelectorAll('[data-lm]').forEach(i => i.onchange = () => { LM_T[i.dataset.lm] = i.checked ? 1 : 0; lastMileSide(); });
}
const TABS = {
  'DFD Live'() {
    $('ex-main').innerHTML = `<div class="card" style="padding:0;overflow:hidden;background:#11161D"><svg id="dfd-live" viewBox="0 0 1920 1080" width="100%" aria-label="Animated system DFD Level 0/1 with live packets"></svg></div>`;
    side('<h3>DFD kaise padhein</h3><p>Left se right: <b>sources → adapters → 5 experts → physics + meta-fusion → decision → human review → alerts</b>. Har chalta dot ek data packet hai; tag batata hai usme kya hai: <span class="mono">pᵢ,uᵢ</span> expert ki probability/uncertainty, <span class="mono">cᵢ</span> physics consistency, <span class="mono">p̂,U*</span> fused risk, <span class="mono">level</span>, <span class="mono">token</span> operator ka signature.</p><p>Box chamakta hai jab packet pahunchta hai. Neeche red bus: internet band ho to alert offline queue → gateway → LoRa relays → pager / siren → runner; satellite aur cell/FM taps alag.</p>'+OB('REAL_CONFIG','src/trinetra/* · ws3_alert/last_mile.py'));
    const svg = $('dfd-live'), start = performance.now(); let dead = false;
    const tick = now => { if (dead) return; svg.innerHTML = dfdScene((now - start) / 1000); requestAnimationFrame(tick); }; requestAnimationFrame(tick);
    __dfdStop = () => { dead = true };
  },
  'Last Mile'() {
    if (!LM) { $('ex-main').innerHTML = '<p>Run TRINETRA/ANIM/tools/extract_last_mile.py to generate data/last_mile.js.</p>'; return; }
    $('ex-main').innerHTML = `<div class="card"><svg id="lm-live" viewBox="0 0 1500 740" width="100%" aria-label="Animated last-mile offline alert coverage"></svg></div>`;
    lastMileSide();
    const svg = $('lm-live'), start = performance.now(); let dead = false;
    const tick = now => { if (dead) return; renderLastMile(svg, (now - start) / 1000); requestAnimationFrame(tick); }; requestAnimationFrame(tick);
    __dfdStop = () => { dead = true };
  },
  Pipeline() {
    const byL = LAYERS.map((l, i) => (D.modules || []).filter(m => m.layer === l));
    let svg = `<svg viewBox="0 0 1200 760" width="100%" style="max-width:1200px">`;
    byL.forEach((ms, i) => { const y = 20 + i * 122;
      svg += R(10, y, 1180, 108, {fill: 'rgba(22,32,90,.6)'}) + T(30, y + 32, `${i + 1} ${LAYERS[i]}`, {size: 18, w: 800, fill: C.gold, mono: true});
      const bw = Math.min(230, (1180 - 210) / Math.max(1, ms.length) - 12);
      ms.forEach((m, j) => { const x = 210 + j * (bw + 12); svg += `<g class="node" data-mod="${m.id}">` + R(x, y + 8, bw, 94, {fill: C.panel2, stroke: m.status === 'PLANNED' ? C.amber : C.teal, dash: m.status === 'PLANNED' ? '6 4' : undefined}) +
        TW(x + 12, y + 32, m.name, Math.floor(bw / 9.4), {size: bw < 200 ? 13 : 15, w: 700, lh: bw < 200 ? 15 : 19}) + T(x + 12, y + 94, m.status, {size: 12, fill: m.status === 'PLANNED' ? C.amber : C.teal, mono: true}) + '</g>'; });
      if (i < 5) svg += L(600, y + 108, 600, y + 122, {stroke: C.saffron, sw: 3});
    });
    $('ex-main').innerHTML = svg + '</svg><p class="k">Click a module. Solid teal = implemented in the repo; dashed amber = planned.</p>';
    $('ex-main').querySelectorAll('[data-mod]').forEach(g => g.onclick = () => {
      const m = D.modules.find(x => x.id === g.dataset.mod); const ph = (D.physics || []).find(p => m.id.includes(p.id));
      side(`<h3>${esc(m.name)}</h3><p>${m.status} · layer ${m.layer}</p><p class="src mono">${esc(m.file)}</p>${OB('REAL_CONFIG', m.file)}` +
        (m.id === 'fusion' || m.id === 'decision' ? `<div class="card"><b>Rules</b><br>${['weight_rule', 'u_star_rule', 'consistency_rule', 'tiers', 'uncertain_threshold', 'p_star'].map(k => F[k] ? `${esc(k)}: <span class="mono">${esc(F[k].value)}</span>${OB(F[k].origin, F[k].source)}` : '').join('<br>')}</div>` : '') +
        (ph ? `<div class="card"><b>${esc(ph.equation)}</b> · class ${ph.class}<br>${ph.symbols.map(s => `${esc(s[0])} = ${esc(s[1])} [${esc(s[2])}]`).join('<br>')}<br>regime: ${esc(ph.regime)}</div>` : '') +
        `<p class="k">What it does, in plain words, is shown in the film scene for this layer; the file path above is the source of truth.</p>`);
    });
  },
  Datasets() {
    $('ex-main').innerHTML = `<table><tr><th>ID</th><th>Dataset</th><th>Role</th><th>Full</th><th>Subset</th><th>Licence</th></tr>${(D.datasets || []).map((d, i) => `<tr class="click" data-i="${i}"><td class="mono">${esc(d.id)}</td><td>${esc(d.name)}</td><td>${esc(d.role)}</td><td>${esc(d.size_full)}</td><td>${esc(d.size_subset)}</td><td>${esc(d.license)}</td></tr>`).join('')}</table>`;
    $('ex-main').querySelectorAll('tr[data-i]').forEach(r => r.onclick = () => { const d = D.datasets[+r.dataset.i];
      side(`<h3>${esc(d.name)}</h3>${OB(d.origin, d.source)}<div class="card"><b>Link</b><br><span class="mono src">${esc(d.link)}</span></div><div class="card"><b>Feeds</b> ${esc(d.modules)}<br><b>Task</b> ${esc(d.task)}<br><b>Role</b> ${esc(d.role)}</div>` +
        `<div class="card"><b>Size</b> full ${esc(d.size_full)} · subset ${esc(d.size_subset)}<br><b>Licence</b> ${esc(d.license)}</div><div class="card"><b>Known issues</b><br>${esc(d.known_issues)}<br><b>What we do</b><br><span class="mono src">${esc(d.mitigation)}</span></div><p class="k">${esc(d.status)}</p>`); });
  },
  Surveys() {
    $('ex-main').innerHTML = `<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(340px,1fr))">${(D.surveys || []).map(v => `<div class="card"><div style="font-size:34px;font-weight:800;color:${C.gold}">${esc(v.value)}</div><div>${esc(v.label)}</div><div class="src">${esc(v.source)}</div>${OB('PAPER')}<span class="chip ${v.confidence === 'A' ? 'o-REAL_RESULT' : 'o-ILLUSTRATIVE'}">CONF ${v.confidence}</span></div>`).join('')}</div><p class="k">Public reports and surveys, compiled in TRINETRA/docs/26 with confidence tags. They size the problem; none of them is a TRINETRA result.</p>`;
    side('<h3>Why surveys?</h3><p>Evaluators ask "why does this matter". These are the sourced answers: deaths, losses, relief spending, and the measured value of early warning. Confidence B values must be verified before quoting.</p>');
  },
  'Parameter Lab'() {
    const zc = cur('zeroshot_threshold');
    if (!zc) { $('ex-main').innerHTML = '<p>NOT FOUND IN REPO: zero-shot OOF scores.</p>'; return; }
    $('ex-main').innerHTML = `<div class="card"><h3>Decision threshold on REAL zero-shot scores (${zc.value.n.toLocaleString('en-IN')} OOF images)</h3>${OB('REAL_RESULT', zc.source)}
      <input id="thr" type="range" min="0" max="1" step="0.0167" value="${fmt(PSTAR, 3)}"><div id="thr-out" class="mono"></div><svg id="thr-svg" viewBox="0 0 900 360" width="100%"></svg></div>
      <div class="card"><h3>Calibration temperature (transform of the real reliability bins)</h3><input id="tmp" type="range" min="0.3" max="3" step="0.05" value="1"><div id="tmp-out" class="mono"></div><svg id="tmp-svg" viewBox="0 0 900 360" width="100%"></svg>
      <p class="k">Bins are the real cross-fit calibrated scores; moving T re-applies σ(logit(p)/T) to the bin centres to show how temperature bends the curve. T = 1 is the measured state.</p></div>`;
    const pts = zc.value.points;
    const drawThr = () => { const t = +$('thr').value, p = pts.reduce((a, b) => Math.abs(b.t - t) < Math.abs(a.t - t) ? b : a);
      $('thr-out').textContent = `threshold ${fmt(t, 3)} → catches ${fmt(p.tpr * 100, 1)}% of fire/smoke images, false alarms on ${fmt(p.fpr * 100, 1)}% of non-fire images, precision ${fmt(p.precision * 100, 1)}%${Math.abs(t - PSTAR) < .02 ? '  (≈ p*, the cost-based line)' : ''}`;
      let s = L(60, 320, 860, 320, {stroke: C.line}) + L(60, 320, 60, 20, {stroke: C.line}) + T(460, 352, 'false-alarm rate →', {size: 14, anchor: 'middle', fill: C.dim}) + T(70, 30, 'catch rate', {size: 14, fill: C.dim});
      s += h('polyline', {points: pts.map(q => `${60 + q.fpr * 800},${320 - q.tpr * 300}`).join(' '), fill: 'none', stroke: C.teal, 'stroke-width': 3});
      s += h('circle', {cx: 60 + p.fpr * 800, cy: 320 - p.tpr * 300, r: 9, fill: C.gold}); $('thr-svg').innerHTML = s; };
    const rel = zc.value.reliability;
    const drawTmp = () => { const T0 = +$('tmp').value; $('tmp-out').textContent = `T = ${fmt(T0, 2)}${T0 === 1 ? ' (measured)' : ' (what-if)'}`;
      let s = L(60, 320, 360, 20, {stroke: C.dim, dash: '6 6'}) + L(60, 320, 360, 320, {stroke: C.line}) + L(60, 320, 60, 20, {stroke: C.line});
      rel.forEach(b => { const lg = Math.log(clamp(b.conf, 1e-4, 1 - 1e-4) / (1 - clamp(b.conf, 1e-4, 1 - 1e-4))), c2 = 1 / (1 + Math.exp(-lg / T0)); s += h('circle', {cx: 60 + c2 * 300, cy: 320 - b.acc * 300, r: 4 + Math.sqrt(b.n) / 4, fill: C.teal}); });
      $('tmp-svg').innerHTML = s + T(420, 60, 'dashed line = perfect calibration', {size: 15, fill: C.dim}); };
    $('thr').oninput = drawThr; $('tmp').oninput = drawTmp; drawThr(); drawTmp();
    side('<h3>Parameter Lab</h3><p>The threshold slider moves along the real zero-shot score curve. TRINETRA\'s default cut is p* = C_FA/(C_FA + C_miss) = 5/105: a miss costs 20× a false alarm, so it alarms early, which is exactly why zero-shot alone produced too many false alarms and was not admitted.</p>' + OB('REAL_CONFIG', 'configs/default.json'));
  },
  'Fusion Lab'() {
    const ex = CANON.map(e => ({...e, c: 1}));
    $('ex-main').innerHTML = `<div class="card"><h3>Move the experts; every averaging rule updates live</h3>${OB('WORKED')}<div id="fl"></div><div id="fl-out"></div></div>`;
    const draw = () => { const f = fuse(ex); $('fl-out').innerHTML = `<table><tr><th>rule</th><th>fused p</th><th>level</th></tr>${Object.entries(RULES).map(([n, fn]) => { const v = fn(ex); return `<tr><td>${n}</td><td class="mono">${fmt(v, 3)}</td><td><span class="chip" style="background:${LV[level(v)]};color:#0B1238">${level(v)}</span></td></tr>`; }).join('')}</table><p class="mono">FM-1 U* = ${fmt(f.u, 3)}${f.uncertain ? ' → uncertain: human review' : ''} · τ ${TAU} · λ ${LAM} · p* ${fmt(PSTAR, 4)}</p>`; };
    $('fl').innerHTML = `<div class="flrow k"><span>expert</span><span>risk p</span><span>uncertainty u</span><span>reliability r</span><span>on</span></div>` + ex.map((e, i) => `<div class="flrow"><b>${esc(e.name)}</b>${['p', 'u', 'r'].map(k => `<input data-i="${i}" data-k="${k}" type="range" min="0" max="1" step="0.01" value="${e[k]}" aria-label="${k}">`).join('')}<input data-i="${i}" data-k="avail" type="checkbox" checked aria-label="available"></div>`).join('');
    $('fl').querySelectorAll('input').forEach(inp => inp.oninput = () => { const e = ex[+inp.dataset.i]; if (inp.dataset.k === 'avail') e.avail = inp.checked; else e[inp.dataset.k] = +inp.value; draw(); });
    draw();
    side('<h3>Why FM-1?</h3><p>Plain mean is pulled by one outlier; max lets one over-confident model ring alone; log-linear pooling lets a single p≈0 veto a real alarm. FM-1 weights each expert by reliability × physics consistency × e^(−u/τ), stays bounded, and a missing expert simply gets weight 0. Correlated experts are handled by the BLUE/GLS rule in the code (not in this toy).</p>' + OB('REAL_CONFIG', 'ws5_fusion_rl/fusion_models.py · nf.py'));
  },
  Scenarios() {
    $('ex-main').innerHTML = `<div class="card">${Object.entries(SC).map(([k, v]) => `<button data-sc="${k}" style="margin:4px">${esc(v.name)}</button>`).join('')}<input id="sc-x" type="range" min="0" max="1" step="0.005" value="0.6"></div><svg id="sc-svg" viewBox="0 120 1920 760" width="100%"></svg><p class="k">SIMULATED REPLAY: inputs are seeded; the fusion, consistency, tiers and validator use the repo rules.</p>`;
    let kind = 'steam'; const draw = () => { $('sc-svg').innerHTML = DEFS + replayScene(kind, +$('sc-x').value, 140); };
    $('ex-main').querySelectorAll('[data-sc]').forEach(b => b.onclick = () => { kind = b.dataset.sc; draw(); }); $('sc-x').oninput = draw; draw();
    side('<h3>Scenario picker</h3><p>Steam, fog and headlights are classic false alarms; the fire case shows early detection; the fake case shows media screening. Drag the slider to move through the incident.</p>');
  },
  Compare() {
    $('ex-main').innerHTML = `<table><tr><th>ID</th><th>Typical failure (category)</th><th>TRINETRA answer</th><th>Ladder</th><th>Evidence</th></tr>${(D.failure_patterns || []).map(p => `<tr><td class="mono">${p.id}</td><td>${esc(p.pattern)}<div class="k">${esc(p.hinglish)}</div></td><td>${esc(p.answer)}</td><td><span class="chip" style="background:${LADDER[p.ladder][1]};color:${LADDER[p.ladder][2]}">${LADDER[p.ladder][0]}</span></td><td class="src">${esc(p.evidence)}</td></tr>`).join('')}</table>`;
    side('<h3>Compare view</h3><p>Category-level patterns only, never named products. No C4 chip yet, so no "best" anywhere.</p>');
  },
  Results() {
    const rows = Object.entries(D.results || {}).map(([k, v]) => `<tr><td class="mono">${esc(k)}</td><td class="mono">${v.value === 'RESULT PENDING' ? '<span class="chip pending">RESULT PENDING</span>' : esc(typeof v.value === 'object' ? JSON.stringify(v.value) : v.value)}</td><td>${OB(v.origin, v.source)}<div class="k">${esc(v.note || '')}</div></td></tr>`).join('');
    $('ex-main').innerHTML = `<table><tr><th>key</th><th>value</th><th>origin · source</th></tr>${rows}</table>`;
    side('<h3>Results</h3><p>Only values present in results/ appear. Pending stages stay pending; nothing is estimated.</p>');
  },
  Mentor() {
    const QA = [['Why physics?', 'It works with zero labels on day one (AUC 0.758 on 184 real landslides), it explains WHY an alert fires, and it can veto physically impossible alarms. It is checked, not trusted blindly: every model has a validity regime.'],
      ['Why zero-shot?', 'To recognise hazards it was never trained on by writing a sentence. Measured: AUC 0.889 on D-Fire, but many false alarms on candles and weather, so it was not admitted and stays a low-trust helper (cap 0.5).'],
      ['How does fusion work, and why this averaging?', 'FM-1: weight = reliability × physics consistency × e^(−u/τ); fused p = weighted mean; U* adds disagreement. It is bounded, a missing expert gets weight 0, and an outlier cannot dominate. See the Fusion Lab.'],
      ['How did you stop leakage?', 'Group and spatial-block splits (video, site, flood event, frame, 0.1° block), perceptual-hash dedupe across datasets, and held-out sets from a different source.'],
      ['Why small or older datasets?', 'They are free, licensed and verifiable in 36 hours. We validate the protocol, not a benchmark score; every number says "prototype subset".'],
      ['What is not validated yet?', 'Fire CNN, media and EO numbers (Kaggle runs pending), any field trial, the cyclone module, and Class C hypotheses (kept OFF).'],
      ['How is this different from typical systems?', 'Typical: one detector and a fixed threshold. TRINETRA: several experts, physics consistency, calibrated uncertainty, cost-based tiers, a human gate, an offline path. Status chips say what is built vs measured.'],
      ['What with more time?', 'Matched-protocol benchmarks (target C4), a shadow-mode pilot with an SDMA, cyclone physics, IMERG 0.1° rain and Indian InSAR frames.']];
    $('ex-main').innerHTML = QA.map(([q, a]) => `<div class="card"><h3>${esc(q)}</h3><p>${esc(a)}</p></div>`).join('');
    side('<h3>Mentor panel</h3><p>Eight hard questions with honest answers. Do not claim "best", "first" or "solves"; there is no C4 result yet.</p>');
  },
};
function openExplore(tab = 'DFD Live') {
  if (__dfdStop) { __dfdStop(); __dfdStop = null; }
  document.body.classList.add('exploring'); E.playing = false; setPlay();
  $('ex-tabs').innerHTML = Object.keys(TABS).map(k => `<button data-tab="${k}" aria-selected="${k === tab}">${k}</button>`).join(' ');
  $('ex-tabs').querySelectorAll('button').forEach(b => b.onclick = () => openExplore(b.dataset.tab));
  $('ex-complete').textContent = `data completeness: ${Math.round((D.completeness || 0) * 100)}% REAL (rest ribboned ILLUSTRATIVE)`;
  TABS[tab]();
}
function closeExplore() { if (__dfdStop) { __dfdStop(); __dfdStop = null; } document.body.classList.remove('exploring'); }
$('ex-close').onclick = closeExplore;
if (Q.has('explore')) openExplore(Q.get('explore') || 'Pipeline');

/* ======================================================================= recorded video (full film if rendered, else the teaser) */
const VIDS = [['TRINETRA_live_flow_story.mp4', 'Full film (4:55)'], ['TRINETRA_live_flow_teaser.mp4', '15-second teaser']];
function openVideo() {
  E.playing = false; setPlay(); document.body.classList.add('video');
  const v = $('vid-el'); let i = 0;
  const tryNext = () => {
    if (i >= VIDS.length) { $('vid-note').textContent = 'No video file next to this page. Open the app at #live, or render one with TRINETRA/ANIM/tools/record.mjs.'; return; }
    const [f, label] = VIDS[i++]; $('vid-title').textContent = `TRINETRA Live Flow · ${label}`; $('vid-note').textContent = f; v.src = f; v.load();
  };
  v.onerror = tryNext; v.onloadeddata = () => v.play().catch(() => {}); tryNext();
}
function closeVideo() { const v = $('vid-el'); v.pause(); document.body.classList.remove('video'); }
$('b-vid').onclick = openVideo; $('vid-close').onclick = closeVideo;
if (Q.has('video')) openVideo();
