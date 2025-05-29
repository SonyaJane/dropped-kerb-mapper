import searchLocation from './search-location.js';

// This is the clear search handler which resets the search box and the icon
export default function clearSearchHandler() {
    // Clear the text in the input box
    document.getElementById("text-search-input").value = "";

    // Remove marker if it exists
    if (window.DKM.map.searchResultMarker) {
        window.DKM.map.searchResultMarker.remove();
        delete window.DKM.map.searchResultMarker;
    }
    // Remove polygon layer if it exists
    if (window.DKM.map.getLayer('place')) {
        window.DKM.map.removeLayer('place');
        window.DKM.map.removeSource('place');
    }
    
    // Reset the search submit button icon back to magnifying glass
    const searchSubmitIcon = document.querySelector('#text-search-submit i');
    searchSubmitIcon.classList.remove("bi-x");
    searchSubmitIcon.classList.add("bi-arrow-right");

    // remove the event listener for clearing search input
    const searchSubmitBtn = document.getElementById("text-search-submit");
    searchSubmitBtn.removeEventListener('click', clearSearchHandler);

    // Reattach the event listener for the search submit button
    searchSubmitBtn.addEventListener('click', searchLocation);

    // remove the search results div if it exists
    const existingResultsDiv = document.querySelector('#location-search-results');
    if (existingResultsDiv) {
        existingResultsDiv.remove();
    }   
}