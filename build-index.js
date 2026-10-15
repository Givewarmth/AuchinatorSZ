const fs = require('fs');
const path = require('path');

const ITEMS_DIR = path.join(__dirname, 'data', 'items');
const OUT_FILE  = path.join(__dirname, 'data', 'index.json');
const LANG = 'ru';

function walk(dir, files = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) walk(full, files);
    else if (e.name.toLowerCase().endsWith('.json')) files.push(full);
  }
  return files;
}

function extractName(json) {
  const n = json.name;
  if (n && typeof n === 'object') {
    if (n.lines && typeof n.lines === 'object') {
      const v = n.lines[LANG] || n.lines.ru || n.lines.en;
      if (typeof v === 'string' && v.trim()) return v.trim();
    }
    if (typeof n.ru === 'string' && n.ru.trim()) return n.ru.trim();
    if (typeof n.en === 'string' && n.en.trim()) return n.en.trim();
  }
  if (typeof n === 'string' && n.trim()) return n.trim();
  return null;
}

function extractColor(json) {
  return json.color || '';
}

if (!fs.existsSync(ITEMS_DIR)) {
  console.error('Не найдена папка: ' + ITEMS_DIR);
  console.error('Скопируй ru/items в data/items.');
  process.exit(1);
}

const files = walk(ITEMS_DIR);
console.log('Найдено JSON-файлов: ' + files.length);

const index = [];
let skipped = 0;

for (const file of files) {
  try {
    const json = JSON.parse(fs.readFileSync(file, 'utf8'));
    const id    = String(json.id || path.basename(file, '.json')).trim();
    const name  = extractName(json);
    const color = extractColor(json);
    if (!id || !name) { skipped++; continue; }
    index.push({ id, name, category: json.category || null, color });
  } catch (err) {
    skipped++;
  }
}

const unique = Array.from(new Map(index.map(x => [x.id, x])).values());
unique.sort((a, b) => a.name.localeCompare(b.name, 'ru'));

fs.writeFileSync(OUT_FILE, JSON.stringify(unique, null, 2), 'utf8');

console.log('Индекс сохранён: ' + OUT_FILE);
console.log('Записей: ' + unique.length);
if (skipped) console.log('Пропущено: ' + skipped);