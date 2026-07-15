# Django imports
from django import forms
from django.contrib.auth import get_user_model

from .validators import validate_password_strength

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

    def clean_mobile_number(self):
        """
        Validates the mobile_number

        Ensures the mobile number contains only digits.
        """
        mobile_number = self.cleaned_data.get("mobile_number")

        if mobile_number and not mobile_number.isdigit():
            raise forms.ValidationError("mobile number must contain  only digits.")

        return mobile_number

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password:
            validate_password_strength(password)

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get("password")

        if commit:
            user.set_password(password)
            user.save()

        return user


class ProfileForm(forms.ModelForm):
    """
    Model form for updating user profile.
    """

    old_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ["username", "email", "mobile_number", "address"]
        widgets = {
            "address": forms.Textarea(),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Username already exists.")

        return username

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")

        if mobile_number and not mobile_number.isdigit():
            raise forms.ValidationError("Only digits allowed")

        return mobile_number

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("Email already exists.")

        return email

    def clean(self):
        cleaned_data = super().clean()

        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if not (old_password or new_password or confirm_password):
            return cleaned_data

        if not old_password:
            raise forms.ValidationError("Old password is required.")

        if not self.instance.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")

        if not new_password:
            raise forms.ValidationError("New password is required.")

        if not confirm_password:
            raise forms.ValidationError("Confirm password is required.")

        validate_password_strength(new_password)

        if new_password != confirm_password:
            raise forms.ValidationError(
                "New password  and confirm password do not match."
            )

        if old_password == new_password:
            raise forms.ValidationError(
                "New password cannot be same as the old password."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        new_password = self.cleaned_data.get("new_password")

        if new_password:
            user.set_password(new_password)

        if commit:
            user.save()

        return user


class ForgotPasswordForm(forms.Form):
    """Form to request password reset OTP."""

    email = forms.EmailField()


class OTPForm(forms.Form):
    """Form for OTP verification."""

    otp = forms.CharField(max_length=6)


class ResetPasswordForm(forms.Form):
    """Form for resetting user password."""

    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password:
            validate_password_strength(new_password)

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
