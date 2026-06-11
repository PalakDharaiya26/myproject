from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from accounts import views as web_views
from quickstart import views as api_views

router = routers.DefaultRouter()
router.register(r"users", api_views.UserViewSet)
router.register(r"groups", api_views.GroupViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", web_views.register_view),
    path("login/", web_views.login_view, name="login"),
    path("dashboard/", web_views.dashboard, name="home"),
    path("logout/", web_views.logout_view, name="logout"),
    path("profile/", web_views.profile, name="profile"),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
