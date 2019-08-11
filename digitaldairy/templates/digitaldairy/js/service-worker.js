const FILES_TO_CACHE = [
    // Update cache names any time any of the cached files change.
    '../html/milk-production.html',
];
// Precache static resources here.
evt.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
        console.log('[ServiceWorker] Pre-caching offline page');
        return cache.addAll(FILES_TO_CACHE);
    })
);
// CODELAB: Remove previous cached data from disk.
evt.waitUntil(
    caches.keys().then((keyList) => {
        return Promise.all(keyList.map((key) => {
            if (key !== CACHE_NAME) {
                console.log('[ServiceWorker] Removing old cache', key);
                return caches.delete(key);
            }
        }));
    })
);
// CODELAB: Remove previous cached data from disk.
evt.waitUntil(
    caches.keys().then((keyList) => {
        return Promise.all(keyList.map((key) => {
            if (key !== CACHE_NAME) {
                console.log('[ServiceWorker] Removing old cache', key);
                return caches.delete(key);
            }
        }));
    })
);
// CODELAB: Add fetch event handler here.
if (evt.request.mode !== 'navigate') {
    // not a navigation page, bail
    return;
}
evt.respondWith(
    fetch(evt.request)
        .catch(() => {
            return caches.open(CACHE_NAME).then((cache) => {
                return cache.match('offline.html')
            })
        })
);
