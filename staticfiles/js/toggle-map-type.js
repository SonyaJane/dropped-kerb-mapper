import selectNewReportLocation from "./select-new-report-location.js";
/**
* Toggles between the Google Satellite and OS Map layer when the satellite button is clicked
*/
export default function toggleMapType() {
    // get the map container element
    const mapContainer = document.getElementById("map");
    const toggleSatelliteBtn = document.getElementById("toggle-satellite");
    if (DKM.isSatelliteViewOn === false) {
        // If currently showing the OS Map layer, switch to Google Satellite layer
        DKM.map.setLayoutProperty("os-layer", "visibility", "none");
        DKM.map.setLayoutProperty("google-satellite-layer", "visibility", "visible");
        mapContainer.classList.add("hide-os");
        // Show the Google attribution elements.
        document.getElementById("google-logo").style.display = "block";
        toggleSatelliteBtn.classList.add('button-active');
        DKM.isSatelliteViewOn = true; // Update the state to indicate satellite view is on
        DKM.map.off('click', selectNewReportLocation); // Remove add report click event listener from the map
        // Hide all markers
        if (Array.isArray(DKM.markers)) {
            DKM.markers.forEach(marker => {
                marker.getElement().style.display = "none";
            });
        }
        // Disable new report form submit button

        document.querySelector(".report-submit-btn").disabled = true;
    } else {
        // If currently showing the Google Satellite layer, switch to OS Map layer
        DKM.map.setLayoutProperty("google-satellite-layer", "visibility", "none");
        DKM.map.setLayoutProperty("os-layer", "visibility", "visible");
        mapContainer.classList.remove("hide-os");
        // Hide the Google attribution elements.
        document.getElementById("google-logo").style.display = "none";
        toggleSatelliteBtn.classList.remove('button-active');
        DKM.isSatelliteViewOn = false; // Update the state to indicate satellite view is off
        // Add a click event listener to the map if add report mode is active
        if (document.getElementById('add-report').classList.contains('button-active')) {
            DKM.map.on('click', selectNewReportLocation);
        }
        DKM.map.on('click', selectNewReportLocation); 
        // Show all markers
        if (Array.isArray(DKM.markers)) {
            DKM.markers.forEach(marker => {
                marker.getElement().style.display = "";
            });
        }
        // Renable new report form submit button
        document.querySelector(".report-submit-btn").disabled = false;
    }
}