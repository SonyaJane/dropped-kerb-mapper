export default function initialiseMap() {

    // Create a map style object using the ZXY service.
    const style = {
        "version": 8,
        "sources": {
            "os-tiles": {
                "type": "raster",
                "tiles": [window.location.origin + '/os_tiles/{z}/{x}/{y}/'], // Django proxy URL for tiles
                "tileSize": 256,
                "maxzoom": 20,
                "attribution": "Contains OS data &copy; Crown copyright and database rights 2025 | Maplibre"
            },
            "google-satellite": {
                "type": "raster",
                "tiles": [window.location.origin + '/google_satellite_tiles/{z}/{x}/{y}/'],
                "tileSize": 256,
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
        // max zoom:
        maxZoom: 20,
        style: style,
        center: [-3.11, 55.95], // Initial map center (longitude, latitude)
        zoom: 10,
        attributionControl: false, // Disable default attribution control
    });

    // Add navigation controls to the map
    DKM.map.addControl(new maplibregl.NavigationControl());

    // Add a custom AttributionControl with compact mode enabled.
    const attributionControl = new maplibregl.AttributionControl({
        compact: true
    });
    DKM.map.addControl(attributionControl, 'bottom-right');
}