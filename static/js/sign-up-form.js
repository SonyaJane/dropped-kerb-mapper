function initSignUpForm() {

  // toggle the display of the mobility device containers based on the selected value of the yes/no dropdown
  const mobilitySelect = document.getElementById("id_uses_mobility_device");
  const deviceContainer = document.getElementById("div_id_mobility_device_type");
  const mobilitySelectCaree = document.getElementById("id_is_carer");
  const deviceContainerCaree = document.getElementById("div_id_mobility_device_type_caree");
  const usesMobilityDeviceDiv = document.getElementById("div_id_uses_mobility_device");
  const careeDiv = document.getElementById("div_id_is_carer");

  //  Change CSS classes for some of the form fields
  usesMobilityDeviceDiv.children[0].classList.remove("col-sm-4");
  usesMobilityDeviceDiv.children[0].classList.add("col-sm-9");
  usesMobilityDeviceDiv.children[1].classList.remove("col-sm-8");
  usesMobilityDeviceDiv.children[1].classList.add("col-sm-3");
  deviceContainer.children[0].classList.remove("col-sm-4");
  deviceContainer.children[0].classList.add("col-sm-6");
  deviceContainer.children[1].classList.remove("col-sm-8");
  deviceContainer.children[1].classList.add("col-sm-6");
  careeDiv.children[0].classList.remove("col-sm-4");
  careeDiv.children[0].classList.add("col-sm-9");
  careeDiv.children[1].classList.remove("col-sm-8");
  careeDiv.children[1].classList.add("col-sm-3");
  deviceContainerCaree.children[0].classList.remove("col-sm-4");
  deviceContainerCaree.children[0].classList.add("col-sm-6");
  deviceContainerCaree.children[1].classList.remove("col-sm-8");
  deviceContainerCaree.children[1].classList.add("col-sm-6");

  // move the id_password1_helptext div to below the password1 field
  const password1HelpText = document.getElementById("id_password1_helptext");
  const grandParent = password1HelpText.parentElement.parentElement;
  grandParent.parentElement.insertBefore(password1HelpText, grandParent.nextSibling);

  function toggleDeviceContainer() {
    // Check the value of the mobility device dropdown.
    // The values are the strings "True" or "False" as rendered.
    if (mobilitySelect.value === "True") {
      deviceContainer.classList.remove("invisible");
    } else {
      deviceContainer.classList.add("invisible");
    }
  }

  function toggleCareeDeviceContainer() {
    // Check the value of the carees mobility device dropdown.
    // The values are the strings "True" or "False" as rendered.
    if (mobilitySelectCaree.value === "True") {
      deviceContainerCaree.classList.remove("invisible");
    } else {
      deviceContainerCaree.classList.add("invisible");
    }
  }

  // Run on page load
  toggleDeviceContainer();
  toggleCareeDeviceContainer()

  // Add an event listener to update on change
  mobilitySelect.addEventListener("change", toggleDeviceContainer);
  mobilitySelectCaree.addEventListener("change", toggleCareeDeviceContainer);
}



