// JavaScript file for the National Debt Tracker

/**
 * Function to fetch national debt from an API
 */
function fetchDebt() {      
  fetch('https://api.nationaldebt.io/debt')
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // Clear error message if exists
      clearErrorMessage();

      // Update the debt value on the webpage
      var debtValueElement = document.getElementById('debtValue');
      var debtChartCanvas = document.getElementById('debtChart');
      debtValueElement.textContent = 'National Debt: $' + data.debt;

      createDebtChart(debtChartCanvas, data.debt); // Create debt chart

      // Log the analytics event
      logAnalyticsEvent('national_debt_fetched', { debt: data.debt });
    })
    .catch(function (error) {
      console.error('Error fetching national debt:', error);

      // Display error message on the webpage
      var errorText = document.createElement('p');
      errorText.textContent = 'Error fetching national debt. Please try again later.';
      errorText.classList.add('error');
      var debtValueElement = document.getElementById('debtValue');
      clearErrorMessage();
      debtValueElement.appendChild(errorText);
    });
}

/**
 * Event listener for the fetch button
 */
document.getElementById('fetchDebtButton').addEventListener('click', fetchDebt);

/**
 * Function to clear the error message from the DOM
 */
function clearErrorMessage() {
  var debtValueElement = document.getElementById('debtValue');
  var errorElements = debtValueElement.getElementsByClassName('error');

  // Remove all error elements from the DOM
  while (errorElements.length > 0) {
    errorElements[0].parentNode.removeChild(errorElements[0]);
  }
}

/**
 * Function to create a chart displaying the national debt
 * @param {HTMLCanvasElement} canvas - The canvas element to render the chart
 * @param {string} debt - The national debt
 */
function createDebtChart(canvas, debt) {
  var ctx = canvas.getContext('2d');
  var chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['United States Debt'],
      datasets: [
        {
          label: 'Debt in trillions of dollars',
          data: [debt],
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function (value) {
              return value.toLocaleString();
            },
          },
        },
      },
    },
  });
}