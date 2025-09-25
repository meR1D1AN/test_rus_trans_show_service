import os

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker
from tqdm import tqdm

from conts.choices import RoleChoices
from transport_app.models import User


class Command(BaseCommand):
    help = "Команда для создания тестовых данных"

    def handle(self, *args, **kwargs):
        self.fake = Faker("ru_RU")

        with transaction.atomic():
            self.create_fixed_users()
            self.create_random_users()

    def create_fixed_users(self):
        users_data = [
            {
                "username": os.getenv("ADMIN_USERNAME"),
                "password": os.getenv("ADMIN_PASSWORD"),
                "first_name": "Админ",
                "last_name": "Админов",
                "email": "admin@admin.com",
                "role": RoleChoices.ADMIN,
                "is_superuser": True,
            },
            {
                "username": "manager_natasha",
                "password": "manager_natashA1",
                "first_name": "Наташа",
                "last_name": "Менеджеровна",
                "email": "manager_natasha@mer1d1an.ru",
                "role": RoleChoices.MANAGER,
                "is_superuser": False,
            },
            {
                "username": "driver_nikita",
                "password": "driver_nikitA1",
                "first_name": "Никита",
                "last_name": "Водилов",
                "email": "driver_nikita@mer1d1an.ru",
                "role": RoleChoices.DRIVER,
                "is_superuser": False,
            },
        ]

        for user_data in users_data:
            self.create_single_user(**user_data)

    def create_single_user(
        self,
        username,
        password,
        first_name,
        last_name,
        email,
        role,
        is_superuser,
    ):
        if not User.objects.filter(username=username).exists():
            if is_superuser:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                )
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                )
            user.set_password(password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Создан тестовый пользователь c username = {user.username} (роль: {role}).")
            )
        else:
            self.stdout.write(self.style.WARNING(f"Пользователь с username = {username} уже существует."))

    def create_random_users(self):
        test_password = "random_passworD1"
        hashed_password = make_password(test_password)
        roles_data = [
            (RoleChoices.MANAGER, 10, "Создание менеджеров"),
            (RoleChoices.DRIVER, 10, "Создание водителей"),
        ]
        users_to_create = []

        for role, count, desc in roles_data:
            for _ in tqdm(range(count), desc=desc):
                user = User(
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    username=self.fake.user_name(),
                    password=hashed_password,
                    email=self.fake.email(),
                    role=role,
                )
                users_to_create.append(user)

        User.objects.bulk_create(users_to_create)
        self.stdout.write(self.style.SUCCESS("Тестовые менеджеры и водители созданы."))
