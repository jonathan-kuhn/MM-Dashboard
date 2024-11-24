function validateName() {
  let name = document.getElementById("name").value;
  const pattern = /^[a-zA-Z0-9_.-]+$/;
  if (!name || name === "" || name == null) {
    showError("No name specified!", "name");
  } else if (!pattern.test(name)) {
    showError("Invalid Name!", "name");
  } else {
    resetError("name");
  }
}

function validateVersion() {
  let version = documentl.getElementById("VERSION");
  const version_pattern  = /^[0-9](?:[0-9.]*[0-9])?$/
  if ((version = null || version === "" || !version)) {
    showError("Nothing specified!");
  } else if (!version_pattern.test(version)) {
    showError("Invalid version!", "version");
  } else if (version.indexOf("1") != 0){
    showError("Invalid version!", "version");
  } else {
    resetError("version");
  }
}

function showError(errorMessage, inputField) {
  let field = document.getElementById(inputField);
  field.classList.add("error");
  if (inputField == "guessedCategory") {
    inputField.selectedIndex = 0;
  } else {
    field.value = null;
    field.placeholder = errorMessage;
  }
}

function resetError(id) {
  let field = document.getElementById(id);
  field.classList.remove("error");
}
