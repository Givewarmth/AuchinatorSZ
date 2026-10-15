const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const { getGridForResolution } = require('./grid-utils');

const SCREENSHOTS_DIR = path.join(__dirname, 'data', 'screenshots');
const DEBUG_OUT_DIR   = path.join(__dirname, 'data', 'debug-grid');

function buildSvg(width, height, grid) {
  let lines = '';

  for (let col = 0; col <= grid.cols; col++) {
    const x = grid.startX + col * grid.cellW;
    lines += '<line x1="' + x + '" y1="0" x2="' + x + '" y2="' + height + '" stroke="red" stroke-width="2" />';
  }
  for (let row = 0; row <= grid.rows; row++) {
    const y = grid.startY + row * grid.cellH;
    lines += '<line x1="0" y1="' + y + '" x2="' + width + '" y2="' + y + '" stroke="red" stroke-width="2" />';
  }

  const cx = grid.startX;
  const cy = grid.startY;

  lines += '<rect x="' + (cx + grid.iconBox.x)  + '" y="' + (cy + grid.iconBox.y)  + '" width="' + grid.iconBox.w  + '" height="' + grid.iconBox.h  + '" fill="none" stroke="cyan" stroke-width="2" />';
  lines += '<rect x="' + (cx + grid.priceBox.x) + '" y="' + (cy + grid.priceBox.y) + '" width="' + grid.priceBox.w + '" height="' + grid.priceBox.h + '" fill="none" stroke="lime" stroke-width="2" />';
  lines += '<rect x="' + (cx + grid.qtyBox.x)   + '" y="' + (cy + grid.qtyBox.y)   + '" width="' + grid.qtyBox.w   + '" height="' + grid.qtyBox.h   + '" fill="none" stroke="magenta" stroke-width="2" />';

  return '<svg width="' + width + '" height="' + height + '" xmlns="http://www.w3.org/2000/svg">' + lines + '</svg>';
}

async function main() {
  fs.mkdirSync(DEBUG_OUT_DIR, { recursive: true });

  const files = fs.readdirSync(SCREENSHOTS_DIR)
    .filter(function(f) { return f.toLowerCase().endsWith('.png'); })
    .filter(function(f) { return !f.includes('grid') && !f.includes('fixed'); });

  console.log('Screenshots: ' + files.length);

  for (const file of files) {
    const src = path.join(SCREENSHOTS_DIR, file);
    const out = path.join(DEBUG_OUT_DIR, file.replace(/\.png$/i, '-grid.png'));
    const buf = fs.readFileSync(src);
    const meta = await sharp(buf).metadata();

    let grid;
    try {
      grid = getGridForResolution(meta.width, meta.height, file);
    } catch (e) {
      console.error(file + ': ' + e.message);
      continue;
    }

    const svg = buildSvg(meta.width, meta.height, grid);

    await sharp(buf)
      .composite([{ input: Buffer.from(svg), top: 0, left: 0 }])
      .png()
      .toFile(out);

    console.log('  OK ' + file);
  }

  console.log('Done. Open data/debug-grid/');
}

main().catch(function(err) { console.error('Error:', err); process.exit(1); });