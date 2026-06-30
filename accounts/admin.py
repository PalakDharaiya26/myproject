# Django imports
from django.contrib import admin

# Local imports
from .models import CustomUser

admin.site.register(CustomUser)
