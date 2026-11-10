// Erzeugt die B31G3L-Logos als SVG. Aufruf: node brand/make-brand.js brand
const fs = require('fs');
const path = require('path');
const out = process.argv[2];
fs.mkdirSync(out, { recursive: true });

const rep = (row, n) => Array(n).fill(row);
const G = {
  B: ['####.', '#...#', '#...#', '####.', '#...#', '#...#', '####.'],
  '3': ['####.', '....#', '....#', '.###.', '....#', '....#', '####.'],
  '1': ['..#..', '.##..', '..#..', '..#..', '..#..', '..#..', '.###.'],
  G: ['.####', '#....', '#....', '#.###', '#...#', '#...#', '.###.'],
  L: [...rep('#....', 6), '#####'],
  _: [...rep('.....', 6), '#####'],
  '0': ['.###.', '#...#', '#..##', '#.#.#', '##..#', '#...#', '.###.'],
  '4': ['...#.', '..##.', '.#.#.', '#..#.', '#####', '...#.', '...#.'],
  H: [...rep('#...#', 3), '#####', ...rep('#...#', 3)],
  N: ['#...#', '##..#', '#.#.#', '#..##', '#...#', '#...#', '#...#'],
  W: ['#...#', '#...#', '#...#', '#.#.#', '#.#.#', '##.##', '#...#'],
  R: ['####.', '#...#', '#...#', '####.', '#.#..', '#..#.', '#...#'],
  U: [...rep('#...#', 6), '.###.'],
  M: ['#...#', '##.##', '#.#.#', '#.#.#', '#...#', '#...#', '#...#'],
  T: ['#####', ...rep('..#..', 6)],
  D: ['####.', ...rep('#...#', 5), '####.'],
  S: ['.####', '#....', '#....', '.###.', '....#', '....#', '####.'],
  C: ['.####', ...rep('#....', 5), '.####'],
  F: ['#####', '#....', '#....', '####.', '#....', '#....', '#....'],
  V: [...rep('#...#', 5), '.#.#.', '..#..'],
  P: ['####.', '#...#', '#...#', '####.', '#....', '#....', '#....'],
  ' ': rep('...', 7),
};

const DARK = { bg: '#0c100e', ink: '#e9eeea', soft: '#9aa69f', accent: '#4ade80', dot: '#1b231f' };
const LIGHT = { bg: '#f6f5f0', ink: '#15181c', soft: '#59606b', accent: '#0b7a4b', dot: '#e0ddd3' };

// Breite eines Worts in Zellen (Zeichenbreite + 1 Zelle Abstand)
const wordWidth = (text) => [...text].reduce((w, ch) => w + G[ch][0].length + 1, -1);

// Zeichnet ein Wort ab (x, y) mit Zellgröße c; Ziffern und Cursor in Akzentfarbe.
function word(text, x, y, c, pal, inkColor = pal.ink) {
  let ink = '', acc = '', col = 0;
  for (const ch of text) {
    let d = '';
    G[ch].forEach((row, r) => {
      // waagerechte Läufe zusammenfassen, damit keine Haarlinien zwischen Zellen entstehen
      let start = -1;
      for (let k = 0; k <= row.length; k++) {
        const on = row[k] === '#';
        if (on && start < 0) start = k;
        if (!on && start >= 0) {
          d += `M${x + (col + start) * c} ${y + r * c}h${(k - start) * c}v${c}h${-(k - start) * c}z`;
          start = -1;
        }
      }
    });
    if (/[0-9_]/.test(ch)) acc += d; else ink += d;
    col += G[ch][0].length + 1;
  }
  return `<path fill="${inkColor}" d="${ink}"/><path fill="${pal.accent}" d="${acc}"/>`;
}

function svg(w, h, body) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" shape-rendering="crispEdges">${body}</svg>\n`;
}

function dots(w, h, step, r, pal) {
  let d = '';
  for (let y = step / 2; y < h; y += step)
    for (let x = step / 2; x < w; x += step) d += `M${x - r} ${y - r}h${2 * r}v${2 * r}h${-2 * r}z`;
  return `<path fill="${pal.dot}" d="${d}"/>`;
}

const tile = (s, pal, rounded) =>
  `<rect width="${s}" height="${s}" ${rounded ? `rx="${s * 0.22}" ` : ''}fill="${pal.bg}" shape-rendering="geometricPrecision"/>`;

// 1) Logo: gestapelt B31 / G3L auf 28er-Raster (passt auch in einen Kreis-Ausschnitt)
function logo(pal, rounded) {
  const c = 16, n = 28, s = n * c;
  const x = ((n - 17) / 2) * c, y = ((n - 16) / 2) * c;
  return svg(s, s, tile(s, pal, rounded) + word('B31', x, y, c, pal) + word('G3L', x, y + 9 * c, c, pal));
}

// 2) Marke: nur "31", für kleine Größen (Favicon)
function mark(pal, rounded) {
  const c = 32, n = 16, s = n * c;
  return svg(s, s, tile(s, pal, rounded) + word('31', 2.5 * c, 4.5 * c, c, pal));
}

// 3) Wortmarke: B31G3L_ ohne Hintergrund
function wordmark(pal) {
  const c = 16, t = 'B31G3L_';
  return svg(wordWidth(t) * c, 7 * c, word(t, 0, 0, c, pal));
}

// 4) Banner: Wortmarke mittig auf Punktraster; optional darunter eine Zeile mit Schlagworten.
//    c = Zellgröße der Wortmarke, tc = Zellgröße der Schlagworte, bg = Raster-Zellgröße
function banner(w, h, c, pal, tags, tc, bg = c) {
  const t = 'B31G3L_';
  const sep = 13; // Zellen zwischen zwei Schlagworten, in der Mitte ein Punkt
  const tagW = tags ? tags.reduce((s, tag) => s + wordWidth(tag), 0) + sep * (tags.length - 1) : 0;
  const gap = tags ? Math.round(c * 2.5) : 0;
  const blockH = 7 * c + (tags ? gap + 7 * tc : 0);
  const blockW = Math.max(wordWidth(t) * c, tags ? tagW * tc : 0);
  const x = Math.round((w - wordWidth(t) * c) / 2), y = Math.round((h - blockH) / 2);
  const pad = bg * 3;
  let body = `<rect width="${w}" height="${h}" fill="${pal.bg}"/>` + dots(w, h, bg * 2, bg / 8, pal);
  body += `<rect x="${Math.round((w - blockW) / 2) - pad}" y="${y - pad}" width="${blockW + 2 * pad}" height="${blockH + 2 * pad}" fill="${pal.bg}"/>`;
  body += word(t, x, y, c, pal);
  if (tags) {
    let tx = Math.round((w - tagW * tc) / 2);
    const ty = y + 7 * c + gap;
    tags.forEach((tag, i) => {
      body += word(tag, tx, ty, tc, pal, pal.soft);
      tx += wordWidth(tag) * tc;
      if (i < tags.length - 1) {
        body += `<rect x="${tx + ((sep - 1) / 2) * tc}" y="${ty + 3 * tc}" width="${tc}" height="${tc}" fill="${pal.accent}"/>`;
        tx += sep * tc;
      }
    });
  }
  return svg(w, h, body);
}

const TAGS = ['N0 4DS', 'M4D3 W1TH P4SS10N', 'S0L0 D3V'];

const files = {
  'logo.svg': logo(DARK, true),
  'logo-square.svg': logo(DARK, false),
  'logo-light.svg': logo(LIGHT, true),
  'mark.svg': mark(DARK, true),
  'mark-square.svg': mark(DARK, false),
  'wordmark-dark.svg': wordmark(DARK),
  'wordmark-light.svg': wordmark(LIGHT),
  'play-header.svg': banner(4096, 2304, 48, DARK, TAGS, 12, 64),
  'play-feature.svg': banner(1024, 500, 16, DARK),
  'social.svg': banner(1200, 630, 20, DARK),
  'github-banner.svg': banner(1280, 640, 20, DARK),
};
for (const [name, content] of Object.entries(files)) fs.writeFileSync(path.join(out, name), content);
console.log(Object.keys(files).join('\n'));
