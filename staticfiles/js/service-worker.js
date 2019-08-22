var CACHE_NAME = 'digitaldairy-cache-v1';
const FILES_TO_CACHE = [
    // Update cache names any time any of the cached files change.
    '/',
];
// update caches before showing information 
self.addEventListener('push', (evt) => {
    console.log(evt.data);
    const payload = evt.data ? evt.data.text() : 'no-payload';
    evt.waitUntil(caches.open(CACHE_NAME).then((cache) => {
        return fetch('/inbox.json').then((response) => {
            cache.put('/inbox.json', response.clone);
            return response.json();
        });
    }).then((emails) => {
        self.registration.showNotification('New Notification', {
            body: payload,
            "vibrate": [200, 100, 200, 100, 200, 100, 400],
            tag: 'new-payload'
        });
    })
    );
})
self.addEventListener('notificationclick', (evt) => {
    if (evt.notification.tag == 'new-payload') {
        // Assume that all of the resources needed to render
        // /inbox/ have previously been cached, e.g. as part
        // of the install handler.
        new WindowClient('/inbox/')
    }
})
self.addEventListener('install', (evt) => {
    console.log('[Service worker] install');
    // Precache static resources here.
    evt.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[ServiceWorker] Pre-caching offline page');
            return cache.addAll(FILES_TO_CACHE);
        })
    );
})
// Remove previous cached data from disk.
self.addEventListener('activate', (evt) => {
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
});
// intercept fetch events 
self.addEventListener('fetch', (evt) => {
    // CODELAB: Add fetch event handler here.
    console.log('Request Mode ' + evt.request.mode)
    if (evt.request.mode !== 'navigate') {
        // not a navigation page, bail
        return;
    }
    evt.respondWith(
        caches.match(evt.request).then((r) => {
            console.log('[Service Worker] fetching resource ' + evt.request.url);
            return r || fetch(e.request).then((response) => {
                return caches.open(CACHE_NAME).then((cache) => {
                    console.log('[Service Worker] Caching new resource ' + e.request.url);
                    cache.put(e.request, response.clone);
                    return response;
                });
            });
        })
    );
});
