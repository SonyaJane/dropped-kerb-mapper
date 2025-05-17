/**
* Turn reasons field into a Choices.js multi‑select widget and 
* store the instance on the global DKM namespace as reasonsChoices.
* - Enables removal of selected options via an "×" button. 
* - Uses a placeholder text "click to show options".
* - Sorts the items alphabetically.
* - Hides the default item select text.
*/
export default function initialiseReasonsChoices() {
    window.DKM = window.DKM || {}; // || {} ensures that if the namespace already exists, it won't be overwritten

    // Initialise Choices on the multi-select field with ID "id_reasons"
    const reasonsSelect = document.getElementById("reasons");
    if (reasonsSelect) {
        DKM.reasonsChoices = new Choices(reasonsSelect, {
            removeItemButton: true, // Allows removal of selected options via an "x"
            shouldSort: true,
            itemSelectText: "",
            renderChoiceLimit: -1,
            searchFields: [],
            placeholder: true,
            placeholderValue: 'Click to show options',
            addItems: false,
            searchEnabled: false, // Disable search functionality as keyboard gets in the way
            searchChoices: false, 
        });

        

        // Add toggle open/close on click
        const choices = document.querySelector('.choices');
        // Add text to the button to open the dropdown
        const button = choices.querySelector('.choices__inner');
        // Add text to the button to open the dropdown
        const p = document.createElement('p');
        p.textContent = 'Click to show options';
        p.classList.add('mb-1');
        button.insertBefore(p, button.firstChild);

        choices.addEventListener('click', function (e) { 
            if (choices.classList.contains('is-open')) {
                DKM.reasonsChoices.hideDropdown();
                p.classList.remove('hidden');
            } else {
                DKM.reasonsChoices.showDropdown();
                // remove the text from the button to open the dropdown
                p.classList.add('hidden');
            }
        });
    }
}