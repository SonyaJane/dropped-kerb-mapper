import removeCrispyClassesFromForm from "./remove-crispy-classes-from-form.js";
import initialiseReasonsChoices from "./initialise-reasons-choices.js";
import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";
import validateNewReportForm from "./validate-new-report-form.js";

document.addEventListener('DOMContentLoaded', () => { 

    removeCrispyClassesFromForm()
    initialiseReasonsChoices()
    // toggleReasonsFieldVisibility()
    // Attach event listener to condition field dropdown
    const condition = document.getElementById('condition');
    condition.addEventListener('change', toggleReasonsFieldVisibility);

    // Add event listener to the edit report form submit button to valdate the form 
    // and disable buttons if valid
    const form = document.querySelector(".report-form");
    form.addEventListener('submit', e => {
            validateNewReportForm(e)
        }, { capture: true });

});