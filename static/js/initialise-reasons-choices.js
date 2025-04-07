export default function initialiseReasonsChoices() {

    // Initialise Choices on the multi-select field with ID "id_reasons"
    const reasonsSelect = document.getElementById("reasons");
    if (reasonsSelect) {
        DKM.reasonsChoices = new Choices(reasonsSelect, {
            removeItemButton: true, // Allows removal of selected options via an "x"
            placeholderValue: "Add reasons for classification",
            shouldSort: true
        });
    }
}