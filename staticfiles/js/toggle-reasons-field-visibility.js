export default function toggleReasonsFieldVisibility() {

    // toggle the visibility of the reasons field based on the classification selected

    // get the classification dropdown element
    const reasonsDiv = document.getElementById('div_id_reasons');

    // get selected classification from dropdown
    const selectedClassification = classification.value;

    if (selectedClassification && (selectedClassification === 'red' || selectedClassification === 'orange')) {
        // Show the reasons div if classification is red or orange
        reasonsDiv.style.display = 'block';
    } else {
        // Hide the reasons div if classification is not red or orange
        reasonsDiv.style.display = 'none';
        // remove items from Choices field if the classification is not red or orange
        DKM.reasonsChoices.removeActiveItems(); // Clear any user selected items
    }

}