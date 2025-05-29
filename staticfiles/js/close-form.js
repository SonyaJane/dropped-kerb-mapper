import resetForm from './reset-form.js';

/**
 * Remove the marker and hide the form container when the close button is clicked. 
 * Also resets the form.
 */
export default function closeForm() {
    const formContainer = document.getElementById('map-report-form-container');
    if (DKM.newMarker) {
        DKM.newMarker.remove(); // Remove the marker if it exists
    }
    formContainer.classList.add('hidden'); // Hide the form container
    resetForm();                           // Reset the form
}