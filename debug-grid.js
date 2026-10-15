// debug-grid.js
// Рисует сетку поверх скриншота для калибровки координат
const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const SCREENSHOT = path.join(__dirname, 'data', 'screenshots', 'vendor.png');
const OUT_FILE   = path.join(__dirname, 'data', 'screenshots', 'vendor-grid.png');

// ⚙️ Те же координаты, что в parse-vendor-screenshot.js
const GRID = {
  startX: 445,
  startY: 300,
  cellW: 128,
  cellH: 128,
  cols: 6,
  rows: 6,
};

async function main() {
  if (!fs.existsSync(SCREENSHOT)) {
    console.error('❌ Нет файла:', SCREENSHOT);
    process.exit(1);
  }

  const imageBuf = fs.readFileSync(SCREENSHOT);
  const meta = await sharp(imageBuf).metadata();
  console.log(`[image] ${meta.width}x${meta.height}`);

  // Строим SVG-сетку с теми же размерами, что у картинки
  let lines = '';

  for (let col = 0; col <= GRID.cols; col++) {
    const x = GRID.startX + col * GRID.cellW;
    lines += `<line x1="${x}" y1="0" x2="${x}" y2="${meta.height}" stroke="red" stroke-width="2" />`;
  }

  for (let row = 0; row <= GRID.rows; row++) {
    const y = GRID.startY + row * GRID.cellH;
    lines += `<line x1="0" y1="${y}" x2="${meta.width}" y2="${y}" stroke="red" stroke-width="2" />`;
  }

  // Номера ячеек
  for (let row = 0; row < GRID.rows; row++) {
    for (let col = 0; col < GRID.cols; col++) {
      const x = GRID.startX + col * GRID.cellW + 5;
      const y = GRID.startY + row * GRID.cellH + 20;
      lines += `<text x="${x}" y="${y}" font-size="14" fill="yellow" font-family="Arial">${row},${col}</text>`;
    }
  }

  const svg = `
    <svg width="${meta.width}" height="${meta.height}" xmlns="http://www.w3.org/2000/svg">
      ${lines}
    </svg>
  `;

  await sharp(imageBuf)
    .composite([{ input: Buffer.from(svg), top: 0, left: 0 }])
    .png()
    .toFile(OUT_FILE);

  console.log(`✅ Сетка нарисована: ${OUT_FILE}`);
  console.log('   Открой файл и посмотри, попадают ли линии на границы ячеек с иконками.');
}

main().catch(err => { console.error('❌', err); process.exit(1); });