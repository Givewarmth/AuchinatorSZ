require('dotenv').config();
const cache = require('./cache');

const BASE_URL  = process.env.API_URL || 'https://eapi.stalcraft.net';
const REGION    = process.env.REGION || 'RU';
const TOKEN_URL = 'https://exbo.net/oauth/token';

const CLIENT_ID     = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;

const LOT_PAGE  = 100;
const HIST_PAGE = 100;
const HIST_MAX  = 1000;

// ─── Окна для расчёта ───
const TRADE_RETENTION_DAYS = 30;   // храним сырые сделки не старше 30 дней
const MEDIAN_WINDOW_DAYS   = 7;    // основное окно для медианы
const FALLBACK_WINDOW_DAYS = 30;   // если мало данных — расширяем
const MIN_SAMPLES          = 50;   // минимум сделок для медианы

const EMPTY_SKIP_DAYS = 7;
const BATCH_DELAY_MS  = 300;

let cachedToken    = null;
let tokenExpiresAt = 0;
let tokenPromise   = null;

async function getAppToken() {
  if (cachedToken && Date.now() < tokenExpiresAt - 60_000) return cachedToken;
  if (tokenPromise) return tokenPromise;
  tokenPromise = (async () => {
    const body = new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    });
    const res = await fetch(TOKEN_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: body.toString(),
    });
    if (!res.ok) throw new Error(`OAuth ${res.status}`);
    const j = await res.json();
    cachedToken = j.access_token;
    tokenExpiresAt = Date.now() + (j.expires_in ?? 3600) * 1000;
    return cachedToken;
  })();
  try { return await tokenPromise; }
  finally { tokenPromise = null; }
}

async function apiGet(path, params = {}, attempt = 0) {
  const token = await getAppToken();
  const url = new URL(`${BASE_URL}${path}`);
  Object.entries(params).forEach(([k, v]) => {
    if (v != null) url.searchParams.set(k, v);
  });
  let res = await fetch(url, {
    headers: { Authorization: `Bearer ${token}`, Accept: 'application/json' },
  });
  if (res.status === 401 && attempt < 3) {
    cachedToken = null; tokenExpiresAt = 0;
    const t = await getAppToken();
    res = await fetch(url, {
      headers: { Authorization: `Bearer ${t}`, Accept: 'application/json' },
    });
  }
  if (res.status === 429 && attempt < 4) {
    const wait = 2000 * Math.pow(2, attempt);
    console.log(`[EAPI] 429 rate limit, ждём ${wait} мс (попытка ${attempt + 1}/4)`);
    await new Promise(r => setTimeout(r, wait));
    return apiGet(path, params, attempt + 1);
  }
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`EAPI ${res.status}: ${text.slice(0, 150)}`);
  }
  return res.json();
}

function median(arr) {
  if (!arr.length) return 0;
  const s = [...arr].sort((a, b) => a - b);
  const m = Math.floor(s.length / 2);
  return s.length % 2 ? s[m] : Math.round((s[m - 1] + s[m]) / 2);
}
function percentile(s, p) {
  if (!s.length) return 0;
  const i = (s.length - 1) * p;
  const lo = Math.floor(i), hi = Math.ceil(i);
  return lo === hi ? s[lo] : s[lo] + (s[hi] - s[lo]) * (i - lo);
}
function iqr(arr) {
  if (arr.length < 4) return arr;
  const s = [...arr].sort((a, b) => a - b);
  const q1 = percentile(s, 0.25);
  const q3 = percentile(s, 0.75);
  const r = q3 - q1;
  return arr.filter(v => v >= q1 - 1.5 * r && v <= q3 + 1.5 * r);
}
function pickNum(o, keys) {
  if (!o) return null;
  for (const k of keys) {
    const v = o[k];
    if (v != null && v !== '') {
      const n = Number(v);
      if (!Number.isNaN(n)) return n;
    }
  }
  return null;
}
const extractQlt = (l) => pickNum(l?.additional, ['qlt']) ?? pickNum(l, ['qlt']);
const extractPtn = (l) => pickNum(l?.additional, ['ptn']) ?? pickNum(l, ['ptn']);

function ptnRange(ptn) {
  if (ptn == null) return null;
  const n = Number(ptn);
  if (Number.isNaN(n)) return null;
  if (n >= 15) return 15;
  if (n >= 10) return 10;
  if (n >= 5)  return 5;
  return 0;
}

const groupKey = (q, p) => `${q ?? 'null'}|${p ?? 'null'}`;

// ─── Дедупликация и мерж сделок ───
function tradeKey(t) {
  return `${t.time}|${t.price}|${t.amount}|${t.qlt ?? 'null'}|${t.ptn ?? 'null'}`;
}

function mergeTrades(oldTrades, newTrades) {
  const map = new Map();
  for (const t of oldTrades || []) map.set(tradeKey(t), t);
  for (const t of newTrades || []) map.set(tradeKey(t), t);
  return [...map.values()];
}

function pruneOldTrades(trades, maxAgeDays) {
  const cutoff = Date.now() - maxAgeDays * 86400000;
  return trades.filter(t => {
    const ts = new Date(t.time).getTime();
    return !Number.isNaN(ts) && ts >= cutoff;
  });
}

// ─── Расчёт медиан по окну + реальный daysCovered ───
function computeMediansFromTrades(trades, windowDays) {
  const cutoff = Date.now() - windowDays * 86400000;
  const inWindow = trades.filter(t => {
    const ts = new Date(t.time).getTime();
    return !Number.isNaN(ts) && ts >= cutoff;
  });

  const byGroup = {};
  for (const t of inWindow) {
    if (!t.price || t.price <= 0) continue;
    const amt = t.amount || 1;
    const key = groupKey(t.qlt ?? null, ptnRange(t.ptn));
    if (!byGroup[key]) byGroup[key] = [];
    byGroup[key].push(t.price / amt);
  }

  const medians = {};
  const counts = {};
  let totalSamples = 0;
  for (const [k, prices] of Object.entries(byGroup)) {
    const filtered = iqr(prices);
    medians[k] = filtered.length >= MIN_SAMPLES ? Math.round(median(filtered)) : 0;
    counts[k] = filtered.length;
    totalSamples += filtered.length;
  }

  // Реальный диапазон дат в выборке
  let firstTime = null, lastTime = null;
  for (const t of inWindow) {
    const ts = new Date(t.time).getTime();
    if (Number.isNaN(ts)) continue;
    if (!firstTime || ts < firstTime) firstTime = ts;
    if (!lastTime  || ts > lastTime)  lastTime  = ts;
  }

  let daysCovered = 0;
  if (firstTime && lastTime && lastTime > firstTime) {
    daysCovered = (lastTime - firstTime) / 86400000;
  }

  // Если данных меньше 1 дня — берём окно
  const effectiveDays = daysCovered >= 1 ? daysCovered : windowDays;

  const salesPerDay = effectiveDays > 0
    ? Math.round((inWindow.length / effectiveDays) * 10) / 10
    : 0;

  return {
    medians, counts,
    totalInWindow: inWindow.length,
    totalSamples,
    daysCovered: Math.round(effectiveDays * 10) / 10,
    salesPerDay,
  };
}

// ─── Загрузка с аукциона ───
async function fetchFirstPageLots(itemId, { limit = LOT_PAGE } = {}) {
  const page = await apiGet(`/${REGION}/auction/${itemId}/lots`, {
    limit, offset: 0,
    sort: 'buyout_price', order: 'asc',
    additional: 'true',
  });
  return Array.isArray(page) ? page : (page?.lots || []);
}

async function fetchAllHistory(itemId) {
  const all = [];
  let offset = 0;
  while (all.length < HIST_MAX) {
    const page = await apiGet(`/${REGION}/auction/${itemId}/history`, {
      limit: HIST_PAGE, offset, additional: 'true',
    });
    const prices = Array.isArray(page) ? page : (page?.prices || []);
    if (!prices.length) break;
    all.push(...prices);
    if (prices.length < HIST_PAGE) break;
    offset += HIST_PAGE;
  }
  return all;
}

// ─── Скачивание одного предмета в кэш ───
async function downloadItemToCache(item) {
  const { id, name, category } = item;

  // 1. Свежие сделки
  const fresh = await fetchAllHistory(id);

  // 2. Нормализация
  const normalized = fresh
    .filter(h => h.price > 0 && h.time)
    .map(h => ({
      time: h.time,
      price: h.price,
      amount: h.amount || 1,
      qlt: extractQlt(h),
      ptn: extractPtn(h),
    }));

  // 3. Мерж с существующими
  const existing = cache.getItem(id);
  const existingTrades = existing?.recentTrades || [];
  const merged = mergeTrades(existingTrades, normalized);

  // 4. Чистка старше 30 дней
  const pruned = pruneOldTrades(merged, TRADE_RETENTION_DAYS);

  // 5. Медианы по 7 дням
  let result = computeMediansFromTrades(pruned, MEDIAN_WINDOW_DAYS);
  let windowUsed = MEDIAN_WINDOW_DAYS;

  // 6. Fallback на 30 дней
  if (result.totalSamples < MIN_SAMPLES) {
    result = computeMediansFromTrades(pruned, FALLBACK_WINDOW_DAYS);
    windowUsed = FALLBACK_WINDOW_DAYS;
  }

  const isEmpty = pruned.length === 0;

  // 7. Сохраняем
  cache.setItem(id, {
    id, name, category,
    recentTrades: pruned,
    medians: result.medians,
    counts: result.counts,
    isEmpty,
    windowUsed,
    salesPerDay: result.salesPerDay,
    daysCovered: result.daysCovered,
    totalCount: result.totalInWindow,
    totalAllTime: pruned.length,
    firstSeen: existing?.firstSeen || new Date().toISOString(),
    lastUpdated: new Date().toISOString(),
  });

  return { isEmpty, salesPerDay: result.salesPerDay, totalCount: pruned.length };
}

// ─── Массовое скачивание ───
async function downloadMediansForCategory(items, {
  onProgress, concurrency = 4, force = false, shouldCancel,
} = {}) {
  const total = items.length;
  let processed = 0, updated = 0, skipped = 0, rateLimited = 0, otherErrors = 0, cancelled = false;

  for (let i = 0; i < items.length; i += concurrency) {
    if (shouldCancel && shouldCancel()) {
      cancelled = true;
      console.log(`[download] отменено на ${processed}/${total}`);
      break;
    }
    const batch = items.slice(i, i + concurrency);

    await Promise.all(batch.map(async (item) => {
      try {
        if (!force) {
          const existing = cache.getItem(item.id);
          if (existing && existing.isEmpty && existing.lastUpdated) {
            const ageDays = (Date.now() - new Date(existing.lastUpdated).getTime()) / 86400000;
            if (ageDays < EMPTY_SKIP_DAYS) {
              skipped++; processed++;
              if (onProgress) onProgress(processed, total, skipped);
              return;
            }
          }
        }
        const { isEmpty } = await downloadItemToCache(item);
        if (!isEmpty) updated++; else skipped++;
      } catch (err) {
        if (err.message.includes('429')) rateLimited++;
        else { otherErrors++; if (otherErrors <= 5) console.error(`[download] ${item.name}:`, err.message); }
      }
      processed++;
      if (onProgress) onProgress(processed, total, skipped);
    }));

    if (i + concurrency < items.length) {
      await new Promise(r => setTimeout(r, BATCH_DELAY_MS));
    }
  }

  cache.save();

  console.log(`[download] processed=${processed}, updated=${updated}, skipped=${skipped}, rateLimited=${rateLimited}, otherErrors=${otherErrors}`);
  return { processed, updated, skipped, cancelled, rateLimited, otherErrors };
}

// ─── Поиск медианы ───
function findMedian(medians, qlt, ptn) {
  if (!medians) return 0;
  const range = ptnRange(ptn);
  const exact = medians[groupKey(qlt, range)];
  if (exact && exact > 0) return exact;
  return 0;
}

// ─── Лоты одного предмета ───
async function fetchItemLotsWithProfit(itemId, itemName) {
  const lots = await fetchFirstPageLots(itemId);
  const cached = cache.getItem(itemId);
  const medians = cached?.medians || {};

  const result = lots
    .map((lot) => {
      const amount = lot.amount ?? 1;
      const buyout = lot.buyoutPrice || lot.startPrice || 0;
      if (buyout <= 0) return null;

      const buyPerUnit = Math.round(buyout / amount);
      const qlt = extractQlt(lot);
      const ptn = extractPtn(lot);
      const ref = findMedian(medians, qlt, ptn);
      const hasMedian = ref > 0;
      const sell = hasMedian ? ref : buyPerUnit;
      const profit = hasMedian ? Math.round((ref - buyPerUnit) * amount) : 0;

      return {
        id: lot.id, itemId, item: itemName,
        amount,
        buy: Math.round(buyout), buyPerUnit,
        sell, profit,
        qlt, ptn, hasMedian,
        createdAt: lot.startTime ?? lot.time_created,
        hasBuyout: (lot.buyoutPrice || 0) > 0,
      };
    })
    .filter(Boolean);

  result.sort((a, b) => b.profit - a.profit);
  return result;
}

// ─── Лоты всей категории ───
async function fetchCategoryLiveLots(items, { onProgress, concurrency = 10 } = {}) {
  const result = [];
  const total = items.length;
  let processed = 0;

  for (let i = 0; i < items.length; i += concurrency) {
    const batch = items.slice(i, i + concurrency);

    const batchResults = await Promise.all(batch.map(async (item) => {
      try {
        const lots = await fetchFirstPageLots(item.id);
        return { item, lots };
      } catch (err) {
        return { item, lots: [] };
      }
    }));

    for (const { item, lots } of batchResults) {
      const cached = cache.getItem(item.id);
      const medians = cached?.medians || {};

      for (const lot of lots) {
        const amount = lot.amount ?? 1;
        const buyout = lot.buyoutPrice || 0;
        if (buyout <= 0) continue;

        const qlt = extractQlt(lot);
        const ptn = extractPtn(lot);
        const ref = findMedian(medians, qlt, ptn);
        const hasMedian = ref > 0;
        const buyPerUnit = Math.round(buyout / amount);
        const dealPercent = hasMedian
          ? Math.round(((buyPerUnit - ref) / ref) * 100)
          : null;

        result.push({
          id: lot.id,
          itemId: item.id,
          item: item.name,
          category: item.category,
          amount,
          buy: Math.round(buyout),
          buyPerUnit,
          qlt, ptn,
          itemMedian: ref,
          dealPercent,
          hasMedian,
          createdAt: lot.startTime ?? lot.time_created,
        });
      }
      processed++;
    }

    if (onProgress) onProgress(processed, total);
  }

  result.sort((a, b) => {
    if (a.hasMedian !== b.hasMedian) return a.hasMedian ? -1 : 1;
    if (a.hasMedian && b.hasMedian) {
      if (a.dealPercent !== b.dealPercent) return a.dealPercent - b.dealPercent;
    }
    return new Date(b.createdAt || 0) - new Date(a.createdAt || 0);
  });

  return result;
}

module.exports = {
  downloadMediansForCategory,
  fetchItemLotsWithProfit,
  fetchCategoryLiveLots,
  REGION,
};