export default function addEventListenerFormCloseButtons(formcontainer) {
    // Add event listener to the close buttons
    const closeButtons = document.querySelectorAll('.close-btn');
    closeButtons.forEach(button => {
        button.addEventListener('click', function () {
            DKM.newMarker.remove();                // Remove the marker
            formcontainer.style.display = 'none';  // Hide the form
            DKM.map.getCanvas().style.cursor = ''; // Reset cursor style
        });
    });
}