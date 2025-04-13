import handleMapClick from "./handle-map-click.js";

export default function addEventListenerAddReportButton() {

    // add an event listener to the add-report button that enables a click event listener on the map
    const addReportButton = document.getElementById('add-report');

    addReportButton.addEventListener('click', () => {
        if (addReportButton.classList.contains('add-report-active')) {
            // If the button is active, disable "add report" mode
            addReportButton.classList.remove('add-report-active'); // Remove the active class
            DKM.map.getCanvas().style.cursor = ''; // Reset the cursor to default
            DKM.map.off('click', handleMapClick) // Remove click event listener to the map        
            } else {
            // If the button is not active, enable "add report" mode
            addReportButton.classList.add('add-report-active'); // Add the active class
            DKM.map.getCanvas().style.cursor = 'crosshair'; // Change the cursor to crosshair
            DKM.map.on('click', handleMapClick) // Add a click event listener to the map        }
        }
    });
}
