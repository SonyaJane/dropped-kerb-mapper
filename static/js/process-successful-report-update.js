import generatePopupHTML from './generate-popup-html.js';
import setMarkerColour from './set-marker-colour.js';
/**
* Handles the HTMX swap after a successful report location update:
*  - Reads the updated report data from the `<script id="report-data">` JSON embed.
*  - Parses it into a report object (which must include a `marker` reference).
*  - Removes the JSON `<script>` element from the DOM.
*  - Refreshes the marker’s popup with new coordinates, place name, and county.
*  - Disables dragging on the marker and resets its color to match the report’s condition.
*
* Expects:
*  • A `<script id="report-data" type="application/json">` containing the updated report.
*  • `report.marker` to reference the MapLibre GL marker instance.
*/
export default function processSuccessfulReportUpdate() {
    // get the new report data from the embedded JSON in the DOM
    const data = document.getElementById('report-data');
    
    // Parse the JSON data
    const report = JSON.parse(data.textContent); 

    // remove the report data from the DOM
    data.remove();

    // find the matching marker in the markers array
    const marker = DKM.markers.find(m => m._reportId === report.id);
    
    // Refresh the popup content with updated data
    marker.setPopup(new maplibregl.Popup().setHTML(
        generatePopupHTML(report)
    ));
        
    // disable dragging after the location is updated
    if (marker.isDraggable()) {
        marker.setDraggable(false); 
        setMarkerColour(marker.getElement(), report.condition); // Reset the marker colour to its original condition colour
    }
}