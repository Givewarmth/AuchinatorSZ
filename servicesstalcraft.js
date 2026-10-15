require('dotenv').config();

const BASE_URL = process.env.DEMO_API_URL || 'https://dapi.stalcraft.net';
const TOKEN    = process.env.DEMO_APP_TOKEN;
const REGION   = process.env.REGION || 'RU';

/**
 * Универсальный GET-запрос к EAPI с логированием.
 */
async function apiGet(path, params = {}) {
  const url = new URL(`${BASE_URL}${path}`);
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null) url.searchParams.set(k, v);
  });

  console.log(`[EAPI] GET ${url.toString()}`);

  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${TOKEN}`,
      Accept: 'application/json',
    },
  });

  const text = await res.text();
  console.log(`[EAPI] ${res.status} ${res.statusText} → ${text.slice(0, 300)}`);

  if (!res.ok) {
    throw new Error(`EAPI ${res.status}: ${text.slice(0, 200)}`);
  }

  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`EAPI вернул не-JSON: ${text.slice(0, 200)}`);
  }
}

async function fetchLots(itemId, { limit = 50, offset = 0, sort = 'buyout_price', order = 'asc' } = {}) {
  return apiGet(`/${REGION}/auction/${itemId}/lots`, { limit, offset, sort, order });
}

async function fetchHistory(itemId, { limit = 50, offset = 0 } = {}) {
  return apiGet(`/${REGION}/auction/${itemId}/history`, { limit, offset });
}

async function getLotsWithProfit(itemId) {
  const [lotsResult, historyResult] = await Promise.allSettled([
    fetchLots(itemId),
    fetchHistory(itemId),
  ]);

  const lots = lotsResult.status === 'fulfilled' ? lotsResult.value : [];
  const history = historyResult.status === 'fulfilled' ? historyResult.value : [];

  if (lotsResult.status === 'rejected') {
    console.error('[lots] не удалось получить лоты:', lotsResult.reason.message);
  }
  if (historyResult.status === 'rejected') {
    console.error('[history] не удалось получить историю:', historyResult.reason.message);
  }

  const avgSell = history.length
    ? Math.round(history.reduce((s, h) => s + (h.price ?? 0), 0) / history.length)
    : 0;

  return lots
    .map((lot) => {
      const buy = lot.buyout_price ?? lot.start_price ?? 0;
      return {
        id: lot.id,
        item: 'Астрикцин',
        buy,
        sell: avgSell,
        profit: avgSell - buy,
        seller: lot.seller,
        createdAt: lot.time_created,
        amount: lot.amount ?? 1,
      };
    })
    .filter((l) => l.buy > 0)
    .sort((a, b) => b.profit - a.profit);
}

module.exports = { fetchLots, fetchHistory, getLotsWithProfit, REGION };