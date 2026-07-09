# Django imports
from django.contrib import admin

# Local imports
from .models import CustomUser, PasswordResetOTP

admin.site.register(CustomUser)
admin.site.register(PasswordResetOTP)
