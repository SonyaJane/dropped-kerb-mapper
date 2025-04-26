export default function addEventListenerReportSubmitButton() {
    
    const form = document.getElementById("map-report-form");
    // get report submit button
    const submitBtn = document.getElementById("report-submit-btn");
    // get report cancel button
    const cancelBtn = document.getElementById("report-cancel-btn");
    if (form && submitBtn) {
        form.addEventListener("submit", function(e) {
            // If the form validates.. 
            if (form.checkValidity()) {
                // Disable the submit button to prevent multiple submissions
                submitBtn.disabled = true;
                submitBtn.value = "Submitting...";
                // Disable the cancel button to prevent it from being clicked while the form is submitting.                
                cancelBtn.disabled = true;
            }
        });
    }
};