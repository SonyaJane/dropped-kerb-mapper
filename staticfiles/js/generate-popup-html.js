/**
 * Constructs an HTML snippet for a MapLibre marker popup based on a report object.
 * - Shows report number (uses `id` or `user_report_number` for non-superusers).
 * - Includes view/edit links for the report.
 * - Displays latitude, longitude, place name, and county.
 * - Conditionally includes reasons and comments for red/orange conditions.
 * - Conditionally embeds the report photo if `photoUrl` is provided.
 *
 *   Returns an HTML string suitable for use in a MapLibre GL Popup.
 */
export default function generatePopupHTML(report) {
    // If the user who created the report is a superuser, show the report id.
    // Otherwise, show the user_report_number.
    const reportNumber = (report.user && report.user_is_superuser) ? report.id : report.user_report_number;
    // Only include the reasons line if condition is red or orange.
    let reasons = '';
    if ((report.condition === 'red' || report.condition === 'orange')) {
        reasons = `<p><span class="orange-font">${report.reasons}</span></p>`;
    }
    // Only include the comments line if there are comments.
    let comments = '';
    if (report.comments) {
        comments = `<p><span class="orange-font">${report.comments}</span></p>`;
    }
    return `
        <p>
            <span>Report ${reportNumber}</span>
            <span>&nbsp;</span>
            <a href="/reports/${report.id}/" class="custom-link">view</a>
            <span>&nbsp;</span>
            <a href="/reports/${report.id}/edit/" class="custom-link">edit</a>
        </p>
        <p>
            <span id="latitude-${report.id}"> ${report.latitude}, </span>
            <span id="longitude-${report.id}"> ${report.longitude}</span>
        </p>
        <p><span id="place_name-${report.id}"> ${report.place_name || 'Unknown'}</span></p>
        <p><span id="county-${report.id}"> ${report.county}</span></p>
        <p>${report.reasons}</p>
        <p>${report.comments}</p>
        ${report.photoUrl ? `<img src="${report.photoUrl}" alt="Photo of dropped kerb" class="popup-photo">` : ''}
    `;
}