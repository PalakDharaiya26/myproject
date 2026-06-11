from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea, required=False)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data.get("password")

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

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")

        if not mobile.isdigit() or len(mobile) != 10:
            raise forms.ValidationError("Mobile number must be 10 digits")

        return mobile

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data
