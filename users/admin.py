from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "username",
        "email",
        "role",
    )
    list_display_links = (
        "id",
        "first_name",
        "username",
    )
