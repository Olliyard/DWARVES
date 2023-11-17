// functions.js

// Function to create and append an image element
function createImage(src) {
    const img = document.createElement("img");
    img.src = src;
    img.classList.add("petri-dish");
    return img;
}

// Update the generateImageMatrix function
function generateImageMatrix(data) {
    const container = document.getElementById("image-container");
    const colonyPopup = document.getElementById("colony-popup");
    const saveChangesButton = document.getElementById("save-changes");

    for (let i = 1; i <= 9; i++) {
        const colonyKey = `colony${i}`;
        const isOccupied = data[colonyKey] ? data[colonyKey].occupied : false;
        const src = isOccupied ? "assets/PetriDish.png" : "assets/PetriDishEmpty.png";
        const img = createImage(src);

        img.addEventListener("click", () => {
            // Show the colony information popup
            colonyPopup.style.display = "block";

            // Populate the popup fields with colony data
            document.getElementById("daytime_hours").value = data[colonyKey].daytime_hours;
            // Populate other fields similarly

            // Save the currently selected colony key
            colonyPopup.dataset.colonyKey = colonyKey;
        });

        container.appendChild(img);
    }

    saveChangesButton.addEventListener("click", () => {
        // Get the selected colony key from the dataset
        const selectedColonyKey = colonyPopup.dataset.colonyKey;

        // Update the colony data based on user input
        data[selectedColonyKey].daytime_hours = document.getElementById("daytime_hours").value;
        // Update other fields similarly

        // Close the popup
        colonyPopup.style.display = "none";
    });
}



// Function to load JSON from a file
function loadJSON(filePath, callback) {
    fetch(filePath)
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => console.error(error));
}


