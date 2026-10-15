const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const OUT_FILE = path.join(__dirname, 'data', 'stalfarm-recipes.json');
const BASE = 'https://www.stalfarm.com/crafts/';

function parseIconUrl(url) {
  if (!url) return { category: null, itemId: null };
  const m = url.match(/\/icons\/(.+?)\/([^/]+)\.png/);
  if (!m) return { category: null, itemId: null };
  return { category: m[1], itemId: m[2] };
}

async function extractFromPage(page) {
  return await page.evaluate(() => {
    const buttons = document.querySelectorAll('.calcbtn');
    const result = [];

    for (const btn of buttons) {
      try {
        const raw = btn.getAttribute('data-calc');
        if (!raw) continue;
        const data = JSON.parse(raw);

        const row = btn.closest('tr');
        if (!row) continue;

        const typeEl = row.querySelector('.type');
        const perkEl = row.querySelector('.perk');
        const liqEl  = row.querySelector('.liq');
        const linkEl = row.querySelector('.itemlink');
        const imgEl  = row.querySelector('.ic');

        // ВАЖНО: textContent, а не innerText (innerText даёт КАПС из CSS)
        const perkText = perkEl?.textContent?.trim() || '';
        const skillMatch = perkText.match(/^(.+?)\s*·\s*ур\.\s*(\d+)/i);

        const liqText = liqEl?.textContent?.trim() || '';
        const liqMatch = liqText.match(/≈([\d.,]+)/);

        result.push({
          name: data.name,
          slug: linkEl?.getAttribute('href')?.replace(/^\/items\//, '').replace(/\/$/, '') || null,
          output: data.per || data.base || 1,
          energy: data.energy || 0,
          salesPerDay: liqMatch ? parseFloat(liqMatch[1].replace(',', '.')) : (data.sales || 0),
          type: typeEl?.textContent?.trim() || '',
          skill: skillMatch ? skillMatch[1].trim() : '',
          skillLevel: skillMatch ? parseInt(skillMatch[2]) : 0,
          iconUrl: imgEl?.getAttribute('src') || '',
          ingredients: (data.ing || []).map(i => ({
            name: i.n, count: i.a, iconUrl: i.ic || '',
          })),
        });
      } catch (e) {}
    }
    return result;
  });
}

async function main() {
  console.log('🚀 Парсер stalfarm.com');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  );

  const all = [];
  const seen = new Set();
  let pageNum = 1;

  while (true) {
    const url = pageNum === 1 ? BASE : `${BASE}?page=${pageNum}`;
    console.log(`📄 Страница ${pageNum}: ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2', timeout: 60000 });

    try {
      await page.waitForSelector('.calcbtn', { timeout: 15000 });
    } catch {
      console.log(`   нет рецептов, стоп`);
      break;
    }

    const recipes = await extractFromPage(page);
    let added = 0;
    for (const r of recipes) {
      const key = `${r.slug}|${r.name}`;
      if (seen.has(key)) continue;
      seen.add(key);

      // Пост-обработка: категория + itemId
      const item = parseIconUrl(r.iconUrl);
      r.category = item.category;
      r.itemId = item.itemId;
      for (const ing of r.ingredients) {
        const p = parseIconUrl(ing.iconUrl);
        ing.category = p.category;
        ing.itemId = p.itemId;
      }

      all.push(r);
      added++;
    }
    console.log(`   +${added} новых (всего ${all.length})`);

    // Проверяем, есть ли ссылка на следующую страницу
    const hasNext = await page.evaluate((n) => {
      return !!document.querySelector(`a[href*="page=${n + 1}"]`);
    }, pageNum);

    if (!hasNext) {
      console.log(`   следующей страницы нет, стоп`);
      break;
    }

    pageNum++;
    if (pageNum > 50) break; // защита
    await new Promise(r => setTimeout(r, 500));
  }

  fs.writeFileSync(OUT_FILE, JSON.stringify(all, null, 2), 'utf8');
  console.log(`\n✅ Всего рецептов: ${all.length}`);
  console.log(`📦 Сохранено: ${OUT_FILE}`);
  if (all[0]) {
    console.log('\n--- Пример первого рецепта ---');
    console.log(JSON.stringify(all[0], null, 2));
  }
  await browser.close();
}

main().catch(err => { console.error('❌', err); process.exit(1); });