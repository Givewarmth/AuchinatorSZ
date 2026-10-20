const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const SCREENSHOTS_DIR = path.join(__dirname, 'data', 'screenshots');
const GRIDS_FILE      = path.join(__dirname, 'data', 'grids.json');

// Зона поиска магазина в долях от размера картинки (левая часть экрана)
const SEARCH = {
  xMin: 0.13,
  xMax: 0.36,
  yMin: 0.18,
  yMax: 0.83,
};

function smooth(arr, radius) {
  const out = new Array(arr.length);
  for (let i = 0; i < arr.length; i++) {
    let sum = 0, cnt = 0;
    for (let j = Math.max(0, i - radius); j <= Math.min(arr.length - 1, i + radius); j++) {
      sum += arr[j];
      cnt++;
    }
    out[i] = sum / cnt;
  }
  return out;
}

// Ищем локальные минимумы с ограничением по минимальному расстоянию
function findBorders(signal, from, to, minGap) {
  const borders = [];
  for (let i = from + 2; i < to - 2; i++) {
    const v = signal[i];
    if (v <= signal[i - 2] && v <= signal[i - 1] && v <= signal[i + 1] && v <= signal[i + 2]) {
      if (borders.length === 0 || i - borders[borders.length - 1] >= minGap) {
        borders.push(i);
      }
    }
  }
  return borders;
}

function median(arr) {
  if (!arr.length) return 0;
  const s = [...arr].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2);
}

function diffs(arr) {
  const out = [];
  for (let i = 1; i < arr.length; i++) out.push(arr[i] - arr[i - 1]);
  return out;
}

async function detectGrid(buf, meta) {
  const W = meta.width, H = meta.height;
  const raw = await sharp(buf).greyscale().raw().toBuffer();

  const x0 = Math.floor(W * SEARCH.xMin);
  const x1 = Math.floor(W * SEARCH.xMax);
  const y0 = Math.floor(H * SEARCH.yMin);
  const y1 = Math.floor(H * SEARCH.yMax);

  // Проекция по X — средняя яркость каждого столбца в области магазина
  const colMean = new Array(W).fill(0);
  for (let x = x0; x < x1; x++) {
    let sum = 0;
    for (let y = y0; y < y1; y++) sum += raw[y * W + x];
    colMean[x] = sum / (y1 - y0);
  }

  // Проекция по Y — средняя яркость каждой строки в области магазина
  const rowMean = new Array(H).fill(0);
  for (let y = y0; y < y1; y++) {
    let sum = 0;
    for (let x = x0; x < x1; x++) sum += raw[y * W + x];
    rowMean[y] = sum / (x1 - x0);
  }

  const sc = smooth(colMean, 2);
  const sr = smooth(rowMean, 2);

  // Границы между колонками и строками — локальные минимумы
  const colBorders = findBorders(sc, x0, x1, 40);
  const rowBorders = findBorders(sr, y0, y1, 40);

  if (colBorders.length < 3 || rowBorders.length < 3) {
    throw new Error('не удалось найти границы ячеек (минимумов: ' +
                    colBorders.length + ' x ' + rowBorders.length + ')');
  }

  const cellW = median(diffs(colBorders));
  const cellH = median(diffs(rowBorders));

  // startX — первый минимум + смещение внутрь ячейки на 1 px (чтобы не захватить границу)
  const startX = colBorders[0] + 1;
  const startY = rowBorders[0] + 1;

  // cols/rows — сколько ячеек помещается от start до конца области
  const cols = Math.max(1, Math.floor((x1 - startX) / cellW));
  const rows = Math.max(1, Math.floor((y1 - startY) / cellH));

  return { startX, startY, cellW, cellH, cols, rows };
}

async function main() {
  if (!fs.existsSync(GRIDS_FILE)) {
    console.error('Нет data/grids.json');
    process.exit(1);
  }
  const grids = JSON.parse(fs.readFileSync(GRIDS_FILE, 'utf8'));

  const files = fs.readdirSync(SCREENSHOTS_DIR)
    .filter(f => f.toLowerCase().endsWith('.png'))
    .filter(f => !f.includes('grid') && !f.includes('fixed'));

  console.log('Найдено скриншотов: ' + files.length);

  for (const file of files) {
    const src = path.join(SCREENSHOTS_DIR, file);
    const buf = fs.readFileSync(src);
    const meta = await sharp(buf).metadata();
    const key = meta.width + 'x' + meta.height;

    try {
      const detected = await detectGrid(buf, meta);
      console.log('  ' + file + ': startX=' + detected.startX +
                  ' startY=' + detected.startY +
                  ' cellW=' + detected.cellW +
                  ' cellH=' + detected.cellH +
                  ' cols=' + detected.cols +
                  ' rows=' + detected.rows);

      // Обновляем grids.json
      if (!grids[key]) {
        grids[key] = {
          startX: detected.startX,
          startY: detected.startY,
          cellW: detected.cellW,
          cellH: detected.cellH,
          cols: detected.cols,
          rows: detected.rows,
          iconBox:  { x: 3, y: 3, w: detected.cellW - 6, h: detected.cellH - 6 },
          priceBox: { x: 3, y: Math.round(detected.cellH * 0.66), w: detected.cellW - 6, h: Math.round(detected.cellH * 0.30) },
          qtyBox:   { x: Math.round(detected.cellW * 0.55), y: 2, w: Math.round(detected.cellW * 0.42), h: Math.round(detected.cellH * 0.28) },
          mseThreshold: 3000,
          overrides: {},
        };
      }

      // Для каждого файла — свой override
      if (!grids[key].overrides) grids[key].overrides = {};
      grids[key].overrides[file] = {  
        startX: detected.startX,
        startY: detected.startY,
        cellW: detected.cellW,
        cellH: detected.cellH,
        cols: detected.cols,
        rows: detected.rows,
      };
    } catch (e) {
      console.error('  ' + file + ': ОШИБКА — ' + e.message);
    }
  }

  fs.writeFileSync(GRIDS_FILE, JSON.stringify(grids, null, 2), 'utf8');
  console.log('\nСохранено в data/grids.json');
  console.log('Теперь запусти: node debug-grid-all.js');
  console.log('Открой data/debug-grid/*.png и проверь, что красные линии идут ровно по границам.');
}

main().catch(err => { console.error('Ошибка:', err); process.exit(1); });