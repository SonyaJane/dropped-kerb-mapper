export default function addEventListenerReportSubmitButton() {
    // reset the form when submit is clicked
    // get the form element
    const form = document.getElementById("map-report-form");

    form.addEventListener("submit", e => {
        const condition = document.getElementById('condition');
        const reasons = document.querySelector('.choices__list');
        let nReasons = 0;
        if (reasons) {
            console.log(reasons.childElementCount);
            nReasons = reasons.childElementCount;
        }
        // clear any prior inline error next to condition
        const existingError = condition.parentElement.querySelector('.text-danger.inline-error');
        if (existingError) existingError.remove();

        // only validate if condition is red or orange
        if (['red','orange'].includes(condition.value) && nReasons === 0) {
            e.preventDefault();

            // build the error element
            const msg = document.createElement('div');
            msg.className = 'text-danger inline-error';
            msg.textContent = 'Please select at least one reason when condition is red or orange.';

            // insert it immediately after the condition's parent wrapper
            const wrapper = condition.parentElement;
            wrapper.insertAdjacentElement('afterend', msg);

            // scroll into view
            msg.scrollIntoView({ behavior: 'smooth' });
            return;
        }

        // If validation passed
        // Disable the submit button to prevent multiple submissions
        const submitBtn = document.getElementById("report-submit-btn");
        submitBtn.disabled = true;
        submitBtn.value = "Submitting...";
        // Disable the cancel button to prevent it from being clicked while the form is submitting.                
        const cancelBtn = document.getElementById("report-cancel-btn");
        cancelBtn.disabled = true;
        // add a css class to the submit button to indicate that it is disabled
        submitBtn.classList.add("button-disabled");
        // add a css class to the cancel button to indicate that it is disabled
        cancelBtn.classList.add("button-disabled");
    });
}