const fs = require('fs');
const path = require('path');

const RECIPES_FILE = path.join(__dirname, 'data', 'stalfarm-recipes.json');
const CACHE_FILE   = path.join(__dirname, 'data', 'medians-cache.json');
const OUT_JSON     = path.join(__dirname, 'data', 'craft-profit.json');
const OUT_TXT      = path.join(__dirname, 'data', 'craft-profit.txt');

const ENERGY_PRICE = 1;
const COMMISSION   = 0.05;

const BONUS_MODE = 'cap1';

const MY_SKILLS = {
  'Боеприпасы':           2,
  'Пиротехника':          1,
  'Защитное снаряжение':  1,
  'Инженерия':            4,
  'Кулинария':            3,
  'Самогоноварение':      4,
  'Медицина':             4,
  'Сырьё и материалы':    5,
};

function normSkill(s) {
  return String(s || '').toLowerCase().replace(/ё/g, 'е').replace(/\s+/g, ' ').trim();
}
const SKILLS_NORM = {};
for (const [name, level] of Object.entries(MY_SKILLS)) {
  SKILLS_NORM[normSkill(name)] = { name, level };
}
function getMySkillLevel(skillName) {
  const n = SKILLS_NORM[normSkill(skillName)];
  return n ? n.level : 0;
}

if (!fs.existsSync(RECIPES_FILE)) {
  console.error('❌ Нет файла: ' + RECIPES_FILE);
  process.exit(1);
}
if (!fs.existsSync(CACHE_FILE)) {
  console.error('❌ Нет файла: ' + CACHE_FILE);
  process.exit(1);
}

const recipes = JSON.parse(fs.readFileSync(RECIPES_FILE, 'utf8'));
const cache   = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));

// ─── Вендорские цены ───
const VENDOR_FILE = path.join(__dirname, 'data', 'vendor-prices.json');
let vendorPrices = {};
if (fs.existsSync(VENDOR_FILE)) {
  try {
    const raw = JSON.parse(fs.readFileSync(VENDOR_FILE, 'utf8'));
    for (const [id, entry] of Object.entries(raw)) {
      if (id.startsWith('_')) continue;
      if (entry && typeof entry.price === 'number' && entry.price > 0) {
        vendorPrices[id] = entry;
      }
    }
    console.log(`[vendor] загружено цен: ${Object.keys(vendorPrices).length}`);
  } catch (e) {
    console.error('[vendor] ошибка парсинга:', e.message);
  }
} else {
  console.log('[vendor] файл vendor-prices.json не найден');
}

function getGroups(itemId) {
  const entry = cache[itemId];
  if (!entry || !entry.medians) return [];
  return Object.entries(entry.medians)
    .filter(([, v]) => v > 0)
    .map(([k, v]) => {
      const [q, p] = k.split('|');
      return {
        q: q === 'null' ? null : Number(q),
        p: p === 'null' ? null : Number(p),
        price: v,
      };
    });
}

function getBasePrice(itemId) {
  const groups = getGroups(itemId);

  // 1. Аукционная цена
  let auctionPrice = 0;
  let auctionSource = 'нет данных';
  if (groups.length) {
    const noPtn = groups.filter(g => g.p === null);
    if (noPtn.length) {
      noPtn.sort((a, b) => (a.q ?? 0) - (b.q ?? 0));
      auctionPrice = noPtn[0].price;
      auctionSource = `аукцион (qlt=${noPtn[0].q ?? 'null'})`;
    } else {
      groups.sort((a, b) => a.price - b.price);
      auctionPrice = groups[0].price;
      auctionSource = `аукцион fallback`;
    }
  }

  // 2. Вендорская цена
  const vendor = vendorPrices[itemId];
  const vendorPrice = vendor?.price || 0;

  // 3. Берём минимум
  if (vendorPrice > 0 && (auctionPrice === 0 || vendorPrice < auctionPrice)) {
    return {
      price: Math.round(vendorPrice * 100) / 100,
      source: `вендор: ${vendor.name || itemId}`,
    };
  }

  return {
    price: Math.round(auctionPrice * 100) / 100,
    source: auctionSource,
  };
}

function bonusOutput(baseOutput, skillName, reqLevel) {
  if (BONUS_MODE === 'off') return baseOutput;
  const myLevel = getMySkillLevel(skillName);
  if (!myLevel || myLevel <= reqLevel) return baseOutput;
  const diff = myLevel - reqLevel;
  const chance = diff * 75;
  if (BONUS_MODE === 'cap1') {
    return chance >= 100 ? baseOutput + 1 : baseOutput;
  }
  if (BONUS_MODE === 'prob') {
    return Math.floor(baseOutput + Math.min(1, chance / 100));
  }
  return baseOutput;
}

const recipeSkills = new Set();
for (const r of recipes) if (r.skill) recipeSkills.add(r.skill);

const rows = [];
const txtLines = [];
const skipped = { noIngredient: 0, noOutput: 0 };

txtLines.push('═══════════════════════════════════════════════════════');
txtLines.push('  КРАФТ STALZONE — расчёт прибыли');
txtLines.push(`  Энергия: ${ENERGY_PRICE} ₽/ед.  ·  Комиссия: ${COMMISSION * 100}%`);
txtLines.push(`  Бонусный крафт: ${BONUS_MODE}`);
txtLines.push(`  Ликвидность: своя (из EAPI) — окно 7 дней, fallback 30`);
txtLines.push(`  Мои навыки: ${JSON.stringify(MY_SKILLS)}`);
txtLines.push('═══════════════════════════════════════════════════════');

for (const r of recipes) {
  let ingCost = 0;
  const missing = [];
  const ingDetails = [];

  for (const ing of r.ingredients) {
    const { price, source } = getBasePrice(ing.itemId);
    if (!price) { missing.push(ing.name); continue; }
    ingCost += price * ing.count;
    ingDetails.push({
      name: ing.name, count: ing.count, itemId: ing.itemId,
      unitPrice: price, source,
    });
  }

  if (missing.length) { skipped.noIngredient++; continue; }

  const outInfo = getBasePrice(r.itemId);
  if (!outInfo.price) { skipped.noOutput++; continue; }

  const outputWithBonus = bonusOutput(r.output, r.skill, r.skillLevel);
  const energyCost      = r.energy * ENERGY_PRICE;
  const totalCost       = ingCost + energyCost;
  const revenueNet      = outInfo.price * outputWithBonus * (1 - COMMISSION);
  const profit          = revenueNet - totalCost;
  const roi             = totalCost > 0 ? (profit / totalCost) * 100 : 0;
  const myLevel         = getMySkillLevel(r.skill);

  const outEntry      = cache[r.itemId];
  const mySalesPerDay = outEntry?.salesPerDay || 0;
  const myTotalCount  = outEntry?.totalCount  || 0;
  const myWindowUsed  = outEntry?.windowUsed  || 0;
  const myDaysCovered = outEntry?.daysCovered || 0;

  rows.push({
    name: r.name,
    slug: r.slug,
    itemId: r.itemId,
    category: r.category,
    type: r.type,
    skill: r.skill,
    skillLevel: r.skillLevel,
    myLevel,
    baseOutput: r.output,
    outputWithBonus,
    energy: r.energy,
    ingCost,
    energyCost,
    totalCost,
    outPricePerUnit: outInfo.price,
    outSource: outInfo.source,
    revenueNet,
    profit,
    roi,
    salesPerDay: mySalesPerDay,
    stalfarmSalesPerDay: r.salesPerDay,
    totalCount: myTotalCount,
    windowUsed: myWindowUsed,
    daysCovered: myDaysCovered,
    ingredients: ingDetails,
  });
}

rows.sort((a, b) => b.profit - a.profit);

txtLines.push('');
txtLines.push(`Всего рецептов: ${recipes.length}`);
txtLines.push(`Обработано: ${rows.length}`);
txtLines.push(`Пропущено (нет цен ингредиентов): ${skipped.noIngredient}`);
txtLines.push(`Пропущено (нет цены готового): ${skipped.noOutput}`);
txtLines.push('');
txtLines.push('────── ТОП-30 ПО ПРИБЫЛИ ──────');

for (const r of rows.slice(0, 30)) {
  const bonus = r.outputWithBonus !== r.baseOutput
    ? ` (база ${r.baseOutput} → +1 бонус = ${r.outputWithBonus})` : '';
  const myInfo = r.myLevel ? ` / у меня ур.${r.myLevel}` : ' / навык не указан';
  const lowLiq = r.salesPerDay < 100 ? '  ⚠️ НИЗКАЯ ЛИКВИДНОСТЬ' : '';

  txtLines.push('');
  txtLines.push(`▶ ${r.name}  [${r.type}, ${r.skill} ур.${r.skillLevel}${myInfo}]${lowLiq}`);
  txtLines.push(`   💰 ПРИБЫЛЬ:   ${Math.round(r.profit).toLocaleString('ru-RU')} ₽   (ROI ${r.roi.toFixed(1)}%)`);
  txtLines.push(`   Выход: ${r.outputWithBonus} шт${bonus}  ·  Энергия: ${r.energy}`);
  txtLines.push(`   Себестоимость: ${Math.round(r.totalCost).toLocaleString('ru-RU')} ₽ (ингр. ${Math.round(r.ingCost).toLocaleString('ru-RU')} + энергия ${r.energyCost.toLocaleString('ru-RU')})`);
  txtLines.push(`   Продажа:       ${Math.round(r.revenueNet).toLocaleString('ru-RU')} ₽ (${r.outPricePerUnit.toLocaleString('ru-RU')}/шт × ${r.outputWithBonus} − 5%)`);
  txtLines.push(`   Источник цены выхода: ${r.outSource}`);
  if (r.salesPerDay > 0) {
    txtLines.push(`   Ликвидность:   ${r.salesPerDay} прод/день (${r.totalCount} сделок за ${r.daysCovered} дн.)`);
  }
  txtLines.push('   Ингредиенты:');
  for (const ing of r.ingredients) {
    txtLines.push(`      ${String(ing.count).padStart(3)}× ${ing.name.padEnd(35)} ${ing.unitPrice.toLocaleString('ru-RU').padStart(10)} ₽/шт = ${(ing.unitPrice * ing.count).toLocaleString('ru-RU').padStart(12)} ₽  [${ing.source}]`);
  }
}

const lowLiqRows = rows
  .filter(r => r.salesPerDay < 100 && r.profit > 0)
  .sort((a, b) => b.roi - a.roi)
  .slice(0, 15);

if (lowLiqRows.length) {
  txtLines.push('');
  txtLines.push('────── ВЫСОКИЙ ROI, НО НИЗКАЯ ЛИКВИДНОСТЬ ──────');
  for (const r of lowLiqRows) {
    txtLines.push(`${r.name.padEnd(40)} ROI ${r.roi.toFixed(1).padStart(6)}%  ·  ${String(r.salesPerDay).padStart(6)} прод/день`);
  }
}

txtLines.push('');
txtLines.push('────── ТОП-10 УБЫТОЧНЫХ ──────');
const lossRows = rows.filter(r => r.profit < 0).slice(-10).reverse();
if (lossRows.length) {
  for (const r of lossRows) {
    txtLines.push(`${r.name.padEnd(40)} убыток ${Math.round(r.profit).toLocaleString('ru-RU').padStart(12)} ₽  (ROI ${r.roi.toFixed(1)}%)`);
  }
} else {
  txtLines.push('(нет убыточных рецептов)');
}

fs.writeFileSync(OUT_JSON, JSON.stringify(rows, null, 2), 'utf8');
fs.writeFileSync(OUT_TXT, txtLines.join('\n'), 'utf8');

console.log('✅ Готово!');
console.log(`   Обработано: ${rows.length} из ${recipes.length}`);
console.log(`   Пропущено (нет ингредиентов): ${skipped.noIngredient}`);
console.log(`   Пропущено (нет цены выхода): ${skipped.noOutput}`);
console.log(`   JSON: ${OUT_JSON}`);
console.log(`   TXT:  ${OUT_TXT}`);

if (rows[0]) {
  console.log('\n🏆 ТОП-5 по прибыли:');
  for (const r of rows.slice(0, 5)) {
    console.log(`   ${r.name} → ${Math.round(r.profit).toLocaleString('ru-RU')} ₽ (ROI ${r.roi.toFixed(1)}%, ${r.salesPerDay} прод/день)`);
  }

  if (lowLiqRows.length) {
    console.log('\n⚠️  Высокий ROI, но низкая ликвидность:');
    for (const r of lowLiqRows.slice(0, 5)) {
      console.log(`   ${r.name} → ROI ${r.roi.toFixed(1)}%, всего ${r.salesPerDay} прод/день`);
    }
  }
}

console.log('\n📚 Профессии из рецептов:');
for (const s of recipeSkills) {
  const myLvl = getMySkillLevel(s);
  const icon = myLvl > 0 ? '✅' : '⚠️ ';
  console.log(`   ${icon} ${s}${myLvl ? ` = ${myLvl}` : ' — НЕ УКАЗАН'}`);
}