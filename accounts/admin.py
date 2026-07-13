from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, PasswordResetOTP


class PasswordResetOTPInline(admin.TabularInline):
    model = PasswordResetOTP
    extra = 0
    can_delete = False


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [PasswordResetOTPInline]
