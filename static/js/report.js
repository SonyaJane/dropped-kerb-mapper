document.addEventListener('DOMContentLoaded', function () {
    const classificationField = document.querySelectorAll('input[name="classification"]');
    // Get the reasons div
    const reasonsField = document.getElementById('div_id_reasons');
    function toggleReasonsField() {
        const selectedClassification = document.querySelector('input[name="classification"]:checked');
        if (selectedClassification && (selectedClassification.value === 'red' || selectedClassification.value === 'orange')) {
            reasonsField.style.display = '';
        } else {
            reasonsField.style.display = 'none';
            // Uncheck all reasons if hidden
            document.querySelectorAll('input[name="reasons"]').forEach(checkbox => checkbox.checked = false);
        }
    }

    // Attach event listeners to classification radio buttons
    classificationField.forEach(radio => {
        radio.addEventListener('change', toggleReasonsField);
    });

    // Initialise the reasons field visibility
    toggleReasonsField();
});