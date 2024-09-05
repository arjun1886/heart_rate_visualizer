document.addEventListener('DOMContentLoaded', function () {
  // Set up WebSocket connection
  const socket = io('http://127.0.0.1:5000');

  // Get references to the DOM elements
  const uploadButton = document.getElementById('uploadButton');
  const anomalyField = document.getElementById('anomalyField');
  const ctx = document.getElementById('heartRateChart').getContext('2d');

  const heartRateChart = new Chart(ctx, {
    type: 'line',  // Line chart for heart rate over time
    data: {
        labels: [],  // This will hold the timestamps
        datasets: [{
            label: 'Heart Rate (bpm)',  // Label for the dataset
            data: [],  // This will hold the heart rate data points
            borderColor: 'rgba(75, 192, 192, 1)',  // Line color
            backgroundColor: 'rgba(75, 192, 192, 0.2)',  // Background color under the line
            fill: true,  // Fill the area under the line
        }]
    },
    options: {
        scales: {
            x: {
                type: 'time',  // Use time scale for x-axis
                time: {
                    unit: 'second',  // Display timestamps in seconds
                    tooltipFormat: 'HH:mm:ss',  // Format for tooltip when hovering
                    displayFormats: {
                        second: 'HH:mm:ss'  // Display format for x-axis
                    }
                },
                title: {
                    display: true,
                    text: 'Timestamp'  // Label for the x-axis
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Heart Rate (bpm)'  // Label for the y-axis
                },
                beginAtZero: true,  // Start y-axis at zero
            }
        }
    }
});

  function csvJSON(csv) {
    const lines = csv.split('\n');
    const headers = lines[0].split(',');
  
    const result = [];
  
    for (let i = 1; i < lines.length; i++) {
      const currentLine = lines[i].split(',');
      const obj = {};
  
      for (let j = 0; j < headers.length; j++) {
        obj[headers[j]] = currentLine[j];
      }
  
      result.push(obj);
    }
  
    return JSON.stringify(result);
  }
  
  // Handle CSV file upload
  uploadButton.addEventListener('click', function () {
      const fileInput = document.getElementById('fileInput');
      const file = fileInput.files[0];

      if (file) {
          const reader = new FileReader();
          reader.onload = function (e) {
              const csvData = e.target.result;
              // Send CSV data to the backend
              fetch('/process/csv', {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body: csvJSON(csvData)
              })
              .then(response => response.json())
              .then(data => {
                  console.log('CSV data uploaded successfully:', data);
              })
              .catch(error => {
                  console.error('Error uploading CSV data:', error);
              });
          };
          reader.readAsText(file);
      } else {
          alert('Please select a CSV file to upload.');
      }
    
    socket.emit("file_uploaded");
  });

  // Function to update the chart with new data
  function updateChart(timestamp, heartRate) {
      heartRateChart.data.labels.push(timestamp);
      heartRateChart.data.datasets[0].data.push(heartRate);
      heartRateChart.update();
  }

  // Listen for heart rate data and anomalies from the server
  socket.on('heart_rate_data', function (data) {
      const timestamp = new Date(data.timestamp);  // Convert timestamp to Date object
      const heartRate = data.heart_rate;
      const anomaly = data.anomaly;
      // Update the chart with the new data
      updateChart(timestamp, heartRate);

      // Display the anomaly in the text field if it exists
      if (anomaly) {
        anomalyField.textContent = `Anomaly detected : ${anomaly}`;
      } else {
        anomalyField.textContent = null
      }
  });
});