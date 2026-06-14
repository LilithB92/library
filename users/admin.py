from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Администрирование модели Пользователь(User).
    Супер позволяет управлять пользователями и их активностью.
    """

    list_display = (
        "id",
        "full_name",
        "email",
        "phone_number",
        "avatar",
        "address",
        "is_active",
    )
