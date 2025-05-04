/**
* Toggles the visibility of the reasons field based on the condition selected.
* If the condition is 'red' or 'orange', the reasons field is shown.
* Otherwise, it is hidden and any selected reasons are cleared.
*/
export default function toggleReasonsFieldVisibility() {
    // get the reasons elements
    const reasonsContainer = document.getElementById('reasons-container');
    // get selected condition from dropdown
    const selectedCondition = condition.value;

    if (selectedCondition && (selectedCondition === 'red' || selectedCondition === 'orange')) {
        // Show the reasons div if condition is red or orange
        reasonsContainer.classList.remove('hidden');

    } else {
        // Hide the reasons div if condition is not red or orange
        reasonsContainer.classList.add('hidden');
        // remove items from Choices field if the condition is not red or orange
        DKM.reasonsChoices.removeActiveItems(); // Clear any user selected items
    }
}