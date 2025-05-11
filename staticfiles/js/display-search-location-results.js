import handleLocationSelect from './handle-location-select.js';
/**
 * Displays the results of a search for a place or address.
 * Creates a title div with an exit button.
 * Then creates a new div for each result with a click event listener.
 */
export default function displaySearchLocationResults(data) {

    // if a results div already exists, remove it
    const existingResultsDiv = document.querySelector('#location-search-results');
    if (existingResultsDiv) {
        existingResultsDiv.remove();
    }

    // create a new div with id #location-search-results
    const resultsDiv = document.createElement('div');
    resultsDiv.id = 'location-search-results';

    // Iterate through the data
    for (let place of data) {
        // Create a new div for each result
        const placeDiv = document.createElement('div');
        let name = place.display_name;
        // remove 'United Kingdom' from the name if present
        if (name.includes('United Kingdom')) {
            name = name.replace(', United Kingdom', '').trim();
        }
        // add html to the div
        placeDiv.innerHTML = `<p class="mb-0 py-2">${name}</p>`;
        // add css classes to the div if place is not the last one
        if (place === data[data.length - 1]) {
            placeDiv.classList.add('p-3', 'cursor-pointer', 'mango-hover');
        } else {
            placeDiv.classList.add('border-bottom-mango', 'p-3', 'cursor-pointer', 'mango-hover');
        }

        // add latitude and longitude to the div
        placeDiv.dataset.latitude = place.lat;
        placeDiv.dataset.longitude = place.lon;
        
        // get the place polygon if class = "boundary" and it is not a point
        const placeClass = place.class;

        // or if the class is boundary or place, and we have a polygon or multipolygon
        // add the geometry to the div 

        if (placeClass === 'boundary' || placeClass === 'place'  && place.geojson.type != "Point") {
            // add geometry to the div
            placeDiv.dataset.geometry = JSON.stringify(place.geojson);
        }

        // add an event listener to the div for choosing the location
        placeDiv.addEventListener('click', e => {
            handleLocationSelect(e);
        });

        // Append the div to the new div
        resultsDiv.appendChild(placeDiv);
    }
        
    // Append the new div to the search-location div
    document.querySelector('#search-location').appendChild(resultsDiv);
}