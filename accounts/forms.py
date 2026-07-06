# Django imports
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    Model form for user registration.

    Fields:
        username (Model field): User's unique username.
        email (Model field): User's email address.
        mobile_number (Model field): User's mobile number.
        address (Model field): User's address.
        password (CharField): User's password.
        confirm_password (CharField): Password confirmation.
    """

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "mobile_number", "address"]
        widgets = {
            "address": forms.Textarea(),
        }

    def clean_password(self):
        """
        validate the password

        Ensures the password contains at least 8 characters,
        one uppercase letter, one lowercase letter, and one number
        """
        password = self.cleaned_data.get("password")

        if not password:
            return password

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")

        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter"
            )

        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                "Password must contain at least one lowercase letter"
            )

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number")

        return password

    def clean_mobile_number(self):
        """
        Validates the mobile_number

        Ensures the mobile number contains only digits.
        """
        mobile_number = self.cleaned_data.get("mobile_number")

        if not mobile_number.isdigit():
            raise forms.ValidationError(
                "mobile_number number must contain only numbers."
            )

        return mobile_number

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data
