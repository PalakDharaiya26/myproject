"""
Models for the Accounts application.

This module contains the custom user model used for
user authentication and profile management.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model with additional fields such as
    mobile number, address, and profile picture.
    """

    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(blank=True, null=True)

    def __str__(self):
        """
        Return the username of the user.
        """
        return self.username
