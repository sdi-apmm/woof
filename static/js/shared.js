// Function to delay the page reroute if there are any success alert messages
function delayBeforeReroute(location) {
   // Select all elements with the class 'alert-success'
  const messages = document.querySelectorAll('.alert-success');
  // If there is at least one success message
  if (messages.length > 0) {
    setTimeout(function() {
      // Set a timeout to redirect the page after 3 seconds
      window.location.href = location;
    }, 3000);
  }
}

// Add an event listener to run this code once the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Select all elements with the class 'close'
  const messages = document.querySelectorAll('.close');
   // For each 'close' button element
  messages.forEach(m => {
    m.addEventListener("click", (e) => {
        // When the 'close' button is clicked, hide its parent element
        m.parentElement.style.display = 'none';
    });
  });
});

// Export the delayBeforeReroute function for use in other modules
export {delayBeforeReroute};