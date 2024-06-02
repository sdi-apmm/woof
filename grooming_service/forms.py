from django import forms
from django.core.exceptions import ValidationError
from django_flatpickr.schemas import FlatpickrOptions
from django_flatpickr.widgets import DateTimePickerInput

from .models import *


# Base form class to handle common functionalities
class BaseForm(forms.ModelForm):
    # Adds common CSS classes to form fields
    def add_field_classes(self, fields):
        for field in fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'required': 'true'})

    # Static method that validates fields based on given criteria
    @staticmethod
    def validate_fields(cleaned_data, fields_to_validate):
        errors = []
        for field, message, regex in fields_to_validate:
            value = cleaned_data.get(field)
            if regex:
                # Validates field value against regex
                errors = Validators.append_error_messages_when_field_does_not_match_regex(value, regex, message, errors)
            # Validates if the field is empty
            errors = Validators.append_error_messages_when_field_is_empty(value, message, errors)
        return errors


# Form for user registration
class RegistrationForm(BaseForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "phone_number", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_field_classes(self.fields.keys())
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'required': 'true'})

    def clean(self):
        cleaned_data = super().clean()
        # Validates fields using the base class method
        errors = self.validate_fields(cleaned_data, [
            ("first_name", "First name can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("last_name", "Last name can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("email", "Email is not in a valid format.", r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'),
            ("password", "Password cannot be empty.", None),
            ("phone_number", "Phone number can only contain digits.", r'^\d+$'),
            ("address", "Address cannot be empty.", None),
        ])

        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        # Checks if email and phone number are unique
        errors = Validators.append_uniqueness_error(email, User, "email", "This email is already in use.", errors)
        errors = Validators.append_uniqueness_error(phone_number, User, "phone_number",
                                                    "This phone number is already in use.", errors)

        if errors:
            raise ValidationError(errors)

        return cleaned_data


# Form for editing user information
class EditUserForm(BaseForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "phone_number", "address", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adds common CSS classes to form fields except the image as it should not be a required field
        keys_excluding_image = [key for key in self.fields.keys() if key != 'image']
        self.add_field_classes(keys_excluding_image)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        # Validates fields using the base class method
        errors = self.validate_fields(cleaned_data, [
            ("first_name", "First name can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("last_name", "Last name can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("email", "Email is not in a valid format.", r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'),
            ("password", "Password cannot be empty.", None),
            ("phone_number", "Phone number can only contain digits.", r'^\d+$'),
            ("address", "Address cannot be empty.", None),
        ])

        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        # Checks if email and phone number are unique only if email and phone number are not the same as currently
        # stored ones
        if email and email != self.instance.email:
            errors = Validators.append_uniqueness_error(email, User, "email", "This email is already in use.", errors)

        if phone_number and phone_number != self.instance.phone_number:
            errors = Validators.append_uniqueness_error(phone_number, User, "phone_number",
                                                        "This phone number is already in use.", errors)

        if errors:
            raise ValidationError(errors)

        return cleaned_data


# Form for user login
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Form for scheduling an appointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["service", "pet", "start_date_time", "description"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # Customizes the date and time picker input widget using Django Flatpickr
        self.fields["start_date_time"].widget = DateTimePickerInput(
            options=FlatpickrOptions(
                altFormat="d-m-Y H:i",
            )
        )

        self.fields["start_date_time"].widget.attrs.update({'class': 'form-control', 'required': 'true'})

        # Choices for the service and pet fields
        self.fields["service"] = forms.ModelChoiceField(
            queryset=Service.objects.all(),
            required=True,
            empty_label="Select a service"
        )
        self.fields["service"].widget.attrs.update({'class': 'form-control'})

        self.fields["pet"] = forms.ModelChoiceField(
            queryset=Pet.objects.none(),
            required=True,
            empty_label="Select a pet"
        )
        self.fields["description"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter additional information here...'
            })
        )
        self.fields["pet"].widget.attrs.update({'class': 'form-control'})
        if user:
            # Filters pets by the user
            self.fields["pet"].queryset = Pet.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        service = cleaned_data.get("service")
        pet = cleaned_data.get("pet")

        if service is None:
            errors.append("You must select a valid service.")
        if pet is None:
            errors.append("You must select a valid pet.")
        if errors:
            raise ValidationError(errors)

        return cleaned_data


# Form for creating a pet
class PetForm(BaseForm):
    class Meta:
        model = Pet
        fields = ["name", "breed", "age", "medical_notes", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adds common CSS classes to form fields except the medical_notes as it should not be a required field
        keys_excluding_medical_notes = [key for key in self.fields.keys() if key != 'medical_notes']
        self.add_field_classes(keys_excluding_medical_notes)
        self.fields["medical_notes"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter additional information here...'
            })
        )

    def clean(self):
        cleaned_data = super().clean()
        errors = self.validate_fields(cleaned_data, [
            ("name", "Pet can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("breed", "Breed can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("age", "Age cannot be empty", None)
        ])
        age = cleaned_data.get("age")
        if age and age <= 0:
            errors.append("Age must be a positive number.")

        if errors:
            raise ValidationError(errors)
        return cleaned_data


# Form for editing a pet
class EditPetForm(BaseForm):
    class Meta:
        model = Pet
        fields = ["name", "breed", "age", "medical_notes", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"] = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'edit_pet_name'})
        )

        self.fields["breed"] = forms.CharField(
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'edit_pet_breed'}),
        )

        self.fields["age"] = forms.IntegerField(
            required=True,
            widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'edit_pet_age'})
        )

        self.fields["medical_notes"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'edit_medical_notes',
                'placeholder': 'Enter additional information here...'
            })
        )

        self.fields['image'].widget.attrs.update({'class': 'form-control', 'id': 'edit_pet_image'})

    def clean(self):
        cleaned_data = super().clean()
        errors = self.validate_fields(cleaned_data, [
            ("name", "Pet can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("breed", "Breed can only contain letters and white spaces.", r'^[A-Za-z\s]+$'),
            ("age", "Age cannot be empty", None)
        ])
        age = cleaned_data.get("age")
        if age and age <= 0:
            errors.append("Age must be a positive number.")

        if errors:
            raise ValidationError(errors)
        return cleaned_data
