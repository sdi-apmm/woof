// Check if the browser supports the history.replaceState method
if (window.history.replaceState) {
    // Use replaceState to modify the history entry, preventing form resubmission on page reload
  window.history.replaceState(null, null, window.location.href);
}

// Import the delayBeforeReroute function from the shared.js module
import {delayBeforeReroute} from './shared.js'

// Add an event listener to run this code once the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", function() {
     // Call delayBeforeReroute function with the root URL (home) as the target location
    delayBeforeReroute("/")
});


