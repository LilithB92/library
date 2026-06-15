from django.db import models
from django_countries.fields import CountryField


class Author(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    nationality = CountryField(
        blank=True, null=True, blank_label="(Select nationality)"
    )

    def __str__(self):
        return f"{self.full_name} ({self.nationality.name})"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
