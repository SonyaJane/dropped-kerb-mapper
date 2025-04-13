export default function addExistingReportsToMap() {
    // Retrieve the reports data from the embedded JSON script
    const reports = JSON.parse(document.getElementById('reports-data').textContent);
    // Add markers for each report
    reports.forEach(report => {
        const marker = new maplibregl.Marker({
            color: report.classification, // Set the marker colour
            draggable: true
        })
            .setLngLat([report.longitude, report.latitude]) // Set marker position
            .setPopup(new maplibregl.Popup().setHTML(
                generatePopupHTML(report, report.latitude, report.longitude, report.place_name, report.county)
            ))
            .addTo(DKM.map);

         // Add an event listener to capture the new position when the marker is dragged
        marker.on('dragend', () => {
            const newLngLat = marker.getLngLat();
            // round the coordinates to 6 decimal places
            newLngLat.lat = parseFloat(newLngLat.lat.toFixed(6));
            newLngLat.lng = parseFloat(newLngLat.lng.toFixed(6));

            // check if the clicked location is within the boundary of the UK

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
                .catch(error => {
                    console.error('Error updating report location:', error);
                    alert(`An error occurred while updating the location: ${error.message}`);
                });
        });   
    });
}

function generatePopupHTML(report, latitude, longitude, placeName, county) {
    return `
        <strong>Report ID:</strong> ${report.id}<br>
        <strong>Latitude:</strong><span id="latitude-${report.id}"> ${latitude} </span><br>
        <strong>Longitude:</strong><span id="longitude-${report.id}"> ${longitude}</span><br>
        <strong>Place:</strong><span id="place_name-${report.id}"> ${placeName || 'Unknown'}</span><br>
        <strong>County:</strong><span id="county-${report.id}"> ${county || 'Unknown'}</span><br>
        <strong>Classification:</strong> ${report.classification}<br>
        <strong>Reasons:</strong> ${report.reasons}<br>
        <strong>Comments:</strong> ${report.comments}<br>
        ${report.photoUrl ? `<img src="${report.photoUrl}" alt="Photo of dropped kerb" style="max-width: 100%; height: auto;">` : ''}
        <br>
        <a href="/reports/${report.id}/edit/" class="btn btn-primary btn-sm" style="margin-top: 10px;">Edit</a>
    `;
}

// Function to send the updated location to the server
async function updateReportLocation(reportId, latitude, longitude) {
    const csrfToken = getCSRFToken(); // Get the CSRF token for security
    const response = await fetch(`/reports/${reportId}/update-location/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken // Ensure you include the CSRF token for security
        },
        body: JSON.stringify({ latitude, longitude })
    });
    
    if (!response.ok) {
        throw new Error('Failed to update location. Please try again.');
    }

    return await response.json(); // Parse the JSON response.
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