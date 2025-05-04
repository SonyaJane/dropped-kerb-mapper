import setMarkerColour from "./set-marker-colour.js";
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
    const marker = new maplibregl.Marker({
        draggable: false
    })
        .setLngLat([report.longitude, report.latitude]) // Set marker position
        .setPopup(new maplibregl.Popup().setHTML(
            generatePopupHTML(report, report.latitude, report.longitude, report.place_name, report.county)
        ))
        .addTo(DKM.map);
    
    const markerElement = marker.getElement();
    setMarkerColour(markerElement, report.condition)

    // Intercept multi‐clicks in the capture phase and swallow them:
    // remove the default click-popup listener:
    markerElement.removeEventListener('click', marker._markerClickListener);

        // now install your own click handler that waits a bit:
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
            marker.togglePopup();
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

    // Add an event listener to capture the new position when the marker is dragged
    marker.on('dragend', () => {
        // Close the popup if it is open
        if (marker.getPopup()) {
            marker.getPopup().remove();
        }

        const newLngLat = marker.getLngLat();
        // round the coordinates to 6 decimal places
        newLngLat.lat = parseFloat(newLngLat.lat.toFixed(6));
        newLngLat.lng = parseFloat(newLngLat.lng.toFixed(6));

        // Check if the clicked location is within the boundary of the UK
        const point = turf.point([newLngLat.lng, newLngLat.lat]);
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

        // Send the updated latitude and longitude to the server
        updateReportLocation(report.id, newLngLat.lat, newLngLat.lng)
            .then(data => {
                // Refresh the popup content with updated data
                marker.setPopup(new maplibregl.Popup().setHTML(
                    generatePopupHTML(report, newLngLat.lat, newLngLat.lng, data.place_name, data.county)
                ));
            })
            // then display a meesage to the user saying the location has been updated  
            .then(() => {
                // Create a success message in a new div
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.textContent = 'Location changed successfully!';
                
                // Append the success message to the map container
                const mapContainer = document.getElementById('map');
                mapContainer.appendChild(successMessage);

                // Automatically remove the success message after 1.5 seconds
                setTimeout(() => {
                    successMessage.remove();
                }, 1500);
            })
            .catch(error => {
                console.error('Error updating report location:', error);
                alert(`An error occurred while updating the location: ${error.message}`);
            });
        
        // disable dragging after the location is updated
        if (marker.isDraggable()) {
            marker.setDraggable(false); 
            setMarkerColour(marker.getElement(), report.condition); // Reset the marker colour to its original condition colour
        }
    });

    // Add a click event listener to the map to disable marker dragging
    DKM.map.on('click', () => {
        if (marker.isDraggable()) {
            marker.setDraggable(false); // Disable dragging
            setMarkerColour(marker.getElement(), report.condition); // Reset the marker colour to its original condition colour
        }
    });

    // stash the popup on the marker so we can remove it then re‑attach later
    marker._savedPopup = marker.getPopup();
    // add the marker to the markers array
    DKM.markers.push(marker);

}

function generatePopupHTML(report, latitude, longitude, placeName, county) {
    // If the user who created the report is a superuser, show the report id.
    // Otherwise, show the user_report_number.
    const reportNumber = (report.user && report.user_is_superuser) ? report.id : report.user_report_number;
    // Only include the reasons line if condition is red or orange.
    let reasons = '';
    if ((report.condition === 'red' || report.condition === 'orange')) {
        reasons = `<p><span class="orange-font">${report.reasons}</span></p>`;
    }
    // Only include the comments line if there are comments.
    let comments = ''
    if (report.comments) {
        comments = `<p><span class="orange-font">${report.comments}</span></p>`;
    }
    return `
        <p>
            <span class="orange-font">Report ${reportNumber}</span>
            <span>&nbsp;</span>
            <a href="/reports/${report.id}/" class="custom-link">view</a>
            <span>&nbsp;</span>
            <a href="/reports/${report.id}/edit/" class="custom-link">edit</a>
        </p>
        <p>
            <span class="orange-font" id="latitude-${report.id}"> ${latitude}, </span>
            <span class="orange-font" id="longitude-${report.id}"> ${longitude}</span>
        </p>
        <p><span class="orange-font" id="place_name-${report.id}"> ${placeName || 'Unknown'}</span></p>
        <p><span class="orange-font" id="county-${report.id}"> ${county}</span></p>
        ${reasons}
        ${comments}
        ${report.photoUrl ? `<img src="${report.photoUrl}" alt="Photo of dropped kerb" style="max-width: 100%; height: auto;">` : ''}
    `;
}

// Function to send the updated location to the server
async function updateReportLocation(reportId, latitude, longitude) {
    console.log('Inside updateReportLocation()');
    const csrfToken = getCSRFToken(); // Get the CSRF token for security
    const response = await fetch(`/reports/${reportId}/update-location/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ latitude, longitude })
    });

    if (!response.ok) {
        throw new Error('Failed to update location. Please try again.');
    }

    return await response.json();
}

// Function to get the CSRF token from the cookie
function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

// Attach the function to the global window object for use when a new marker is added
window.addMarkerForReport = addMarkerForReport;