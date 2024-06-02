// Check if the browser supports the history.replaceState method
if (window.history.replaceState) {
  // Use replaceState to modify the history entry, preventing form resubmission on page reload
  window.history.replaceState(null, null, window.location.href);
}

// Import the delayBeforeReroute function from the shared.js module
import {delayBeforeReroute} from './shared.js'
document.addEventListener("DOMContentLoaded", function () {
  // Selecting elements
  const editButtons = document.querySelectorAll('.editBtn');
  const addPetButton = document.getElementById('addPetButton');
  const cancelButtons = document.querySelectorAll('.cancelBtn');
  const deletePetButtons = document.querySelectorAll('.deletePetBtn');
  const dateField = document.getElementById("start_date");
  const petField = document.getElementById("id_pet");
  const serviceField = document.getElementById("id_service");
  const description = document.getElementById("id_description");
  const dateFieldIcon = document.getElementById("start-date-icon");
  const appointmentIdField = document.getElementById("appointment_id");
  const petIdField = document.getElementById("pet_id");
  const cancelAppointmentIdField = document.getElementById("cancel_appointment_id");
  const deletePetIdField = document.getElementById("pet_id");
  const confirmCancelButton = document.getElementById("confirmCancelButton");
  const confirmDeletePetButton = document.getElementById("confirmDeletePetButton");
  const addPetModal = document.getElementById("addPetModal");
  const editPetButtons = document.querySelectorAll('.editPetBtn');

    // Handling tab triggers
  const triggerTabList = document.querySelectorAll('#v-tabs-tab button')
  triggerTabList.forEach(triggerEl => {
    const tabTrigger = new bootstrap.Tab(triggerEl)
    triggerEl.addEventListener('click', event => {
      event.preventDefault()
      tabTrigger.show()
    });
  });


  //Handling tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });


   // Handle cancel appointment
  handleConfirmationModal(
    "confirmCancelAppointmentModal",
    "cancelAppointmentForm",
    cancelButtons,
    confirmCancelButton,
    cancelAppointmentIdField,
      'cancelAppointmentFormMessageContainer');

  // Handle edit appointment
  handleFormSubmit(
    "saveChangesButton",
    "editAppointmentForm",
    "editAppointmentFormErrors");

  // Handle edit appointment modal
  editButtons.forEach(function (btn) {
    const appointmentModal = document.getElementById("editAppointmentModal");
    btn.addEventListener('click', function () {
      const appointmentId = btn.getAttribute('id');

      renderFlatPickr();
      renderCalendarIcon(dateFieldIcon, dateField);
      appointmentIdField.innerHTML = "";
      fetch(`/api/appointment/${appointmentId}/`)
        .then((response) => response.json())
        .then((data) => {
          const appointment = data.appointment

          setDefaultOption(dateField, appointment.start_date_time)
          setDefaultOption(description, appointment.description);
          setDefaultSelectOption(petField, appointment.pet.id);
          setDefaultSelectOption(serviceField, appointment.service.id);
          appointmentIdField.value = appointmentId;
        })

      const modal = new bootstrap.Modal(appointmentModal);
      modal.show();


    });
  });

   // Show add pet modal
  addPetButton.addEventListener('click', function () {
    const modal = new bootstrap.Modal(addPetModal);
    modal.show();
  });

   // Handle add pet
  handleFormSubmit(
    "addPetSubmitButton",
    "addPetForm",
    "petFormErrors");

   // Handle edit pet modal
  editPetButtons.forEach(function (btn) {
    const editPetModal = document.getElementById("editPetModal");
    btn.addEventListener('click', function () {
      const petId = btn.getAttribute('id');

      petIdField.innerHTML = "";
      fetch(`/api/pet/${petId}/`)
        .then((response) => response.json())
        .then((data) => {
          const pet = data.pet
          petIdField.value = petId;
          const petNameField = document.getElementById("edit_pet_name");
          const petBreedField = document.getElementById("edit_pet_breed");
          const petAgeField = document.getElementById("edit_pet_age");
          const petMedicalNotesField = document.getElementById("edit_medical_notes");
          setDefaultOption(petNameField, pet.name)
          setDefaultOption(petBreedField, pet.breed);
          setDefaultOption(petAgeField, pet.age);
          setDefaultOption(petMedicalNotesField, pet.medical_notes)
        });

      const modal = new bootstrap.Modal(editPetModal);
      modal.show();
    });
  });

  // Handle edit pet
    handleFormSubmit(
    "editPetButton",
    "editPetForm",
    "editPetFormErrors");

  // Handle delete pet
  handleConfirmationModal(
      "confirmDeletePetModal",
      "deletePetForm",
      deletePetButtons,
      confirmDeletePetButton,
      deletePetIdField,
      'deletePetFormMessageContainer');
});


// Render Flatpickr date-time picker
function renderFlatPickr() {
  // Initialize Flatpickr on the element with the ID 'start_date'
  flatpickr('#start_date', {
    // Set the date format to "day-month-year hour:minute"
    "dateFormat": "d-m-Y H:i",
    // Enable time selection
    "enableTime": true,
    // Set the minimum date to today, disabling past dates
    "minDate": "today",
    // Disable weekends (Saturdays and Sundays)
    "disable": [
        function(date) {
            // Disable if the day is Sunday (0) or Saturday (6)
            return (date.getDay() === 0 || date.getDay() === 6);
        }
    ],
    // Set the minimum time to 08:00 AM
    "minTime": "08:00",
    // Set the maximum time to 05:00 PM
    "maxTime": "17:00",
  });
}


/**
 * Adds a click event listener to a calendar icon to trigger the opening of the Flatpickr date-time picker.
 *
 * @param {HTMLElement} icon - The calendar icon element that will be clickable to open the date-time picker.
 * @param {HTMLElement} dateField - The input field associated with the Flatpickr date-time picker instance.
 */
function renderCalendarIcon(icon, dateField) {
  // Add a click event listener to the calendar icon
  icon.addEventListener("click", function (event) {
    // Prevent the default action of the event (e.g., if the icon is within a link)
    event.preventDefault();

    // Open the Flatpickr date-time picker associated with the dateField
    dateField._flatpickr.open();
  });
}

/**
 * Sets the default value for a specified form field.
 *
 * @param {HTMLElement} field - The form field element to set the value for.
 * @param {string} value - The default value to be assigned to the form field.
 */
function setDefaultOption(field, value) {
  // Set the value of the field to the provided value
  field.value = value;
}

/**
 * Set the default selected option for a given select field based on the provided ID.
 *
 * @param {HTMLSelectElement} field - The select field element.
 * @param {string | number} id - The ID of the option to be selected.
 */
function setDefaultSelectOption(field, id) {
  // Iterate through all options in the select field
  for (let i = 0; i < field.options.length; i++) {
    let option = field.options[i];
    // Check if the option's value matches the provided ID
    if (option.value == id) {
      // Set the option as selected
      option.selected = true;
      break; // Exit the loop once the matching option is found
    }
  }
}

/**
 * Convert the format of a date-time string from "d-m-Y H:i" to "Y-m-d H:i".
 *
 * @param {string} dateTimeStr - The date-time string in "d-m-Y H:i" format.
 * @returns {string} The date-time string converted to "Y-m-d H:i" format.
 */
function convertDateTimeFormat(dateTimeStr) {
  // Split the input string into date and time parts
  const [datePart, timePart] = dateTimeStr.split(' ');

  // Split the date part into day, month, and year
  const [day, month, year] = datePart.split('-');

  // Return the date-time string in the new format "Y-m-d H:i"
  return `${year}-${month}-${day} ${timePart}`;
}

/**
 * Handle the confirmation modal for various actions triggered by specific buttons.
 *
 * @param {string} modal - The ID of the confirmation modal element.
 * @param {string} confirmationForm - The ID of the form associated with the confirmation action.
 * @param {NodeList} triggerButtons - The NodeList of buttons that trigger the confirmation modal.
 * @param {Element} confirmationButton - The confirmation button within the modal.
 * @param {Element} idField - The hidden input field storing the ID associated with the action.
 * @param {string} formErrorContainer - The ID of the container for displaying form errors.
 */
function handleConfirmationModal(modal, confirmationForm, triggerButtons, confirmationButton, idField, formErrorContainer) {
  // Iterate over each button that triggers the confirmation modal
  triggerButtons.forEach(function (btn) {
    // Get the confirmation modal element
    const confirmationModal = document.getElementById(modal);

    // Add a click event listener to the trigger button
    btn.addEventListener('click', function (event) {
      event.preventDefault();

      // Get the ID from the button's attribute
      const id = btn.getAttribute('id');

      // Show the confirmation modal
      const modal = new bootstrap.Modal(confirmationModal);
      modal.show();

      // Add a click event listener to the confirmation button
      confirmationButton.addEventListener("click", function () {
        // Set the hidden input field with the ID
        idField.value = id;

        // Get the form element and create a FormData object from it
        let form = document.getElementById(confirmationForm);
        const formData = new FormData(form);

        // Update the form action URL with the ID
        form.action = form.action.replace('/0/', '/' + id + '/');

        // Send the form data using the fetch API
        fetch(form.action, {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
          },
        })
          .then(response => response.text())
          .then(data => {
            // Handle the response and render any form errors
            handleMessageRendering(formErrorContainer, data);
          })
          .catch(error => {
            console.error('Error:', error);
          });
      });
    });
  });
}


/**
 * Handle form submission asynchronously.
 *
 * @param {string} submitButton - The ID of the submit button.
 * @param {string} submitForm - The ID of the form to be submitted.
 * @param {string} formErrorContainer - The ID of the container to display form errors
 */
function handleFormSubmit(submitButton, submitForm, formErrorContainer) {
  // Add click event listener to the submit button
  document.getElementById(submitButton).addEventListener('click', function (event) {
    event.preventDefault();

    // Get the form element and create a FormData object from it
    const form = document.getElementById(submitForm);
    const formData = new FormData(form);

    // Check if the form type is 'edit_appointment_form' to convert the date-time format
    const formType = formData.get("form_type");
    if (formType === 'edit_appointment_form') {
      const startDateTime = formData.get('start_date_time');
      const convertedDateTime = convertDateTimeFormat(startDateTime);
      formData.set('start_date_time', convertedDateTime);
    }

    // Clear any previous form errors
    document.getElementById(formErrorContainer).innerHTML = '';

    // Send the form data using the fetch API
    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(response => response.text())
      .then(data => {
        // Handle the response and render any form errors
        handleMessageRendering(formErrorContainer, data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  });
}

/**
 * Render and handle form messages based on the response data.
 *
 * @param {string} formErrorContainer - The ID of the container to display form errors.
 * @param {string} data - The HTML response data from the server.
 */
function handleMessageRendering(formErrorContainer, data) {
  // Parse the HTML response data
  const parser = new DOMParser();
  const doc = parser.parseFromString(data, 'text/html');

  // Select all alert messages from the parsed data
  const formMessages = doc.querySelectorAll(`#${formErrorContainer} .alert`);
  // Select success messages specifically
  const successMessage = doc.querySelectorAll(`#${formErrorContainer} .alert-success`);

  // If there are any form messages, render them
  if (formMessages.length !== 0) {
    handleMessageLoading(formErrorContainer, formMessages);
  }

  // If there are any success messages, delay before redirecting
  if (successMessage.length !== 0) {
    delayBeforeReroute('/profile');
  }

  // Add close event listeners to form messages
  handleCloseMessagesForm();
}

/**
 * Append messages to the message container.
 *
 * @param {string} messageContainer - The ID of the container to display messages.
 * @param {NodeList} messages - The list of message elements to be appended.
 */
function handleMessageLoading(messageContainer, messages) {
  const messageDiv = document.getElementById(messageContainer);
  // Append each message to the message container
  messages.forEach(message => {
    messageDiv.appendChild(message);
  });
}

/**
 * Add event listeners to close buttons in the form messages.
 */
function handleCloseMessagesForm() {
  // Select all elements with the 'close' class
  const messages = document.querySelectorAll('.close');
  // Add click event listener to each close button to hide the message
  messages.forEach(m => {
    m.addEventListener("click", (e) => {
      m.parentElement.style.display = 'none';
    });
  });
}