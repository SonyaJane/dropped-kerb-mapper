/**
* Maplibre GL and Ordnance Survey or Google Maps attribution is in the bottom right corner of the map.
* On small screens the attribution control is set to compact mode (closed) which a small icon.
* On screens > 550px the attribution control is set to open mode (expanded) which shows the full attribution text.
*/
export default function updateAttributionControl() {
    const screenWidth = window.innerWidth;
    const attributionElement = document.querySelector('.maplibregl-ctrl-attrib');
    if (screenWidth < 550) {
        attributionElement.classList.remove('maplibregl-compact-show');
        attributionElement.removeAttribute('open');
    } else {
        attributionElement.classList.add('maplibregl-compact-show');
        attributionElement.setAttribute('open', '');
    }
}