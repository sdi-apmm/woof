import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Validators:
    """
    Utility class containing validation methods.
    """

    def validate_string_input(value):
        """
       Validation method that checks if a given string contains only letters (a-z, A-Z).
       If the string contains anything other than letters, it raises a ValidationError.

       Args:
           value (str): The string value to validate.

       Raises:
           ValidationError: If the string contains non-letter characters.
       """
        # Regular expressions to check if the input contains only letters.
        if not re.match("^[a-zA-Z]+$", value):
            raise ValidationError(_("This field must contain only letters."))

    def validate_phone_number(value):
        """
         Validation method that checks if a given string contains only digits (0-9).
          If the string contains anything other than digits, it raises a ValidationError.

          Args:
              value (str): The phone number string to validate.

          Raises:
              ValidationError: If the phone number contains non-digit characters.
          """
        # Regular expressions to check if the input contains only letters.
        if not re.match(r"^\d+$", value):
            raise ValidationError("Phone number can contain only digits.")

    @staticmethod
    def append_error_messages_when_field_is_empty(field, message, errors):
        """
           Validation method that checks if a field is empty and appends an error message if it is.

           Args:
               field: The field value to check.
               message (str): The error message to append if the field is empty.
               errors (list): The list of current errors.

           Returns:
               list: The updated list of errors.
        """
        if not field:
            errors.append(message)
        return errors

    @staticmethod
    def append_error_messages_when_field_does_not_match_regex(field, regex, message, errors):
        """
        Validation method that checks if a field's value matches a given regex pattern and appends an error message
        if it does not.

           Args:
               field: The field value to check.
               regex (str): The regex pattern to match against.
               message (str): The error message to append if the field does not match the regex.
               errors (list): The list of current errors.

           Returns:
               list: The updated list of errors.
        """
        if field and not re.match(regex, field):
            errors.append(message)
        return errors

    @staticmethod
    def append_uniqueness_error(field, model, field_name, message, errors):
        """
        Validation method that checks if a field's value is unique within a given model and appends an error message
        if it is not.

           Args:
               field: The field value to check.
               model: The Django model to check against.
               field_name (str): The name of the field in the model to check for uniqueness.
               message (str): The error message to append if the field value is not unique.
               errors (list): The list of current errors.

           Returns:
               list: The updated list of errors.
        """
        if field:
            if model.objects.filter(**{field_name: field}).exists():
                errors.append(message)
        return errors
