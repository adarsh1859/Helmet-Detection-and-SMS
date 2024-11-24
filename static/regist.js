const registrationInput = document.getElementById('registration-number');
const searchButton = document.getElementById('search-button');
const vehicleDetailsContainer = document.getElementById('vehicle-details');

searchButton.addEventListener('click', () => {
  const registrationNumber = registrationInput.value.trim();

  if (!registrationNumber) {
    alert('Please enter a registration number.');
    return;
  }

  fetchVehicleDetails(registrationNumber);
});

function fetchVehicleDetails(registrationNumber) {
  fetch(`rider-data-500.xml?registration=${registrationNumber}`) // Replace with actual XML file path
    .then(response => response.text()) // Parse as text for XML processing
    .then(xmlString => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(xmlString, "text/xml");

      // Search for matching record within all "record" nodes
      const matchingRecord = xmlDoc.querySelector(`record[registration_no="${registrationNumber}"]`);

      if (!matchingRecord) {
        vehicleDetailsContainer.textContent = 'Vehicle not found.';
        return;
      }

      // Extract details from the matching record
      const name = matchingRecord.querySelector('name').textContent;
      const phoneNo = matchingRecord.querySelector('phone_no').textContent; // Use underscore for element name
      const address = matchingRecord.querySelector('address').textContent;
      const registration = matchingRecord.querySelector('registration_no').textContent; // Use underscore for element name

      // Display details in the container (modify HTML structure as needed)
      vehicleDetailsContainer.innerHTML = `
        <h2>Vehicle Details</h2>
        <p>Name: ${name}</p>
        <p>Phone Number: ${phoneNo}</p>
        <p>Address: ${address}</p>
        <p>Registration Number: ${registration}</p>
      `;
    })
    .catch(error => {
      console.error('Error fetching vehicle details:', error);
      vehicleDetailsContainer.textContent = 'An error occurred. Please try again later.';
    });
}
