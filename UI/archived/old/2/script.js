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
}

function closeSettings() {
    const modal = document.getElementById('settingsModal');
    modal.style.display = 'none';
}
