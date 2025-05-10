document.addEventListener('DOMContentLoaded', () => { 

  // toggle the display of the mobility device containers based on the selected value of the yes/no dropdown
  const usesMobilityDevice = document.getElementById("id_uses_mobility_device");
  const usesMobilityDeviceDiv = document.getElementById("div_id_uses_mobility_device");
  const isCarer = document.getElementById("id_is_carer");
  const isCarerDiv = document.getElementById("div_id_is_carer");
  const mobilityDeviceType = document.getElementById("div_id_mobility_device_type");

  //  Change CSS classes for some of the form fields
  usesMobilityDeviceDiv.children[0].classList.remove("col-sm-4");
  usesMobilityDeviceDiv.children[0].classList.add("col-sm-9");
  usesMobilityDeviceDiv.children[1].classList.remove("col-sm-8");
  usesMobilityDeviceDiv.children[1].classList.add("col-sm-3", "d-flex", "justify-content-sm-end");

  isCarerDiv.children[0].classList.remove("col-sm-4");
  isCarerDiv.children[0].classList.add("col-sm-9");
  isCarerDiv.children[1].classList.remove("col-sm-8");
  isCarerDiv.children[1].classList.add("col-sm-3", "d-flex", "justify-content-sm-end");

  mobilityDeviceType.children[0].classList.remove("col-sm-4");
  mobilityDeviceType.children[1].classList.remove("col-sm-8");  

  // move the id_password1_helptext div to below the password1 field
  const password1HelpText = document.getElementById("id_password1_helptext");
  const grandParent = password1HelpText.parentElement.parentElement;
  grandParent.parentElement.insertBefore(password1HelpText, grandParent.nextSibling);

  function toggleDeviceContainer() {
    // Show or hide the device container based on the selected value of the mobility device dropdown
    // and the isCarer checkbox
    if (usesMobilityDevice.value === "True" || isCarer.value === "True") {
      mobilityDeviceType.classList.remove("hidden");
    } else {
      mobilityDeviceType.classList.add("hidden");
    }
  }

  // Run on page load
  toggleDeviceContainer();

  // Add an event listener to update on change
  usesMobilityDevice.addEventListener("change", toggleDeviceContainer);
  isCarer.addEventListener("change", toggleDeviceContainer);
});
