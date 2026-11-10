// Erzeugt die B31G3L-Logos als SVG. Aufruf: node brand/make-brand.js brand
// Ergebnis: vier Sätze mit gleichen Dateinamen
//   brand/            Pixel-Stil, "B31G3L"
//   brand/apps/       Pixel-Stil, "B31G3L_APPS"
//   brand/led/        LED-Stil (Punktmatrix), "B31G3L"
//   brand/led-apps/   LED-Stil, "B31G3L_APPS"
const fs = require('fs');
const path = require('path');
const root = process.argv[2];

const G = {
  B: ['####.', '#...#', '#...#', '####.', '#...#', '#...#', '####.'],
  '3': ['####.', '....#', '....#', '.###.', '....#', '....#', '####.'],
  '1': ['..#..', '.##..', '..#..', '..#..', '..#..', '..#..', '.###.'],
  G: ['.####', '#....', '#....', '#.###', '#...#', '#...#', '.###.'],
  L: ['#....', '#....', '#....', '#....', '#....', '#....', '#####'],
  A: ['.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#'],
  P: ['####.', '#...#', '#...#', '####.', '#....', '#....', '#....'],
  S: ['.####', '#....', '#....', '.###.', '....#', '....#', '####.'],
  _: ['.....', '.....', '.....', '.....', '.....', '.....', '#####'],
};

const DARK = { bg: '#0c100e', ink: '#e9eeea', accent: '#4ade80', dot: '#1b231f' };
const LIGHT = { bg: '#f6f5f0', ink: '#15181c', accent: '#0b7a4b', dot: '#e0ddd3' };

const wordWidth = (text) => text.length * 6 - 1;
const isAccent = (ch) => /[0-9_]/.test(ch);

// Pixel-Stil: Zellen als Quadrate; waagerechte Läufe zusammengefasst (keine Haarlinien).
function wordPixel(text, x, y, c, pal) {
  let ink = '', acc = '';
  [...text].forEach((ch, i) => {
    let d = '';
    G[ch].forEach((row, r) => {
      let start = -1;
      for (let k = 0; k <= row.length; k++) {
        const on = row[k] === '#';
        if (on && start < 0) start = k;
        if (!on && start >= 0) {
          d += `M${x + (i * 6 + start) * c} ${y + r * c}h${(k - start) * c}v${c}h${-(k - start) * c}z`;
          start = -1;
        }
      }
    });
    if (isAccent(ch)) acc += d; else ink += d;
  });
  return `<path fill="${pal.ink}" d="${ink}"/><path fill="${pal.accent}" d="${acc}"/>`;
}

const circle = (cx, cy, r) => `M${cx - r} ${cy}a${r} ${r} 0 1 0 ${2 * r} 0a${r} ${r} 0 1 0 ${-2 * r} 0z`;

// LED-Stil: jede Zelle ein Punkt; unbeleuchtete Punkte bleiben schwach sichtbar.
function wordLed(text, x, y, c, pal, withOff = true) {
  const r = +(c * 0.38).toFixed(2);
  let ink = '', acc = '', off = '';
  const cols = wordWidth(text);
  const lit = new Set();
  [...text].forEach((ch, i) => {
    G[ch].forEach((row, rr) => {
      [...row].forEach((v, k) => {
        if (v !== '#') return;
        lit.add(`${i * 6 + k},${rr}`);
        const d = circle(x + (i * 6 + k + 0.5) * c, y + (rr + 0.5) * c, r);
        if (isAccent(ch)) acc += d; else ink += d;
      });
    });
  });
  if (withOff)
    for (let rr = 0; rr < 7; rr++)
      for (let k = 0; k < cols; k++)
        if (!lit.has(`${k},${rr}`)) off += circle(x + (k + 0.5) * c, y + (rr + 0.5) * c, r);
  return `<path fill="${pal.dot}" d="${off}"/><path fill="${pal.ink}" d="${ink}"/><path fill="${pal.accent}" d="${acc}"/>`;
}

function svg(w, h, body, crisp) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}"${crisp ? ' shape-rendering="crispEdges"' : ''}>${body}</svg>\n`;
}

function buildSet(style, apps) {
  const led = style === 'led';
  const word = led ? wordLed : wordPixel;
  const crisp = !led;
  const full = apps ? 'B31G3L_APPS' : 'B31G3L_';

  const tile = (s, pal, rounded) =>
    `<rect width="${s}" height="${s}" ${rounded ? `rx="${s * 0.22}" ` : ''}fill="${pal.bg}" shape-rendering="geometricPrecision"/>`;

  // Logo: B31 / G3L gestapelt, bei "apps" darunter klein _APPS
  function logo(pal, rounded) {
    const c = 16, n = apps ? 30 : 28, s = n * c;
    const h = apps ? 21.5 : 16;
    const x = ((n - 17) / 2) * c, y = ((n - h) / 2) * c;
    let body = tile(s, pal, rounded) + word('B31', x, y, c, pal) + word('G3L', x, y + 9 * c, c, pal);
    if (apps) body += word('_APPS', x, y + 18 * c, c / 2, pal);
    return svg(s, s, body, crisp);
  }

  // Marke: nur "31" für kleine Größen
  function mark(pal, rounded) {
    const c = 32, n = 16, s = n * c;
    return svg(s, s, tile(s, pal, rounded) + word('31', 2.5 * c, 4.5 * c, c, pal), crisp);
  }

  function wordmark(pal) {
    const c = 16;
    return svg(wordWidth(full) * c, 7 * c, word(full, 0, 0, c, pal), crisp);
  }

  // Banner: Schriftzug mittig; Pixel-Stil auf feinem Punktraster, LED-Stil als durchgehende Matrix
  function banner(w, h, pal) {
    const c = apps ? Math.floor((w * 0.76) / wordWidth(full)) : { 4096: 64, 1024: 16 }[w] || 20;
    const x = Math.round((w - wordWidth(full) * c) / 2), y = Math.round((h - 7 * c) / 2);
    let body = `<rect width="${w}" height="${h}" fill="${pal.bg}"/>`;
    if (led) {
      const r = +(c * 0.38).toFixed(2);
      let d = '';
      for (let cy = y - Math.ceil(y / c) * c + c / 2; cy < h + c; cy += c)
        for (let cx = x - Math.ceil(x / c) * c + c / 2; cx < w + c; cx += c) d += circle(cx, cy, r);
      body += `<path fill="${pal.dot}" d="${d}"/>` + wordLed(full, x, y, c, pal, false);
    } else {
      const step = c * 2, r = c / 8, pad = c * 3;
      let d = '';
      for (let cy = step / 2; cy < h; cy += step)
        for (let cx = step / 2; cx < w; cx += step) d += `M${cx - r} ${cy - r}h${2 * r}v${2 * r}h${-2 * r}z`;
      body += `<path fill="${pal.dot}" d="${d}"/>`;
      body += `<rect x="${x - pad}" y="${y - pad}" width="${wordWidth(full) * c + 2 * pad}" height="${7 * c + 2 * pad}" fill="${pal.bg}"/>`;
      body += word(full, x, y, c, pal);
    }
    return svg(w, h, body, crisp);
  }

  return {
    'logo.svg': logo(DARK, true),
    'logo-square.svg': logo(DARK, false),
    'logo-light.svg': logo(LIGHT, true),
    'mark.svg': mark(DARK, true),
    'mark-square.svg': mark(DARK, false),
    'wordmark-dark.svg': wordmark(DARK),
    'wordmark-light.svg': wordmark(LIGHT),
    'play-header.svg': banner(4096, 2304, DARK),
    'play-feature.svg': banner(1024, 500, DARK),
    'social.svg': banner(1200, 630, DARK),
    'github-banner.svg': banner(1280, 640, DARK),
  };
}

const sets = { '': ['pixel', false], apps: ['pixel', true], led: ['led', false], 'led-apps': ['led', true] };
for (const [dir, [style, apps]] of Object.entries(sets)) {
  const out = path.join(root, dir);
  fs.mkdirSync(out, { recursive: true });
  for (const [name, content] of Object.entries(buildSet(style, apps))) fs.writeFileSync(path.join(out, name), content);
}
console.log('ok');
