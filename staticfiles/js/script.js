// Check if the browser supports the replaceState method
if (window.history.replaceState) {
    // Use replaceState to modify the history entry, preventing form resubmission on page reload
  window.history.replaceState(null, null, window.location.href);
}

// Import the delayBeforeReroute function from the shared.js module
import {delayBeforeReroute} from "./shared.js";

// Add an event listener to run this code once the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    const dateFieldIcon = document.getElementById("start-date-icon");
    const serviceSelect = document.getElementById("id_service");
    const dateTimeFlatpickrContainer = document.getElementsByClassName("django-flatpickr")[0]._flatpickr;

    // Check if Flatpickr container is ready
    if (dateTimeFlatpickrContainer) {
         // Function to disable weekends in Flatpickr
         function disableWeekends(date) {
             return (date.getDay() === 0 || date.getDay() === 6);
         }

         // Update the Flatpickr options to disable weekends and set time schedule
         dateTimeFlatpickrContainer.set('disable', [disableWeekends]);
         dateTimeFlatpickrContainer.set('minTime', '08:00')
         dateTimeFlatpickrContainer.set('minDate', 'today')
         dateTimeFlatpickrContainer.set('maxTime', '17:00')
    }
    // Add click event listener to the date field icon
    dateFieldIcon.addEventListener("click", function(event) {
       event.preventDefault();
       dateTimeFlatpickrContainer.open();
    });

    // Add a change event listener to the service select element
    serviceSelect.addEventListener('change', function (event) {
        const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];
        const selectedValue = selectedOption.value;
        const priceRangeContainer = document.getElementById('servicePrice');
        priceRangeContainer.innerHTML = "";
        if (selectedValue) {
            // Fetch the price range for the selected service
              fetch(`/api/service/price/${selectedValue}/`)
                  .then((response) => response.json())
                  .then((data) => {
                      priceRangeContainer.hidden = false;
                      // Display the range in the container
                      priceRangeContainer.innerHTML = `Approximate Price: £${data.price_range.vary_price1} - £${data.price_range.vary_price2}`
                  });
        }
    });

    delayBeforeReroute("/profile")
});
