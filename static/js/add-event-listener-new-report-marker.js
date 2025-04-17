document.addEventListener('htmx:afterSwap', (e) => {
    const response = e.detail.xhr.response;
    try {
        const data = JSON.parse(response);
        if (data.success) {
            const reportId = data.report_id;
            console.log(`Report ID: ${reportId}`);
            // Fetch the full report data from the report_detail endpoint
            fetch(`/reports/${reportId}/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Mark this as an AJAX request
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to fetch report data.');
                    }
                    return response.json();
                })
                .then(report => {
                    console.log('Fetched report data:', report); // Log the resolved JSON

                    // Add the marker to the map
                    addMarkerForReport(report);
                    // hide the report form div
                    const reportFormDiv = document.querySelector('.map-report-form-container');
                    if (reportFormDiv) {
                        reportFormDiv.style.display = 'none';
                    }
                    // Show a success message
                    const successMessage = document.createElement('div');
                    successMessage.className = 'success-message';
                    successMessage.textContent = 'Report submitted successfully!';
                    document.body.appendChild(successMessage);

                    // Automatically remove the success message after 3 seconds
                    setTimeout(() => {
                        successMessage.remove();
                    }, 3000);
                })
                .catch(error => {
                    console.error('Error fetching report data:', error);
                });
        } else {
            console.error('Form submission failed:', data.errors);
        }
    } catch (error) {
        console.error('Error processing HTMX response:', error);
    }
});