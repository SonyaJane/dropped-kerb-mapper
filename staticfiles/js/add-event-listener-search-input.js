export default function addEventListenerTextSearchInput() {
    document.getElementById('text-search-input').addEventListener('input', function() {
        const searchSubmitIcon = document.querySelector('#text-search-submit i');
        if (this.value.trim().length > 0) {
            searchSubmitIcon.classList.remove("bi-search");
            searchSubmitIcon.classList.add("bi-x");
            // Add event listener for clearing search
            const searchSubmitBtn = document.getElementById("text-search-submit");
            searchSubmitBtn.addEventListener('click', clearSearchHandler, { once: true });
        } else {
            searchSubmitIcon.classList.remove("bi-x");
            searchSubmitIcon.classList.add("bi-search");
            // Remove the event listener for clearing search if the input is empty
            const searchSubmitBtn = document.getElementById("text-search-submit");
            searchSubmitBtn.removeEventListener('click', clearSearchHandler);
        }
    });
}

function clearSearchHandler() {
    // Clear the text in the input box
    const searchInput = document.getElementById("text-search-input");
    searchInput.value = "";

    // Remove the search results div if it exists
    const resultsDiv = document.querySelector("#location-search-results");
    if (resultsDiv) {
        resultsDiv.remove();
    }

    // Remove any polygon layer (with source 'place') if it exists
    if (window.DKM.map.getLayer('place')) {
        window.DKM.map.removeLayer('place');
        window.DKM.map.removeSource('place');
    }
    // Remove any marker (for point search results) if it exists
    if (window.DKM.map.searchResultMarker) {
        window.DKM.map.searchResultMarker.remove();
        delete window.DKM.map.searchResultMarker;
    }

    // Reset the search submit button icon back to a magnifying glass
    const searchSubmitIcon = document.querySelector("#text-search-submit i");
    if (searchSubmitIcon) {
        searchSubmitIcon.classList.remove("bi-x-circle");
        searchSubmitIcon.classList.add("bi-search");
    }
}