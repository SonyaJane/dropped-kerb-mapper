/**
* Turn reasons field into a Choices.js multi‑select widget and 
* store the instance on the global DKM namespace as reasonsChoices.
* - Enables removal of selected options via an "×" button. 
* - Uses a placeholder text "click to show options".
* - Sorts the items alphabetically.
* - Hides the default item select text.
*/
export default function initialiseReasonsChoices() {
    window.DKM = window.DKM || {}; // || {} ensures that if the namespace already exists, it won't be overwritten

    // Initialise Choices on the multi-select field with ID "id_reasons"
    const reasonsSelect = document.getElementById("reasons");
    if (reasonsSelect) {
        DKM.reasonsChoices = new Choices(reasonsSelect, {
            searchEnabled: false, // Disable search functionality as keyboard gets in the way
            searchChoices: false, 
            removeItemButton: true, // Allows removal of selected options via an "x"
            placeholderValue: 'click to show options',
            shouldSort: true,
            itemSelectText: ""
        });
    }
}