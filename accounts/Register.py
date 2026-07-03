# Django imports
from django import forms


class RegisterForm(forms.Form):
    """
    Form for user registration
        username (CharField): Stores the unique username of the user.
        email (EmailField): Stores the user's official email address.
        mobile_number (CharField): Stores the user's mobile_number.
        address (CharField): Stores the residential or communication address.
        password (CharField): Stores the secure account password.
        confirm_password (CharField): Stores the confirmation password to verify against the original.
    """

    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    mobile_number = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

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
