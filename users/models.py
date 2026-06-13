from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Сохраняет одну запись о пользователья`
    """

    username = None
    full_name = models.CharField(max_length=255, verbose_name="ФИО", help_text="Введите Ваш ФИО")
    email = models.EmailField(unique=True)
    verification_token = models.CharField(max_length=36, blank=True, null=True)
    phone_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Телефон", help_text="Введите Ваш номер телефона"
    )
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватарка")
    address = models.CharField(
        blank=True, null=True, verbose_name="Адрес", help_text="Введите Ваш адрес"
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
