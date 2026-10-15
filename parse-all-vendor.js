const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { createWorker } = require('tesseract.js');
const { getGridForResolution } = require('./grid-utils');

const SCREENSHOTS_DIR = path.join(__dirname, 'data', 'screenshots');
const HASHES_FILE     = path.join(__dirname, 'data', 'icons-hash.json');
const OUT_FILE        = path.join(__dirname, 'data', 'vendor-draft.json');
const DEBUG_DIR       = path.join(__dirname, 'data', 'debug-crops');

const SIZE = 32;
const DEFAULT_BG = { r: 24, g: 24, b: 24 };

function mse(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) {
    const d = a[i] - b[i];
    s += d * d;
  }
  return s / a.length;
}

async function cropIcon(buf, box, bg) {
  return sharp(buf)
    .extract(box)
    .resize(SIZE, SIZE, { fit: 'contain', background: { ...bg, alpha: 1 } })
    .flatten({ background: bg })
    .removeAlpha()
    .raw()
    .toBuffer();
}

async function cropText(buf, box, scale) {
  if (scale === undefined) scale = 3;
  return sharp(buf)
    .extract(box)
    .greyscale()
    .resize(box.width * scale, box.height * scale, { fit: 'fill' })
    .png()
    .toBuffer();
}

/**
 * Определяем цвет фона ячейки, сэмплируя угол ячейки (там где нет иконки).
 */
async function detectCellBg(buf, cellX, cellY) {
  try {
    const { data, info } = await sharp(buf)
      .extract({ left: cellX + 2, top: cellY + 2, width: 6, height: 6 })
      .removeAlpha()          // ← ключевая правка: убираем альфу ДО raw()
      .raw()
      .toBuffer({ resolveWithObject: true });

    const channels = info.channels;   // должно быть 3
    if (channels < 3) return DEFAULT_BG;

    let r = 0, g = 0, b = 0;
    const pixelCount = data.length / channels;
    for (let i = 0; i < data.length; i += channels) {
      r += data[i];
      g += data[i + 1];
      b += data[i + 2];
    }
    return {
      r: Math.round(r / pixelCount),
      g: Math.round(g / pixelCount),
      b: Math.round(b / pixelCount),
    };
  } catch (e) {
    console.error('detectCellBg ошибка:', e.message);
    return DEFAULT_BG;
  }
}

async function main() {
  if (!fs.existsSync(HASHES_FILE)) {
    console.error('Сначала: node build-icon-hashes.js');
    process.exit(1);
  }
  fs.mkdirSync(DEBUG_DIR, { recursive: true });

  const hashes = JSON.parse(fs.readFileSync(HASHES_FILE, 'utf8'));
  for (const h of hashes) h.buf = Buffer.from(h.hash, 'base64');
  console.log('[hash] ' + hashes.length + ' иконок');

  const files = fs.readdirSync(SCREENSHOTS_DIR)
    .filter(f => f.toLowerCase().endsWith('.png'))
    .filter(f => !f.includes('grid') && !f.includes('fixed'));

  console.log('[screen] ' + files.length + ' скриншотов');

  const worker = await createWorker('eng');
  await worker.setParameters({ tessedit_char_whitelist: '0123456789 ' });

  const byId = new Map();
  let totalFound = 0;

  for (const file of files) {
    const src = path.join(SCREENSHOTS_DIR, file);
    const buf = fs.readFileSync(src);
    const meta = await sharp(buf).metadata();

    let grid;
    try { grid = getGridForResolution(meta.width, meta.height, file); }
    catch (e) { console.error(file + ': ' + e.message); continue; }

    // Определяем цвет ячейки
    const detectedBg = await detectCellBg(buf, grid.startX, grid.startY);
    const bg = detectedBg;
    console.log('\n--- ' + file + ' --- фон ячейки: rgb(' + bg.r + ',' + bg.g + ',' + bg.b + ')');

    let foundInFile = 0;
    let totalMatches = 0;

    for (let row = 0; row < grid.rows; row++) {
      for (let col = 0; col < grid.cols; col++) {
        const cx = grid.startX + col * grid.cellW;
        const cy = grid.startY + row * grid.cellH;
        if (cx + grid.cellW > meta.width || cy + grid.cellH > meta.height) continue;

        const iconBox = {
          left: cx + grid.iconBox.x, top: cy + grid.iconBox.y,
          width: grid.iconBox.w, height: grid.iconBox.h,
        };

        let iconCrop;
        try { iconCrop = await cropIcon(buf, iconBox, bg); }
        catch (e) { continue; }

        let bestId = null, bestName = null, bestCat = null, bestBuf = null, bestScore = Infinity;
        for (const h of hashes) {
          const s = mse(iconCrop, h.buf);
          if (s < bestScore) { bestScore = s; bestId = h.id; bestName = h.name; bestCat = h.category; bestBuf = h.buf; }
        }
        totalMatches++;

        const tag = path.basename(file, '.png') + '_r' + row + 'c' + col + '_s' + Math.round(bestScore);
        await sharp(iconCrop, { raw: { width: SIZE, height: SIZE, channels: 3 } })
          .resize(64, 64, { kernel: 'nearest' })
          .png().toFile(path.join(DEBUG_DIR, tag + '-A.png'));
        await sharp(bestBuf, { raw: { width: SIZE, height: SIZE, channels: 3 } })
          .resize(64, 64, { kernel: 'nearest' })
          .png().toFile(path.join(DEBUG_DIR, tag + '-B.png'));

        if (bestScore > grid.mseThreshold) continue;

        const priceBuf = await cropText(buf, {
          left: cx + grid.priceBox.x, top: cy + grid.priceBox.y,
          width: grid.priceBox.w, height: grid.priceBox.h,
        });
        const price = parseInt((await worker.recognize(priceBuf)).data.text.replace(/[^\d]/g, ''), 10);

        const qtyBuf = await cropText(buf, {
          left: cx + grid.qtyBox.x, top: cy + grid.qtyBox.y,
          width: grid.qtyBox.w, height: grid.qtyBox.h,
        });
        const qtyText = (await worker.recognize(qtyBuf)).data.text.replace(/[^\d]/g, '');
        const qty = qtyText ? parseInt(qtyText, 10) : 1;

        if (!Number.isNaN(price) && price > 0) {
          foundInFile++;
          totalFound++;
          const record = {
            itemId: bestId, name: bestName, category: bestCat,
            qty: qty, price: price,
            qtyPerUnit: Math.round((price / qty) * 100) / 100,
            matchScore: Math.round(bestScore),
            source: file, position: row + ',' + col,
          };
          const existing = byId.get(bestId);
          if (!existing || record.price < existing.price) byId.set(bestId, record);
        }
      }
    }
    console.log('  всего ячеек: ' + totalMatches + ' | прошло порог: ' + foundInFile);
  }

  await worker.terminate();

  const result = [...byId.values()].sort((a, b) => a.name.localeCompare(b.name, 'ru'));
  fs.writeFileSync(OUT_FILE, JSON.stringify(result, null, 2), 'utf8');

  console.log('\nOK Уникальных: ' + result.length);
  console.log('   Всего ячеек: ' + totalFound);
  console.log('   ' + OUT_FILE);
}

main().catch(err => { console.error('Ошибка:', err); process.exit(1); });