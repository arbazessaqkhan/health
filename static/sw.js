/**
 * Lifeline Hospital - Service Worker
 * Enables offline functionality and PWA features
 */

const CACHE_NAME = 'lifeline-hospital-v1';
const URLS_TO_CACHE = [
  '/',
  '/about',
  '/facilities',
  '/faq',
  '/contact',
  '/privacy',
  '/services',
  '/doctors',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/js/pwa.js',
  '/static/js/map.js',
  '/static/manifest.json',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Install service worker and cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(URLS_TO_CACHE);
      })
  );
});

// Activate service worker and clean up old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Serve cached content when offline
self.addEventListener('fetch', event => {
  // Skip non-GET requests and requests with authentication/form data
  if (event.request.method !== 'GET' ||
      event.request.url.includes('/auth/') ||
      event.request.url.includes('/patients/portal') ||
      event.request.url.includes('/appointments/book')) {
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Clone the request to avoid consuming it
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then(response => {
          // Check if we received a valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }
          
          // Clone the response to avoid consuming it
          const responseToCache = response.clone();
          
          caches.open(CACHE_NAME)
            .then(cache => {
              cache.put(event.request, responseToCache);
            });
          
          return response;
        }).catch(() => {
          // If the network is unavailable and we don't have a cache match,
          // return the offline page for HTML requests
          if (event.request.headers.get('accept').includes('text/html')) {
            return caches.match('/');
          }
        });
      })
  );
});

// Handle push notifications
self.addEventListener('push', event => {
  let data = {};
  if (event.data) {
    data = event.data.json();
  }
  
  const options = {
    body: data.body || 'New notification from Lifeline Hospital',
    icon: '/static/images/icon-192.png',
    badge: '/static/images/badge.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      url: data.url || '/'
    },
    actions: [
      {
        action: 'open',
        title: 'Open',
        icon: '/static/images/check.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/images/x.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title || 'Lifeline Hospital', options)
  );
});

// Handle notification click
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.action === 'close') {
    return;
  }
  
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(windowClients => {
      const url = event.notification.data.url || '/';
      
      // If a window is already open, focus it
      for (const client of windowClients) {
        if (client.url === url && 'focus' in client) {
          return client.focus();
        }
      }
      
      // Otherwise open a new window
      if (clients.openWindow) {
        return clients.openWindow(url);
      }
    })
  );
});
