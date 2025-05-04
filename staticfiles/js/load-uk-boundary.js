/**
 * This function loads the UK boundary GeoJSON file and assigns it to the DKM.ukBoundary variable.
 * It fetches the GeoJSON file from a specified path and handles any errors that may occur during the fetch process.
 * The function is asynchronous and uses the Fetch API to retrieve the file.
 */
export default async function loadUKBoundary() {
    try {
        const response = await fetch('/static/geojson/uk-boundary.geojson'); // Adjust the path as needed
        if (!response.ok) {
            throw new Error('Failed to load boundary file.');
        }
        DKM.ukBoundary = await response.json(); // Parse the GeoJSON file
        console.log('UK Boundary loaded')
    } catch (error) {
        console.error('Error loading boundary:', error);
    }
}