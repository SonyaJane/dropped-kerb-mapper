/**
* Sends an HTMX POST to the Django endpoint to update a report's latitude
* and longitude on the server.
* - Targets the #updated-report-container for swapping the server's response.
* - Uses swap: "beforeend" to append any returned partial.
* - Includes the CSRF token header via getCSRFToken()
*/
export default function updateReportLocation(reportId, lat, lng) {
            
    // Send the updated latitude and longitude to the server
    htmx.ajax('POST',
        `/reports/${reportId}/update-location/`,
        {
            target: "#updated-report-container",
            swap: "beforeend",
            headers: { 'X-CSRFToken': getCSRFToken() },
            values: { latitude: lat, longitude: lng }
        }
    );
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