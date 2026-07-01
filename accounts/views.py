# Python imports
import logging

# Django imports
from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .Register import RegisterForm
 
User = get_user_model()
logger = logging.getLogger(__name__)


def register_view(request: HttpRequest) -> HttpResponse:
    """Registers a new user after validating the registration form."""

    logger.info("Register page accessed")

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            mobile = form.cleaned_data.get("mobile")
            address = form.cleaned_data.get("address")

            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.mobile = mobile
            user.address = address
            user.save()
            logger.info(f"User '{username}' registered successfully")
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
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
        logger.info(f"User '{username}' logged in successfully")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"User '{username}' logged in successfully")
            return redirect("home")
        else:
            logger.warning(f"Failed login attempt for username '{username}'")
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


@login_required(login_url="login")
def dashboard(request):
    logger.info(f"Dashboard accessed by '{request.user.username}'")
    return render(request, "dashboard.html")


@login_required(login_url="login")
def profile(request: HttpRequest) -> HttpResponse:
    """
    Allows the user to update username, email, mobile number, address, and password after validation.
    """

    user = request.user
    logger.info(f"Profile page accessed by '{user.username}'")

    context = {
        "user": user,
        "success_msg": "",
        "mobile_error": "",
        "old_password_error": "",
        "password_error": "",
    }

    if request.method == "POST":
        mobile = request.POST.get("mobile")
        username = request.POST.get("username")
        address = request.POST.get("address")

        old = request.POST.get("old_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")
        if mobile:
            if not mobile.isdigit():
                context["mobile_error"] = "Mobile must contain only numbers"
            elif len(mobile) != 10:
                context["mobile_error"] = "Mobile must be 10 digits"

        if old and new and confirm:
            if not check_password(old, user.password):
                context["old_password_error"] = "Old password is incorrect"

            elif new != confirm:
                context["password_error"] = "New password & confirm do not match"

            elif old == new:
                context["password_error"] = (
                    "New password cannot be same as old password"
                )

        if (
            not context["mobile_error"]
            and not context["old_password_error"]
            and not context["password_error"]
        ):

            user.username = username
            user.mobile = mobile
            user.address = address

            if old and new and confirm:
                user.set_password(new)
                logger.info(f"Password updated for '{user.username}'")
                update_session_auth_hash(request, user)
            user.save()
            logger.info(f"Profile updated for '{user.username}'")
            context["success_msg"] = "Profile updated successfully!"
    return render(request, "profile.html", context)


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Logs out the current user and redirects to the login page.
    """
    username = request.user.username
    logger.info(f"User '{username}' logged out")
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect("login")
