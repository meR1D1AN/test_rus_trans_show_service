from django.contrib import admin
from django.utils.safestring import mark_safe

from transport_app.models import Document, Location, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "from_location",
        "to_location",
        "driver",
        "manager",
        "status",
        "created_at",
    )
    list_display_links = (
        "id",
        "driver",
        "manager",
    )
    ordering = ("-created_at",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "timestamp",
        "driver",
        "get_latitude_and_longitude",
    )
    list_display_links = (
        "id",
        "order",
    )

    def get_latitude_and_longitude(self, obj):
        if obj.latitude and obj.longitude:
            return f"{obj.latitude}, {obj.longitude}"
        else:
            return "No coordinates"

    get_latitude_and_longitude.short_description = "Широта и долгота"


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "get_file",
        "uploaded_at",
    )
    list_display_links = (
        "id",
        "order",
    )
    readonly_fields = ("get_file_preview",)

    def get_file(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" alt="{obj.file.name}" width=10% height=auto/>')
        return "Нет фото"

    get_file.short_description = "Фото документа"

    def get_file_preview(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.file.url}" alt="{obj.file.name}" width=10% height=auto/>')
        return "Нет фото"

    get_file_preview.short_description = "Предпросмотр фото"
