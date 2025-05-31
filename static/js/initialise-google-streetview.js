import handleStreetViewMapClick from "./handle-streetview-map-click.js";
import updateArrowMarker from "./update-arrow-marker.js";

export default function initialiseGoogleStreetView() {
    // Adds click event listener to the toggle Street View button

    // set up variables
    DKM.streetView = null;           // Google Street View instance
    DKM.isStreetViewVisible = false; // Flag to track if Street View is currently visible
    DKM.awaitingFirstMapClick = false; // Flag to track if we are waiting for a click to set Street View

    // arrow marker variables
    DKM.arrowMarker = null; // MapLibre marker for the arrow
    DKM.arrowEl = null;     // HTML element for the arrow marker

    const svBtn = document.getElementById('toggle-streetview');  // Button to toggle Street View
    const svContainer = document.getElementById('streetview-container'); // Container for Street View
    const mapDiv = document.getElementById('map'); // Map container
    const svMsg = document.getElementById('streetview-message'); // Message to show when waiting for Street View click

    function removeArrowMarker() {
        if (DKM.arrowMarker) {
            DKM.arrowMarker.remove();
            DKM.arrowMarker = null;
            DKM.arrowEl = null;
        }
    }

    // Show/hide Street View panel and manage state
    svBtn.addEventListener('click', function() {
        // Toggle Street View visibility
        DKM.isStreetViewVisible = !DKM.isStreetViewVisible;
        if (DKM.isStreetViewVisible) {
            // Turn on Street View
            svBtn.classList.add('button-active'); // Add active class to button
            svContainer.style.display = 'block'; // Show Street View container
            svContainer.style.pointerEvents = 'auto'; // Enable pointer events on the container
            mapDiv.style.height = '50%'; // Reduce map height to make space for Street View
            DKM.awaitingFirstMapClick = true; // Set flag to indicate we are waiting for a click to set Street View
            // add click event listener to the map to handle Street View clicks
            DKM.map.on('click', handleStreetViewMapClick);
        } else {
            // Turn off Street View
            console.log('Turning off Street View');
            // Remove event listeners for position and POV changes
            if (DKM._positionListener) {
                DKM._positionListener.remove();
                DKM._positionListener = null;
            }
            if (DKM._povListener) {
                DKM._povListener.remove();
                DKM._povListener = null;
            }
            svBtn.classList.remove('button-active'); // Remove active class from button
            DKM.streetView = null; // Clear Street View instance
            DKM.isStreetViewVisible = false; // Clear visibility flag
            DKM.awaitingFirstMapClick = false;  // Clear waiting flag
            svContainer.style.display = 'none'; // Hide Street View container
            svContainer.style.pointerEvents = 'none'; // Disable pointer events on the container
            mapDiv.style.height = '100%'; // Restore full height to the map
            removeArrowMarker(); // Remove arrow marker if it exists
            svMsg.classList.remove('hidden'); // Restore waiting message
            // Remove click event listener from the map
            DKM.map.off('click', handleStreetViewMapClick);
        }
        DKM.map.resize();
    });
    
    // Resize map on window resize or when Street View is toggled
    window.addEventListener('resize', () => DKM.map.resize());
}