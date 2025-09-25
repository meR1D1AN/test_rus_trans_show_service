from django.urls import path

from users.apps import UsersConfig
from users.views import UserListView

app_name = UsersConfig.name

urlpatterns = [
    path("list/", UserListView.as_view(), name="user_list"),
]
