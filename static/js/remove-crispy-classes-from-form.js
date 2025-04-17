export default function removeCrispyClassesFromForm() {
   // Remove .btn-primary class from the submit button
    const submitButton = document.getElementById('submit-btn');
    if (submitButton) {
        submitButton.classList.remove('btn-primary');
    }
    // remove pt-0 class from the form labels
    const formLabels = document.querySelectorAll('.col-form-label');
    formLabels.forEach(label => {
        label.classList.remove('pt-0');
    });
}