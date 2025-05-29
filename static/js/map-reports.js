import initialiseMap from './initialise-map.js';
import initialiseGoogleStreetView from './initialise-google-streetview.js';
import recreateCopyrightAttribution from './recreate-copyright-attribution.js';
import initialiseReasonsChoices from './initialise-reasons-choices.js';
import loadUKBoundary from './load-uk-boundary.js';
import updateAttributionControl from './update-attribution-control.js';
import toggleMapType from './toggle-map-type.js';
import toggleNewReportMode from './toggle-new-report-mode.js';
import toggleSearchBar from './toggle-search-bar.js';
import handleConditionSelectionChange from "./handle-condition-selection-change.js";
import addExistingReportsToMap from './add-existing-reports-to-map.js';
import removeCrispyClassesFromForm from "./remove-crispy-classes-from-form.js";
import validateNewReportForm from "./validate-new-report-form.js";
import searchLocation from "./search-location.js";
import processSuccessfulReportSubmission from "./process-successful-report-submission.js";
import processSuccessfulReportUpdate from "./process-successful-report-update.js";
import removeAllMessages from "./remove-all-messages.js";

document.addEventListener('DOMContentLoaded', () => { 
    
    // Create DKM (Dropped Kerb Mapper) global namespace to store global variables
    window.DKM = window.DKM || {}; // || {} ensures that if the namespace already exists, it won't be overwritten
    DKM.newMarker = null; // Initialise new map marker for the clicked location on adding a new report
    DKM.ukBoundary = null; // Initialise UK boundary variable
    DKM.markers = []; // Initialise markers array to store all markers on the map
    
    // create the map with OS tiles and set the view to the UK
    initialiseMap();

    // Google streetview
    initialiseGoogleStreetView();

    // Disable double-click zoom on the map
    DKM.map.doubleClickZoom.disable();

    // Load the UK boundary coordinates (GeoJSON)
    loadUKBoundary(); 

    // Add existing reports to the map. 
    // If not superuser, only add users reports, otherwise add all reports
    addExistingReportsToMap();

    // Map controls: Add event listeners

    // Search location button (magnifying glass icon)
    const searchSubmitBtn = document.getElementById("text-search-submit");
    searchSubmitBtn.addEventListener('click', searchLocation);
 
    // Map type button - toggles between Google Satellite and OS Map layer
    const toggleSatelliteBtn = document.getElementById("toggle-satellite");
    toggleSatelliteBtn.addEventListener('click', toggleMapType);
    
    // Add-report button - toggles 'new report mode'
    // When active button is orange, cursor is blue crosshair and click 
    // event listener selectNewReportLocation enabled on map
    const addReportButton = document.getElementById('add-report');
    addReportButton.addEventListener('click', () => {
        toggleNewReportMode(addReportButton);
    });
    
    // Toggle the visibility of the search bar when the reveal button is clicked
    const revealBtn = document.getElementById('text-search-reveal');
    revealBtn.addEventListener('click', toggleSearchBar);

    // New report form
    
    // Attach event listener to condition field dropdown
    const condition = document.getElementById('condition');
    condition.addEventListener('change', handleConditionSelectionChange);

    // Turn reasons field into a Choices.js multi‑select widget
    initialiseReasonsChoices();

    // Add event listener to the new report form submit button to valdate the form 
    // and disable buttons if valid
    const form = document.querySelector(".report-form");
    form.addEventListener('submit', e => {
            validateNewReportForm(e);
        }, { capture: true });
    // capture: true enables e.preventDefault() to block the submit before HTMX sees it.

    // remove selected crispy classes from the form
    removeCrispyClassesFromForm();

    // Responsive attribution control
    // Responsive to map tiles or tile source changes 
    DKM.map.on('styledata', recreateCopyrightAttribution);
    // Rresponsive to screen size
    window.addEventListener('resize', updateAttributionControl); 

    // Remove all messages after 5 seconds
    removeAllMessages();

    // Add event listener for any HTMX swap into a report container
    document.body.addEventListener('htmx:afterSwap', e => {
        // If the swap is into the update-report-container
        if (e.target.id === 'updated-report-container') {
            processSuccessfulReportUpdate();
        }
        // If the swap is into the new-reportcontainer, remove all messages after 5 seconds
        if (e.target.id === 'new-report-container') {
            processSuccessfulReportSubmission();
        }
        removeAllMessages();
    });
});