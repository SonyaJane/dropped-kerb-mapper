import selectNewReportLocation from "./select-new-report-location.js";
import handleStreetViewMapClick from "./handle-streetview-map-click.js";
import closeForm from "./close-form.js";

/**
 * Toggles the map add report mode on or off.
 *
 * When activated:
 *   - Turns the add report button orange
 *   - Changes the map cursor to a blue crosshair
 *   - Disables existing marker popups
 *   - Attaches a click listener to the map for selecting a new report location
 *
 * When deactivated:
 *   - Turns the add report button back to white
 *   - Resets the map cursor to default
 *   - Removes the map click listener
 *   - Restores saved popups on existing markers 
 */
let cancelButton = null;
let addReportButtonRef = null;

 function handleCancelClick() {
    if (addReportButtonRef) {
    toggleNewReportMode(addReportButtonRef);
    }
}

export default function toggleNewReportMode(addReportButton) {
    console.log("Toggling new report mode");
    // Build an encoded SVG string to create a blue cross cursor for add report mode
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32">
    <line x1="16" y1="0" x2="16" y2="32" stroke="blue" stroke-width="2"/>
    <line x1="0" y1="16" x2="32" y2="16" stroke="blue" stroke-width="2"/>
    </svg>`;
    const encodedSvg = encodeURIComponent(svg);
    const dataUrl = `url("data:image/svg+xml;charset=UTF-8,${encodedSvg}") 16 16, crosshair`;
    addReportButtonRef = addReportButton;
    if (!cancelButton) {
        cancelButton = document.querySelector('.report-cancel-btn');
    }
   
    // If the button is active, disable "add report" mode
    if (addReportButton.classList.contains('button-active')) {
        console.log("Disabling new report mode");
        // Add click event listener for the street view map
        DKM.map.on('click', handleStreetViewMapClick);

        addReportButton.classList.remove('button-active'); // Remove the active class
        DKM.map.getCanvas().style.cursor = ''; // Reset the cursor to default
        DKM.map.off('click', selectNewReportLocation); // Remove click event listener to the map   
        // reenable popup event listener for all the markers
        DKM.markers.forEach(marker => {
            marker.setPopup(marker._savedPopup);
        });
        // remove the form
        closeForm();
        // If a new marker exists, remove it
        if (DKM.newMarker) {
            DKM.newMarker.remove();
        }
        // Remove event listener from the form cancel button
        if (cancelButton) {
            cancelButton.removeEventListener('click', handleCancelClick);
        }

    } else {
        console.log("Enabling new report mode");
        // Prevent add report mode if satellite view is active
        if (DKM.isSatelliteViewOn) {
            // Optionally show a message to the user here
            alert("You can only add a report when the standard map is active. This is because the satellite view is offset from the standard map, so the location you select may not be accurate.");
            return;
        }   
        // Remove click event listener for the street view map
        DKM.map.off('click', handleStreetViewMapClick);
        // If the button is not active, enable "add report" mode
        addReportButton.classList.add('button-active'); // Add the active class
        // turn the cursor to custom crosshair
        DKM.map.getCanvas().style.cursor = dataUrl;
        DKM.map.on('click', selectNewReportLocation); // Add a click event listener to the map
        // remove popup event listener from all the markers
        DKM.markers.forEach(marker => {
            marker.setPopup(null);
        });
        // Add event listener to the form cancel button
        if (cancelButton) {
            cancelButton.removeEventListener('click', handleCancelClick); // Prevent duplicates
            cancelButton.addEventListener('click', handleCancelClick);
        }
    }
}
