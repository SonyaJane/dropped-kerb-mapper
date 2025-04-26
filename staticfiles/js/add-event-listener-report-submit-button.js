export default function addEventListenerReportSubmitButton() {
    // reset the form when submit is clicked
    // get the form element
    const form = document.getElementById("map-report-form");
    form.addEventListener("submit", function(e) {
        // If the form validates.. 
        if (form.checkValidity()) {
            // Disable the submit button to prevent multiple submissions
            // get report submit button
            const submitBtn = document.getElementById("report-submit-btn");
            submitBtn.disabled = true;
            submitBtn.value = "Submitting...";
            // Disable the cancel button to prevent it from being clicked while the form is submitting.                
            const cancelBtn = document.getElementById("report-cancel-btn");
            cancelBtn.disabled = true;
            // add a css class to the submit button to indicate that it is disabled
            submitBtn.classList.add("button-disabled");
            // add a css class to the cancel button to indicate that it is disabled
            cancelBtn.classList.add("button-disabled");
        }
    });
};