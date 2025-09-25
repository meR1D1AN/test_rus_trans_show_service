from django.db.models import TextChoices


class OrderChoices(TextChoices):
    """
    Класс для выбора статуса заявки.
    """

    CREATED = "Created", "Создана"
    ASSIGNED = "Assigned", "Назначена"
    IN_PROGRESS = "In progress", "Выполняется"
    COMPLETED = "Completed", "Завершена"


class RoleChoices(TextChoices):
    """
    Класс для выбора роли пользователя.
    """

    ADMIN = "Admin", "Администратор"
    MANAGER = "Manager", "Менеджер"
    DRIVER = "Driver", "Водитель"
