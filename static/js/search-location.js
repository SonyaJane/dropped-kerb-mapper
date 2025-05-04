import searchLocationNominatim from './search-location-nominatim.js';
import displaySearchLocationResults from './display-search-location-results.js';
import displayLocationSearchError from './display-location-search-error.js';
/**
* Handles the Search location button click:
 *  - Reads the user's query from the #text-search-input field
 *  - Validates it contains at least one alphanumeric character
 *  - If valid, calls searchLocationNominatim() to fetch geocoding results
 *    and passes them to displaySearchLocationResults()
 *  - If the Nominatim API call fails or returns no results, calls
 *    displayLocationSearchError() to show an error message

 *  - If invalid or empty, clears the input, sets a red placeholder
 *    prompting for valid text, and highlights the field
 */
export default async function searchLocation() {

    const locationText = document.getElementById("text-search-input").value;
    // Regular expression to check if the input contains at least one word (letters)
    let wordPattern = /[a-zA-Z0-9]/;
    if (wordPattern.test(locationText)) {
        // Use the search input to query the Nominatim API
        const data = await searchLocationNominatim(locationText);
        if (data) {
            // Display the search results
            displaySearchLocationResults(data);
        } else {
            // If there is an error, display an error message in the modal
            displayLocationSearchError();
        }
    } else {
        // If the input field is empty, add placeholder text in red
        // First remove any existing text
        document.getElementById("text-search-input").value = "";
        document.getElementById("text-search-input").placeholder = "Enter text to search";
        document.getElementById("text-search-input").classList.add("red-placeholder");
    }
}