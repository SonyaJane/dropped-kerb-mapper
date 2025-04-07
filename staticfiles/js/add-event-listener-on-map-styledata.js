import updateAttributionControl from './update-attribution-control.js';

export default function addEventListenerOnStyledata() {
    // Add an event listener to the map for the map 'styledata' event
    DKM.map.on('styledata', function () {
        const brandingElement = document.querySelector('.os-api-branding.copyright');
        if (brandingElement) {
            brandingElement.remove();
        }
        updateAttributionControl();
    });  
}
