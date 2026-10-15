const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const ICONS_DIR  = path.join(__dirname, 'data', 'icons');
const INDEX_FILE = path.join(__dirname, 'data', 'index.json');
const OUT_FILE   = path.join(__dirname, 'data', 'icons-hash.json');

const SIZE = 32;
const BG = { r: 24, g: 24, b: 24 };   // ← фон ячейки в игре (торговец, инвентарь)

async function main() {
  if (!fs.existsSync(INDEX_FILE)) {
    console.error('Нет data/index.json');
    process.exit(1);
  }
  const index = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8'));
  console.log('Предметов: ' + index.length);

  const hashes = [];
  let failed = 0;

  for (let i = 0; i < index.length; i++) {
    const item = index[i];
    const iconPath = path.join(ICONS_DIR, item.category, item.id + '.png');
    if (!fs.existsSync(iconPath)) { failed++; continue; }

    try {
      const buf = await sharp(iconPath)
        .resize(SIZE, SIZE, { fit: 'contain', background: { ...BG, alpha: 1 } })
        .flatten({ background: BG })
        .removeAlpha()
        .raw()
        .toBuffer();

      hashes.push({
        id: item.id,
        name: item.name,
        category: item.category,
        hash: buf.toString('base64'),
      });
    } catch (e) { failed++; }

    if ((i + 1) % 500 === 0) console.log('  обработано ' + (i + 1));
  }

  fs.writeFileSync(OUT_FILE, JSON.stringify(hashes), 'utf8');
  console.log('OK: ' + hashes.length + ' иконок (пропущено ' + failed + ')');
}

main().catch(err => { console.error('Ошибка:', err); process.exit(1); });