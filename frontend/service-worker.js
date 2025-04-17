self.addEventListener('install', function(e) {
  console.log('Shipmate service worker installed');
});
self.addEventListener('fetch', function(e) {
  e.respondWith(fetch(e.request));
});