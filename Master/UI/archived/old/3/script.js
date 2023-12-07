let currentSettings = {};  // Object to store the current settings

function showSettings(petriDishID) {
    const modal = document.getElementById('settingsModal');
    modal.style.display = 'block';

    // Set the Petri Dish ID
    document.getElementById('petriDishID').innerText = petriDishID;

    // Simulated experiment details (replace with your own logic to get actual dates)
    const experimentBeginDate = new Date().toLocaleDateString();
    const lastObservationDate = new Date(new Date().getTime() + (7 * 24 * 60 * 60 * 1000)).toLocaleDateString();  // Adding 7 days for example
    document.getElementById('experimentBeginDate').innerText = experimentBeginDate;
    document.getElementById('lastObservationDate').innerText = lastObservationDate;

    // Load the saved settings for this Petri Dish ID (if available)
    const savedSettings = JSON.parse(localStorage.getItem(`petriDishSettings_${petriDishID}`));
    if (savedSettings) {
        currentSettings = savedSettings;
        updateSettingsDisplay();
    }
}

function closeSettings() {
    const modal = document.getElementById('settingsModal');
    modal.style.display = 'none';
}

function updateSetting(settingName, value) {
    currentSettings[settingName] = parseFloat(value);
    updateSettingsDisplay();
}

function updateSettingsDisplay() {
    const currentSettingsDisplay = document.getElementById('currentSettings');
    currentSettingsDisplay.innerText = JSON.stringify(currentSettings, null, 2);

    // Save the settings to local storage
    const petriDishID = document.getElementById('petriDishID').innerText;
    localStorage.setItem(`petriDishSettings_${petriDishID}`, JSON.stringify(currentSettings));
}
