// // Give the service worker access to Firebase Messaging.
// // Note that you can only use Firebase Messaging here, other Firebase libraries
// // are not available in the service worker.
importScripts('https://www.gstatic.com/firebasejs/6.3.4/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/6.3.4/firebase-messaging.js');
// // Initialize the Firebase app in the service worker by passing in the
// // messagingSenderId.
firebase.initializeApp({
    'messagingSenderId': '218207212419'
});
// Retrieve an instance of Firebase Messaging so that it can handle background
// messages.
const messaging = firebase.messaging();
messaging.setBackgroundMessageHandler(function (payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    // Customize notification here
    evt.waitUntil(caches.open(CACHE_NAME).then((cache) => {
        return fetch('/digitaldairy/daily_alerts/').then((response) => {
            cache.put('/digitaldairy/daily_alerts/', response.clone());
            return response.text();
        });
    }).then((response) => {
        var notif_from_server = payload.notification;
        console.log('Notification from server ', notif_from_server)
        return self.registration.showNotification(notif_from_server.title, {
            body: notif_from_server.body,
            vibrate: [200, 100, 200, 100, 200, 100, 400],
            icon: '/static/images/icons/digital_dairy128.png',
            badge: '/static/images/icons/digital_dairy128.png',
            tag: 'daily_alert',
        });
    })
    );
});
var CACHE_NAME = 'digitaldairy-cache-v1';
const FILES_TO_CACHE = [
    // Update cache names any time any of the cached files change.
    '/',
];
// update caches before showing information 
self.addEventListener('push', (evt) => {
    const payload = evt.data ? evt.data.json() : 'no-payload';
    console.log("The push payload");
    console.log(payload);
    evt.waitUntil(caches.open(CACHE_NAME).then((cache) => {
        return fetch('/digitaldairy/daily_alerts/').then((response) => {
            cache.put('/digitaldairy/daily_alerts/', response.clone());
            return response.text();
        });
    }).then((response) => {
        var notif_from_server = payload.notification;
        console.log('Notification from server ', notif_from_server)
        self.registration.showNotification(notif_from_server.title, {
            body: notif_from_server.body,
            vibrate: [200, 100, 200, 100, 200, 100, 400],
            icon: '/static/images/icons/digital_dairy128.png',
            badge: '/static/images/icons/digital_dairy128.png',
            tag: 'daily_alert',
        });
        // console.log(response)
    })
    );
})
self.addEventListener('notificationclick', (evt) => {
    if (evt.notification.tag == 'daily_alert') {
        // Assume that all of the resources needed to render
        // /digitaldairy/daily_alerts/ have previously been cached, e.g. as part
        // of the install handler.
        // Create a new window.
        self.clients.openWindow('/digitaldairy/daily_alerts/').then(function (WindowClient) {
            console.log(WindowClient);
        });
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
// // intercept fetch events
// self.addEventListener('fetch', (evt) => {
//     // CODELAB: Add fetch event handler here.
//     console.log('Request Mode ' + evt.request.mode)
//     if (evt.request.mode !== 'navigate') {
//         // not a navigation page, bail
//         return;
//     }
//     evt.respondWith(
//         caches.match(evt.request).then((r) => {
//             console.log('[Service Worker] fetching resource ' + evt.request.url);
//             return r || fetch(evt.request).then((response) => {
//                 return caches.open(CACHE_NAME).then((cache) => {
//                     console.log('[Service Worker] Caching new resource ' + evt.request.url);
//                     cache.put(evt.request, response.clone());
//                     return response;
//                 });
//             }).catch((err) => {
//                 console.log('Network error occurred ', err);
//             });
//         })
//     );
// });
