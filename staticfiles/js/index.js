import initialiseReasonsChoices from './initialise-reasons-choices.js';
import initialiseMap from './initialise-map.js';
import addEventListenerOnStyledata from './add-event-listener-on-map-styledata.js';
import addEventListenerOnWindowResize from './add-event-listener-on-window-resize.js';
import addEventListenerToggleMapStyle from './add-event-listener-toggle-map-style.js';
import addEventListenerAddReportButton from './add-event-listener-add-report-button.js';
import addEventListenerClassificationField from "./add-event-listener-classification-field.js";
import addExistingReportsToMap from './add-existing-reports-to-map.js';

document.addEventListener('DOMContentLoaded', () => { 
    
    // Create DKM (Dropped Kerb Mapper) global namespace to store global variables
    window.DKM = window.DKM || {}; // || {} ensures that if the namespace already exists, it won't be overwritten
    DKM.newMarker = null; // Initialise new map marker for the clicked location on adding a new report

    initialiseMap();
    addEventListenerOnStyledata();
    addEventListenerOnWindowResize();
    addEventListenerToggleMapStyle();
    addEventListenerAddReportButton();
    addExistingReportsToMap();
    initialiseReasonsChoices();
    addEventListenerClassificationField(); 
    
});