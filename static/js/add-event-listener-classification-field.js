import setMarkerColour from "./set-marker-colour.js";
import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";

export default function addEventListenerClassificationField() {
    // Attach event listener to classification dropdown
    classification.addEventListener('change', () => {
        toggleReasonsFieldVisibility();
        // Change the marker colour to the new classification value
        let newMarker = DKM.newMarker.getElement();
        setMarkerColour(newMarker, classification.value); 
    });
}