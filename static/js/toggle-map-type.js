/**
* Toggles between the Google Satellite and OS Map layer when the satellite button is clicked
*/
export default function toggleMapType() {
    // Get visibility of the Google Satellite layer
    const googleVisibility = DKM.map.getLayoutProperty("google-satellite-layer", "visibility");
    // get the map container element
    const mapContainer = document.getElementById("map");
    const toggleSatelliteBtn = document.getElementById("toggle-satellite");

    if (googleVisibility === "none") {
        // If currently showing the OS Map layer, switch to Google Satellite layer
        DKM.map.setLayoutProperty("os-layer", "visibility", "none");
        DKM.map.setLayoutProperty("google-satellite-layer", "visibility", "visible");
        mapContainer.classList.add("hide-os");
        // Show the Google attribution elements.
        document.getElementById("google-logo").style.display = "block";
        toggleSatelliteBtn.classList.add('button-active');
    } else {
        // If currently showing the Google Satellite layer, switch to OS Map layer
        DKM.map.setLayoutProperty("google-satellite-layer", "visibility", "none");
        DKM.map.setLayoutProperty("os-layer", "visibility", "visible");
        mapContainer.classList.remove("hide-os");
        // Hide the Google attribution elements.
        document.getElementById("google-logo").style.display = "none";
        toggleSatelliteBtn.classList.remove('button-active');
    }
}