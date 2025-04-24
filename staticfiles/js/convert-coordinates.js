export default function convertCoordinates(geometry) {
// Define projections
proj4.defs("EPSG:3857","+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs");
proj4.defs("EPSG:4326","+proj=longlat +datum=WGS84 +no_defs");

// Convert coordinates from EPSG:3857 to EPSG:4326
function convertCoord(coord) {
  return proj4("EPSG:3857", "EPSG:4326", coord);
}

// For a Polygon:
if (geometry.type === 'Polygon') {
  const convertedCoordinates = geometry.coordinates.map(ring =>
    ring.map(coord => convertCoord(coord))
  );
  geometry.coordinates = convertedCoordinates;
}