document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the reports data from the embedded JSON script
    const reports = JSON.parse(document.getElementById('reports-data').textContent);

    // Create a map style object using the ZXY service.
    const style = {
        "version": 8,
        "sources": {
            "os-tiles": {
                "type": "raster",
                "tiles": [window.location.origin + '/os_tiles/{z}/{x}/{y}/'], // Django proxy URL for tiles
                "tileSize": 256,
                "maxzoom": 20,
                "attribution": "Contains OS data © Crown copyright and database rights 2025"
            },
            "google-satellite": {
                "type": "raster",
                "tiles": [window.location.origin + '/google_satellite_tiles/{z}/{x}/{y}/'],
                "tileSize": 256,
                "maxzoom": 20,
                "attribution": "Map data &copy; 2025"
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

    // Initialise the map
    const map = new maplibregl.Map({
        container: 'map', // ID of the div where the map will be rendered
        // max zoom:
        maxZoom: 20,
        style: style,
        center: [-3.11, 55.95], // Initial map center (longitude, latitude)
        zoom: 10,
    });

    // Add navigation controls to the map
    map.addControl(new maplibregl.NavigationControl());

    map.on('styledata', function () {
        document.querySelector('.os-api-branding.copyright').remove();
    });
// class="maplibregl-ctrl maplibregl-ctrl-attrib maplibregl-compact"
// class="maplibregl-ctrl maplibregl-ctrl-attrib maplibregl-compact maplibregl-compact-show" open="">

    // Add markers for each report
    reports.forEach(report => {
        new maplibregl.Marker()
            .setLngLat([report.longitude, report.latitude]) // Set marker position
            .setPopup(new maplibregl.Popup().setHTML(`
                <strong>Report ID:</strong> ${report.id}<br>
                <strong>Classification:</strong> ${report.classification}<br>
                <strong>Reasons:</strong> ${report.reasons}<br>
                <strong>Comments:</strong> ${report.comments}
            `)) // Add a popup with report details
            .addTo(map);
    });

    // Toggle the Google Satellite layer when the button is clicked.
    document.getElementById("toggle-satellite").addEventListener("click", function () {
        const toggleText = document.getElementById("toggle-text");
        const toggleIcon = document.getElementById("toggle-icon");
        const googleVisibility = map.getLayoutProperty("google-satellite-layer", "visibility");
        const mapContainer = document.getElementById("map");
        if (googleVisibility === "none") {
            map.setLayoutProperty("google-satellite-layer", "visibility", "visible");
            map.setLayoutProperty("os-layer", "visibility", "none");
            mapContainer.classList.add("hide-os");
            toggleText.innerText = "Map View";
            toggleIcon.src = "{% static 'images/map-icon.png' %}";
            // Show the Google attribution elements.
            document.getElementById("google-logo").style.display = "block";
        } else {
            map.setLayoutProperty("google-satellite-layer", "visibility", "none");
            map.setLayoutProperty("os-layer", "visibility", "visible");
            mapContainer.classList.remove("hide-os");
            toggleText.innerText = "Satellite View";
            toggleIcon.src = "{% static 'images/satellite-icon.png' %}";
            // Hide the Google attribution elements.
            document.getElementById("google-logo").style.display = "none";
        }
    });

});