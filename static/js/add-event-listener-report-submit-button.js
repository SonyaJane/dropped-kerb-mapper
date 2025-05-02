export default function addEventListenerReportSubmitButton() {
    // reset the form when submit is clicked
    // get the form element
    const form = document.querySelector(".report-form");

    form.addEventListener("submit", e => {
        const condition = document.getElementById('condition');
        const reasons = document.querySelector('.choices__list');
        const comments = document.getElementById('id_comments');
        // get the value of the comments element
        const commentsValue = comments.value.trim();

        let nReasons = 0;
        if (reasons) {
            nReasons = reasons.childElementCount;
        }
        // clear any prior inline error next to condition
        const existingError = document.querySelector('.text-danger.inline-error');
        if (existingError) existingError.remove();

        // validate if condition is red, orange, or white (drpped kerb needed but not present)
        if (['red','orange'].includes(condition.value) && nReasons === 0) {
            // prevent HTMX from seeing this submit
            e.preventDefault();
            e.stopImmediatePropagation();

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

        if (condition.value === 'white' && commentsValue.length === 0) {
            // prevent HTMX from seeing this submit
            e.preventDefault();
            e.stopImmediatePropagation();

            // build the error element
            const msg = document.createElement('div');
            msg.className = 'text-danger inline-error';
            msg.textContent = 'Please provide comments when condition is white.';

            // insert it immediately after the condition's parent wrapper
            const wrapper = condition.parentElement;
            wrapper.insertAdjacentElement('afterend', msg);

            // scroll into view
            msg.scrollIntoView({ behavior: 'smooth' });
            return;
        }

        // If validation passed
        // Disable the submit button to prevent multiple submissions
        const submitBtn = document.querySelector(".report-submit-btn");
        submitBtn.disabled = true;
        submitBtn.value = "Submitting...";
        // Disable the cancel button to prevent it from being clicked while the form is submitting.                
        const cancelBtn = document.querySelector(".report-cancel-btn");
        cancelBtn.disabled = true;
        // add a css class to the submit button to indicate that it is disabled
        submitBtn.classList.add("button-disabled");
        // add a css class to the cancel button to indicate that it is disabled
        cancelBtn.classList.add("button-disabled");
    }, { capture: true });
}