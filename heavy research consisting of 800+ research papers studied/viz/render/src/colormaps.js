// colormaps.js — perceptually-uniform, colorblind-safe colormaps (per viz/RESEARCH.md).
// Minimal self-contained RGB control-point tables (0..255) with linear interpolation. No deps.
// inferno/magma → fire radiative power & temperature; viridis/cividis → risk(0–1) & wind.

function makeMap(stops) {
  // stops: array of [t, r, g, b] with t in 0..1, ascending
  return function (t) {
    t = Math.max(0, Math.min(1, t));
    for (let i = 1; i < stops.length; i++) {
      if (t <= stops[i][0]) {
        const a = stops[i - 1], b = stops[i];
        const f = (t - a[0]) / (b[0] - a[0] || 1);
        return [
          Math.round(a[1] + f * (b[1] - a[1])),
          Math.round(a[2] + f * (b[2] - a[2])),
          Math.round(a[3] + f * (b[3] - a[3])),
        ];
      }
    }
    const last = stops[stops.length - 1];
    return [last[1], last[2], last[3]];
  };
}

// Control points sampled from the canonical matplotlib colormaps (BIDS, CC0).
export const inferno = makeMap([
  [0.0, 0, 0, 4], [0.2, 40, 11, 84], [0.4, 101, 21, 110], [0.6, 159, 42, 99],
  [0.75, 212, 72, 66], [0.88, 245, 125, 21], [0.96, 250, 193, 39], [1.0, 252, 255, 164],
]);

export const magma = makeMap([
  [0.0, 0, 0, 4], [0.2, 40, 11, 84], [0.4, 101, 21, 110], [0.6, 183, 55, 121],
  [0.78, 240, 97, 104], [0.9, 253, 159, 108], [1.0, 252, 253, 191],
]);

export const viridis = makeMap([
  [0.0, 68, 1, 84], [0.25, 59, 82, 139], [0.5, 33, 145, 140], [0.75, 94, 201, 98], [1.0, 253, 231, 37],
]);

export const cividis = makeMap([
  [0.0, 0, 32, 76], [0.25, 0, 67, 118], [0.5, 87, 118, 141], [0.75, 165, 161, 128], [1.0, 255, 234, 70],
]);

export const MAPS = { inferno, magma, viridis, cividis };

// return a CSS rgb() string
export function cssColor(map, t) {
  const [r, g, b] = map(t);
  return `rgb(${r},${g},${b})`;
}

// paint a horizontal gradient legend into a canvas
export function paintLegend(canvas, map) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  for (let x = 0; x < w; x++) {
    const [r, g, b] = map(x / (w - 1));
    ctx.fillStyle = `rgb(${r},${g},${b})`;
    ctx.fillRect(x, 0, 1, h);
  }
}
