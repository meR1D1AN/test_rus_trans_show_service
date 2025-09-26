from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from users.views import CustomLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        CustomLoginView.as_view(next_page="transport_app:order_list"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="login"),
        name="logout",
    ),
    path("trans/", include("transport_app.urls")),
    path(
        "users/",
        include("users.urls"),
        name="users",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
