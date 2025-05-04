/**
 * Checks if the clicked location is within the boundary of the UK.
 * If it is, it adds a new marker at the clicked location and shows the report form.
 * Populates the latitude and longitude fields in the form.
 * If a new marker already exists, it removes it before adding the new one, allowing the user to select a new location.
 * Adds an event listener to the form cancel button to close and reset the form when clicked.
 */
import closeForm from "./close-form.js";

export default function selectNewReportLocation(e) {

    // check if the clicked location is within the boundary of the UK
    const { lng, lat } = e.lngLat;
    const point = turf.point([lng, lat]);
    let isWithinUK = false;

    // Check if the point is within any of the 4 UK polygons
    for (const feature of DKM.ukBoundary.features) {
        if (turf.booleanPointInPolygon(point, feature)) {
            isWithinUK = true;
            break; // Exit the loop as soon as the point is within a polygon
        }
    }

    if (!isWithinUK) {
        return; // Exit the function if the location is outside the UK
    }

    // if a newMarker already exists, remove it
    if (DKM.newMarker) {
        DKM.newMarker.remove();
    }

    // Get the current condition value (for the marker colour)
    const condition = document.getElementById('condition');

    // Add a new marker at the clicked location
    DKM.newMarker = new maplibregl.Marker({
        color: condition.value // Set the marker colour
    })
        .setLngLat(e.lngLat) 
        .addTo(DKM.map);

    // Show report form
    const formContainer = document.getElementById('map-report-form-container');
    formContainer.classList.remove('hidden');

    // Populate the latitude and longitude fields in the form
    document.getElementById('latitude').value = lat.toFixed(6);
    document.getElementById('longitude').value = lng.toFixed(6);

    // Add event listener to the form cancel button
    const cancelButton = document.querySelector('.report-cancel-btn');
    cancelButton.addEventListener('click', () => {
        closeForm();
    });
}