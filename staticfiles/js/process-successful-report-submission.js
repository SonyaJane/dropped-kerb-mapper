import addMarkerForReport from './add-marker-for-report.js';
import resetForm from './reset-form.js';
/**
 * Processes the response after a successful report submission via HTMX:
 *  - Reads the new embedded report data from the DOM
 *  - Parses the JSON into a report object
 *  - Adds a marker for the new report on the map using addMarkerForReport()
 *  - Removes the JSON <script> element from the DOM
 *  - Hides the map report form container
 *  - Resets the form inputs to their default state
 */
export default function processSuccessfulReportSubmission() {
    // get the new report data from the embedded JSON in the DOM
    const reportData = document.getElementById('report-data');
    // Parse the JSON data
    const report = JSON.parse(reportData.textContent);
    // Add map marker for the new report, create popup content, and set up interactions
    addMarkerForReport(report);
    
    // remove the report data from the DOM
    reportData.remove();
    
    // hide the report form div
    document.getElementById('map-report-form-container').classList.add('hidden');

    // reset the form
    resetForm();

    // exit new report mode if it is active
    const addReportButton = document.getElementById('add-report');
    toggleNewReportMode(addReportButton);
}