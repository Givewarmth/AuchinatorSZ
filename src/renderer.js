const tbody          = document.querySelector('#lotsTable tbody');
const lotsTable      = document.getElementById('lotsTable');
const lotsTitle      = document.getElementById('lotsTitle');
const itemSearch     = document.getElementById('itemSearch');
const suggestions    = document.getElementById('suggestions');
const downloadBtn    = document.getElementById('downloadBtn');
const stopBtn        = document.getElementById('stopBtn');
const clearBtn       = document.getElementById('clearBtn');
const filterQlt      = document.getElementById('filterQlt');
const filterPtn      = document.getElementById('filterPtn');
const categoryFilter = document.getElementById('categoryFilter');
const minMedian      = document.getElementById('minMedian');
const statusInline   = document.getElementById('statusInline');
const cacheInfo      = document.getElementById('cacheInfo');

let selectedItem = null;
let searchTimer  = null;
let medianTimer  = null;
let lastData     = null;
let currentMode  = 'none';
let isLoading    = false;

const fmt = (n) => (n ?? 0).toLocaleString('ru-RU') + ' ₽';

const QUALITY_NAMES = {
  0: 'Обычный', 1: 'Необычный', 2: 'Особый', 3: 'Редкий',
  4: 'Исключительный', 5: 'Легендарный', 6: 'Уникальный',
};

const CATEGORY_NAMES = {
  weapon: 'Оружие', weapon_modules: 'Оружейные модули', attachment: 'Обвесы',
  armor: 'Броня и костюмы', artefact: 'Артефакты', backpacks: 'Рюкзаки и сумки',
  bullet: 'Патроны', containers: 'Контейнеры', device: 'Устройства',
  grenade: 'Гранаты', medicine: 'Медикаменты и еда', misc: 'Прочее',
  other: 'Разное', supply: 'Расходники',
};

const categoryName = (key) => CATEGORY_NAMES[key] || key;
const qualityName  = (q) => q == null ? '—' : (QUALITY_NAMES[q] || `Q${q}`);

// Округление ptn к 4 группам
function ptnRange(ptn) {
  if (ptn == null) return null;
  const n = Number(ptn);
  if (Number.isNaN(n)) return null;
  if (n >= 15) return 15;
  if (n >= 10) return 10;
  if (n >= 5)  return 5;
  return 0;
}

function timeAgo(iso) {
  if (!iso) return '—';
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60)    return `${diff} сек назад`;
  if (diff < 3600)  return `${Math.floor(diff / 60)} мин назад`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} ч назад`;
  return `${Math.floor(diff / 86400)} дн назад`;
}

// ---- Прогресс ----
if (window.api?.onProgress) {
  window.api.onProgress(({ phase, loaded, total }) => {
    const name = phase === 'lots' ? 'лотов' : 'истории';
    if (isLoading) tbody.innerHTML = `<tr><td colspan="8" class="loading">Загрузка ${name}: ${loaded}${total ? ' из ' + total : ''}...</td></tr>`;
  });
}

if (window.api?.onCategoryProgress) {
  window.api.onCategoryProgress(({ loaded, total }) => {
    if (isLoading) tbody.innerHTML = `<tr><td colspan="8" class="loading">Загрузка лотов категории: ${loaded} из ${total} предметов...</td></tr>`;
  });
}

if (window.api?.onCacheProgress) {
  window.api.onCacheProgress(({ loaded, total, skipped }) => {
    const pct = total ? Math.round((loaded / total) * 100) : 0;
    if (!window.__dlStart) window.__dlStart = Date.now();
    const elapsed = (Date.now() - window.__dlStart) / 1000;
    const perItem = loaded > 0 ? elapsed / loaded : 0;
    const remaining = Math.max(0, Math.round(perItem * (total - loaded)));
    const etaText = remaining > 0
      ? `осталось ~${Math.floor(remaining / 60)}:${String(remaining % 60).padStart(2, '0')}`
      : '';
    if (isLoading) {
      tbody.innerHTML = `<tr><td colspan="8" class="loading">
        Скачивание медиан: <strong>${loaded}</strong> из <strong>${total}</strong> (${pct}%)${skipped ? ` · пропущено: ${skipped}` : ''}
        ${etaText ? `<br><span style="color:#6a7486;font-size:12px">${etaText}</span>` : ''}
      </td></tr>`;
      setStatus(`Скачивание: <strong>${loaded}/${total}</strong> (${pct}%)${skipped ? ` · пропущено: ${skipped}` : ''}`);
    }
  });
}

function setStatus(html) { statusInline.innerHTML = html; }

async function showHealth() {
  try {
    const h = await window.api.health();
    const s = await window.api.cacheStats();
    cacheInfo.innerHTML = `Регион: <strong>${h.region}</strong> · 
      Предметов: <strong>${h.itemsLoaded}</strong> · 
      Медиан в кэше: <strong>${s.count}</strong> (${(s.sizeBytes / 1024).toFixed(1)} КБ)`;
  } catch (err) {
    cacheInfo.textContent = 'Ошибка: ' + err.message;
  }
}

async function loadCategories() {
  try {
    const list = await window.api.listCategories();
    if (!Array.isArray(list) || !list.length) return;
    const options = list.map(c =>
      `<option value="${c.key}">${categoryName(c.key)} (${c.count})</option>`
    ).join('');
    categoryFilter.innerHTML = '<option value="">Все категории</option>' + options;
  } catch (err) {
    console.error('loadCategories:', err);
  }
}

function renderSuggestions(items, category) {
  if (!items.length) {
    suggestions.classList.add('hidden');
    suggestions.innerHTML = '';
    return;
  }
  const header = category
    ? `<div class="sugg-header">${categoryName(category)} — ${items.length} предметов</div>`
    : '';
  const list = items.map(it => `
    <li data-id="${it.id}" data-name="${it.name}" data-category="${it.category || ''}">
      ${it.name}<span class="cat">${it.category || ''}</span>
    </li>`).join('');
  suggestions.innerHTML = header + list;
  suggestions.classList.remove('hidden');
}

function hideSuggestions() { suggestions.classList.add('hidden'); }

async function refreshSuggestions() {
  const query = itemSearch.value.trim();
  const category = categoryFilter.value;
  if (!query && !category) { hideSuggestions(); return; }
  const items = await window.api.searchItems({ query, category });
  renderSuggestions(items, category);
}

// ---- Фильтры ----
function updateQltOptions(lots) {
  const counts = {};
  for (const l of lots) {
    if (l.qlt == null) continue;
    counts[l.qlt] = (counts[l.qlt] || 0) + 1;
  }
  const keys = Object.keys(counts).map(Number).sort((a, b) => a - b);
  const cur = filterQlt.value;
  filterQlt.innerHTML = '<option value="">Все</option>' +
    keys.map(q => `<option value="${q}">${qualityName(q)} (${counts[q]})</option>`).join('');
  if (keys.map(String).includes(cur)) filterQlt.value = cur;
}

function updatePtnOptions(lots) {
  // Считаем лоты по 4 диапазонам
  const ranges = { 0: 0, 5: 0, 10: 0, 15: 0 };
  for (const l of lots) {
    const r = ptnRange(l.ptn);
    if (r == null) continue;
    ranges[r] = (ranges[r] || 0) + 1;
  }
  const cur = filterPtn.value;
  filterPtn.innerHTML = '<option value="">Все</option>' +
    [0, 5, 10, 15].map(r => {
      const c = ranges[r] || 0;
      const label = r === 0 ? '+0 – +4' : `+${r} – +${r + 4 === 19 ? 15 : r + 4}`;
      const shortLabel = r === 15 ? '+15' : `+${r}–+${r + 4}`;
      return `<option value="${r}">${shortLabel}${c ? ` (${c})` : ''}</option>`;
    }).join('');
  if (['0','5','10','15'].includes(cur)) filterPtn.value = cur;
}

function rowFor(lot, mode) {
  const itemClass = (lot.qlt == null) ? 'q-text-unknown' : `q-text-${lot.qlt}`;
  const showUnit = lot.amount > 1;
  // Показываем реальный ptn лота (например +13)
  const ptnLabel = lot.ptn == null ? '—' : (lot.ptn === 0 ? '+0' : '+' + lot.ptn);

  if (mode === 'category') {
    const hasMedian = lot.hasMedian;
    const dealClass = !hasMedian ? 'deal-none'
                    : lot.dealPercent < 0 ? 'profit-positive'
                    : lot.dealPercent > 0 ? 'profit-negative' : '';
    const dealText = hasMedian
      ? `${lot.dealPercent > 0 ? '+' : ''}${lot.dealPercent}%`
      : '—';
    return `
      <tr>
        <td class="icon-cell">
          <img class="item-icon" src="../data/icons/${lot.category}/${lot.itemId}.png"
            alt="" loading="lazy" onerror="this.style.display='none'" />
        </td>
        <td class="${itemClass}">${lot.item}</td>
        <td class="ptn-cell">${ptnLabel}</td>
        <td class="amount-cell">${lot.amount}</td>
        <td>
          ${fmt(lot.buy)}
          ${showUnit ? `<span class="per-unit">${fmt(lot.buyPerUnit)}/шт</span>` : ''}
        </td>
        <td>
          ${hasMedian
            ? fmt(lot.itemMedian) + '<span class="per-unit">/шт</span>'
            : '<span class="no-median">нет медианы</span>'}
        </td>
        <td class="${dealClass}">${dealText}</td>
        <td>${timeAgo(lot.createdAt)}</td>
      </tr>
    `;
  }

  const hasMedian = lot.hasMedian !== false;
  const profitClass = !hasMedian ? 'deal-none'
                    : lot.profit >= 0 ? 'profit-positive'
                    : 'profit-negative';
  const profitText = hasMedian
    ? `${lot.profit >= 0 ? '+' : ''}${fmt(lot.profit)}`
    : '—';
  return `
    <tr>
      <td class="icon-cell">
        <img class="item-icon" src="../data/icons/${selectedItem.category}/${lot.itemId}.png"
          alt="" loading="lazy" onerror="this.style.display='none'" />
      </td>
      <td class="${itemClass}">${lot.item}</td>
      <td class="ptn-cell">${ptnLabel}</td>
      <td class="amount-cell">${lot.amount}</td>
      <td>
        ${fmt(lot.buy)}
        ${showUnit ? `<span class="per-unit">${fmt(lot.buyPerUnit)}/шт</span>` : ''}
      </td>
      <td>
        ${hasMedian ? fmt(lot.sell) + '<span class="per-unit">/шт</span>'
                    : '<span class="no-median">нет медианы</span>'}
      </td>
      <td class="${profitClass}">${profitText}</td>
      <td>${timeAgo(lot.createdAt)}</td>
    </tr>
  `;
}

function renderTable() {
  if (!lastData) return;
  const qltFilter = filterQlt.value === '' ? null : Number(filterQlt.value);
  const ptnFilter = filterPtn.value === '' ? null : Number(filterPtn.value);

  let lots = lastData.lots;
  if (qltFilter !== null) lots = lots.filter(l => l.qlt === qltFilter);
  if (ptnFilter !== null) lots = lots.filter(l => ptnRange(l.ptn) === ptnFilter);

  if (!lots.length) {
    tbody.innerHTML = `<tr><td colspan="8" class="loading">Нет лотов по фильтру</td></tr>`;
    return;
  }
  tbody.innerHTML = lots.map(l => rowFor(l, currentMode)).join('');
}

// ---- События ----
itemSearch.addEventListener('input', () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(refreshSuggestions, 150);
});

categoryFilter.addEventListener('change', () => {
  const cat = categoryFilter.value;
  itemSearch.value = '';
  selectedItem = null;
  hideSuggestions();
  if (cat) {
    loadCategoryLots(cat);
  } else {
    currentMode = 'none';
    lastData = null;
    tbody.innerHTML = `<tr><td colspan="8" class="loading">Выбери категорию или предмет</td></tr>`;
    lotsTitle.textContent = 'Живая лента лотов';
    setStatus('');
  }
});

suggestions.addEventListener('click', (e) => {
  const li = e.target.closest('li');
  if (!li || !li.dataset.id) return;
  itemSearch.value = li.dataset.name;
  hideSuggestions();
  loadItemLots(li.dataset.id, li.dataset.name, li.dataset.category || '');
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') hideSuggestions();
});

filterQlt.addEventListener('change', renderTable);
filterPtn.addEventListener('change', renderTable);

minMedian.addEventListener('input', () => {
  clearTimeout(medianTimer);
  medianTimer = setTimeout(() => {
    if (categoryFilter.value) loadCategoryLots(categoryFilter.value);
  }, 700);
});

// ---- Все лоты категории ----
async function loadCategoryLots(category) {
  currentMode = 'category';
  isLoading = true;
  lotsTitle.textContent = `Обзор категории — ${categoryName(category)}`;
  tbody.innerHTML = `<tr><td colspan="8" class="loading">Загрузка лотов категории...</td></tr>`;
  setStatus('');

  const threshold = Number(minMedian.value) || 0;

  try {
    const t0 = Date.now();
    const data = await window.api.fetchCategoryLots({ category, minMedian: threshold });
    isLoading = false;

    if (!data.ok) {
      tbody.innerHTML = `<tr><td colspan="8" class="loading" style="color:#ff5f57">Ошибка: ${data.error}</td></tr>`;
      return;
    }

    if (!data.lots.length) {
      tbody.innerHTML = `<tr><td colspan="8" class="loading">
        Нет лотов. Попробуй снизить «Мин. медиана» или нажми 📥 Скачать всю базу.
      </td></tr>`;
      setStatus(`Всего: <strong>${data.itemsTotal}</strong> · После фильтра: <strong>${data.itemsScanned}</strong>`);
      return;
    }

    lastData = data;
    updateQltOptions(data.lots);
    updatePtnOptions(data.lots);

    setStatus(`Всего предметов: <strong>${data.itemsTotal}</strong> · 
      После фильтра: <strong>${data.itemsScanned}</strong>${data.skippedByMedian ? ` (пропущено ${data.skippedByMedian})` : ''} · 
      Лотов: <strong>${data.count}</strong> · 
      Загружено за <strong>${Date.now() - t0} мс</strong>`);
    renderTable();
  } catch (err) {
    isLoading = false;
    tbody.innerHTML = `<tr><td colspan="8" class="loading" style="color:#ff5f57">Ошибка: ${err.message}</td></tr>`;
  }
}

// ---- Лоты одного предмета ----
async function loadItemLots(itemId, itemName, itemCategory) {
  selectedItem = { id: itemId, name: itemName, category: itemCategory };
  currentMode = 'single';
  isLoading = true;
  lotsTitle.textContent = `${itemName} — лоты`;
  tbody.innerHTML = `<tr><td colspan="8" class="loading">Загрузка лотов...</td></tr>`;
  setStatus('');

  try {
    const data = await window.api.fetchLots({ itemId, itemName });
    isLoading = false;

    if (!data.ok) {
      tbody.innerHTML = `<tr><td colspan="8" class="loading" style="color:#ff5f57">Ошибка: ${data.error}</td></tr>`;
      return;
    }

    lastData = data;
    updateQltOptions(data.lots);
    updatePtnOptions(data.lots);

    setStatus(`Предмет: <strong>${itemName}</strong> · 
      ID: <strong>${itemId}</strong> · 
      Лотов: <strong>${data.count}</strong> · 
      Медианы: <strong>${data.hasMedians ? 'есть' : 'нет'}</strong>`);
    renderTable();
  } catch (err) {
    isLoading = false;
    tbody.innerHTML = `<tr><td colspan="8" class="loading" style="color:#ff5f57">Ошибка: ${err.message}</td></tr>`;
  }
}

// ---- Кнопки ----
downloadBtn.addEventListener('click', async () => {
  const s = await window.api.cacheStats();
  const msg = `Скачать медианы для ВСЕХ предметов в базе?\n\n` +
    `Всего: 2354 предмета.\n` +
    `Уже в кэше: ${s.count}.\n\n` +
    `Пустые предметы пропускаются на 7 дней.\n` +
    `Занимает 15-25 минут. Можно остановить кнопкой.`;
  if (!confirm(msg)) return;

  currentMode = 'download';
  isLoading = true;
  window.__dlStart = Date.now();
  downloadBtn.classList.add('hidden');
  stopBtn.classList.remove('hidden');
  lotsTitle.textContent = 'Скачивание всей базы';
  tbody.innerHTML = `<tr><td colspan="8" class="loading">Начинаю скачивание...</td></tr>`;
  setStatus('Подготовка...');

  try {
    const res = await window.api.downloadAll();
    isLoading = false;
    window.__dlStart = null;
    downloadBtn.classList.remove('hidden');
    stopBtn.classList.add('hidden');

    if (!res.ok) {
      tbody.innerHTML = `<tr><td colspan="8" class="loading" style="color:#ff5f57">Ошибка: ${res.error}</td></tr>`;
      return;
    }

    const extra = res.rateLimited ? `\n\nRate-limit ошибок: ${res.rateLimited}. Запусти ещё раз — докачает пропущенные.` : '';
    if (res.cancelled) {
      alert(`Остановлено пользователем.\nОбработано: ${res.processed}\nМедиан: ${res.updated}\nПустых: ${res.skipped}\nВремя: ${res.elapsed} сек.` + extra);
    } else {
      alert(`Готово!\nОбработано: ${res.processed}.\nМедиан: ${res.updated}.\nПустых: ${res.skipped}.\nВремя: ${res.elapsed} сек.` + extra);
    }

    await showHealth();
    if (categoryFilter.value) await loadCategoryLots(categoryFilter.value);
    else tbody.innerHTML = `<tr><td colspan="8" class="loading">Выбери категорию</td></tr>`;
  } catch (err) {
    isLoading = false;
    window.__dlStart = null;
    downloadBtn.classList.remove('hidden');
    stopBtn.classList.add('hidden');
    tbody.innerHTML = `<tr><td colspan="8" class="loading" style="color:#ff5f57">Ошибка: ${err.message}</td></tr>`;
  }
});

stopBtn.addEventListener('click', async () => {
  if (!confirm('Остановить скачивание? Уже скачанное сохранится.')) return;
  await window.api.cancelDownload();
  setStatus('Останавливаю...');
  stopBtn.disabled = true;
  setTimeout(() => { stopBtn.disabled = false; }, 3000);
});

clearBtn.addEventListener('click', async () => {
  if (!confirm('Очистить кэш медиан?')) return;
  await window.api.cacheClear();
  lastData = null;
  currentMode = 'none';
  tbody.innerHTML = `<tr><td colspan="8" class="loading">Кэш очищен</td></tr>`;
  await showHealth();
});

// ---- Старт ----
console.log('[renderer] скрипт запущен');
tbody.innerHTML = `<tr><td colspan="8" class="loading">Выбери категорию или предмет</td></tr>`;

loadCategories().catch(err => console.error('loadCategories:', err));
showHealth().catch(err => console.error('showHealth:', err));