from django.contrib import admin

from library.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Администрирование модели Пользователь(User).
    Супер позволяет управлять пользователями и их активностью.
    """

    list_display = (
        "pk",
        "full_name",
        "date_of_birth",
        "date_of_death",
        "nationality",
    )
