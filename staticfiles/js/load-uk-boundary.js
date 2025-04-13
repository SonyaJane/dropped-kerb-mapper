export default async function loadBoundary() {
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