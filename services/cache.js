const fs = require('fs');
const path = require('path');

const CACHE_FILE = path.join(__dirname, '..', 'data', 'medians-cache.json');
let cache = null;
let saveCounter = 0;

function load() {
  if (cache) return cache;
  try {
    cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf8'));
    console.log(`[cache] предметов: ${Object.keys(cache).length}`);
  } catch {
    cache = {};
    console.log('[cache] файл отсутствует');
  }
  return cache;
}

function save() {
  if (!cache) return;
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache), 'utf8');
  saveCounter = 0;
}

function setItem(itemId, data) {
  const c = load();
  c[itemId] = data;
  saveCounter++;
  if (saveCounter >= 20) save();
}

function getItem(itemId) {
  return load()[itemId] || null;
}

function clear() {
  cache = {};
  saveCounter = 0;
  save();
}

function stats() {
  const c = load();
  let sizeBytes = 0;
  try { sizeBytes = fs.statSync(CACHE_FILE).size; } catch {}
  return { count: Object.keys(c).length, sizeBytes };
}

module.exports = { load, save, setItem, getItem, clear, stats };