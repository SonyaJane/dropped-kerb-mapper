export default function setMarkerColour(colour) {
    // change the colour of the marker to the classification value
    let element = DKM.newMarker.getElement();
    let svg = element.getElementsByTagName("svg")[0];
    let path = svg.getElementsByTagName("path")[0];
    path.setAttribute("fill", colour);
}