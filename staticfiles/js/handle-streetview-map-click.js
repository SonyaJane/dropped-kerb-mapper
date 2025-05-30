import updateArrowMarker from "./update-arrow-marker.js";

// On map click, create or move marker and Street View (if active and waiting)
export default function handleStreetViewMapClick(e) {
    // Get clicked location
    const lngLat = {lng: e.lngLat.lng, lat: e.lngLat.lat};
    const latLng = {lat: e.lngLat.lat, lng: e.lngLat.lng};
    const svMsg = document.getElementById('streetview-message'); // Message to show when waiting for Street View click


    // Very first click after toggling Street View
    if (DKM.isStreetViewVisible && DKM.awaitingStreetViewClick) {
        // If it doesnt already exist, Create streetview and show at clicked location
        if (!DKM.streetView) {
            // Create new Street View panorama
            DKM.streetView = new google.maps.StreetViewPanorama(
            document.getElementById('streetview'), {
                position: latLng,
                pov: {heading: 0, pitch: 0},
                zoom: 1,
                motionTracking: false, // disables device orientation following
                motionTrackingControl: false,
                disableDefaultUI: true, // Hide default UI
            });

            DKM.streetView.setMotionTracking(false);
            DKM.streetView.addListener('pano_changed', () => DKM.streetView.setMotionTracking(false));
            DKM.streetView.addListener('visible_changed', () => DKM.streetView.setMotionTracking(false));
            DKM.streetView.addListener('pov_changed', () => DKM.streetView.setMotionTracking(false));
            google.maps.event.addListenerOnce(DKM.streetView, 'status_changed', () => DKM.streetView.setMotionTracking(false));
            setTimeout(() => DKM.streetView.setMotionTracking(false), 1000);

            // Add event listener for position or heading change in streetview 
            // to rotate or move arrow
            DKM.streetView.addListener('position_changed', updateArrowMarker);
            DKM.streetView.addListener('pov_changed', updateArrowMarker);
            
            // Remove waiting message
            svMsg.remove();
            // No longer waiting for first click    
            DKM.awaitingStreetViewClick = false; 
        } 
    } else {
        // If Street View already exists, just update its position
        if (DKM.streetView) {
            DKM.streetView.setPosition(latLng);
            // Update arrow marker position
            updateArrowMarker();
        }
    }
}