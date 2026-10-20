// Диагностика: для указанной ячейки (row,col) сохраняет топ-10 матчей
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { getGridForResolution } = require('./grid-utils');

const SCREENSHOT = 'vendor.png';
const ROW = 0;
const COL = 0;

const SCREENSHOTS_DIR = path.join(__dirname, 'data', 'screenshots');
const HASHES_FILE = path.join(__dirname, 'data', 'icons-hash.json');
const OUT_DIR = path.join(__dirname, 'data', 'debug-top-improved');

const SIZE = 32;

// Улучшенная функция сравнения с учетом формы и контраста
function improvedMSE(a, b) {
  let s = 0;
  const len = Math.min(a.length, b.length);

  // Сравниваем пиксели по отдельности с учетом контраста
  for (let i = 0; i < len; i++) {
    const diff = Math.abs(a[i] - b[i]);
    s += diff * diff;
  }
  return s / len;
}

// Функция для анализа контраста
function analyzeContrast(buffer) {
  let total = 0;
  let count = 0;

  for (let i = 0; i < buffer.length; i += 3) {
    const r = buffer[i];
    const g = buffer[i + 1];
    const b = buffer[i + 2];
    // Среднее значение цвета (для анализа контраста)
    total += (r + g + b) / 3;
    count++;
  }

  return count > 0 ? total / count : 0;
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });

  const hashes = JSON.parse(fs.readFileSync(HASHES_FILE, 'utf8'));
  for (const h of hashes) h.buf = Buffer.from(h.hash, 'base64');

  const src = path.join(SCREENSHOTS_DIR, SCREENSHOT);
  const buf = fs.readFileSync(src);
  const meta = await sharp(buf).metadata();
  const grid = getGridForResolution(meta.width, meta.height, SCREENSHOT);
  const bg = grid.bgColor || { r: 30, g: 30, b: 30 };

  const cx = grid.startX + COL * grid.cellW;
  const cy = grid.startY + ROW * grid.cellH;

  // 1. Кроп оригинальной ячейки целиком (для контекста)
  await sharp(buf)
    .extract({ left: cx, top: cy, width: grid.cellW, height: grid.cellH })
    .resize(200, 200, { kernel: 'nearest' })
    .png().toFile(path.join(OUT_DIR, 'cell-original.png'));

  // 2. Кроп иконки в 32×32 → для сравнения
  const iconCrop = await sharp(buf)
    .extract({
      left: cx + grid.iconBox.x, top: cy + grid.iconBox.y,
      width: grid.iconBox.w, height: grid.iconBox.h,
    })
    .resize(SIZE, SIZE, { fit: 'contain', background: { ...bg, alpha: 1 } })
    .flatten({ background: bg })
    .removeAlpha()
    .raw()
    .toBuffer();

  // 3. Считаем MSE всех кандидатов
  const scored = hashes.map(h => {
    const score = improvedMSE(iconCrop, h.buf);
    const contrast = analyzeContrast(h.buf);

    return {
      id: h.id, name: h.name, category: h.category,
      score: score,
      contrast: contrast,
      buf: h.buf,
    };
  }).sort((a, b) => a.score - b.score);

  // 4. Сохраняем топ-10
  console.log('\nТоп-10 кандидатов для ячейки (' + ROW + ',' + COL + '):\n');
  for (let i = 0; i < 10; i++) {
    const c = scored[i];
    if (!c) break;
    console.log(
      '  #' + String(i + 1).padStart(2) +
      '  score=' + String(Math.round(c.score)).padStart(6) +
      '  contrast=' + String(Math.round(c.contrast)).padStart(4) +
      '  ' + c.name.padEnd(30) +
      '  [' + c.id + ']'
    );

    // Оригинал A
    await sharp(iconCrop, { raw: { width: SIZE, height: SIZE, channels: 3 } })
      .resize(128, 128, { kernel: 'nearest' })
      .png().toFile(path.join(OUT_DIR, 'A-from-screenshot.png'));

    // Кандидат B
    await sharp(c.buf, { raw: { width: SIZE, height: SIZE, channels: 3 } })
      .resize(128, 128, { kernel: 'nearest' })
      .png().toFile(path.join(OUT_DIR, 'B-rank' + (i + 1) + '-' + c.id + '.png'));
  }

  console.log('\nКропы сохранены в data/debug-top-improved/');
  console.log('  A-from-screenshot.png — что реально в ячейке');
  console.log('  B-rank1-*.png ... B-rank10-*.png — топ-10 совпадений');
}

main().catch(err => { console.error('Ошибка:', err); process.exit(1); });