import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";
/**
 * Clears and resets all inputs in the report form to their defaults:
 *   - Empties the comments textarea
 *   - Clears the photo file input
 *   - Resets the condition select to "none"
 *   - Removes any inline validation error messages
 *   - Re‑enables and restores the submit button label to "Submit"
 */
export default function resetForm() {
    // Clear the comments input value
    const commentsInput = document.getElementById('id_comments');
    commentsInput.value = "";
    
    // clear the photo input value
    document.getElementById('id_photo').value = "";

    // set the condition to none 
    const conditionSelect = document.getElementById('condition');
    conditionSelect.value = "none";

    // Clear the selected reasons in the reasons field
    // and hide the reasons field
    toggleReasonsFieldVisibility()
    


    // clear any inline error next to condition
    const existingError = document.querySelector('.text-danger.inline-error');
    if (existingError) existingError.remove();

    //reenable the submit and cancel buttons
    const submitBtn = document.querySelector(".report-submit-btn");
    const cancelBtn = document.querySelector(".report-cancel-btn");

    submitBtn.disabled = false;
    submitBtn.value = "Submit";
    submitBtn.classList.remove("button-disabled");

    cancelBtn.disabled = false;
    cancelBtn.classList.remove("button-disabled");

}