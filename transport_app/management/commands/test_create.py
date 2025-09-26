import os
import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker
from tqdm import tqdm

from conts.choices import OrderChoices, RoleChoices
from transport_app.models import Location, Order, User


class Command(BaseCommand):
    help = "Команда для создания тестовых данных"

    def handle(self, *args, **kwargs):
        self.fake = Faker("ru_RU")

        with transaction.atomic():
            self.create_fixed_users()
            self.create_random_users()
            self.create_orders()
            self.create_locations()

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
                "username": "manager",
                "password": "manageR1",
                "first_name": "Наташа",
                "last_name": "Менеджеровна",
                "email": "manager_natasha@mer1d1an.ru",
                "role": RoleChoices.MANAGER,
                "is_superuser": False,
            },
            {
                "username": "driver",
                "password": "driveR1",
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

    def create_orders(self):
        managers = list(User.objects.filter(role=RoleChoices.MANAGER))
        drivers = list(User.objects.filter(role=RoleChoices.DRIVER))

        orders_create = []
        for _ in tqdm(range(1000), desc="Создание заявок"):
            manager = random.choice(managers)
            driver = random.choice(drivers)

            order = Order(
                description=self.fake.text(max_nb_chars=100),
                from_location=self.fake.address(),
                to_location=self.fake.address(),
                status=OrderChoices.CREATED,
                manager=manager,
                driver=driver,
            )
            if order.status == OrderChoices.CREATED:
                if random.random() < 0.5:
                    pass
                else:
                    if random.random() < 0.5:
                        order.status = OrderChoices.IN_PROGRESS
                    else:
                        order.status = OrderChoices.COMPLETED
            if order.driver and order.status == OrderChoices.CREATED:
                order.status = OrderChoices.ASSIGNED

            orders_create.append(order)

        Order.objects.bulk_create(orders_create)
        self.stdout.write(self.style.SUCCESS("Тестовые заявки созданы."))

    def create_locations(self):
        assigned_orders = Order.objects.filter(status=OrderChoices.ASSIGNED)

        locations_create = []
        for order in tqdm(assigned_orders, desc="Создание местоположений"):
            num_locations = random.randint(1, 5)

            for _ in range(num_locations):
                latitude = round(random.uniform(41.18, 81.86), 6)
                longitude = round(random.uniform(19.62, 169.03), 6)

                location = Location(
                    order=order,
                    driver=order.driver,
                    latitude=latitude,
                    longitude=longitude,
                )
                locations_create.append(location)

        Location.objects.bulk_create(locations_create)
        self.stdout.write(self.style.SUCCESS("Тестовые местоположения созданы. "))
