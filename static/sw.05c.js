// chrome --disable-web-security --allow-file-access-from-files --unsafely-treat-insecure-origin-as-secure=http://localhost --user-data-dir=%TEMP%
var CACHE_NAME = 'cache_nkctf'; // const CACHE_URL = [];

self.addEventListener('install', function (event) {
  self.skipWaiting();
});
self.addEventListener('activate', function (event) {
  self.clients.claim();
});
self.addEventListener('fetch', function (event) {
  event.respondWith(caches.match(event.request).then(function (response) {
    if (response) {
      return response;
    }

    var fetchRequest = event.request.clone();
    return fetch(fetchRequest).then(function (response) {
      if (!response || response.status !== 200 || response.type !== 'basic' || !/\.(png|jpe?g|gif|svg|mp4)(\?.*)?$/.test(response.url)) {
        return response;
      }

      var responseToCache = response.clone();
      caches.open(CACHE_NAME).then(function (cache) {
        cache.put(event.request, responseToCache);
      });
      return response;
    }).catch(function (err) {
      console.warn("[Warn] \u2193 may be a chrome bug when devtools are open.");
      console.error(err);
    });
  }));
});