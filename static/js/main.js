/**
 * Lifeline Hospital - Main JavaScript file
 * Contains core functionality for the hospital website
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Handle offline/online status for PWA
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
    
    // Initialize date pickers (if any)
    const datePickers = document.querySelectorAll('.datepicker');
    if (datePickers.length > 0) {
        datePickers.forEach(input => {
            // Set min date to today
            const today = new Date().toISOString().split('T')[0];
            input.setAttribute('min', today);
        });
    }
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Department filter on doctors page
    const departmentFilter = document.getElementById('department-filter');
    if (departmentFilter) {
        departmentFilter.addEventListener('change', function() {
            const url = new URL(window.location);
            if (this.value) {
                url.searchParams.set('department', this.value);
            } else {
                url.searchParams.delete('department');
            }
            window.location = url.toString();
        });
    }
    
    // Specialty filter on doctors page
    const specialtyFilter = document.getElementById('specialty-filter');
    if (specialtyFilter) {
        specialtyFilter.addEventListener('change', function() {
            const url = new URL(window.location);
            if (this.value) {
                url.searchParams.set('specialty', this.value);
            } else {
                url.searchParams.delete('specialty');
            }
            window.location = url.toString();
        });
    }
    
    // Appointment cancellation confirmation
    const cancelButtons = document.querySelectorAll('.cancel-appointment-btn');
    cancelButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to cancel this appointment?')) {
                e.preventDefault();
            }
        });
    });
    
    // Language selector
    const languageSelectors = document.querySelectorAll('.language-selector .dropdown-item');
    languageSelectors.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            window.location = this.getAttribute('href');
        });
    });
    
    // PWA installation
    let deferredPrompt;
    const installPrompt = document.getElementById('install-prompt');
    const installButton = document.getElementById('install-button');
    const closePromptButton = document.getElementById('close-prompt');
    
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent Chrome 67 and earlier from automatically showing the prompt
        e.preventDefault();
        // Stash the event so it can be triggered later
        deferredPrompt = e;
        // Update UI to notify the user they can add to home screen
        if (installPrompt) installPrompt.classList.add('show');
    });
    
    if (installButton) {
        installButton.addEventListener('click', async () => {
            if (!deferredPrompt) return;
            
            // Show the install prompt
            deferredPrompt.prompt();
            
            // Wait for the user to respond to the prompt
            const { outcome } = await deferredPrompt.userChoice;
            
            // We no longer need the prompt regardless of outcome
            deferredPrompt = null;
            
            // Hide the install promotion
            installPrompt.classList.remove('show');
        });
    }
    
    if (closePromptButton) {
        closePromptButton.addEventListener('click', () => {
            installPrompt.classList.remove('show');
        });
    }
    
    // Check if the app is already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
        // App is installed, hide the install prompt
        if (installPrompt) installPrompt.style.display = 'none';
    }
    
    // Initialize service worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('Service Worker registered with scope:', registration.scope);
        }).catch(function(error) {
            console.error('Service Worker registration failed:', error);
        });
    }
});
