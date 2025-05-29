import searchLocation from './search-location.js';
import clearSearchHandler from './clear-search-handler.js';

/**
 * Invoked when a user clicks on one of the Nominatim search results.
 * - Removes the #location-search-results div containing the results.
 * - Clears any existing results polygon layer or point marker from the map.
 * - Populates the search input (#text-search-input) with the selected place name.
 * - Toggles the search button icon from a magnifying glass to a clear ×.
 * - Swaps the click handler on the search button from searchLocation() to clearSearchHandler().
 * - If the result has GeoJSON geometry (Polygon or MultiPolygon):
 *     • Adds it as a new source/layer on the map.
 *     • Fits the map view to the geometry’s bounds with padding.
 *   Otherwise (point result):
 *     • Creates a new marker at the result’s coordinates.
 *     • Centers and zooms the map to that marker.
 */
export default function handleLocationSelect(e) {
    
    // actions for when a Nominatim location search result is clicked

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
    searchSubmitBtn.removeEventListener('click', searchLocation);

    // Attach event listener for clearing search input
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
            
            // create a custom marker element with marker.png
            const markerEl = document.createElement('div');
            markerEl.className = 'custom-marker';
            markerEl.style.backgroundImage = "url('/static/images/marker.png')";
            markerEl.style.backgroundRepeat = 'no-repeat';
            markerEl.style.width = '32px';
            markerEl.style.height = '48px';
            markerEl.style.backgroundSize = '100%';

            window.DKM.map.searchResultMarker = new maplibregl.Marker({ element: markerEl })
                .setLngLat(coordinates)
                .addTo(window.DKM.map);
            // set the map view to the marker
            window.DKM.map.flyTo({
                center: coordinates,
                zoom: 15
            });
        }
}