export default function initialiseReasonsChoices() {
    window.DKM = window.DKM || {}; // || {} ensures that if the namespace already exists, it won't be overwritten

    // Initialise Choices on the multi-select field with ID "id_reasons"
    const reasonsSelect = document.getElementById("reasons");
    if (reasonsSelect) {
        DKM.reasonsChoices = new Choices(reasonsSelect, {
            removeItemButton: true, // Allows removal of selected options via an "x"
            placeholderValue: 'click to show options',
            shouldSort: true,
            itemSelectText: ""
        });
    }
}