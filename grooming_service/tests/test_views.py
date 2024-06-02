from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from django.utils import timezone

from grooming_service.forms import *


class TestNotFoundView(TestCase):
    def test_not_found_view(self):
        # Use the test client to make a GET request to the 'not_found' view
        response = self.client.get(reverse('not_found'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used
        self.assertTemplateUsed(response, '404.html')


class TestHomeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up test data for the whole TestCase
        # Create 3 service instances, 2 with short descriptions and 1 without
        Service.objects.create(name="Service 1", short_description="Description 1")
        Service.objects.create(name="Service 2", short_description="Description 2")
        Service.objects.create(name="Service 3", short_description="")  # This should be excluded

    def test_home_view_status_code(self):
        # Use the test client to make a GET request to the 'home' view
        response = self.client.get(reverse('home'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        # Use the test client to make a GET request to the 'home' view
        response = self.client.get(reverse('home'))
        response = self.client.get(reverse('home'))
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/home.html')

    def test_home_view_context_data(self):
        # Use the test client to make a GET request to the 'home' view
        response = self.client.get(reverse('home'))
        # Check that 'home_services' is in the context
        self.assertIn('home_services', response.context)
        # Get the home services from the context
        home_services = response.context['home_services']
        # Check that there are 2 services in the context (the one without a short description is excluded)
        self.assertEqual(home_services.count(), 2)
        # Check that the services are ordered by '-id'
        self.assertEqual(home_services[0].name, "Service 2")
        self.assertEqual(home_services[1].name, "Service 1")


class TestAboutView(TestCase):
    def test_about_view_status_code(self):
        # Use the test client to make a GET request to the 'about' view
        response = self.client.get(reverse('about'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_about_view_template(self):
        # Use the test client to make a GET request to the 'about' view
        response = self.client.get(reverse('about'))
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/about.html')


class TestGetServicesView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up test data for the whole TestCase
        Service.objects.create(name="Service 1", short_description="Description 1")
        Service.objects.create(name="Service 2", short_description="Description 2")

    def test_get_services_view_status_code(self):
        # Use the test client to make a GET request to the 'get_services' view
        response = self.client.get(reverse('services'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_get_services_view_template(self):
        # Use the test client to make a GET request to the 'get_services' view
        response = self.client.get(reverse('services'))
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/services.html')

    def test_get_services_view_context_data(self):
        # Use the test client to make a GET request to the 'get_services' view
        response = self.client.get(reverse('services'))
        # Check that 'services' is in the context
        self.assertIn('services', response.context)
        # Get the services from the context
        services = response.context['services']
        # Check that there are 2 services in the context
        self.assertEqual(services.count(), 2)
        # Check the names of the services
        self.assertEqual(services[0].name, "Service 1")
        self.assertEqual(services[1].name, "Service 2")


class TestRegisterView(TestCase):
    def test_register_view_get_request(self):
        # Use the test client to make a GET request to the 'register' view
        response = self.client.get(reverse('register'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/register.html')
        # Check that the form is included in the context
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_view_post_request_valid_form(self):
        # Use the test client to make a POST request to the 'register' view with valid data
        response = self.client.post(reverse('register'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)
        # Check that the user was created
        self.assertTrue(User.objects.filter(email='jane.smith@example.com').exists())
        # Check that the user is logged in
        user = User.objects.get(email='jane.smith@example.com')
        self.assertTrue(user.is_authenticated)
        # Check that the success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(message.message == "Your account has been created! Logging you in..." for message in messages))

    def test_register_view_post_request_invalid_form(self):
        # Use the test client to make a POST request to the 'register' view with invalid data
        response = self.client.post(reverse('register'), {
            'first_name': '',
            'last_name': '',
            'email': 'invalidemail',
            'password': '',
            'phone_number': '',
            'address': ''
        })
        # Check that the response is 200 OK (form re-rendered with errors)
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/register.html')
        # Check that the form is included in the context and is not valid
        form = response.context['form']
        self.assertIsInstance(form, RegistrationForm)
        self.assertFalse(form.is_valid())
        # Check that the error messages were added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "register_form" for message in messages))


class TestUserLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test user for authentication
        User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')

    def test_user_login_view_get_request(self):
        # Use the test client to make a GET request to the 'user_login' view
        response = self.client.get(reverse('login'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/login.html')
        # Check that the form is included in the context
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_user_login_view_post_request_valid_credentials(self):
        # Use the test client to make a POST request to the 'user_login' view with valid credentials
        response = self.client.post(reverse('login'), {
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)
        # Check that the user is logged in
        user = User.objects.get(email='john.doe@example.com')
        self.assertTrue(user.is_authenticated)
        # Check that the success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == "Login successful. Please wait..." for message in messages))

    def test_user_login_view_post_request_invalid_credentials(self):
        # Use the test client to make a POST request to the 'user_login' view with invalid credentials
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        # Check that the response is 200 OK (form re-rendered with errors)
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/login.html')
        # Check that the form is included in the context and is not valid
        form = response.context['form']
        self.assertIsInstance(form, LoginForm)
        # Check that the error message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "login_form" for message in messages))


class TestUserLogoutView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test user for authentication
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')

    def test_user_logout_view(self):
        # Log in the user
        self.client.login(email='john.doe@example.com', password='password123')

        # Use the test client to make a GET request to the 'user_logout' view
        response = self.client.get(reverse('logout'))

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 302)
        # Check that the user is logged out
        self.assertNotIn('_auth_user_id', self.client.session)
        # Check that the success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == "You have been logged out." for message in messages))
        # Check that the user is redirected to the home page
        self.assertRedirects(response, reverse('home'))


class TestBookAppointmentView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test user for authentication
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')
        cls.service = Service.objects.create(name="Service 1", short_description="Description 1")

    def setUp(self):
        # Set up a test client
        self.client = Client()
        # Log in the user
        self.client.login(email='john.doe@example.com', password='password123')

    def test_book_appointment_view_redirect_if_not_logged_in(self):
        # Log out the user
        self.client.logout()
        # Use the test client to make a GET request to the 'book_appointment' view
        response = self.client.get(reverse('appointment'))
        # Check that the response is a redirect to the login page
        self.assertRedirects(response, f'/login/?next={reverse("appointment")}')

    def test_book_appointment_view_get_request(self):
        # Use the test client to make a GET request to the 'book_appointment' view
        response = self.client.get(reverse('appointment'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/appointment.html')
        # Check that the form is included in the context
        self.assertIn('form', response.context)
        # Check that the form is an instance of AppointmentForm
        self.assertIsInstance(response.context['form'], AppointmentForm)

    def test_book_appointment_view_post_request_valid_form(self):
        # Create a pet for the user
        pet = self.user.pet_set.create(name='Test Pet', breed='Husky', age=3)
        # Use the test client to make a POST request to the 'book_appointment' view with valid data
        response = self.client.post(reverse('appointment'), {
            'start_date_time': timezone.now() + timezone.timedelta(days=1),
            'description': 'Test appointment',
            'pet': pet.id,
            'service': self.service.id,
        })
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)
        # Check that the appointment was created
        self.assertTrue(Appointment.objects.filter(user_id=self.user.id).exists())
        # Check that the success message was added
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn("Your appointment has been successfully created! Redirecting you to profile page...", messages)

    def test_book_appointment_view_post_request_invalid_form_appointment_booked(self):
        # Create an existing appointment
        current_time = timezone.now() + timezone.timedelta(days=1)
        current_time_str = current_time.strftime('%d-%m-%Y %H:%M')
        current_time_str_new_format = datetime.strptime(current_time_str, '%d-%m-%Y %H:%M')
        pet = self.user.pet_set.create(name='Test Pet', breed='Husky', age=3)
        Appointment.objects.create(start_date_time=current_time_str_new_format,
                                   description='Test appointment', pet_id=pet.id, service_id=self.service.id,
                                   user_id=self.user.id, status=1)

        # Use the test client to make a POST request to the 'book_appointment' view with start_date_time thats already booked
        response = self.client.post(reverse('appointment'), {
            'start_date_time': current_time_str_new_format,
            'description': 'Test appointment',
            'pet': pet.id,
            'service': self.service.id,
        })
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)
        appointments = Appointment.objects.filter(user_id=self.user.id)
        # Check that the appointment was not created
        self.assertEqual(len(appointments), 1)
        # Check that the error message was added
        messages = list(response.context['messages'])
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "book_appointment_form" for message in messages))


class TestEditProfileView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test user for authentication
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')

    def setUp(self):
        # Set up a test client
        self.client = Client()
        # Log in the user
        self.client.login(email='john.doe@example.com', password='password123')

    def test_edit_profile_view_get_request(self):
        # Use the test client to make a GET request to the 'edit_profile' view
        response = self.client.get(reverse('edit_profile'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/edit_profile.html')
        # Check that the form is included in the context
        self.assertIsInstance(response.context['form'], EditUserForm)

    def test_edit_profile_view_post_request_valid_data(self):
        # Use the test client to make a POST request to the 'edit_profile' view with valid data
        response = self.client.post(reverse('edit_profile'), {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe54@example.com",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
        })

        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)
        # Check that the success message was added
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn(
            "Your profile has been successfully saved with the new changes. Redirecting you to profile page...",
            messages)

    def test_edit_profile_view_post_request_invalid_data(self):
        # Use the test client to make a POST request to the 'edit_profile' view with invalid data
        response = self.client.post(reverse('edit_profile'), {
            "first_name": "",
            "last_name": "",
            "email": "invalidemail",
            "password": "",
            "phone_number": "",
            "address": "",
        })

        # Check that the response is 200 OK (form re-rendered with errors)
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/edit_profile.html')
        # Check that the form is included in the context and is not valid
        form = response.context['form']
        self.assertIsInstance(form, EditUserForm)
        self.assertFalse(form.is_valid())
        # Check that the error message was added
        messages = list(response.context['messages'])
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "edit_profile_form" for message in messages))


class TestManageProfileView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test users
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')
        cls.user2 = User.objects.create_user(
            first_name='John',
            last_name='Travolta',
            email='john.travolta@example.com',
            password='password123',
            phone_number='12345422290',
            address='123 Main St')
        cls.service1 = Service.objects.create(name="Service 1", short_description="Description 1")
        cls.service2 = Service.objects.create(name="Service 2", short_description="Description 2")

    def setUp(self):
        # Set up a test client
        self.client = Client()
        # Log in the user
        self.client.login(email='john.doe@example.com', password='password123')

    def test_manage_profile_view_get_request(self):
        # Use the test client to make a GET request to the 'manage_profile' view
        response = self.client.get(reverse('profile'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/profile.html')
        # Check that the appointmentForm, petForm, and editPetForm are included in the context
        self.assertIsInstance(response.context['appointmentForm'], AppointmentForm)
        self.assertIsInstance(response.context['petForm'], PetForm)
        self.assertIsInstance(response.context['editPetForm'], EditPetForm)

    def test_handle_edit_appointment_form_valid_data(self):
        # Create an existing appointment
        current_time = timezone.now() + timezone.timedelta(days=1)
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M')
        current_time_str_new_format = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M')

        updated_time = timezone.now() + timezone.timedelta(days=2)
        updated_time_str = updated_time.strftime('%Y-%m-%d %H:%M')
        updated_time_str_new_format = datetime.strptime(updated_time_str, '%Y-%m-%d %H:%M')

        pet = self.user.pet_set.create(name='Test Pet', breed='Husky', age=3)
        appointment = Appointment.objects.create(start_date_time=current_time_str_new_format,
                                                 description='Test appointment', pet_id=pet.id,
                                                 service_id=self.service1.id,
                                                 user_id=self.user.id, status=1)

        # Create a test request with valid data
        response = self.client.post(reverse('profile'), {
            'appointment_id': appointment.id,
            'start_date_time': updated_time_str,  # Update the appointment time
            'description': 'Updated description',
            'pet': pet.id,
            'service': self.service2.id,
            'form_type': 'edit_appointment_form'
        })

        # Retrieve the updated appointment from the database
        updated_appointment = Appointment.objects.get(id=appointment.id)

        # Check that the appointment was updated with the new data
        self.assertEqual(updated_appointment.start_date_time.date(), updated_time_str_new_format.date())
        self.assertEqual(updated_appointment.description, 'Updated description')
        self.assertEqual(updated_appointment.pet, pet)
        self.assertEqual(updated_appointment.service, self.service2)

        # Check that the success message was added
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn("Your appointment has been successfully updated. Redirecting you to profile page...", messages)

    def test_handle_edit_appointment_form_invalid_data(self):
        # Set time for test in correct format without seconds
        current_time = timezone.now() + timezone.timedelta(days=1)
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M')
        current_time_str_new_format = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M')

        updated_time = timezone.now() + timezone.timedelta(days=2)
        updated_time_str = updated_time.strftime('%Y-%m-%d %H:%M')
        updated_time_str_new_format = datetime.strptime(updated_time_str, '%Y-%m-%d %H:%M')

        pet = self.user.pet_set.create(name='Test Pet', breed='Husky', age=3, user_id=self.user.id)
        pet2 = self.user.pet_set.create(name='Test Pet 2', breed='Husky', age=3, user_id=self.user2.id)

        # Create appointment for another user
        Appointment.objects.create(start_date_time=updated_time_str_new_format,
                                   description='Test appointment 2', pet_id=pet2.id,
                                   service_id=self.service1.id,
                                   user_id=self.user2.id, status=1)

        # Create existing appointment for current user
        appointment = Appointment.objects.create(start_date_time=current_time_str_new_format,
                                                 description='Test appointment', pet_id=pet.id,
                                                 service_id=self.service1.id,
                                                 user_id=self.user.id, status=1)

        # Create a test request with invalid data
        response = self.client.post(reverse('profile'), {
            'appointment_id': appointment.id,
            'start_date_time': updated_time_str,  # Update the appointment time to the time of user 2
            'description': 'Updated description',
            'pet': pet.id,
            'service': self.service2.id,
            'form_type': 'edit_appointment_form'
        })

        # Retrieve the updated appointment from the database
        updated_appointment = Appointment.objects.get(id=appointment.id)

        # Check that the appointment was not updated with the new data
        self.assertNotEqual(updated_appointment.start_date_time.date(), updated_time_str_new_format.date())
        self.assertNotEqual(updated_appointment.description, 'Updated description')
        self.assertNotEqual(updated_appointment.service, self.service2)

        # Check that the error messages was added
        messages = list(response.context['messages'])
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "edit_appointment_form" for message in messages))

    def test_handle_pet_edit_form_valid_data(self):

        # Create a test pet
        pet = Pet.objects.create(user=self.user, name="Test Pet", breed="Test Breed", age=3,
                                 image="media/images/tey9seavfcldmybatmmt", medical_notes="Test notes")

        # Create a test request with valid data
        response = self.client.post(reverse('profile'), {
            'pet_id': pet.id,
            'name': 'Updated Pet',
            'breed': 'Updated Breed',
            'age': 4,
            'image': 'media/images/tey9seavfcldmybatmmt', #cloudinary field
            'medical_notes': 'Updated notes',
            'form_type': 'edit_pet_form'
        })

        # Retrieve the updated pet from the database
        updated_pet = Pet.objects.get(id=pet.id)

        # Check that the pet was updated with the new data
        self.assertEqual(updated_pet.name, 'Updated Pet')
        self.assertEqual(updated_pet.breed, 'Updated Breed')
        self.assertEqual(updated_pet.age, 4)
        self.assertEqual(updated_pet.image, 'media/images/tey9seavfcldmybatmmt')
        self.assertEqual(updated_pet.medical_notes, 'Updated notes')

        # Check that the success message was added
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn(f"{updated_pet.name} has been successfully updated. Redirecting you to profile page...", messages)

    def test_handle_pet_edit_form_invalid_data(self):
        # Create a test pet
        pet = Pet.objects.create(user=self.user, name="Test Pet", breed="Test Breed", age=3,
                                 image="media/images/tey9seavfcldmybatmmt", medical_notes="Test notes")

        # Create a test request with invalid data
        response = self.client.post(reverse('profile'), {
            'pet_id': pet.id,
            'name': 'Updated Pet23',
            'breed': 'Updated Breed23',
            'age': -4,
            'image': 'media/images/tey9seavfcldmybatmmt',  # cloudinary field
            'medical_notes': 'Updated notes',
            'form_type': 'edit_pet_form'
        })

        # Retrieve the pet from the database
        updated_pet = Pet.objects.get(id=pet.id)

        # Check that the pet was not updated with the new data
        self.assertNotEqual(updated_pet.name, 'Updated Pet23')
        self.assertNotEqual(updated_pet.breed, 'Updated Breed23')
        self.assertNotEqual(updated_pet.age, -4)
        self.assertNotEqual(updated_pet.medical_notes, 'Updated notes')

        # Check that the error messages was added
        messages = list(response.context['messages'])
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "edit_pet_form" for message in messages))

    def test_handle_pet_add_form_valid_data(self):
        # Create a test request with valid data
        response = self.client.post(reverse('profile'), {
            'name': 'Test Pet',
            'breed': 'Test Breed',
            'age': 4,
            'image': 'media/images/tey9seavfcldmybatmmt',  # cloudinary field
            'medical_notes': 'Notes',
            'form_type': 'pet_form'
        })

        # Retrieve the newly created pet from the database
        new_pet = Pet.objects.last()

        # Check that the pet was created with the correct data
        self.assertEqual(new_pet.name, 'Test Pet')
        self.assertEqual(new_pet.breed, 'Test Breed')
        self.assertEqual(new_pet.age, 4)
        self.assertEqual(new_pet.medical_notes, 'Notes')

        # Check that the success message was added
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn(f"{new_pet.name} has been successfully created. Redirecting you to profile page...", messages)

    def test_handle_pet_add_form_invalid_data(self):
        # Create a test request with invalid data
        response = self.client.post(reverse('profile'), {
            'name': 'Test Pet 23',
            'breed': 'Test Breed 23',
            'age': -4,
            'image': 'media/images/tey9seavfcldmybatmmt',  # cloudinary field
            'medical_notes': 'Notes',
            'form_type': 'pet_form'
        })

        # Check that the error messages was added
        messages = list(response.context['messages'])
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "add_pet_form" for message in messages))


class TestCancelAppointmentView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test user for authentication
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')
        cls.service1 = Service.objects.create(name="Service 1", short_description="Description 1")
        cls.service2 = Service.objects.create(name="Service 2", short_description="Description 2")

    def setUp(self):
        # Set up a test client
        self.client = Client()


    def test_cancel_appointment_success(self):
        current_time = timezone.now() + timezone.timedelta(days=1)
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M')
        current_time_str_new_format = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M')
        pet = self.user.pet_set.create(name='Test Pet', breed='Husky', age=3, user_id=self.user.id)

        # Log in the user
        self.client.login(email='john.doe@example.com', password='password123')

        # Create a test appointment belonging to the user
        appointment = Appointment.objects.create(start_date_time=current_time_str_new_format,
                                                 description='Test appointment', pet_id=pet.id,
                                                 service_id=self.service1.id,
                                                 user_id=self.user.id, status=1)

        # Use the test client to make a GET request to the 'cancel_appointment' view
        response = self.client.get(reverse('cancel_appointment', kwargs={'cancel_appointment_id': appointment.id}))

        # Check that the appointment was cancelled
        self.assertEqual(Appointment.objects.filter(id=appointment.id).count(), 0)

        appointment_time = appointment.start_date_time.strftime('%Y-%m-%d %H:%M')

        # Check that the success message was added
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn(f"Your appointment on the {appointment_time} has been cancelled. Redirecting you to profile page...", messages)

    def test_cancel_appointment_permission_denied(self):
        # Create a test appointment belonging to another user
        other_user = User.objects.create_user(
            first_name='Johnny',
            last_name='Bravo',
            email='johnny.bravo@example.com',
            password='password123',
            phone_number='125455567890',
            address='123 Main St')

        # Create a test appointment belonging to the user
        current_time = timezone.now() + timezone.timedelta(days=1)
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M')
        current_time_str_new_format = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M')
        pet = self.user.pet_set.create(name='Test Pet', breed='Husky', age=3, user_id=self.user.id)
        appointment = Appointment.objects.create(start_date_time=current_time_str_new_format,
                                                 description='Test appointment', pet_id=pet.id,
                                                 service_id=self.service1.id,
                                                 user_id=self.user.id, status=1)

        # Log in the user
        self.client.login(username='johnny.bravo@example.com', password='password123')

        # Use the test client to make a GET request to the 'cancel_appointment' view
        response = self.client.get(reverse('cancel_appointment', kwargs={'cancel_appointment_id': appointment.id}))

        # Check that the appointment was not cancelled
        self.assertEqual(Appointment.objects.filter(id=appointment.id).count(), 1)

        self.assertRedirects(response, reverse('profile'))

    def test_cancel_appointment_not_found(self):
        # Log in the user
        self.client.login(email='john.doe@example.com', password='password123')

        # Use the test client to make a GET request to the 'cancel_appointment' view with an appointment ID that doesn't exist
        response = self.client.get(reverse('cancel_appointment', kwargs={'cancel_appointment_id': 999}))


        # Check that that 404 was returned
        self.assertEqual(response.status_code, 404)


class DeletePetViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test users
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')
        cls.user2 = User.objects.create_user(
            first_name='John',
            last_name='Travolta',
            email='john.travolta@example.com',
            password='password123',
            phone_number='12345422290',
            address='123 Main St')

    def test_delete_pet_success(self):
        # Create a pet for the test user
        pet = Pet.objects.create(user=self.user, name='Test Pet', breed='Test Breed', age=3, medical_notes='Test notes')

        # Log in the test user
        self.client.login(email='john.doe@example.com', password='password123')

        # Make a GET request to delete the pet
        response = self.client.get(reverse('delete_pet', kwargs={'delete_pet_id': pet.id}))

        # Check that the pet was deleted
        self.assertEqual(Pet.objects.filter(id=pet.id).count(), 0)

        # Check success message and redirection
        # Check that the success message was added
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn(
            f"{pet.name} has been successfully deleted. Redirecting you to profile page...",
            messages)

    def test_delete_pet_permission_denied(self):
        # Create a pet for another user
        pet = Pet.objects.create(user=self.user2, name='Test Pet', breed='Test Breed', age=3, medical_notes='Test notes')

        # Log in the test user
        self.client.login(email='john.doe@example.com', password='password123')

        # Make a GET request to delete the pet
        response = self.client.get(reverse('delete_pet', kwargs={'delete_pet_id': pet.id}))

        # Check that the pet was not deleted
        self.assertEqual(Pet.objects.filter(id=pet.id).count(), 1)
        self.assertRedirects(response, reverse('profile'))

    def test_delete_pet_not_found(self):
        # Log in the test user
        self.client.login(email='john.doe@example.com', password='password123')

        # Make a GET request to delete a non-existent pet
        response = self.client.get(reverse('delete_pet', kwargs={'delete_pet_id': 999}))

        # Check that 404 was returned
        self.assertEqual(response.status_code, 404)


class TestDeleteUserView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test users
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')
        cls.user2 = User.objects.create_user(
            first_name='John',
            last_name='Travolta',
            email='john.travolta@example.com',
            password='password123',
            phone_number='12345422290',
            address='123 Main St')

    def test_delete_user_success(self):
        # Log in the test user
        self.client.login(email='john.doe@example.com', password='password123')

        # Make a GET request to delete the user
        response = self.client.get(reverse('delete_user', kwargs={'delete_user_id': self.user.id}))

        # Check that the user was deleted
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

        # Check success message and redirection
        messages = [str(m) for m in response.wsgi_request._messages]
        self.assertIn(
            "Your account has been successfully deleted",
            messages)
        self.assertRedirects(response, reverse('home'))

    def test_delete_user_permission_denied(self):
        # Log in the test user 2
        self.client.login(email='john.travolta@example.com', password='password123')

        # Make a GET request to delete another user
        response = self.client.get(reverse('delete_user', kwargs={'delete_user_id': self.user.id}))

        # Check that the other user was not deleted
        self.assertTrue(User.objects.filter(id=self.user.id).exists())

        # Check redirection
        self.assertRedirects(response, reverse('home'))

    def test_delete_user_not_found(self):
        # Log in the test user
        self.client.login(email='john.travolta@example.com', password='password123')

        # Make a GET request to delete a non-existent user
        response = self.client.get(reverse('delete_user', kwargs={'delete_user_id': 999}))

        # Check that that 404 was returned
        self.assertEqual(response.status_code, 404)


class TestGetAppointmentByIdView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test users
        cls.user = User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')
        cls.service1 = Service.objects.create(name="Service 1", short_description="Description 1")

    def test_get_appointment_by_id_success(self):
        current_time = timezone.now() + timezone.timedelta(days=1)
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M')
        current_time_str_new_format = datetime.strptime(current_time_str, '%Y-%m-%d %H:%M')
        pet = self.user.pet_set.create(name='Test Pet', breed='Husky', age=3, user_id=self.user.id)

        # Log in the user
        self.client.login(email='john.doe@example.com', password='password123')

        # Create a test appointment belonging to the user
        appointment = Appointment.objects.create(start_date_time=current_time_str_new_format,
                                                 description='Test appointment', pet_id=pet.id,
                                                 service_id=self.service1.id,
                                                 user_id=self.user.id, status=1)

        # Make a GET request to get the appointment by its ID
        response = self.client.get(reverse('get_appointment_by_id', kwargs={'appointment_id': appointment.id}))

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check the content of the JSON response
        expected_data = {
            "id": appointment.id,
            "start_date_time": appointment.start_date_time.strftime('%d-%m-%Y %H:%M'),
            "description": appointment.description,
            "pet": {
                "name": appointment.pet.name,
                "id": appointment.pet.id
            },
            "service": {
                "name": appointment.service.name,
                "id": appointment.service.id
            }
        }
        self.assertEqual(response.json(), {"appointment": expected_data})

    def test_get_appointment_by_id_not_found(self):
        # Make a GET request with an invalid appointment ID
        response = self.client.get(reverse('get_appointment_by_id', kwargs={'appointment_id': 999}))

        # Check that the response status code is 404
        self.assertEqual(response.status_code, 404)

        # Check the content of the JSON response
        self.assertEqual(response.json(), {"message": "Appointment not found"})

    def test_get_appointment_by_id_invalid_request(self):
        # Make a GET request without providing an appointment ID
        response = self.client.get(reverse('get_appointment_by_id', kwargs={'appointment_id': ''}))

        # Check that the response status code is 400
        self.assertEqual(response.status_code, 400)

        # Check the content of the JSON response
        self.assertEqual(response.json(), {"message": "Invalid request"})
