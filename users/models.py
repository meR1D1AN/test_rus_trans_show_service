from django.contrib.auth.models import AbstractUser
from django.db import models

from conts.choices import RoleChoices


class User(AbstractUser):
    role = models.CharField(
        max_length=13,
        verbose_name="Роль",
        help_text="Выберите роль",
        choices=RoleChoices.choices,
        default=RoleChoices.MANAGER,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"
