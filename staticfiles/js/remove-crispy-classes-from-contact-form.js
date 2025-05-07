/** 
* Removes default crispy-forms CSS classes from the contact form elements 
* to allow custom styling:
*  - Strips .btn-primary from the submit button
*  - Strips .pt-0 from all .col-form-label elements
*  - Adds class="btn-container" to the submit button's parent div
*    so that the button will right-align in the form
*/
export default function removeCrispyClassesFromContactForm() {
    // Remove .btn-primary class from the submit button
     const submitButton = document.getElementById('contact-submit-btn');
     if (submitButton) {
         submitButton.classList.remove('btn-primary');
     }
     // remove pt-0 class from the form labels
     const formLabels = document.querySelectorAll('.col-form-label');
     formLabels.forEach(label => {
         label.classList.remove('pt-0');
     });
     // add class="btn-container" to the submit button's parent div
     const submitButtonParent = submitButton.parentElement;
        if (submitButtonParent) {
            submitButtonParent.classList.add('btn-container');
        }
}