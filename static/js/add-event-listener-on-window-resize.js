import updateAttributionControl from './update-attribution-control.js';

export default function addEventListenerOnWindowResize() {
    // Run updateAttributionControl on window resize`
    window.addEventListener('resize', updateAttributionControl);
}