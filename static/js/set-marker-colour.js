export default function setMarkerColour(marker, colour) {
    // If colour is none, set it to blue
    switch (colour) {
        case "none":
            colour = "SteelBlue";
            break;
        case "red":
            colour = "#c9352a";
            break;
        case "orange":
            colour = "#bd612c";
            break;
        case "green":
            colour = "#637052";
            break;
        case "white":
            colour = "#FFFFFF";
            break;
    }

    // change the colour of the marker to the condition value
    let svg = marker.getElementsByTagName("svg")[0];
    let path = svg.getElementsByTagName("path")[0];
    path.setAttribute("fill", colour);

    if (colour === "#FFFFFF") {
        // make the outline black
        path.setAttribute("stroke", "#000000"); // Set stroke to black for white marker
        // add a stroke to the 2nd circle
        path = svg.getElementsByTagName("circle")[1];
        path.setAttribute("stroke-width", "1px"); // Set stroke width for white marker
        path.setAttribute("stroke", "#000000"); // Set stroke to black for white marker
    }
}