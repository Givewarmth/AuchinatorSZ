const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  searchItems:     (p) => ipcRenderer.invoke('items:search', p),
  listCategories:  () => ipcRenderer.invoke('categories:list'),
  fetchLots:       (p) => ipcRenderer.invoke('lots:live', p),
  fetchCategoryLots: (p) => ipcRenderer.invoke('category:live', p),
  downloadAll:     (p) => ipcRenderer.invoke('cache:downloadAll', p || {}),
  cancelDownload:  () => ipcRenderer.invoke('cache:cancelDownload'),
  cacheStats:      () => ipcRenderer.invoke('cache:stats'),
  cacheClear:      () => ipcRenderer.invoke('cache:clear'),
  cacheHasItem:    (id) => ipcRenderer.invoke('cache:hasItem', id),
  health:          () => ipcRenderer.invoke('health'),
  onProgress:      (cb) => ipcRenderer.on('lots:progress', (_e, d) => cb(d)),
  onCategoryProgress: (cb) => ipcRenderer.on('category:progress', (_e, d) => cb(d)),
  onCacheProgress: (cb) => ipcRenderer.on('cache:progress', (_e, d) => cb(d)),
});