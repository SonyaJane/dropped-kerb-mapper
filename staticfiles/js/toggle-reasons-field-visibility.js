export default function toggleReasonsFieldVisibility() {

    // toggle the visibility of the reasons field based on the condition selected

    // get the reasons elements
    const reasonsField = document.getElementById('div_id_reasons');
    const reasonsLabel = document.getElementById('reasons-label');

    // get selected condition from dropdown
    const selectedCondition = condition.value;

    if (selectedCondition && (selectedCondition === 'red' || selectedCondition === 'orange')) {
        // Show the reasons div if condition is red or orange
        reasonsLabel.style.display = 'block';
        reasonsField.style.display = 'block';

    } else {
        // Hide the reasons div if condition is not red or orange
        reasonsLabel.style.display = 'none';
        reasonsField.style.display = 'none';
        // remove items from Choices field if the condition is not red or orange
        DKM.reasonsChoices.removeActiveItems(); // Clear any user selected items
    }

}