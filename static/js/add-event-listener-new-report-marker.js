// This script listens for the htmx:afterSwap event and adds a marker to the map for the new report.
// It also hides the report form and shows a success message after the report is submitted.
document.addEventListener('htmx:afterSwap', (e) => {
    // get the new report data
    const reportData = document.getElementById('report-data');
    const report = JSON.parse(reportData.textContent);
    addMarkerForReport(report);
    // remove the report data from the DOM
    reportData.remove();
    // hide the report form div
    const reportFormDiv = document.querySelector('.map-report-form-container');
    if (reportFormDiv) {
        reportFormDiv.style.display = 'none';
    }
    // Show a success message
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.textContent = 'Report submitted successfully!';
    // Append the success message to the map container
    const mapContainer = document.getElementById('map');
    mapContainer.appendChild(successMessage);

    // Automatically remove the success message after 3 seconds
    setTimeout(() => {
        successMessage.remove();
    }, 3000);
});
