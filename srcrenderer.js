const tbody = document.querySelector('#lots tbody');
const search = document.getElementById('search');
const minProfit = document.getElementById('minProfit');
const refresh = document.getElementById('refresh');
const status = document.getElementById('status');

function fmt(n) {
  return (n ?? 0).toLocaleString('ru-RU') + ' ₽';
}

function timeAgo(iso) {
  if (!iso) return '—';
  const diff = Math.floor((Date.now() - new Date(iso).getTime()) / 1000);
  if (diff < 60) return `${diff} сек назад`;
  if (diff < 3600) return `${Math.floor(diff / 60)} мин назад`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} ч назад`;
  return `${Math.floor(diff / 86400)} дн назад`;
}

async function showHealth() {
  try {
    const h = await window.api.health();
    status.innerHTML = `
      <div>Регион: <strong>${h.region}</strong></div>
      <div>ID предмета: <strong>${h.itemId}</strong></div>
      <div>API: <strong>${h.apiUrl}</strong></div>
      <div>Токен: <strong>${h.hasToken ? 'есть' : 'нет'}</strong></div>
    `;
  } catch (err) {
    status.textContent = 'Не удалось получить статус: ' + err.message;
  }
}

async function loadLots() {
  tbody.innerHTML = `<tr><td colspan="6" class="loading">Загрузка лотов...</td></tr>`;
  status.innerHTML = 'Запрос к API...';

  const filters = {
    search: search.value.trim(),
    minProfit: Number(minProfit.value) || 0,
  };

  try {
    const data = await window.api.fetchLots(filters);

    if (!data.ok) {
      status.innerHTML = `<span style="color:#ff5f57">Ошибка: ${data.error}</span>`;
      tbody.innerHTML = `<tr><td colspan="6" class="loading" style="color:#ff5f57">Не удалось загрузить лоты</td></tr>`;
      return;
    }

    status.innerHTML = `
      <div>Регион: <strong>${data.region}</strong></div>
      <div>Лотов найдено: <strong>${data.count}</strong></div>
      <div>Обновлено: ${new Date().toLocaleTimeString('ru-RU')}</div>
    `;

    if (!data.lots.length) {
      tbody.innerHTML = `<tr><td colspan="6" class="loading">Нет лотов по заданным фильтрам</td></tr>`;
      return;
    }

    tbody.innerHTML = data.lots.map((l) => `
      <tr>
        <td>${l.item}</td>
        <td>${fmt(l.buy)}</td>
        <td>${fmt(l.sell)}</td>
        <td class="${l.profit >= 0 ? 'profit-positive' : 'profit-negative'}">
          ${l.profit >= 0 ? '+' : ''}${fmt(l.profit)}
        </td>
        <td>${l.seller || '—'}</td>
        <td>${timeAgo(l.createdAt)}</td>
      </tr>
    `).join('');
  } catch (err) {
    status.innerHTML = `<span style="color:#ff5f57">Ошибка: ${err.message}</span>`;
    tbody.innerHTML = `<tr><td colspan="6" class="loading" style="color:#ff5f57">Не удалось загрузить лоты</td></tr>`;
  }
}

refresh.addEventListener('click', loadLots);
search.addEventListener('input', loadLots);
minProfit.addEventListener('input', loadLots);

showHealth();
loadLots();