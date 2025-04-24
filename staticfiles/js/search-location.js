import searchLocationNominatim from './search-location-nominatim.js';
import displaySearchLocationResults from './display-search-location-results.js';
// import displayLocationSearchError from './display-location-search-error.js';

//  Add click event listener to button for "Search for place or address" text input
// (Magnifying glass icon)
export default function addSearchLocationListener() {
    document.getElementById("text-search-submit").addEventListener('click', async e => {

        const locationText = document.getElementById("text-search-input").value;
        // Regular expression to check if the input contains at least one word (letters)
        let wordPattern = /[a-zA-Z0-9]/;
        if (wordPattern.test(locationText)) {
            // 
            // Use the search input to query the Nominatim API
            const data = await searchLocationNominatim(locationText);
            if (data) {
                // Display the search results
                displaySearchLocationResults(data);
            } else {
                // If there is an error, display an error message in the modal
                // displayLocationSearchError();
            }
        } else {
            // If the input field is empty, add placeholder text in red
            // First remove any existing text
            document.getElementById("text-search-input").value = "";
            document.getElementById("text-search-input").placeholder = "Enter text to search";
            document.getElementById("text-search-input").classList.add("red-placeholder");
        }

    });

}