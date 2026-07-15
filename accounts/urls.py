# django imports
from django.urls import path

# Local imports
from accounts import views as web_views

urlpatterns = [
    path("register/", web_views.register_view, name="register"),
    path("login/", web_views.login_view, name="login"),
    path("profile/", web_views.profile, name="profile"),
    path("dashboard/", web_views.dashboard, name="home"),
    path("logout/", web_views.logout_view, name="logout"),
    path(
        "forgot-password/",
        web_views.forgot_password,
        name="forgot_password",
    ),
    path(
        "verify-otp/",
        web_views.verify_otp,
        name="verify_otp",
    ),
    path(
        "reset-password/",
        web_views.reset_password,
        name="reset_password",
    ),
    path(
        "resend-otp/",
        web_views.resend_otp,
        name="resend_otp",
    ),
]
