import setMarkerColour from "./set-marker-colour.js";
import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";

export default function addEventListenerConditionField() {
    // Attach event listener to condition dropdown
    condition.addEventListener('change', () => {
        toggleReasonsFieldVisibility();
        // Change the marker colour to the new condition value
        let newMarker = DKM.newMarker.getElement();
        setMarkerColour(newMarker, condition.value); 
    });
}