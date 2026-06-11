from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render

from .Register import RegisterForm

User = get_user_model()


# register
def register_view(request):
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
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below")
    return render(request, "register.html", {"form": form})


# login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "login.html")


# dashboard
def dashboard(request):
    return render(request, "dashboard.html")


# profile
@login_required
def profile(request):
    user = request.user
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
        email = request.POST.get("email")
        address = request.POST.get("address")

        old = request.POST.get("old_password")
        new = request.POST.get("new_password")
        confirm = request.POST.get("confirm_password")
        # mobile validation
        if mobile:
            if not mobile.isdigit():
                context["mobile_error"] = "Mobile must contain only numbers"
            elif len(mobile) != 10:
                context["mobile_error"] = "Mobile must be 10 digits"
        # password validation
        if old or new or confirm:
            if not check_password(old, user.password):
                context["old_password_error"] = "Old password is incorrect"
            elif new != confirm:
                context["password_error"] = "New password & confirm do not match"

        if (
            not context["mobile_error"]
            and not context["old_password_error"]
            and not context["password_error"]
        ):

            user.username = username
            user.email = email
            user.mobile = mobile
            user.address = address

            if old and new and confirm:
                user.set_password(new)
                update_session_auth_hash(request, user)
            user.save()
            context["success_msg"] = "Profile updated successfully!"
    return render(request, "profile.html", context)


# logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return redirect("login")
