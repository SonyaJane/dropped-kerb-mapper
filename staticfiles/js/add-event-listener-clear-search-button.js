export default function addClearSearchButtonListener() {    
    // Attach event listener to the clear search icon
    document.getElementById("clear-search-btn").addEventListener('click', () => {
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
        // Optionally hide the clear search button again
        document.getElementById("clear-search-btn").style.display = "none";
    });
}