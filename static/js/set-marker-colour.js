export default function setMarkerColour(marker, colour) {
    // If colour is none, set it to blue
    if (colour === "none") {
        colour = "blue";
    }
    // change the colour of the marker to the condition value
    let svg = marker.getElementsByTagName("svg")[0];
    let path = svg.getElementsByTagName("path")[0];
    path.setAttribute("fill", colour);
}