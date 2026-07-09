# Python imports
import logging
import random
from datetime import timedelta

from django.conf import settings

# Django imports
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import (
    ForgotPasswordForm,
    OTPForm,
    ProfileForm,
    RegisterForm,
    ResetPasswordForm,
)
from .models import PasswordResetOTP

User = get_user_model()
logger = logging.getLogger(__name__)


def register_view(request: HttpRequest) -> HttpResponse:
    """Registers a new user after validating the registration form."""

    logger.info("Register page accessed")

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            logger.info("User '%s' registered successfully", user.username)
            messages.success(request, "Account created successfully!")
            return redirect("login")

        else:
            logger.warning("Registration failed: %s", form.errors)
            messages.error(request, "Please correct the errors below")

    return render(request, "register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Checks the username and password. If they are correct,the user is logged in and redirected to the home page.
    """
    logger.info("Login page accessed")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info("User '%s' logged in successfully", username)
            return redirect("home")
        else:
            logger.warning("Failed login attempt for username '%s'", username)
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request: HttpRequest) -> HttpResponse:
    logger.info("Dashboard accessed by '%s'", request.user.username)
    return render(request, "dashboard.html")


@login_required(login_url="login")
def profile(request: HttpRequest) -> HttpResponse:
    """
    Update user profile using ProfileForm
    """

    user = request.user
    logger.info("Profile page accessed by '%s'", user.username)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            updated_user = form.save()
            update_session_auth_hash(request, updated_user)

            logger.info("Profile updated for '%s'", user.username)
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)
    return render(request, "profile.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logs out the current user and redirects to the login page.
    """
    username = request.user.username
    logger.info("User '%s' logged out", username)
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect("login")


def forgot_password(request):
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(email=email)

                otp = str(random.randint(100000, 999999))

                PasswordResetOTP.objects.filter(user=user).delete()

                PasswordResetOTP.objects.create(
                    user=user,
                    otp=otp,
                    expiry_time=timezone.now() + timedelta(minutes=2),
                )

                request.session["reset_user"] = user.id

                send_mail(
                    "Password Reset OTP",
                    f"Your OTP is: {otp}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent successfully.")
                return redirect("verify_otp")

            except User.DoesNotExist:
                messages.error(request, "Email not found.")
    else:
        form = ForgotPasswordForm()

    return render(request, "forgot_password.html", {"form": form})


def verify_otp(request):
    if request.method == "POST":
        form = OTPForm(request.POST)

        if form.is_valid():
            otp = form.cleaned_data["otp"]

            user_id = request.session.get("reset_user")

            otp_record = PasswordResetOTP.objects.get(user_id=user_id)

            if not otp_record:
                messages.error(request, "OTP not found.")
                return redirect("forgot_password")

            if timezone.now() > otp_record.expiry_time:
                otp_record.delete()
                messages.error(request, "OTP expired.")
                return redirect("forgot_password")

            if otp == otp_record.otp:
                return redirect("reset_password")

            messages.error(request, "Invalid OTP.")
    else:
        form = OTPForm()

    return render(request, "verify_otp.html", {"form": form})


def reset_password(request):
    user_id = request.session.get("reset_user")

    if not user_id:
        messages.error(request, "Session expired.")
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data["new_password"]

            user.set_password(new_password)
            user.save()

            PasswordResetOTP.objects.filter(user=user).delete()
            request.session.pop("reset_user", None)

            messages.success(request, "Password changed successfully.")
            return redirect("login")
    else:
        form = ResetPasswordForm()

    return render(request, "reset_password.html", {"form": form})


def resend_otp(request):
    user_id = request.session.get("reset_user")

    if not user_id:
        messages.error(request, "Session expired.")
        return redirect("forgot_password")

    user = User.objects.get(id=user_id)

    otp = str(random.randint(100000, 999999))

    PasswordResetOTP.objects.filter(user=user).delete()

    PasswordResetOTP.objects.create(
        user=user,
        otp=otp,
        expiry_time=timezone.now() + timedelta(minutes=2),
    )

    send_mail(
        "Password Reset OTP",
        f"Your new OTP is: {otp}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    messages.success(request, "A new OTP has been sent to your email.")
    return redirect("verify_otp")
