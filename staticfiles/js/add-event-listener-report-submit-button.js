export default function addEventListenerReportSubmitButton() {
    
    const form = document.getElementById("map-report-form");
    const submitBtn = document.getElementById("report-submit-btn");
    if (form && submitBtn) {
        form.addEventListener("submit", function(e) {
            // If the form validates, disable the submit button to prevent multiple submissions.
            if (form.checkValidity()) {
                console.log("Form is valid. Submitting...");
                submitBtn.disabled = true;
                submitBtn.value = "Submitting...";
            }
        });
    }
};