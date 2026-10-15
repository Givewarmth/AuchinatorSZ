// Диагностика: для указанной ячейки (row,col) сохраняет топ-10 матчей
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { getGridForResolution } = require('./grid-utils');

const SCREENSHOT = 'vendor.png';      // какой файл
const ROW = 0;                        // какая строка (0..)
const COL = 0;                        // какая колонка (0..)

const SCREENSHOTS_DIR = path.join(__dirname, 'data', 'screenshots');
const HASHES_FILE     = path.join(__dirname, 'data', 'icons-hash.json');
const OUT_DIR         = path.join(__dirname, 'data', 'debug-top');

const SIZE = 32;

function mse(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) {
    const d = a[i] - b[i];
    s += d * d;
  }
  return s / a.length;
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
  const scored = hashes.map(h => ({
    id: h.id, name: h.name, category: h.category,
    score: mse(iconCrop, h.buf),
    buf: h.buf,
  })).sort((a, b) => a.score - b.score);

  // 4. Сохраняем топ-10
  console.log('\nТоп-10 кандидатов для ячейки (' + ROW + ',' + COL + '):\n');
  for (let i = 0; i < 10; i++) {
    const c = scored[i];
    if (!c) break;
    console.log(
      '  #' + String(i + 1).padStart(2) +
      '  score=' + String(Math.round(c.score)).padStart(6) +
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

  console.log('\nКропы сохранены в data/debug-top/');
  console.log('  A-from-screenshot.png — что реально в ячейке');
  console.log('  B-rank1-*.png ... B-rank10-*.png — топ-10 совпадений');
}

main().catch(err => { console.error('Ошибка:', err); process.exit(1); });
