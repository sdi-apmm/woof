// Check if the browser supports the replaceState method
if (window.history.replaceState) {
  // Replace the current history state with a new one to prevent form resubmission
  window.history.replaceState(null, null, window.location.href);
}

// Import the delayBeforeReroute function from the shared.js module
import {delayBeforeReroute} from "./shared.js";

// Execute the following code when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  // Get references to the delete button, modal, and confirmation button
  const deleteUserBtn = document.getElementById('deleteUserBtn');
  const deleteUserModal = document.getElementById('confirmDeleteProfileModal');
  const confirmDeleteUser = document.getElementById('confirmDeleteUserButton');

  // Add a click event listener to the delete button to show the modal
  deleteUserBtn.addEventListener('click', function () {
    // Create and show the Bootstrap modal
    const modal = new bootstrap.Modal(deleteUserModal);
    modal.show();

    // Get the hidden user ID input from the modal
    const hiddenUserIdInput = deleteUserModal.getElementsByClassName('hidden_input');
    const user_id = hiddenUserIdInput[0].getAttribute('id');

    // Add a click event listener to the confirmation button to submit the form
    confirmDeleteUser.addEventListener("click", function () {
      // Get the delete user form
      let form = document.getElementById('deleteUserForm');
      // Update the form action URL with the user ID
      form.action = form.action.replace('/0/', '/' + user_id + '/');
      // Submit the form
      form.submit();
    });
  });

  delayBeforeReroute("/profile")
});
