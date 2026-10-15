// Парсер рецептов убежища с stalfarm.com
// Запуск: node parse-recipes.js

const fs = require('fs');
const path = require('path');

const OUT_FILE = path.join(__dirname, 'data', 'hideout-recipes.json');

// Список известных рецептов (собирается вручную или парсится)
const RECIPE_URLS = [
  'https://www.stalfarm.com/items/alcobull/',
  'https://www.stalfarm.com/items/astrixin/',
  'https://www.stalfarm.com/items/biopatch/',
  // ... добавляй сюда все рецепты
];

// Простой HTML-парсер (без внешних библиотек)
function extractIngredients(html) {
  const result = [];
  // Ищем блоки ингредиентов
  const regex = /(\d+)×\s*([^<]+?)\s*<span/g;
  let match;
  while ((match = regex.exec(html)) !== null) {
    const count = parseInt(match[1]);
    const name = match[2].trim();
    if (count > 0 && name) {
      result.push({ count, name });
    }
  }
  return result;
}

function extractEnergy(html) {
  const match = html.match(/(\d+)\s*Energy/);
  return match ? parseInt(match[1]) : 0;
}

function extractOutput(html) {
  const match = html.match(/(\d+)\s*×\s*[^<]+?<\/a>\s*<\/div>/);
  return match ? parseInt(match[1]) : 1;
}

async function parseRecipes() {
  const recipes = [];

  for (const url of RECIPE_URLS) {
    try {
      const res = await fetch(url);
      const html = await res.text();

      const nameMatch = html.match(/<h1[^>]*>([^<]+)<\/h1>/);
      const name = nameMatch ? nameMatch[1].trim() : url.split('/').pop();

      const ingredients = extractIngredients(html);
      const energy = extractEnergy(html);
      const output = extractOutput(html);

      if (ingredients.length > 0) {
        recipes.push({
          name,
          url,
          output,
          energy,
          ingredients,
          category: 'unknown',
        });
        console.log(`✅ ${name}: ${ingredients.length} ингредиентов, ${energy} энергии`);
      } else {
        console.log(`⚠️ ${name}: ингредиенты не найдены`);
      }
    } catch (err) {
      console.error(`❌ ${url}: ${err.message}`);
    }
  }

  fs.writeFileSync(OUT_FILE, JSON.stringify(recipes, null, 2), 'utf8');
  console.log(`\n📦 Сохранено: ${OUT_FILE}`);
  console.log(`   Рецептов: ${recipes.length}`);
}

parseRecipes();