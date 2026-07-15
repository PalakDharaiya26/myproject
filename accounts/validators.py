# django imports
from django import forms


def validate_password_strength(password):
    """
    Validate password strength.
    """

    if len(password) < 8:
        raise forms.ValidationError("Password must be at least 8 characters.")

    if not any(char.isupper() for char in password):
        raise forms.ValidationError(
            "Password must contain at least one uppercase letter."
        )

    if not any(char.islower() for char in password):
        raise forms.ValidationError(
            "Password must contain at least one lowercase letter."
        )

    if not any(char.isdigit() for char in password):
        raise forms.ValidationError("Password must contain at least one number.")
