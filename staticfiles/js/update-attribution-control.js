// Compact mode for small screens
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