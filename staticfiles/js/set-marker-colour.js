export default function setMarkerColour(marker, colour) {
    // change the colour of the marker to the classification value
    let svg = marker.getElementsByTagName("svg")[0];
    let path = svg.getElementsByTagName("path")[0];
    path.setAttribute("fill", colour);
}