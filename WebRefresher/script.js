function loadAndShowContent(htmlFile, targetId, imagePath) {
    // Fetch the content of the specified HTML file
    fetch(htmlFile)
        .then(response => response.text())
        .then(data => {
            let tempContainer = document.createElement('div');
            tempContainer.innerHTML = data;

            let contentElement = tempContainer.querySelector('.' + targetId);

            if (contentElement) {
                let hiddenContent = document.getElementById('hiddenContent');
                hiddenContent.innerHTML = contentElement.innerHTML;
                hiddenContent.classList.remove('hidden');

                clearTableContainer();
                showImage(imagePath);
                showImage(imagePath);

                // Remove 'clicked' class from all rows
                let allRows = document.querySelectorAll('#table-container table tr');
                allRows.forEach(row => row.classList.remove('clicked'));

                // Apply the 'clicked' class to the clicked row
                let clickedRow = document.querySelector('#table-container table tr td:first-child');
                if (clickedRow) {
                    clickedRow.parentNode.classList.add('clicked');
                } else {
                    console.error('Clicked row not found.');
                }
            }
        })
        .catch(error => console.error('Error fetching content:', error));
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
