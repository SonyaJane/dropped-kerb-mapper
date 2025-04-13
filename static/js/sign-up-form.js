function initSignUpForm() {
    const mobilitySelect = document.getElementById("id_uses_mobility_device");
    const deviceContainer = mobilitySelect.parentElement.nextElementSibling
  
    function toggleDeviceContainer() {
      // Check the value of the mobility device dropdown.
      // The values are the strings "True" or "False" as rendered.
      if (mobilitySelect.value === "True") {
        deviceContainer.style.display = "block";
      } else {
        deviceContainer.style.display = "none";
      }
    }
    
    // Run on page load in case a value is already set.
    toggleDeviceContainer();
    
    // Add an event listener to update on change
    mobilitySelect.addEventListener("change", toggleDeviceContainer);
}