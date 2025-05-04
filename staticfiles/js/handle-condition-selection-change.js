/**
* Invoked when the "condition" select field changes value.
* - Calls toggleReasonsFieldVisibility() to show or hide the reasons field
*   depending on the selected condition.
* - If a new report marker is active (DKM.newMarker), updates its icon color
*   to match the chosen condition via setMarkerColour().
*/
import setMarkerColour from "./set-marker-colour.js";
import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";

export default function handleConditionSelectionChange() {
    // Show or hide the reasons field based on the selected condition
    toggleReasonsFieldVisibility();
    // Change the marker colour to the new condition value
    if (DKM.newMarker){
        let newMarker = DKM.newMarker.getElement();
        setMarkerColour(newMarker, condition.value);
    }
}