// document.getElementById('videoForm').addEventListener('submit', function(event) {
//     event.preventDefault();

//     const formData = new FormData(this);

//     fetch('/process', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => {
//         if (!response.ok) {
//             throw new Error('Network response was not ok');
//         }
//         return response.text();
//     })
//     .then(data => {
//         console.log(data); // Log the response from the Flask route
//     })
//     .catch(error => {
//         console.error('There was a problem with the fetch operation:', error);
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('videoForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                console.log('Processing started successfully');
            } else {
                console.error('Failed to start processing');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});

