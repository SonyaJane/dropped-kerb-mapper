import handleMapClick from "./handle-map-click.js";

export default function addEventListenerAddReportButton() {

    // add an event listener to the add-report button that enables a click event listener on the map
    const addReportButton = document.getElementById('add-report');
    // Build an encoded SVG string for the vlue cursor
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32">
    <line x1="16" y1="0" x2="16" y2="32" stroke="blue" stroke-width="2"/>
    <line x1="0" y1="16" x2="32" y2="16" stroke="blue" stroke-width="2"/>
    </svg>`;
    const encodedSvg = encodeURIComponent(svg);
    const dataUrl = `url("data:image/svg+xml;charset=UTF-8,${encodedSvg}") 16 16, crosshair`;
    console.log(dataUrl);

    addReportButton.addEventListener('click', () => {
        if (addReportButton.classList.contains('button-active')) {
            // If the button is active, disable "add report" mode
            addReportButton.classList.remove('button-active'); // Remove the active class
            DKM.map.getCanvas().style.cursor = ''; // Reset the cursor to default
            DKM.map.off('click', handleMapClick) // Remove click event listener to the map   
            // reenable popup event listener for all the markers
            DKM.markers.forEach(marker => {
                marker.setPopup(marker._savedPopup);
              });     
            } else {
            // If the button is not active, enable "add report" mode
            addReportButton.classList.add('button-active'); // Add the active class
            // enable the submit button
            const submitBtn = document.getElementById("report-submit-btn");
            submitBtn.disabled = false;
            submitBtn.value = "Submit";
            // turn the cursor to custom crosshair
            DKM.map.getCanvas().style.cursor = dataUrl;
            DKM.map.on('click', handleMapClick) // Add a click event listener to the map
            // remove popup event listener from all the markers
            DKM.markers.forEach(marker => {
                marker.setPopup(null);
            });
        }
    });
}
