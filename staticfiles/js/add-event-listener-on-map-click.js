import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";
import addEventListenerFormCloseButtons from "./add-event-listener-form-close-buttons.js";

export default function addEventListenerOnMapClick() {

    // Add a click event listener to the map
    DKM.map.on('click', function handleMapClick(e) {

        // add a marker at the clicked location

        // if a newMarker already exists, remove it
        if (DKM.newMarker) {
            DKM.newMarker.remove();
        }

        // Get the current classification value (for the marker colour)
        const classification = document.getElementById('classification');

        // add marker
        DKM.newMarker = new maplibregl.Marker({
            color: classification.value // Set the marker colour
        })
            .setLngLat(e.lngLat) 
            .addTo(DKM.map);

        // Show new report form
        const formContainer = document.getElementById('map-report-form-container');
        formContainer.style.display = 'block';

        // Populate the latitude and longitude fields in the form
        const { lng, lat } = e.lngLat;
        document.getElementById('latitude').value = lat.toFixed(6);
        document.getElementById('longitude').value = lng.toFixed(6);

        // Call the function once to set the initial state
        toggleReasonsFieldVisibility();
        // Add event listener to the close buttons
        addEventListenerFormCloseButtons(formContainer); 
    });
}