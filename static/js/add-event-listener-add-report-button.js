import addEventListenerOnMapClick from './add-event-listener-on-map-click.js';

export default function addEventListenerAddReportButton() {

    // add an event listener to the add-report button that enables a click event listener on the map
    const addReportButton = document.getElementById('add-report');

    addReportButton.addEventListener('click', function () {

        // turn the cursor into crosshair
        DKM.map.getCanvas().style.cursor = 'crosshair';

        // Add a click event listener to the map
        addEventListenerOnMapClick()
    });
}