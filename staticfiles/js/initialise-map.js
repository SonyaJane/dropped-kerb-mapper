/**
 * This function creates a map of the UK using MapLibre GL JS 
 * Sets up the map style, geolocation control, and zooms to user's location.
 * Adds custom, collapsable attribution to the bottom right of the map.
 */ 
export default function initialiseMap() {

    // Create a map style object using the ZXY service.
    const style = {
        "version": 8,
        "sources": {
            "os-tiles": {
                "type": "raster",
                "tiles": [window.location.origin + '/os_tiles/{z}/{x}/{y}/'], // Django proxy URL for tiles
                "tileSize": 256,
                "minzoom": 7,
                "maxzoom": 20,
                "attribution": "Contains OS data &copy; Crown copyright and database rights 2025 | Maplibre"
            },
            "google-satellite": {
                "type": "raster",
                "tiles": [window.location.origin + '/google_satellite_tiles/{z}/{x}/{y}/'],
                "tileSize": 256,
                "minzoom": 7,
                "maxzoom": 20,
                "attribution": "Map data &copy; 2025 | Maplibre"
            }
        },
        "layers": [
            {
                "id": "os-layer",
                "type": "raster",
                "source": "os-tiles"
            },
            {
                "id": "google-satellite-layer",
                "type": "raster",
                "source": "google-satellite",
                "layout": {
                    visibility: "none"  // Initially hidden
                },
            }
        ]
    };

    // Create map
    DKM.map = new maplibregl.Map({
        container: 'map', // ID of the div where the map will be rendered
        minZoom: 7,
        maxZoom: 20,
        style: style,
        center: [-3.2, 55],  // Rough center of the UK
        zoom: 7,
        maxBounds: [
            [ -10.76418, 49.528423 ],
            [ 1.9134116, 61.331151 ]
        ], // UK bounds
        attributionControl: false, // Disable default attribution control
    });

    // add geolocation control to the map
    const geolocateControl = new maplibregl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
        },
        trackUserLocation: true,
        showAccuracyCircle: false,
    });
    DKM.map.addControl(geolocateControl);

    // Move the control to the map controls container
    const geolocateEl = document.querySelector('.maplibregl-ctrl-top-right');
    const mapControlsContainer = document.getElementById('map-controls-container');
    if (geolocateEl && mapControlsContainer) {
        mapControlsContainer.insertBefore(geolocateEl, mapControlsContainer.firstChild);
        //  add class to the geolocate control for styling
        geolocateEl.classList.add('map-control');
        // Add a custom crosshair icon to the geolocate control
        // Remove the default icon and add a Bootstrap icon
        const crosshairIcon = document.querySelector('.maplibregl-ctrl-icon');
        if (crosshairIcon) {
            crosshairIcon.remove();
        }
        const geolocateButton = document.querySelector('.maplibregl-ctrl-geolocate');
        geolocateButton.classList.add('bi', 'bi-crosshair');
    }

    // Add a custom AttributionControl with compact mode enabled.
    const attributionControl = new maplibregl.AttributionControl({
        compact: true
    });
    DKM.map.addControl(attributionControl, 'bottom-right');

    // Track if satellite view is on or off
    DKM.isSatelliteViewOn = false; 

    // Disable Double-Click Zoom on the Map (So our double tap to select a marker handler isn't blocked)
    DKM.map.doubleClickZoom.disable();
}