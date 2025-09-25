from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from conts.choices import OrderChoices, RoleChoices
from conts.models import NULLABLE
from users.models import User


class Order(models.Model):
    """
    Модель заявки.
    """

    description = models.TextField(
        verbose_name="Описание заявки",
        help_text="Введите описание заявки",
    )
    from_location = models.CharField(
        max_length=200,
        verbose_name="Откуда",
        help_text="Адрес загрузки",
        **NULLABLE,
    )
    to_location = models.CharField(
        max_length=200,
        verbose_name="Куда",
        help_text="Адрес доставки",
        **NULLABLE,
    )
    status = models.CharField(
        max_length=13,
        verbose_name="Статус заявки",
        help_text="Выберите статус заявки",
        choices=OrderChoices.choices,
        default=OrderChoices.CREATED,
    )
    manager = models.ForeignKey(
        User,
        verbose_name="Менеджер",
        help_text="Выберите менеджера",
        on_delete=models.CASCADE,
        related_name="managed_orders",
        limit_choices_to={"role": RoleChoices.MANAGER},
    )
    driver = models.ForeignKey(
        User,
        verbose_name="Водитель",
        help_text="Выберите водителя",
        on_delete=models.SET_NULL,
        related_name="driver_orders",
        limit_choices_to={"role": RoleChoices.DRIVER},
        **NULLABLE,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания заявки",
        help_text="Дата и время создания заявки автоматически назначается при создании заявки",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"№-{self.id}: {self.description[:20]} ({self.status})"


@receiver(pre_save, sender=Order)
def set_assigned_status(sender, instance, **kwargs):
    if instance.driver and instance.status == OrderChoices.CREATED:
        instance.status = OrderChoices.ASSIGNED


class Location(models.Model):
    """
    Модель местоположения.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заявка",
        help_text="Выберите заявку",
        related_name="locations",
        **NULLABLE,
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Водитель",
        help_text="Выберите водителя",
        related_name="locations",
        limit_choices_to={"role": RoleChoices.DRIVER},
        **NULLABLE,
    )
    latitude = models.FloatField(
        verbose_name="Широта",
        help_text="Широта (от -90 до 90)",
        default=55.682935,
        validators=[
            MinValueValidator(-90.0),
            MaxValueValidator(90.0),
        ],
    )
    longitude = models.FloatField(
        verbose_name="Долгота",
        help_text="Долгота (от -180 до 180)",
        default=37.865576,
        validators=[
            MinValueValidator(-180.0),
            MaxValueValidator(180.0),
        ],
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата и время создания местоположения",
        help_text="Введите дату и время создания местоположения",
        default=timezone.now,
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Позиция {self.driver.get_full_name()} ({self.latitude}, {self.longitude})"


class Document(models.Model):
    """
    Модель документа.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заявка",
        help_text="Выберите заявку",
        related_name="documents",
    )
    file = models.ImageField(
        verbose_name="Фотография документа",
        help_text="Загрузите фото транспортной документации (JPEG/PNG)",
        upload_to="documents/%Y/%m/%d/",
        blank=True,
    )
    uploaded_at = models.DateTimeField(
        verbose_name="Дата загрузки",
        help_text="Дата и время загрузки документа автоматически назначается при загрузке документа",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return f"Фото для заявки №-{self.order.id} {self.order.description[:30]}."
