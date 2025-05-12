// Service Worker for Lifeline Hospital PWA

const CACHE_NAME = 'lifeline-hospital-v1';
const URLS_TO_CACHE = [
  '/',
  '/about',
  '/contact',
  '/static/css/style.css',
  '/static/css/bootstrap.min.css',
  '/static/js/main.js',
  '/static/js/bootstrap.bundle.min.js',
  '/static/img/logo.svg',
  '/static/img/favicon.svg',
  '/static/manifest.json'
];

// Install event - cache assets
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(URLS_TO_CACHE);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', function(event) {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch event - serve from cache if available, otherwise fetch from network
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Clone the request because it's a one-time use stream
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Clone the response because it's a one-time use stream
            const responseToCache = response.clone();
            
            caches.open(CACHE_NAME)
              .then(function(cache) {
                // Don't cache API requests or dynamic content
                if (!event.request.url.includes('/api/') && 
                    !event.request.url.includes('/patient/') &&
                    !event.request.url.includes('/appointment/')) {
                  cache.put(event.request, responseToCache);
                }
              });
            
            return response;
          }
        );
      })
    );
});

// Handle push notifications
self.addEventListener('push', function(event) {
  let notificationData = {};
  
  try {
    notificationData = event.data.json();
  } catch (e) {
    notificationData = {
      title: 'Lifeline Hospital',
      content: event.data.text()
    };
  }
  
  const options = {
    body: notificationData.content,
    icon: '/static/img/logo.svg',
    badge: '/static/img/favicon.svg',
    vibrate: [100, 50, 100],
    data: {
      url: notificationData.url || '/'
    }
  };
  
  event.waitUntil(
    self.registration.showNotification(notificationData.title, options)
  );
});

// Handle notification click
self.addEventListener('notificationclick', function(event) {
  event.notification.close();
  
  const urlToOpen = new URL(event.notification.data.url, self.location.origin);
  
  event.waitUntil(
    clients.matchAll({
      type: 'window',
      includeUncontrolled: true
    })
    .then(function(clientList) {
      // If there's already a window open, focus it
      for (let i = 0; i < clientList.length; i++) {
        const client = clientList[i];
        if (client.url === urlToOpen.href && 'focus' in client) {
          return client.focus();
        }
      }
      
      // Otherwise, open a new window
      if (clients.openWindow) {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});
