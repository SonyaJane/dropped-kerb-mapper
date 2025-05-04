import addMarkerForReport from "./add-marker-for-report.js";
/**
* Gets the embedded reports data (JSON)
* parses it into an array of report objects, and calls
* addMarkerForReport(report) for each to place them on the map.
* Finally removes the embedded from the DOM to clean up.
*/
export default function addExistingReportsToMap() {
    // Retrieve the reports data from the embedded JSON script
    const reportsData = document.getElementById('reports-data');
    const reports = JSON.parse(reportsData.textContent);
    // Add markers for each report
    reports.forEach(report => {
        addMarkerForReport(report); // Add marker for each report
    });

    // remove the reports data from the DOM
    reportsData.remove();
}