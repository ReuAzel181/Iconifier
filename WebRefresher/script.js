
function loadAndShowContent(htmlFile, imagePath) {
    // Fetch the content of the specified HTML file
    fetch(htmlFile)
        .then(response => response.text())
        .then(data => {
            // Update the hidden content with the fetched HTML
            let hiddenContent = document.getElementById('hiddenContent');
            hiddenContent.innerHTML = data;
            hiddenContent.classList.remove('hidden');
        })
        .catch(error => console.error('Error fetching content:', error));

    // Clear the images in the table-container before showing the image
    clearTableContainer();

    // Show image twice
    showImage(imagePath);
    showImage(imagePath);
}

function showContent(textContent, imagePath) {
    // Display text
    let textElement = document.getElementById('hiddenContent');
    textElement.textContent = textContent;
    textElement.classList.remove('hidden');

    // Clear the images in the table-container before showing the image
    clearTableContainer();

    // Show image twice
    showImage(imagePath);
    showImage(imagePath);
}

function showImage(imagePath) {
    console.log("Image path:", imagePath);

    // Create a new image element
    let img = document.createElement("img");
    img.src = imagePath;
    img.classList.add('table-image'); // Apply the CSS class

    // Append the image to the container div
    document.getElementById('table-container').appendChild(img);
}

function clearTableContainer() {
    // Clear only the images in the table container
    let tableContainer = document.getElementById('table-container');
    let images = tableContainer.querySelectorAll('.table-image');
    
    images.forEach(image => {
        tableContainer.removeChild(image);
    });
}
