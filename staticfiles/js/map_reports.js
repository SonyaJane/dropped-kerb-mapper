document.addEventListener('DOMContentLoaded', function () {
    
    // Initialise Choices on the multi-select field with ID "id_reasons"
    const reasonsSelect = document.getElementById("reasons");
    console.log(reasonsSelect);
    if (reasonsSelect) {
        new Choices(reasonsSelect, {
        removeItemButton: true,       // Allows removal of selected options via an "x"
        placeholderValue: "Add reasons for classification",  // Placeholder text
        shouldSort: true             // Maintain the original order of options
        });
    }

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

    // Initialise the map
    const map = new maplibregl.Map({
        container: 'map', // ID of the div where the map will be rendered
        // max zoom:
        maxZoom: 20,
        style: style,
        center: [-3.11, 55.95], // Initial map center (longitude, latitude)
        zoom: 10,
        attributionControl: false, // Disable default attribution control
    });

    // Add navigation controls to the map
    map.addControl(new maplibregl.NavigationControl());

    // Add a custom AttributionControl with compact mode enabled.
    const attributionControl = new maplibregl.AttributionControl({
        compact: true
    });
    map.addControl(attributionControl, 'bottom-right');

    // Compact mode for small screens
    function updateAttributionControl() {
        const screenWidth = window.innerWidth;
        const attributionElement = document.querySelector('.maplibregl-ctrl-attrib');
        if (screenWidth < 550) {
            attributionElement.classList.remove('maplibregl-compact-show');
            attributionElement.removeAttribute('open');
        } else {
            attributionElement.classList.add('maplibregl-compact-show');
            attributionElement.setAttribute('open', '');
        }
    }

    // Run on window resize
    window.addEventListener('resize', updateAttributionControl);

    map.on('styledata', function () {
        const brandingElement = document.querySelector('.os-api-branding.copyright');
        if (brandingElement) {
            brandingElement.remove();
        }
        updateAttributionControl();
    });    

    // Toggle the Google Satellite and Os Map layer when the button is clicked
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
            toggleIcon.src = mapIconUrl;
            // Show the Google attribution elements.
            document.getElementById("google-logo").style.display = "block";
        } else {
            map.setLayoutProperty("google-satellite-layer", "visibility", "none");
            map.setLayoutProperty("os-layer", "visibility", "visible");
            mapContainer.classList.remove("hide-os");
            toggleText.innerText = "Satellite View";
            toggleIcon.src = satelliteIconUrl;
            // Hide the Google attribution elements.
            document.getElementById("google-logo").style.display = "none";
        }
    });

    // add an event listener to the add-report button that enables a click event listener on the map
    const addReportButton = document.getElementById('add-report');
    let newMarker = null;
    addReportButton.addEventListener('click', function () {
        // turn the cursor into crosshair
        map.getCanvas().style.cursor = 'crosshair';
        // Add a click event listener to the map
        map.on('click', function handleMapClick(e) {
            // Show form
            const formContainer = document.querySelector('.map-report-form-container');
            formContainer.style.display = 'block';

            // if a newMarker already exists, remove it
            if (newMarker) {
                newMarker.remove(); // Remove the previous marker
            }

            // Add an event listener to the classification selection dropdown
            const classification = document.getElementById('classification');

            // add a marker at the clicked location
            newMarker = new maplibregl.Marker({
                color: classification.value // Set the marker color to green
            })
                .setLngLat(e.lngLat)  // Set marker position
                .addTo(map);          // Add marker to the map

            const { lng, lat } = e.lngLat;

            // Populate the latitude and longitude fields in the form
            document.getElementById('latitude').value = lat.toFixed(6);
            document.getElementById('longitude').value = lng.toFixed(6);

            function toggleReasonsField() {
                const reasonsDiv = document.getElementById('div_id_reasons');
                // get selected classification from dropdown
                const selectedClassification = classification.value;
        
                if (selectedClassification && (selectedClassification === 'red' || selectedClassification === 'orange')) {
                    reasonsDiv.style.display = '';
                    console.log('Reasons div should be visible');
                } else {
                    reasonsDiv.style.display = 'none';
                    console.log('Reasons div should be hidden');
                    // Unselect all reasons in the dropdown
                    // const reasons = document.querySelectorAll('input[name="reasons"]');
                }

            }

            function setMarkerColor() {
                // change the colour of the marker to the classification valu
                
                let element = newMarker.getElement();
                let svg = element.getElementsByTagName("svg")[0];
                let path = svg.getElementsByTagName("path")[0];
                path.setAttribute("fill", classification.value);
            }
            
            // Attach event listener to classification dropdown
            classification.addEventListener('change', function () {
                toggleReasonsField();
                setMarkerColor();
            });

            // Call the function once to set the initial state
            toggleReasonsField();

            // Add event listener to the close buttons
            const closeButtons = document.querySelectorAll('.close-btn');
            closeButtons.forEach(button => {
                button.addEventListener('click', function () {
                    // Remove the marker from the map
                    newMarker.remove(); // Remove the marker
                    formContainer.style.display = 'none'; // Hide the form
                    map.getCanvas().style.cursor = ''; // Reset cursor style
                    map.off('click'); // Remove click event listener from the map
                });
            });
        });
    });

    // Retrieve the reports data from the embedded JSON script
    const reports = JSON.parse(document.getElementById('reports-data').textContent);
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

});