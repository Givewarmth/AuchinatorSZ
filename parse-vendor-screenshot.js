// parse-vendor-screenshot.js
// Распознаёт магазин вендора на скриншоте и пишет data/vendor-draft.json
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { createWorker } = require('tesseract.js');

const SCREENSHOT  = path.join(__dirname, 'data', 'screenshots', 'vendor.png');
const HASHES_FILE = path.join(__dirname, 'data', 'icons-hash.json');
const OUT_FILE    = path.join(__dirname, 'data', 'vendor-draft.json');
const DEBUG_DIR   = path.join(__dirname, 'data', 'debug-crops');

// ⚙️ Настройки сетки — при необходимости подстрой под своё разрешение
// Как измерить:
//   1) Открой скриншот в Paint/Photoshop
//   2) Наведи на ЛЕВЫЙ ВЕРХНИЙ угол первой ячейки — запиши X, Y
//   3) Наведи на ЛЕВЫЙ ВЕРХНИЙ угол второй ячейки по горизонтали — это cellW
//   4) Наведи на ЛЕВЫЙ ВЕРХНИЙ угол второй ячейки по вертикали — это cellH
const GRID = {
  startX: 445,
  startY: 300,
  cellW: 128,
  cellH: 128,
  cols: 6,
  rows: 6,

  // Область иконки внутри ячейки (без бейджей по углам)
  iconBox: { x: 29, y: 29, w: 70, h: 70 },

  // Область цены — берём нижнюю часть ячейки
  priceBox: { x: 5, y: 95, w: 118, h: 30 },

  // Область количества — правый верхний угол
  qtyBox: { x: 65, y: 0, w: 60, h: 30 },
};

const SIZE = 32;
const MSE_THRESHOLD = 3000; // порог для отсева "не нашли совпадение"

function mse(a, b) {
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    const d = a[i] - b[i];
    sum += d * d;
  }
  return sum / a.length;
}

async function main() {
  if (!fs.existsSync(SCREENSHOT)) {
    console.error(`❌ Нет файла: ${SCREENSHOT}`);
    console.error('   Положи скриншот магазина в data/screenshots/vendor.png');
    process.exit(1);
  }
  if (!fs.existsSync(HASHES_FILE)) {
    console.error('❌ Нет data/icons-hash.json — сначала запусти: node build-icon-hashes.js');
    process.exit(1);
  }

  fs.mkdirSync(DEBUG_DIR, { recursive: true });

  const hashes = JSON.parse(fs.readFileSync(HASHES_FILE, 'utf8'));
  console.log(`[hash] загружено ${hashes.length} иконок`);

  // Декодируем base64 в Buffer один раз
  for (const h of hashes) {
    h.buf = Buffer.from(h.hash, 'base64');
  }

// Универсально читаем файл — sharp сам разберётся с форматом
const imageBuf = fs.readFileSync(SCREENSHOT);
console.log(`[image] размер файла: ${imageBuf.length} байт, формат: ${imageBuf.slice(0, 8).toString('hex')}`);

let meta;
try {
  meta = await sharp(imageBuf).metadata();
} catch (e) {
  console.error('❌ sharp не может распарсить файл:', e.message);
  console.error('   Первые байты:', imageBuf.slice(0, 16).toString('hex'));
  console.error('   Пересохрани файл через Paint в PNG.');
  process.exit(1);
}
console.log(`[image] ${meta.width}x${meta.height}, format: ${meta.format}`);


  const worker = await createWorker('eng');
  await worker.setParameters({
    tessedit_char_whitelist: '0123456789 ',
  });

  const items = [];
  let processed = 0;

  for (let row = 0; row < GRID.rows; row++) {
    for (let col = 0; col < GRID.cols; col++) {
      const cx = GRID.startX + col * GRID.cellW;
      const cy = GRID.startY + row * GRID.cellH;

      // Границы ячейки
      if (cx + GRID.cellW > meta.width || cy + GRID.cellH > meta.height) continue;

      // --- Иконка ---
      const iconCrop = await sharp(SCREENSHOT)
        .extract({
          left: cx + GRID.iconBox.x,
          top:  cy + GRID.iconBox.y,
          width:  GRID.iconBox.w,
          height: GRID.iconBox.h,
        })
        .resize(SIZE, SIZE, { fit: 'contain', background: { r: 51, g: 51, b: 51, alpha: 1 } })
        .flatten({ background: { r: 51, g: 51, b: 51 } })
        .removeAlpha()
        .raw()
        .toBuffer();

      // Ищем лучший матч
      let bestId = null, bestName = null, bestCat = null, bestScore = Infinity;
      for (const h of hashes) {
        const score = mse(iconCrop, h.buf);
        if (score < bestScore) {
          bestScore = score;
          bestId = h.id;
          bestName = h.name;
          bestCat = h.category;
        }
      }

      // Если матч слишком плохой — пропускаем (пустая ячейка)
      if (bestScore > MSE_THRESHOLD) continue;

      // --- Цена ---
      const priceBuf = await sharp(SCREENSHOT)
        .extract({
          left: cx + GRID.priceBox.x,
          top:  cy + GRID.priceBox.y,
          width:  GRID.priceBox.w,
          height: GRID.priceBox.h,
        })
        .greyscale()
        .resize(GRID.priceBox.w * 3, GRID.priceBox.h * 3, { fit: 'fill' })
        .png()
        .toBuffer();

      const priceRes = await worker.recognize(priceBuf);
      const priceText = priceRes.data.text.replace(/\s/g, '');
      const price = parseInt(priceText, 10);

      // --- Количество ---
      const qtyBuf = await sharp(SCREENSHOT)
        .extract({
          left: cx + GRID.qtyBox.x,
          top:  cy + GRID.qtyBox.y,
          width:  GRID.qtyBox.w,
          height: GRID.qtyBox.h,
        })
        .greyscale()
        .resize(GRID.qtyBox.w * 3, GRID.qtyBox.h * 3, { fit: 'fill' })
        .png()
        .toBuffer();

      const qtyRes = await worker.recognize(qtyBuf);
      const qtyText = qtyRes.data.text.replace(/[^\d]/g, '');
      const qty = qtyText ? parseInt(qtyText, 10) : 1;

      // Сохраняем кропы для отладки
      const tag = `r${row}c${col}`;
      await sharp(iconCrop, { raw: { width: SIZE, height: SIZE, channels: 3 } })
        .png().toFile(path.join(DEBUG_DIR, `${tag}-icon.png`));

      if (!Number.isNaN(price) && price > 0) {
        items.push({
          row, col,
          itemId: bestId,
          name: bestName,
          category: bestCat,
          matchScore: Math.round(bestScore),
          qty,
          price,
        });
        processed++;
      }
    }
  }

  await worker.terminate();

  fs.writeFileSync(OUT_FILE, JSON.stringify(items, null, 2), 'utf8');
  console.log(`✅ Распознано позиций: ${processed}`);
  console.log(`   Файл: ${OUT_FILE}`);
  console.log(`   Отладочные кропы: ${DEBUG_DIR}/`);
  console.log('');
  console.log('Проверь результат, потом вручную исправь неверные распознавания и подтверди.');
}

main().catch(err => { console.error('❌', err); process.exit(1); });