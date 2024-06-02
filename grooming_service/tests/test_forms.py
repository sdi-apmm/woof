from django.test import TestCase
from grooming_service.forms import *
from grooming_service.models import *


class TestRegisterUserForm(TestCase):

    def setUp(self):
        # Create a user to test the unique constraints
        self.user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St'
        )

    def test_registration_form_valid_data(self):
        # Test with valid data to ensure the form is valid
        form = RegistrationForm(data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        self.assertTrue(form.is_valid())

    def test_registration_form_empty_fields(self):
        # Test with empty data to ensure the form is invalid and contains errors
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors['__all__']), 6)

    def test_registration_form_invalid_email(self):
        # Test with an invalid email format to ensure the form is invalid and contains error for the email
        form = RegistrationForm(data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'invalid-email',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_registration_form_invalid_phone_number(self):
        # Test with an invalid phone number to ensure the form is invalid and contains error for the phone_number
        form = RegistrationForm(data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'phone_number': 'phone123',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Phone number can only contain digits.', form.errors['__all__'])

    def test_registration_form_invalid_first_name(self):
        # Test with an invalid first name to ensure the form is invalid and contains error for the first_name
        form = RegistrationForm(data={
            'first_name': 'Jane123',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('First name can only contain letters and white spaces.', form.errors['__all__'])

    def test_registration_form_invalid_last_name(self):
        # Test with an invalid last name to ensure the form is invalid and contains error for the last_name
        form = RegistrationForm(data={
            'first_name': 'Jane',
            'last_name': 'Smith123',
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Last name can only contain letters and white spaces.', form.errors['__all__'])

    def test_registration_form_unique_email(self):
        # Test with a duplicate email to ensure the form is invalid and contains error for the email
        form = RegistrationForm(data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'john.doe@example.com',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('This email is already in use.', form.errors['__all__'])

    def test_registration_form_unique_phone_number(self):
        # Test with a duplicate email to ensure the form is invalid and contains error for the phone_number
        form = RegistrationForm(data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'phone_number': '1234567890',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('This phone number is already in use.', form.errors['__all__'])


class TestEditUserForm(TestCase):

    def setUp(self):
        # Create a user to test the unique constraints
        self.existing_user = User.objects.create(
            first_name="Existing",
            last_name="User",
            email="existinguser@example.com",
            password="password123",
            phone_number="1234567890",
            address="123 Existing Street"
        )

    def test_valid_form(self):
        # Test with valid data to ensure the form is valid
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
            "image": None  # Assuming image field is optional
        }
        form = EditUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_first_name_required(self):
        # Test with an empty first name to ensure the form is invalid and contains error for the first_name
        form_data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("First name can only contain letters and white spaces.", form.errors["__all__"])

    def test_last_name_required(self):
        # Test with an empty last name to ensure the form is invalid and contains error for the last_name
        form_data = {
            "first_name": "John",
            "last_name": "",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Last name can only contain letters and white spaces.", form.errors["__all__"])

    def test_email_required(self):
        # Test with an empty email to ensure the form is invalid and contains error for the email
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Email is not in a valid format.", form.errors["__all__"])

    def test_password_required(self):
        # Test with an empty password to ensure the form is invalid and contains error for the password
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "",
            "phone_number": "9876543210",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Password cannot be empty.", form.errors["__all__"])

    def test_phone_number_required(self):
        # Test with an empty phone number to ensure the form is invalid and contains error for the phone_number
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Phone number can only contain digits.", form.errors["__all__"])

    def test_address_required(self):
        # Test with an empty address to ensure the form is invalid and contains error for the address
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Address cannot be empty.", form.errors["__all__"])

    def test_invalid_phone_number(self):
        # Test with an invalid phone number to ensure the form is invalid and contains error for the phone_number
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "abcd1234",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Phone number can only contain digits.", form.errors["__all__"])

    def test_invalid_email(self):
        # Test with an invalid email to ensure the form is invalid and contains error for the email
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Email is not in a valid format.", form.errors["__all__"])

    def test_invalid_first_name(self):
        # Test with an invalid first name to ensure the form is invalid and contains error for the first_name
        form_data = {
            "first_name": "John123",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("First name can only contain letters and white spaces.", form.errors["__all__"])

    def test_invalid_last_name(self):
        # Test with an invalid last name to ensure the form is invalid and contains error for the last_name
        form_data = {
            "first_name": "John",
            "last_name": "Doe123",
            "email": "john.doe@example.com",
            "password": "password123",
            "phone_number": "9876543210",
            "address": "456 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Last name can only contain letters and white spaces.", form.errors["__all__"])

    def test_duplicate_phone_number(self):
        # Test with a duplicate phone number to ensure the form is invalid and contains error for phone_number
        form_data = {
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "password123",
            "phone_number": "1234567890",  # same as self.existing_user
            "address": "789 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This phone number is already in use.", form.errors["__all__"])

    def test_duplicate_email(self):
        # Test with a duplicate email to ensure the form is invalid and contains error for email
        form_data = {
            "first_name": "New",
            "last_name": "User",
            "email": "existinguser@example.com",  # same as self.existing_user
            "password": "password123",
            "phone_number": "9876543210",
            "address": "789 New Street",
        }
        form = EditUserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("This email is already in use.", form.errors["__all__"])


class TestLoginForm(TestCase):
    def test_login_form_valid_data(self):
        # Test with valid data to ensure the form is valid
        form = LoginForm(data={
            'email': 'user@example.com',
            'password': 'password123',
        })
        self.assertTrue(form.is_valid())

    def test_login_form_empty_fields(self):
        # Test with empty data to ensure the form is invalid and contains 2 errors
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_login_form_invalid_email(self):
        # Test with an invalid email format to ensure the form is invalid and contains error for email
        form = LoginForm(data={
            'email': 'invalid-email',
            'password': 'password123',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid email address.', form.errors['email'])

    def test_login_form_missing_password(self):
        # Test with an invalid password format to ensure the form is invalid and contains error for password
        form = LoginForm(data={
            'email': 'user@example.com',
            'password': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['password'])


class AppointmentFormTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St'
        )

        # Create some sample data for testing
        self.service = Service.objects.create(name='Grooming', description='Pet grooming service')
        self.pet = Pet.objects.create(user=self.user, name='Buddy', breed='Labrador', age=5, medical_notes='None')

    def test_appointment_form_valid_data(self):
        # Test with valid data to ensure the form is valid
        form = AppointmentForm(data={
            'service': self.service.id,
            'pet': self.pet.id,
            'user': self.user.id,
            'start_date_time': '2024-06-01 10:00',
            'description': 'Routine checkup',
        }, user=self.user)
        self.assertTrue(form.is_valid())

    def test_appointment_form_empty_fields(self):
        # Test with empty data to ensure the form is invalid and contains 4 errors
        form = AppointmentForm(data={}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_appointment_form_missing_service(self):
        # Test with a missing service to ensure the form is invalid and contains error for service
        form = AppointmentForm(data={
            'pet': self.pet.id,
            'start_date_time': '2024-06-01 10:00',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('You must select a valid service.', form.errors["__all__"])

    def test_appointment_form_missing_pet(self):
        # Test with a missing service to ensure the form is invalid and contains error for pet
        form = AppointmentForm(data={
            'service': self.service.id,
            'start_date_time': '2024-06-01 10:00',
        })
        self.assertFalse(form.is_valid())
        self.assertIn("You must select a valid pet.", form.errors["__all__"])

    def test_appointment_form_invalid_start_date_time(self):
        # Test with an invalid start date/time to ensure the form is invalid and contains error for start_date_time
        form = AppointmentForm(data={
            'service': self.service.id,
            'pet': self.pet.id,
            'start_date_time': 'invalid-date-time',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Enter a valid date/time.', form.errors['start_date_time'])


class PetFormsTest(TestCase):
    def test_pet_form_valid_data(self):
        # Test with valid data to ensure that both create and edit forms are valid
        form_data = {
            'name': 'Fluffy',
            'breed': 'Labrador',
            'age': 5,
            'medical_notes': 'None',
            'image': None  # Assuming this is optional or you have a default value
        }
        form = PetForm(data=form_data)
        edit_form = EditPetForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertTrue(edit_form.is_valid())

    def test_pet_form_invalid_age(self):
        # Test with an invalid age to ensure the forms are invalid and both forms contain errors for age
        form_data = {
            'name': 'Fluffy',
            'breed': 'Labrador',
            'age': -5,  # Invalid age
            'medical_notes': 'None',
            'image': None
        }
        form = PetForm(data=form_data)
        edit_form = EditPetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Age must be a positive number.', form.errors['__all__'])
        self.assertFalse(edit_form.is_valid())
        self.assertIn('Age must be a positive number.', edit_form.errors['__all__'])

    def test_pet_form_invalid_name(self):
        # Test with an invalid name to ensure the forms are invalid and both forms contain errors for name
        form_data = {
            'name': 'Fluffy12344',  # Invalid name
            'breed': 'Labrador',
            'age': 5,
            'medical_notes': 'None',
            'image': None
        }
        form = PetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Pet can only contain letters and white spaces.', form.errors['__all__'])

    def test_pet_form_invalid_breed(self):
        # Test with an invalid breed to ensure the forms are invalid and both forms contain errors for breed
        form_data = {
            'name': 'Fluffy',
            'breed': 'Labrador44324223', # Invalid age
            'age': 5,
            'medical_notes': 'None',
            'image': None
        }
        form = PetForm(data=form_data)
        edit_form = EditPetForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Breed can only contain letters and white spaces.', form.errors['__all__'])
        self.assertFalse(edit_form.is_valid())
        self.assertIn('Breed can only contain letters and white spaces.', edit_form.errors['__all__'])
