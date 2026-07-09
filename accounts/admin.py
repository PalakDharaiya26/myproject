# Django imports
from django.contrib import admin
from .models import PasswordResetOTP

# Local imports
from .models import CustomUser

admin.site.register(CustomUser)
admin.site.register(PasswordResetOTP)
