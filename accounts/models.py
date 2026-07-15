# Django imports
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

phone_validator = RegexValidator(
    regex=r"^\d{1,15}$",
    message="Mobile number must contain only numbers.",
)


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Fields:
        email (EmailField): Stores the user's unique email address.
        mobile_number (CharField): Stores the user's mobile number (maximum 15 characters).
        address (TextField): Stores the user's address.
    """

    email = models.EmailField(unique=True)
    mobile_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[phone_validator],
    )
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Return the username of the user.
        """
        return self.username


class PasswordResetOTP(models.Model):
    """
    Stores OTP for password reset.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
    )

    otp = models.CharField(max_length=6)

    expiry_time = models.DateTimeField()

    created_at = models.DateTimeField(
        default=timezone.now,
    )

    def __str__(self):
        return f"{self.user.username} - {self.otp}"
