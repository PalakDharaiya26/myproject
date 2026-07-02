# Django imports
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    Fields:
        email (EmailField): Stores the user's unique email address.
        mobile_number (CharField): Stores the user's mobile number (maximum 15 characters).
        address (TextField): Stores the user's address.
        profile_pic (ImageField): Stores the user's profile picture.
    """

    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Return the username of the user.
        """
        return self.username
