import setMarkerColour from "./set-marker-colour.js";
import generatePopupHTML from "./generate-popup-html.js";
import updateReportLocation from "./update-report-location.js";
/**
 * Creates and adds a MapLibre GL marker for the given report object,
 * configures its popup content, and sets up all related interactions:
 *   - Single‐click toggles the popup (debounced to avoid double-clicks)
 *   - Double‐click enables dragging, with the marker turning purple
 *   - Drag end validates the new position against the UK boundary,
 *     sends an update to the server, and refreshes the popup & shows
 *     a success message
 *   - Clicking elsewhere on the map disables dragging mode
 *   - Marker colour reflects the report condition (or purple when dragging)
 *   - Saves the marker and its popup in the global DKM.markers array
 *
 *   The input report data object is expected to contain:
 *   - id                – numeric primary key
 *   - latitude, longitude – coords
 *   - condition         – 'green'|'orange'|'red'|'none'|'white'|
 *   - place_name        – geocoded place name
 *   - county            – county name
 *   - user_report_number|user_is_superuser – user info
 *   - reasons, comments, photoUrl
 */
export default function addMarkerForReport(report) {
    // Remove inital marker
    if(DKM.newMarker) {
        DKM.newMarker.remove();
        DKM.newMarker = null;
    }

    const marker = new maplibregl.Marker({
        draggable: false
    })
        .setLngLat([report.longitude, report.latitude]) // Set marker position
        .addTo(DKM.map);
    
    const markerElement = marker.getElement();
    setMarkerColour(markerElement, report.condition);

    // Change cursor to pointer when hovering over marker
    markerElement.style.cursor = 'pointer';

    // Intercept multi‐clicks in the capture phase and swallow them:
    // remove the default click-popup listener:
    markerElement.removeEventListener('click', marker._markerClickListener);

    // now install our own click handler that waits in case of a second click:
    let clickTimer = null;
    markerElement.addEventListener('click', e => {
        e.stopImmediatePropagation();
        e.preventDefault();

        // if there's already a pending click, that means this is the 2nd click
        if (clickTimer) {
            clearTimeout(clickTimer);
            clickTimer = null;
            return; // swallow the 2nd click so no popup opens
        }

        // otherwise schedule a popup on a short delay
        clickTimer = setTimeout(() => {
            // Find the marker for this report
            const foundMarker = DKM.markers.find(m => m._reportId === report.id);
            if (foundMarker) {
                // Create and set the popup
                const popup = new maplibregl.Popup()
                    .setLngLat([report.longitude, report.latitude])
                    .setHTML(generatePopupHTML(report));
                foundMarker.setPopup(popup);
                foundMarker.togglePopup();
            } 
            clickTimer = null;
        }, 300); // 300ms is typical dblclick threshold
    }, { capture: true });

    // Add a double-click event listener to make marker draggable
    marker.getElement().addEventListener('dblclick', (e) => {
        e.stopPropagation(); // Prevent the map click event from firing
        e.preventDefault(); // Prevent the popup from toggling
        // Close the popup if it is open
        if (marker.getPopup()) {
            marker.getPopup().remove();
        }
        // Enable dragging
        marker.setDraggable(true); 
        // Change the marker colour to purple when in dragging mode
        setMarkerColour(marker.getElement(), 'purple');
    });

    // Add custom double-tap (touch) handler for iOS/iPad/tablets
    let lastTap = 0;
    markerElement.addEventListener('touchend', function(e) {
        const currentTime = new Date().getTime();
        const tapLength = currentTime - lastTap;
        if (tapLength < 400 && tapLength > 0) { // 400ms threshold
            // Double-tap detected: enable dragging, turn marker purple, close popup
            e.stopPropagation();
            e.preventDefault();

            if (marker.getPopup()) marker.getPopup().remove();
            marker.setDraggable(true);
            setMarkerColour(marker.getElement(), 'purple');
        }
        lastTap = currentTime;
    });

    // Add an event listener to capture the new position when the marker is dragged
    marker.on('dragend', () => {
        // Close the popup if it is open
        if (marker.getPopup()) {
            marker.getPopup().remove();
        }

        let { lat, lng } = marker.getLngLat();
        // round the coordinates to 6 decimal places
        lat = parseFloat(lat.toFixed(6));
        lng = parseFloat(lng.toFixed(6));

        // Check if the clicked location is within the boundary of the UK
        const point = turf.point([lng, lat]);

        // Check if the point is within any of the 4 UK polygons
        let isWithinUK = false;
        for (const feature of DKM.ukBoundary.features) {
            if (turf.booleanPointInPolygon(point, feature)) {
                isWithinUK = true;
                break; // Exit the loop as soon as the point is within a polygon
            }
        }

        if (!isWithinUK) {
            // return the marker to its original position
            marker.setLngLat([report.longitude, report.latitude]); // Set marker position
            return; // Exit the function if the location is outside the UK
        }

        updateReportLocation(report.id, lat, lng); // Send the updated location to the server
        
    });

    // Add a click event listener to the map to disable marker dragging
    DKM.map.on('click', () => {
        if (marker.isDraggable()) {
            marker.setDraggable(false); // Disable dragging
            setMarkerColour(marker.getElement(), report.condition); // Reset the marker colour to its original condition colour
        }
    });

    // stash the report id on the marker instance so we can update it later
    marker._reportId = report.id;
    // add the marker to the markers array
    DKM.markers.push(marker);
}

// Attach the function to the global window object for use when a new marker is added
window.addMarkerForReport = addMarkerForReport;