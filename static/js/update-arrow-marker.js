export default function updateArrowMarker() {
    console.log('Updating arrow marker');
    if (!DKM.isStreetViewVisible || !DKM.streetView) return;
    // Get the actual Street View position
    const position = DKM.streetView.getPosition();
    if (!position) return;
    const lat = position.lat();
    const lng = position.lng();
    const heading = DKM.streetView.getPov().heading;

    // Centre the map on the Street View position, allowing for the controls
    DKM.map.panTo([lng, lat],{
        padding: {top: 80, bottom:0, left:0, right:0}
    });
    
    // Create the marker at the actual panorama position if it doesn't exist
    if (!DKM.arrowMarker) {
        DKM.arrowEl = document.createElement('div');
        DKM.arrowEl.id = 'arrow-marker';
        DKM.arrowEl.innerHTML = `
            <svg id="arrow-svg" viewBox="0 0 32 32" width="32" height="32">
                <polygon points="16,4 28,28 16,22 4,28" fill="#2e85ff" stroke="#fff" stroke-width="2"/>
            </svg>
        `;
        DKM.arrowMarker = new maplibregl.Marker({
            element: DKM.arrowEl,
            anchor: 'center'
        }).setLngLat([lng, lat]).addTo(DKM.map);
    } else {
        DKM.arrowMarker.setLngLat([lng, lat]);
    }

    // Rotate the SVG, not the marker container
    const svg = DKM.arrowEl.querySelector('svg');
    if (svg) {
        svg.style.transform = `rotate(${heading}deg)`;
    }
}