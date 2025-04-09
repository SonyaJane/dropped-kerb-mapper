export default function addExistingReportsToMap() {
    // Retrieve the reports data from the embedded JSON script
    const reports = JSON.parse(document.getElementById('reports-data').textContent);
    // Add markers for each report
    reports.forEach(report => {
        new maplibregl.Marker({
            color: report.classification // Set the marker colour
        })
            .setLngLat([report.longitude, report.latitude]) // Set marker position
            .setPopup(new maplibregl.Popup().setHTML(`
            <strong>Report ID:</strong> ${report.id}<br>
            <strong>Classification:</strong> ${report.classification}<br>
            <strong>Reasons:</strong> ${report.reasons}<br>
            <strong>Comments:</strong> ${report.comments}
        `)) // Add a popup with report details
            .addTo(DKM.map);
    });
}