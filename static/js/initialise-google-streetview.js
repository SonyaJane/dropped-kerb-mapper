import handleStreetViewMapClick from "./handle-streetview-map-click.js";

export default function initialiseGoogleStreetView() {
    // set up variables
    DKM.streetView = null;           // Google Street View instance
    DKM.isStreetViewVisible = false; // Flag to track if Street View is currently visible
    DKM.awaitingStreetViewClick = false; // Flag to track if we are waiting for a click to set Street View

    // arrow marker variables
    DKM.arrowMarker = null; // MapLibre marker for the arrow
    DKM.arrowEl = null;     // HTML element for the arrow marker

    const svBtn = document.getElementById('toggle-streetview');  // Button to toggle Street View
    const svContainer = document.getElementById('streetview-container'); // Container for Street View
    const mapDiv = document.getElementById('map');               // Map container

    function removeArrowMarker() {
        if (DKM.arrowMarker) {
            DKM.arrowMarker.remove();
            DKM.arrowMarker = null;
            DKM.arrowEl = null;
        }
    }

    // Show/hide Street View panel and manage state
    svBtn.addEventListener('click', function() {
        DKM.isStreetViewVisible = !DKM.isStreetViewVisible;
        if (DKM.isStreetViewVisible) {
            svContainer.style.display = 'block';
            svBtn.classList.add('button-active');
            mapDiv.style.height = '50%';
            DKM.awaitingStreetViewClick = true;
        } else {
            svContainer.style.display = 'none';
            svBtn.classList.remove('button-active');
            mapDiv.style.height = '100%';
            DKM.awaitingStreetViewClick = false;
            removeArrowMarker();
        }
        DKM.map.resize();
    });

    // On map click, create or move marker and Street View (if active and waiting)
    DKM.map.on('click', handleStreetViewMapClick);

    // Resize map on window resize or when Street View is toggled
    window.addEventListener('resize', () => DKM.map.resize());
}