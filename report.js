const componentLinks = document.querySelectorAll('.components a');

componentLinks.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default link behavior

        const componentId = link.id;
        const imageFolder = `images/${componentId}`;

        // Fetch image data using AJAX or fetch API (example using fetch)
        fetch(`image.php?folder=${imageFolder}`)
            .then(response => response.json())
            .then(data => {
                const reportContainer = document.getElementById('report-container');
                reportContainer.innerHTML = ''; // Clear previous content

                data.forEach(image => {
                    const imageElement = document.createElement('img');
                    imageElement.src = image.src;
                    imageElement.alt = image.alt;
                    reportContainer.appendChild(imageElement);
                });

                // Redirect to report.html after fetching images (optional)
                window.location.href = 'render.html';
            })
            .catch(error => {
                console.error('Error fetching images:', error);
                // Handle errors gracefully, e.g., display an error message
            });
    });
});

// Logic for handling report page navigation (if not redirecting after fetch)
// Add event listeners or code to handle navigation within report.html
