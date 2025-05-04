import updateAttributionControl from './update-attribution-control.js';
/** 
* Remove the default Ordnance Survey copyright element from the map
* Re‑create the attribution control based on viewport size (contains the Ordnance Survey copyright element)
*/
export default function recreateCopyrightAttribution() {
        const brandingElement = document.querySelector('.os-api-branding.copyright');
    if (brandingElement) {
        brandingElement.remove();
    }
    updateAttributionControl();
}