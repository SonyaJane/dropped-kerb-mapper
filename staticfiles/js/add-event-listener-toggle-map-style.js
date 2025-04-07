export default function addEventListenerToggleMapStyle() {

    // Toggle between the Google Satellite and OS Map layer when the button is clicked

    document.getElementById("toggle-satellite").addEventListener("click", () => {

        const toggleText = document.getElementById("toggle-text");
        const toggleIcon = document.getElementById("toggle-icon");
        const googleVisibility = DKM.map.getLayoutProperty("google-satellite-layer", "visibility");
        const mapContainer = document.getElementById("map");

        if (googleVisibility === "none") {
            // If currently showing the OS Map layer, switch to Google Satellite layer
            DKM.map.setLayoutProperty("os-layer", "visibility", "none");
            DKM.map.setLayoutProperty("google-satellite-layer", "visibility", "visible");
            mapContainer.classList.add("hide-os");
            toggleText.innerText = "Map View";
            toggleIcon.src = mapIconUrl;
            // Show the Google attribution elements.
            document.getElementById("google-logo").style.display = "block";
        } else {
            // If currently showing the Google Satellite layer, switch to OS Map layer
            DKM.map.setLayoutProperty("google-satellite-layer", "visibility", "none");
            DKM.map.setLayoutProperty("os-layer", "visibility", "visible");
            mapContainer.classList.remove("hide-os");
            toggleText.innerText = "Satellite View";
            toggleIcon.src = satelliteIconUrl;
            // Hide the Google attribution elements.
            document.getElementById("google-logo").style.display = "none";
        }
    });
}