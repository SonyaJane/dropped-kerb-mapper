import addMarkerForReport from "./add-marker-for-report.js";   

export default function addExistingReportsToMap() {
    // Disable double-click zoom on the map
    DKM.map.doubleClickZoom.disable();

    // Retrieve the reports data from the embedded JSON script
    const reports = JSON.parse(document.getElementById('reports-data').textContent);
    // Add markers for each report
    reports.forEach(report => {
        addMarkerForReport(report); // Add marker for each report
    });
}