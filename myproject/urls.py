from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from quickstart import views as api_views

router = routers.DefaultRouter()
router.register(r"users", api_views.UserViewSet)
router.register(r"groups", api_views.GroupViewSet)

urlpatterns = [

    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("snippets/", include("snippets.urls")),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)