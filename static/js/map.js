/**
 * Lifeline Hospital - Facility Map Functions
 * Uses Leaflet.js to create an interactive facility map
 */

// Initialize the facility map if the element exists
document.addEventListener('DOMContentLoaded', function() {
    const mapElement = document.getElementById('facility-map');
    
    if (!mapElement) return;
    
    // Hospital location coordinates
    const hospitalLat = 28.6139;  // Default latitude - New Delhi
    const hospitalLng = 77.2090;  // Default longitude - New Delhi
    
    // Initialize map
    const map = L.map('facility-map').setView([hospitalLat, hospitalLng], 16);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    }).addTo(map);
    
    // Add marker for the hospital
    const hospitalMarker = L.marker([hospitalLat, hospitalLng]).addTo(map);
    hospitalMarker.bindPopup("<strong>Lifeline Hospital</strong><br>Main Campus").openPopup();
    
    // Add departments around the hospital (example locations)
    const departments = [
        { name: "Emergency Department", lat: hospitalLat + 0.0005, lng: hospitalLng + 0.0008, color: "red" },
        { name: "Outpatient Clinic", lat: hospitalLat - 0.0003, lng: hospitalLng + 0.0005, color: "blue" },
        { name: "Diagnostic Center", lat: hospitalLat + 0.0007, lng: hospitalLng - 0.0004, color: "green" },
        { name: "Rehabilitation Center", lat: hospitalLat - 0.0006, lng: hospitalLng - 0.0005, color: "orange" }
    ];
    
    // Add department markers
    departments.forEach(dept => {
        const marker = L.circleMarker([dept.lat, dept.lng], {
            radius: 8,
            fillColor: dept.color,
            color: "#000",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);
        
        marker.bindPopup(`<strong>${dept.name}</strong>`);
    });
    
    // Add hospital building outline (simplified rectangle)
    const buildingOutline = L.polygon([
        [hospitalLat + 0.0008, hospitalLng + 0.0010],
        [hospitalLat + 0.0008, hospitalLng - 0.0010],
        [hospitalLat - 0.0008, hospitalLng - 0.0010],
        [hospitalLat - 0.0008, hospitalLng + 0.0010]
    ], {
        color: '#2c6ba0',
        fillColor: '#2c6ba0',
        fillOpacity: 0.2,
        weight: 2
    }).addTo(map);
    
    // Add parking areas
    const parkingAreas = [
        {
            name: "Main Parking",
            coordinates: [
                [hospitalLat + 0.0012, hospitalLng + 0.0015],
                [hospitalLat + 0.0012, hospitalLng + 0.0005],
                [hospitalLat + 0.0008, hospitalLng + 0.0005],
                [hospitalLat + 0.0008, hospitalLng + 0.0015]
            ]
        },
        {
            name: "Staff Parking",
            coordinates: [
                [hospitalLat - 0.0012, hospitalLng - 0.0015],
                [hospitalLat - 0.0012, hospitalLng - 0.0005],
                [hospitalLat - 0.0008, hospitalLng - 0.0005],
                [hospitalLat - 0.0008, hospitalLng - 0.0015]
            ]
        }
    ];
    
    parkingAreas.forEach(area => {
        const parkingPolygon = L.polygon(area.coordinates, {
            color: '#888',
            fillColor: '#888',
            fillOpacity: 0.3,
            weight: 1
        }).addTo(map);
        
        parkingPolygon.bindPopup(`<strong>${area.name}</strong>`);
    });
    
    // Add entrances
    const entrances = [
        { name: "Main Entrance", lat: hospitalLat, lng: hospitalLng + 0.0010 },
        { name: "Emergency Entrance", lat: hospitalLat + 0.0008, lng: hospitalLng + 0.0005 },
        { name: "Staff Entrance", lat: hospitalLat - 0.0005, lng: hospitalLng - 0.0010 }
    ];
    
    entrances.forEach(entrance => {
        const entranceMarker = L.marker([entrance.lat, entrance.lng], {
            icon: L.divIcon({
                className: 'entrance-marker',
                html: '<i class="fas fa-door-open"></i>',
                iconSize: [20, 20],
                iconAnchor: [10, 10]
            })
        }).addTo(map);
        
        entranceMarker.bindPopup(`<strong>${entrance.name}</strong>`);
    });
    
    // Add get directions link
    document.getElementById('get-directions-btn')?.addEventListener('click', function() {
        // Open Google Maps directions in a new tab
        window.open(`https://www.google.com/maps/dir/?api=1&destination=${hospitalLat},${hospitalLng}`);
    });
    
    // Floor selector
    const floorSelector = document.getElementById('floor-selector');
    if (floorSelector) {
        floorSelector.addEventListener('change', function() {
            const floor = this.value;
            console.log(`Showing floor: ${floor}`);
            
            // Here you would update the map to show the selected floor
            // This would typically involve hiding/showing different layers
            // For this example, we'll just change the popup content of the hospital marker
            
            hospitalMarker.setPopupContent(`<strong>Lifeline Hospital</strong><br>Floor ${floor}`);
            hospitalMarker.openPopup();
        });
    }
});
