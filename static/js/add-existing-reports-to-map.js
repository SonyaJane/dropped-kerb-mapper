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
            .setPopup(new maplibregl.Popup().setHTML(`
            <strong>Report ID:</strong> ${report.id}<br>
            <strong>Latitude:</strong><span id="latitude-${report.id}"> ${report.latitude} </span><br>
            <strong>Longitude:</strong><span id="longitude-${report.id}"> ${report.longitude}</span><br>
            <strong>Classification:</strong> ${report.classification}<br>
            <strong>Reasons:</strong> ${report.reasons}<br>
            <strong>Comments:</strong> ${report.comments}<br>
            ${report.photoUrl ? `<img src="${report.photoUrl}" alt="Photo of dropped kerb" style="max-width: 100%; height: auto;">` : ''}
            <br>
            <a href="/reports/${report.id}/edit/" class="btn btn-primary btn-sm" style="margin-top: 10px;">Edit</a>
        `))
            .addTo(DKM.map);

         // Add an event listener to capture the new position when the marker is dragged
        marker.on('dragend', () => {
            const newLngLat = marker.getLngLat();
            document.getElementById(`latitude-${report.id}`).textContent = newLngLat.lat.toFixed(6);
            document.getElementById(`longitude-${report.id}`).textContent = newLngLat.lng.toFixed(6);
            // Send the updated latitude and longitude to the server
            updateReportLocation(report.id, newLngLat.lat, newLngLat.lng);
        });   
    });
}


// Function to send the updated location to the server
function updateReportLocation(reportId, latitude, longitude) {
    fetch(`/reports/${reportId}/update-location/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken() // Ensure you include the CSRF token for security
        },
        body: JSON.stringify({ latitude, longitude })
    })
        .then(response => {
            if (response.ok) {
                alert('Location updated successfully!');
            } else {
                alert('Failed to update location. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error updating location:', error);
            alert('An error occurred while updating the location.');
        });
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