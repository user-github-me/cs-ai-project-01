/* Cache only the local game. Lessons linked on GitHub remain online resources. */
'use strict';
const CACHE = 'roverlab-v1';
const CORE = ['./', './index.html', './style.css', './engine.js', './script.js', './offline.js', './manifest.webmanifest', './assets/icon.svg', './assets/InterVariable.woff2'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('roverlab-') && key !== CACHE).map(key => caches.delete(key)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;
  // Network first means a redeploy is visible on refresh. Cache is the offline fallback.
  event.respondWith(fetch(event.request).then(response => {
    if (response.ok) {
      const copy = response.clone();
      event.waitUntil(caches.open(CACHE).then(cache => cache.put(event.request, copy)));
    }
    return response;
  }).catch(async () => {
    const saved = await caches.match(event.request);
    if (saved) return saved;
    if (event.request.mode === 'navigate') return caches.match('./index.html');
    return Response.error();
  }));
});
