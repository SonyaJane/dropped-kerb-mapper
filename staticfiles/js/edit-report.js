import removeCrispyClassesFromForm from "./remove-crispy-classes-from-form.js";
import initialiseReasonsChoices from "./initialise-reasons-choices.js";
import addEventListenerConditionField from "./add-event-listener-condition-field.js";
import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";
import addEventListenerReportSubmitButton from "./add-event-listener-report-submit-button.js";

document.addEventListener('DOMContentLoaded', () => { 

    removeCrispyClassesFromForm()
    initialiseReasonsChoices()
    addEventListenerConditionField()
    toggleReasonsFieldVisibility()
    addEventListenerReportSubmitButton()

});