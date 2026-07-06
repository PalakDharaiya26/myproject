from django.urls import path

from accounts import views as web_views

urlpatterns = [
    path("register/", web_views.register_view, name="register"),
    path("login/", web_views.login_view, name="login"),
    path("profile/", web_views.profile, name="profile"),
    path("dashboard/", web_views.dashboard, name="home"),
    path("logout/", web_views.logout_view, name="logout"),
]
