document.addEventListener('DOMContentLoaded', function () {
    // Get the classification input
    const classification = document.getElementById('classification');
    console.log('classification', classification);

    // Get the parent of the reasons div
    const reasonsDiv = document.getElementById('reasons').parentElement;
    console.log('reasonsDiv:', reasonsDiv);

    function toggleReasonsField() {
        console.log('toggleReasonsField called');
        // get selected classification from dropdown
        const selectedClassification = classification.value;
        console.log('selectedClassification:', selectedClassification);

        if (selectedClassification && (selectedClassification === 'red' || selectedClassification === 'orange')) {
            reasonsDiv.style.display = '';
            console.log('Reasons div should be visible');
        } else {
            reasonsDiv.style.display = 'none';
            console.log('Reasons div should be hidden');
            // Unselect all reasons in the dropdown
            // const reasons = document.querySelectorAll('input[name="reasons"]');
        }
    }

    // Attach event listener to classification dropdown
    classification.addEventListener('change', toggleReasonsField);

    // Initialise the reasons field visibility
    toggleReasonsField();
});