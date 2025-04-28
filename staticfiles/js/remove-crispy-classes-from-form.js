export default function removeCrispyClassesFromForm() {
   // Remove .btn-primary class from the submit button
    const submitButton = document.getElementById('report-submit-btn');
    if (submitButton) {
        submitButton.classList.remove('btn-primary');
    }
    // remove pt-0 class from the form labels
    const formLabels = document.querySelectorAll('.col-form-label');
    formLabels.forEach(label => {
        label.classList.remove('pt-0');
    });

    // remove row classes from the fields
    document.getElementById('div_id_latitude').classList.remove('row');  
    document.getElementById('div_id_longitude').classList.remove('row');
    document.getElementById('div_id_condition').classList.remove('row'); 
    document.getElementById('div_id_comments').classList.remove('row'); 
    document.getElementById('div_id_photo').classList.remove('row');
}