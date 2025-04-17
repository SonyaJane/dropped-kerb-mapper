import initialiseReasonsChoices from './initialise-reasons-choices.js';
import initialiseMap from './initialise-map.js';
import loadBoundary from './load-uk-boundary.js';
import addEventListenerOnStyledata from './add-event-listener-on-map-styledata.js';
import addEventListenerOnWindowResize from './add-event-listener-on-window-resize.js';
import addEventListenerToggleMapStyle from './add-event-listener-toggle-map-style.js';
import addEventListenerAddReportButton from './add-event-listener-add-report-button.js';
import addEventListenerClassificationField from "./add-event-listener-classification-field.js";
import addExistingReportsToMap from './add-existing-reports-to-map.js';
import addEventListenerFormCloseButtons from "./add-event-listener-form-close-buttons.js";
import toggleReasonsFieldVisibility from "./toggle-reasons-field-visibility.js";
import removeCrispyClassesFromForm from "./remove-crispy-classes-from-form.js";

document.addEventListener('DOMContentLoaded', () => { 
    
    // Create DKM (Dropped Kerb Mapper) global namespace to store global variables
    window.DKM = window.DKM || {}; // || {} ensures that if the namespace already exists, it won't be overwritten
    DKM.newMarker = null; // Initialise new map marker for the clicked location on adding a new report
    DKM.ukBoundary = null; // Initialise UK boundary variable

    initialiseMap();
    addEventListenerOnStyledata();
    loadBoundary();
    addEventListenerOnWindowResize();
    addEventListenerToggleMapStyle();
    addEventListenerAddReportButton();
    initialiseReasonsChoices();
    addEventListenerClassificationField(); 
    addExistingReportsToMap();
    // Call the function once to set the initial state
    toggleReasonsFieldVisibility();
    // Add event listener to the close buttons on the form
    const formContainer = document.querySelector('.map-report-form-container');
    addEventListenerFormCloseButtons(formContainer); 
    // remove selected crispy classes from the form
    removeCrispyClassesFromForm()
});