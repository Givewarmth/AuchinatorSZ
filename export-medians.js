const fs = require('fs');
const path = require('path');

const CACHE_FILE = path.join(__dirname, 'data', 'medians-cache.json');
const OUT_TSV    = path.join(__dirname, 'data', 'medians.tsv');
const OUT_TXT    = path.join(__dirname, 'data', 'medians.txt');

if (!fs.existsSync(CACHE_FILE)) {
  console.error('❌ Нет файла кэша: data/medians-cache.json');
  console.error('   Сначала нажми «📥 Скачать всю базу» в приложении.');
  process.exit(1);
}

const cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));

const QUALITY_NAMES = {
  0: 'Обычный', 1: 'Необычный', 2: 'Особый', 3: 'Редкий',
  4: 'Исключительный', 5: 'Легендарный', 6: 'Уникальный',
};

const RANGE_LABELS = {
  '0':  '+0 – +4',
  '5':  '+5 – +9',
  '10': '+10 – +14',
  '15': '+15',
};

const MIN_SAMPLES  = 50;
const EXCLUDE_CATS = ['artefact'];   // ← исключаем эти категории
const PRICE_DIVIDE = 2;              // ← делим цену на это число

const rows = [];
const txtLines = [];

const entries = Object.values(cache)
  .filter(e => e && e.medians && Object.keys(e.medians).length > 0)
  // Исключаем артефакты
  .filter(e => {
    const cat = String(e.category || '');
    return !EXCLUDE_CATS.some(ex => cat.startsWith(ex + '/') || cat === ex);
  })
  .sort((a, b) => (a.name || '').localeCompare(b.name || '', 'ru'));

let itemsWithMedian = 0;
let groupsWithMedian = 0;
let excludedCount = 0;

// Подсчёт исключённых
for (const e of Object.values(cache)) {
  const cat = String(e?.category || '');
  if (EXCLUDE_CATS.some(ex => cat.startsWith(ex + '/') || cat === ex)) {
    excludedCount++;
  }
}

for (const entry of entries) {
  const groups = Object.entries(entry.medians)
    .filter(([, v]) => v > 0)
    .map(([k, v]) => {
      const [q, r] = k.split('|');
      const count = entry.counts?.[k] || 0;
      return {
        q: q === 'null' ? null : Number(q),
        r: r === 'null' ? null : Number(r),
        price: v,
        count,
      };
    })
    .filter(g => g.count >= MIN_SAMPLES)
    .sort((a, b) => {
      if (a.q !== b.q) return (a.q ?? 99) - (b.q ?? 99);
      return (a.r ?? 99) - (b.r ?? 99);
    });

  if (!groups.length) continue;
  itemsWithMedian++;

  txtLines.push('');
  txtLines.push(`▶ ${entry.name}  [${entry.id}]`);
  txtLines.push(`  Категория: ${entry.category || '—'}`);

  for (const g of groups) {
    const qName = g.q == null ? '—' : (QUALITY_NAMES[g.q] || `Q${g.q}`);
    const rLabel = g.r == null ? '—' : (RANGE_LABELS[String(g.r)] || `+${g.r}`);

    // Делим медиану
    const adjustedPrice = Math.round(g.price / PRICE_DIVIDE);

    txtLines.push(`    ${qName.padEnd(16)} ${rLabel.padEnd(12)} ${String(adjustedPrice).padStart(12)} ₽   (${g.count} сделок)`);

    rows.push([
      entry.name,
      entry.id,
      entry.category || '',
      qName,
      rLabel,
      adjustedPrice,
      g.count,
    ]);
    groupsWithMedian++;
  }
}

// ---- TSV ----
const header = ['Название', 'ID', 'Категория', 'Редкость', 'Уровень', 'Медиана, ₽', 'Сделок'];
const tsvLines = [header.join('\t')];
for (const r of rows) tsvLines.push(r.join('\t'));
fs.writeFileSync(OUT_TSV, '\uFEFF' + tsvLines.join('\n'), 'utf8');

// ---- TXT ----
fs.writeFileSync(OUT_TXT, txtLines.join('\n'), 'utf8');

console.log(`✅ Готово!`);
console.log(`   Всего предметов в кэше: ${Object.keys(cache).length}`);
console.log(`   Исключено (артефактов): ${excludedCount}`);
console.log(`   Предметов с медианой (≥${MIN_SAMPLES} сделок): ${itemsWithMedian}`);
console.log(`   Строк (группа×предмет): ${groupsWithMedian}`);
console.log(`   Медианы поделены на: ${PRICE_DIVIDE}`);
console.log(`   TSV (для Excel):  ${OUT_TSV}`);
console.log(`   TXT (читаемый):   ${OUT_TXT}`);