/**
 * Display a Nominatim location search error message below the search input field.
 */
export default function displayLocationSearchError() {
    // if a results div already exists, remove it
    const existingResultsDiv = document.querySelector('#location-search-results');
    if (existingResultsDiv) {
        existingResultsDiv.remove();
    }

    // create a new div with id #location-search-results
    const resultsDiv = document.createElement('div');
    resultsDiv.id = 'location-search-results';
    resultsDiv.innerText = "An error has occurred during the location search. Please try again.";
    resultsDiv.classList.add('mt-2', 'text-danger', 'text-center');
}