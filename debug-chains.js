const fs = require('fs');
const path = require('path');

const RECIPES_FILE = path.join(__dirname, 'data', 'stalfarm-recipes.json');
const recipes = JSON.parse(fs.readFileSync(RECIPES_FILE, 'utf8'));

// Строим карту: itemId → рецепт
const recipeByItemId = {};
for (const r of recipes) {
  if (!r.itemId) continue;
  recipeByItemId[r.itemId] = r;
}

console.log(`Всего рецептов: ${recipes.length}`);
console.log(`Уникальных itemId: ${Object.keys(recipeByItemId).length}`);

// ─── 1. Какие ингредиенты сами имеют рецепт? ───
console.log('\n══════════ ИНГРЕДИЕНТЫ, У КОТОРЫХ ЕСТЬ СВОЙ РЕЦЕПТ ══════════');

let foundChains = 0;
const chains = [];

for (const r of recipes) {
  for (const ing of r.ingredients) {
    if (!ing.itemId) continue;
    const subRecipe = recipeByItemId[ing.itemId];
    if (subRecipe) {
      foundChains++;
      chains.push({
        parent: r.name,
        parentId: r.itemId,
        ingredient: ing.name,
        ingredientId: ing.itemId,
        ingredientCount: ing.count,
        subRecipeOutput: subRecipe.output,
      });
    }
  }
}

console.log(`Найдено цепочек: ${foundChains}`);
for (const c of chains.slice(0, 30)) {
  console.log(`  ${c.parent} → ${c.ingredientCount}× ${c.ingredient} (рецепт даёт ${c.subRecipeOutput} шт)`);
}

// ─── 2. Глубина вложенности ───
console.log('\n══════════ ГЛУБИНА ЦЕПОЧЕК ══════════');

function depthOf(itemId, visited = new Set(), depth = 0) {
  if (depth > 10) return depth;   // защита
  if (visited.has(itemId)) return -1;  // цикл
  visited.add(itemId);
  const r = recipeByItemId[itemId];
  if (!r) return depth;
  let maxChildDepth = depth;
  for (const ing of r.ingredients) {
    if (!ing.itemId) continue;
    const d = depthOf(ing.itemId, new Set(visited), depth + 1);
    if (d > maxChildDepth) maxChildDepth = d;
  }
  return maxChildDepth;
}

const depths = {};
for (const r of recipes) {
  const d = depthOf(r.itemId);
  if (!depths[d]) depths[d] = [];
  depths[d].push(r.name);
}

for (const d of Object.keys(depths).sort((a, b) => a - b)) {
  console.log(`  Глубина ${d}: ${depths[d].length} рецептов`);
  if (parseInt(d) >= 2) {
    for (const name of depths[d].slice(0, 5)) {
      console.log(`     · ${name}`);
    }
  }
}

// ─── 3. Циклы ───
console.log('\n══════════ ЦИКЛЫ ══════════');

const cyclesFound = [];
function findCycles(itemId, path = [], visited = new Set()) {
  if (path.includes(itemId)) {
    cyclesFound.push([...path, itemId]);
    return;
  }
  if (visited.has(itemId)) return;
  visited.add(itemId);
  const r = recipeByItemId[itemId];
  if (!r) return;
  for (const ing of r.ingredients) {
    if (!ing.itemId) continue;
    findCycles(ing.itemId, [...path, itemId], new Set(visited));
  }
}

for (const r of recipes) {
  findCycles(r.itemId);
}

if (cyclesFound.length === 0) {
  console.log('  Циклов не найдено ✅');
} else {
  const uniqueCycles = [];
  for (const c of cyclesFound) {
    const key = [...c].sort().join('|');
    if (!uniqueCycles.find(u => [...u].sort().join('|') === key)) {
      uniqueCycles.push(c);
    }
  }
  console.log(`Найдено циклов: ${uniqueCycles.length}`);
  for (const c of uniqueCycles.slice(0, 10)) {
    console.log(`  ${c.join(' → ')}`);
  }
}

// ─── 4. Контейнеры-полуфабрикаты («Сумки») ───
console.log('\n══════════ КОНТЕЙНЕРЫ (требуют ручной проверки) ══════════');

const containers = recipes.filter(r =>
  /^(сумка|фермент|автотрансформатор)/i.test(r.name)
);

for (const c of containers) {
  console.log(`  ${c.name}  [${c.itemId}]  output=${c.output}`);
  console.log(`     Ингредиенты: ${c.ingredients.map(i => `${i.count}× ${i.name}`).join(', ')}`);
}

fs.writeFileSync(
  path.join(__dirname, 'data', 'debug-chains.txt'),
  JSON.stringify({ chains, depths, cycles: cyclesFound, containers }, null, 2),
  'utf8'
);

console.log('\n📦 Полный отчёт: data/debug-chains.txt');