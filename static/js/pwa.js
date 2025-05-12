/**
 * Lifeline Hospital - PWA Support Functions
 * Handles Service Worker registration and PWA functionality
 */

// Register service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('ServiceWorker registration successful with scope: ', registration.scope);
            })
            .catch(err => {
                console.log('ServiceWorker registration failed: ', err);
            });
    });
}

// PWA installation prompt
let deferredPrompt;
const installPromptContainer = document.querySelector('.install-prompt');
const installButton = document.getElementById('install-button');
const closeInstallButton = document.getElementById('close-install');

window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;
    // Show the install button
    if (installPromptContainer) {
        installPromptContainer.classList.add('show');
    }
});

if (installButton) {
    installButton.addEventListener('click', async () => {
        if (!deferredPrompt) return;
        
        // Show the installation prompt
        deferredPrompt.prompt();
        
        // Wait for the user to respond to the prompt
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`User response to the install prompt: ${outcome}`);
        
        // We've used the prompt, and can't use it again, throw it away
        deferredPrompt = null;
        
        // Hide our install UI
        installPromptContainer.classList.remove('show');
    });
}

if (closeInstallButton) {
    closeInstallButton.addEventListener('click', () => {
        installPromptContainer.classList.remove('show');
    });
}

// Detect if the app is already installed
window.addEventListener('appinstalled', () => {
    // Hide the app-provided install promotion
    if (installPromptContainer) {
        installPromptContainer.classList.remove('show');
    }
    console.log('PWA was installed');
});

// Handle online/offline status
window.addEventListener('online', updateOnlineStatus);
window.addEventListener('offline', updateOnlineStatus);

function updateOnlineStatus() {
    const offlineAlert = document.getElementById('offline-alert');
    if (!offlineAlert) return;
    
    if (navigator.onLine) {
        offlineAlert.classList.remove('show');
    } else {
        offlineAlert.classList.add('show');
    }
}

// Initial check
if (navigator.onLine === false) {
    const offlineAlert = document.getElementById('offline-alert');
    if (offlineAlert) {
        offlineAlert.classList.add('show');
    }
}
