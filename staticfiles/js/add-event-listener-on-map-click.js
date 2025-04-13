import handleMapClick from "./handle-map-click.js";

export default function addEventListenerOnMapClick() {

    // Add a click event listener to the map
    DKM.map.on('click', handleMapClick)
}