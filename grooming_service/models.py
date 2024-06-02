from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .validators import Validators
from .custom_user_manager import CustomUserManager
import sys


# Define the custom User model, inheriting from AbstractBaseUser and PermissionsMixin for custom user management
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, validators=[Validators.validate_string_input])  # User's first name with validation
    last_name = models.CharField(max_length=50, validators=[Validators.validate_string_input])   # User's last name with validation
    email = models.EmailField(max_length=255, unique=True, error_messages={"unique": "This email is already in use."})  # Unique email field
    password = models.CharField(max_length=30)  # User's password
    phone_number = models.CharField(max_length=30, unique=True, error_messages={"unique": "This phone number is already in use."}, validators=[Validators.validate_phone_number])  # Unique phone number with validation
    address = models.CharField(max_length=100)  # User's address
    image = models.ImageField(upload_to='images/', default='media/images/go9xwcxemxj7sajmn1zf')  # User's profile image with a default value
    is_staff = models.BooleanField(default=False)  # Indicates if the user is a staff member
    is_active = models.BooleanField(default=True)  # Indicates if the user is active

    USERNAME_FIELD = "email"  # Set the username field to email for authentication

    objects = CustomUserManager()  # Use the custom user manager

    def __str__(self):
        return self.email  # String representation of the user

    class Meta:
        if 'test' not in sys.argv:
            db_table = 'woof_wash_grooming"."User'  # Point to the posgres schema for the database table for non-test environments


# Define the Service model
class Service(models.Model):
    name = models.CharField(max_length=50)  # Name of the service
    description = models.TextField()  # Detailed description of the service
    vary_price1 = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Variable price 1 for the service
    vary_price2 = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Variable price 2 for the service
    image = models.ImageField(upload_to='images/', default='media/images/rlbpt7uaqhxanu59ro9r')  # Image for the service with a default value
    short_description = models.TextField(default="")  # Short description of the service

    def __str__(self):
        return self.name  # String representation of the service

    class Meta:
        if 'test' not in sys.argv:
            db_table = 'woof_wash_grooming"."Service'   # Point to the posgres schema for the database table for non-test environments


# Define the Pet model
class Pet(models.Model):
    name = models.CharField(max_length=255)  # Name of the pet
    breed = models.CharField(max_length=255)  # Breed of the pet
    age = models.IntegerField()  # Age of the pet
    medical_notes = models.TextField(null=True)  # Medical notes about the pet, nullable
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the owner user
    image = models.ImageField(upload_to='images/', default='media/images/tey9seavfcldmybatmmt')  # Image of the pet with a default value

    def __str__(self):
        # String representation of the pet
        return self.name

    class Meta:
        if 'test' not in sys.argv:
            db_table = 'woof_wash_grooming"."Pet'   # Point to the posgres schema for the database table for non-test environments


# Define status choices for appointments
STATUS = ((1, "booked"), (2, "completed"))


# Define the Appointment model
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Reference to the service
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)  # Reference to the pet
    status = models.IntegerField(choices=STATUS, default=0)  # Status of the appointment with choices
    start_date_time = models.DateTimeField()  # Start date and time of the appointment
    description = models.TextField(null=True)  # Description of the appointment, nullable

    class Meta:
        if 'test' not in sys.argv:
            db_table = 'woof_wash_grooming"."Appointment'  # Point to the posgres schema for the database table for non-test environments

    def __str__(self):
        return f"{self.pet}"  # String representation of the appointment
