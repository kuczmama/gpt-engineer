// JavaScript file for analytics

/**
 * Function to send an analytics event to the analytics service
 * @param {string} eventName - The name of the event
 * @param {object} eventData - The data associated with the event
 */
function logAnalyticsEvent(eventName, eventData) {
  // Validate input parameters
  if (typeof eventName !== 'string' || eventName.length === 0) {
    console.error('Invalid eventName:', eventName);
    return;
  }
  if (typeof eventData !== 'object' || eventData === null) {
    console.error('Invalid eventData:', eventData);
    return;
  }

  // Send the analytics event
  fetch('https://api.analytics.io/event', {
    method: 'POST',
    body: JSON.stringify({ event: eventName, data: eventData }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log('Event logged:', data);
    })
    .catch(function (error) {
      console.error('Error logging event:', error);
    });
}