async function validateVersion() {
  try {
    let version = document.getElementById("VERSION").value;
    const response = await fetch(
      "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
    );
    const data = await response.json();

    // Check if version exists in the versions array
    const versionExists = data.versions.some(
      (version) => version.id === version
    );
  } catch {
    showError(
      "There was a problem with the version validation, please contact the system admin",
      "VERSION"
    );
  }

  if (!version) {
    showError("Invalid version!", "VERSION");
  } else {
    resetError("VERSION");
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
