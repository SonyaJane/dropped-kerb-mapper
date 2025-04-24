import searchLocationListener from './search-location.js';

export default function searchResultsEventListener(e) {
    
    // actions for when a search result is clicked

    // Remove the list of search results div
    document.querySelector('#location-search-results').remove();

    // remove any current geometry from the map
    if (window.DKM.map.getLayer('place')) {
        window.DKM.map.removeLayer('place');
        window.DKM.map.removeSource('place');
    }

    // add the chosen place name to the search box
    const placeName = e.currentTarget.innerText;
    document.getElementById("text-search-input").value = placeName;

    // Change the search submit button icon to a cross icon
    const searchSubmitBtn = document.getElementById("text-search-submit");
    const searchSubmitIcon = searchSubmitBtn.querySelector("i");
    searchSubmitIcon.classList.remove("bi-search");
    searchSubmitIcon.classList.add("bi-x");
    
    // remove the event listener from the search submit button
    searchSubmitBtn.removeEventListener('click', searchLocationListener);

    // Attach event listener for clearing search (if not already attached)
    searchSubmitBtn.addEventListener('click', clearSearchHandler);

    // if the geometry is a polygon or multi polygon, add it to the map
    if (e.currentTarget.dataset.geometry) {
        const geometry = JSON.parse(e.currentTarget.dataset.geometry);

        window.DKM.map.addSource('place', {
            'type': 'geojson',
            'data': {
                'type': 'Feature',
                'properties': {},
                'geometry': geometry
            }
        });
        window.DKM.map.addLayer({
            'id': 'place',
            'type': 'line',
            'source': 'place',
            'layout': {},
            "paint": {
                "line-color": "#bd582c",
                "line-width": 2
            }
        });

        // get bounds of the (multi)polygon
        let bounds;
        if (geometry.type === 'Polygon') {
            const coordinates = geometry.coordinates[0];
            bounds = coordinates.reduce((b, coord) => b.extend(coord), new maplibregl.LngLatBounds(coordinates[0], coordinates[0]));
        } else if (geometry.type === 'MultiPolygon') {
            // Initialize bounds with the first coordinate of the first polygon
            const firstPolygonCoords = geometry.coordinates[0][0];
            bounds = new maplibregl.LngLatBounds(firstPolygonCoords, firstPolygonCoords);
            // Loop through each polygon and extend the bounds for each coordinate
            geometry.coordinates.forEach(polygon => {
                polygon[0].forEach(coord => {
                    bounds.extend(coord);
                });
            });
        }
        window.DKM.map.fitBounds(bounds, {
            padding: 50,      // padding around the polygon
            animate: true     
        });
    }   else { // geometry is a point 
            // get the coordinates
            const coordinates = [e.currentTarget.dataset.longitude, e.currentTarget.dataset.latitude];
            // add marker to the map
            window.DKM.map.searchResultMarker = new maplibregl.Marker()
                .setLngLat(coordinates)
                .addTo(window.DKM.map);
            // set the map view to the marker
            window.DKM.map.flyTo({
                center: coordinates,
                zoom: 15
            });
        }
}

// This is the clear search handler which resets the search box and the icon
function clearSearchHandler() {
    // Clear the text in the input box
    document.getElementById("text-search-input").value = "";

    // Remove marker if it exists
    if (window.DKM.map.searchResultMarker) {
        window.DKM.map.searchResultMarker.remove();
        delete window.DKM.map.searchResultMarker;
    }
    // Remove polygon layer if it exists
    if (window.DKM.map.getLayer('place')) {
        window.DKM.map.removeLayer('place');
        window.DKM.map.removeSource('place');
    }
    
    // Reset the search submit button icon back to magnifying glass
    const searchSubmitIcon = document.querySelector('#text-search-submit i');
    searchSubmitIcon.classList.remove("bi-x-circle");
    searchSubmitIcon.classList.add("bi-search");

    // Reattach the event listener for the search submit button
    const searchSubmitBtn = document.getElementById("text-search-submit");
    searchSubmitBtn.addEventListener('click', addSearchLocationListener);

    // remove the search results div if it exists
    const existingResultsDiv = document.querySelector('#location-search-results');
    if (existingResultsDiv) {
        existingResultsDiv.remove();
    }   
}