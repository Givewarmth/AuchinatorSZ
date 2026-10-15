const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const OUT_FILE = path.join(__dirname, 'data', 'stalfarm-debug.txt');
const URL = 'https://www.stalfarm.com/crafts/';

async function main() {
  const log = [];
  const push = (line) => { log.push(line); console.log(line); };

  push('🚀 Диагностика stalfarm.com');

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });
  const page = await browser.newPage();
  await page.setUserAgent(
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  );

  // Логируем все запросы к серверу
  const requests = [];
  page.on('request', (req) => {
    const url = req.url();
    // Пропускаем картинки, шрифты и стили
    if (/\.(png|jpg|jpeg|gif|svg|woff2?|css|ico)$/i.test(url)) return;
    // Пропускаем аналитику
    if (/google|analytics|yandex|facebook|sentry/i.test(url)) return;
    requests.push({ method: req.method(), url, type: req.resourceType() });
  });

  push(`📄 Открываю ${URL}`);
  await page.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('.calcbtn', { timeout: 30000 });

  const countInitial = await page.$$eval('.calcbtn', els => els.length);
  push(`📊 Изначально на странице .calcbtn: ${countInitial}`);

  // Скроллим до конца несколько раз
  for (let i = 0; i < 15; i++) {
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await new Promise(r => setTimeout(r, 1000));
    const count = await page.$$eval('.calcbtn', els => els.length);
    push(`   Скролл ${i + 1}: ${count} рецептов`);
    if (count >= 373) break;
  }

  // Ищем кнопки "показать ещё", "загрузить ещё", "load more"
  const moreButtons = await page.evaluate(() => {
    const buttons = [...document.querySelectorAll('button, a')];
    return buttons
      .filter(b => /ещё|еще|больше|more|load/i.test(b.innerText))
      .map(b => ({ text: b.innerText.trim(), tag: b.tagName, cls: b.className }));
  });
  push(`\n🔘 Кнопки "показать ещё": ${JSON.stringify(moreButtons)}`);

  // Ищем ссылки на пагинацию
  const paginationLinks = await page.evaluate(() => {
    return [...document.querySelectorAll('a')]
      .map(a => ({ text: a.innerText.trim(), href: a.href }))
      .filter(l => /page=|стр=|page\//.test(l.href) || /^\d+$/.test(l.text))
      .slice(0, 20);
  });
  push(`\n🔗 Ссылки пагинации: ${JSON.stringify(paginationLinks, null, 2)}`);

  // Смотрим на HTML одной строки — где находится .perk
  const perkSample = await page.evaluate(() => {
    const btn = document.querySelector('.calcbtn');
    const row = btn?.closest('tr');
    const perkEl = row?.querySelector('.perk');
    const typeEl = row?.querySelector('.type');
    return {
      hasRow: !!row,
      hasPerk: !!perkEl,
      perkInnerText: perkEl?.innerText,
      perkTextContent: perkEl?.textContent,
      perkHTML: perkEl?.outerHTML,
      typeInnerText: typeEl?.innerText,
      typeTextContent: typeEl?.textContent,
    };
  });
  push(`\n📝 Debug .perk: ${JSON.stringify(perkSample, null, 2)}`);

  // Итоговая структура DOM
  const totalButtons = await page.$$eval('.calcbtn', els => els.length);
  const totalRows = await page.$$eval('tr.datarow', els => els.length);
  push(`\n📊 Итог: .calcbtn = ${totalButtons}, tr.datarow = ${totalRows}`);

  // Список всех не-картиночных запросов
  push(`\n🌐 Всего запросов (без картинок): ${requests.length}`);
  const uniqueUrls = [...new Set(requests.map(r => r.url))];
  push(`\nУникальные URL запросов:`);
  uniqueUrls.slice(0, 40).forEach(u => push(`   ${u}`));

  fs.writeFileSync(OUT_FILE, log.join('\n'), 'utf8');
  push(`\n✅ Сохранено: ${OUT_FILE}`);

  await browser.close();
}

main().catch(err => { console.error('❌', err); process.exit(1); });