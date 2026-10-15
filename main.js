require('dotenv').config();
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');
const cache = require('./services/cache');
const {
  downloadMediansForCategory,
  fetchItemLotsWithProfit,
  fetchCategoryLiveLots,
  REGION,
} = require('./services/stalcraft');

const INDEX_FILE = path.join(__dirname, 'data', 'index.json');
let mainWindow;
let itemIndex = [];
let downloadCancelled = false;

function loadIndex() {
  try {
    const raw = fs.readFileSync(INDEX_FILE, 'utf8');
    itemIndex = JSON.parse(raw);
    console.log(`[index] загружено предметов: ${itemIndex.length}`);
  } catch (err) {
    console.error('[index] не удалось загрузить:', err.message);
    itemIndex = [];
  }
  cache.load();
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 860,
    minWidth: 1000,
    minHeight: 600,
    backgroundColor: '#0e1116',
    title: 'Aigex Clone — Лоты STALZONE',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });
  mainWindow.loadFile(path.join(__dirname, 'src', 'index.html'));
  mainWindow.webContents.openDevTools({ mode: 'detach' });
}

function topCategory(cat) {
  return cat ? String(cat).split('/')[0] : '';
}

ipcMain.handle('categories:list', () => {
  if (!itemIndex.length) return [];
  const counts = {};
  for (const it of itemIndex) {
    const top = topCategory(it.category);
    if (!top) continue;
    counts[top] = (counts[top] || 0) + 1;
  }
  return Object.keys(counts)
    .map(key => ({ key, count: counts[key] }))
    .sort((a, b) => b.count - a.count);
});

ipcMain.handle('items:search', (_evt, payload = {}) => {
  const query = String(payload.query || '').toLowerCase().trim();
  const category = payload.category || '';
  let pool = itemIndex;
  if (category) pool = pool.filter(it => topCategory(it.category) === category);

  let filtered;
  if (query) filtered = pool.filter(it => it.name.toLowerCase().includes(query));
  else if (category) filtered = pool.slice(0, 200);
  else return [];

  return filtered.slice(0, 200).map(it => ({
    id: it.id,
    name: it.name,
    category: it.category || '',
    color: it.color || '',
    variantsCount: it.variantsCount || 0,
  }));
});

ipcMain.handle('cache:stats', () => cache.stats());
ipcMain.handle('cache:clear', () => { cache.clear(); return cache.stats(); });
ipcMain.handle('cache:hasItem', (_evt, itemId) => !!cache.getItem(itemId));

ipcMain.handle('cache:downloadAll', async (evt, payload = {}) => {
  if (!itemIndex.length) return { ok: false, error: 'База предметов не загружена' };
  const force = !!payload.force;
  downloadCancelled = false;

  try {
    const t0 = Date.now();
    const onProgress = (loaded, total, skipped) => {
      try { evt.sender.send('cache:progress', { loaded, total, skipped }); } catch {}
    };
    const res = await downloadMediansForCategory(itemIndex, {
      onProgress, concurrency: 8, force,
      shouldCancel: () => downloadCancelled,
    });
    const elapsed = Math.round((Date.now() - t0) / 1000);
    console.log(`[cache:downloadAll] ${JSON.stringify(res)} за ${elapsed} сек`);
    return { ok: true, ...res, total: itemIndex.length, elapsed };
  } catch (err) {
    console.error('[cache:downloadAll]', err);
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('cache:cancelDownload', () => {
  downloadCancelled = true;
  console.log('[cache:cancelDownload] запрошена отмена');
  return { ok: true };
});

// ---------- Все лоты категории ----------
ipcMain.handle('category:live', async (evt, payload = {}) => {
  const { category, minMedian = 0 } = payload;
  if (!category) return { ok: false, error: 'Категория не выбрана' };

  const itemsAll = itemIndex.filter(it => topCategory(it.category) === category);
  if (!itemsAll.length) return { ok: false, error: 'Предметов не найдено' };

  const threshold = Number(minMedian) || 0;
  let itemsFiltered = itemsAll;
  let skippedByMedian = 0;
  let itemsWithoutMedians = 0;

  if (threshold > 0) {
    itemsFiltered = [];
    for (const it of itemsAll) {
      const cached = cache.getItem(it.id);
      if (!cached || !cached.medians) { itemsWithoutMedians++; continue; }
      const medians = Object.values(cached.medians).filter(v => v > 0);
      if (!medians.length) { itemsWithoutMedians++; continue; }
      const minMed = Math.min(...medians);
      if (minMed >= threshold) itemsFiltered.push(it);
      else skippedByMedian++;
    }
  }

  console.log(`[category:live] ${category}: всего ${itemsAll.length}, после фильтра ${itemsFiltered.length}, пропущено ${skippedByMedian}, без медиан ${itemsWithoutMedians} (порог ${threshold})`);

  try {
    const onProgress = (loaded, total) => {
      try { evt.sender.send('category:progress', { loaded, total }); } catch {}
    };
    const t0 = Date.now();
    const lots = await fetchCategoryLiveLots(itemsFiltered, { onProgress, concurrency: 10 });
    console.log(`[category:live] ${category}: ${lots.length} лотов за ${Date.now() - t0} мс`);

    return {
      ok: true,
      count: lots.length,
      lots,
      itemsTotal: itemsAll.length,
      itemsScanned: itemsFiltered.length,
      skippedByMedian,
      itemsWithoutMedians,
      threshold,
    };
  } catch (err) {
    console.error('[category:live]', err);
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('lots:live', async (_evt, payload = {}) => {
  const { itemId, itemName } = payload;
  if (!itemId) return { ok: false, error: 'Не выбран предмет' };
  try {
    const t0 = Date.now();
    const lots = await fetchItemLotsWithProfit(itemId, itemName || itemId);
    console.log(`[lots:live] ${itemName}: ${lots.length} лотов за ${Date.now() - t0} мс`);

    const qltSet = new Set();
    const ptnSet = new Set();
    for (const l of lots) {
      if (l.qlt != null) qltSet.add(l.qlt);
      if (l.ptn != null) ptnSet.add(l.ptn);
    }
    const cached = cache.getItem(itemId);
    return {
      ok: true, region: REGION, itemId, count: lots.length, lots,
      availableQlt: [...qltSet].sort((a, b) => a - b),
      availablePtn: [...ptnSet].sort((a, b) => a - b),
      hasMedians: !!cached,
    };
  } catch (err) {
    console.error('[lots:live]', err);
    return { ok: false, error: err.message };
  }
});

ipcMain.handle('health', () => ({
  region: REGION,
  apiUrl: process.env.API_URL,
  hasCredentials: Boolean(process.env.CLIENT_ID && process.env.CLIENT_SECRET),
  itemsLoaded: itemIndex.length,
}));

app.whenReady().then(() => {
  loadIndex();
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});