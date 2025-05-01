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
            colour = "#F8F8FF";
            break;
    }

    // change the colour of the marker to the condition value
    let svg = marker.getElementsByTagName("svg")[0];
    let path = svg.getElementsByTagName("path")[0];
    path.setAttribute("fill", colour);

    if (colour === "#F8F8FF") {
        // add a stroke to the 2nd circle
        path = svg.getElementsByTagName("circle")[1];
        path.setAttribute("stroke-width", "1px"); // Set stroke width for white marker
        path.setAttribute("stroke", "#AAAAAA"); // Set stroke to grey for white marker
    }
}