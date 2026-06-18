from datetime import timedelta

from django.db import models
from django_countries.fields import CountryField

from config.settings import AUTH_USER_MODEL


class Author(models.Model):
    """Сохраняет одну запись об авторах книг, связанную с:model:`Book`"""

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


class Book(models.Model):
    """Сохраняет одну запись о книгах, связанную с:model:`Author`"""

    title = models.CharField(
        max_length=200, verbose_name="Заголовка", help_text="Ведите заголовку"
    )
    authors = models.ManyToManyField(
        Author,
        related_name="books",
    )
    inventory_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Инвентарный номер",
        help_text="Ведите инвентарный номер",
    )
    status_choices = [
        ("available", "Доступна"),
        ("borrowed", "Выдана"),
    ]
    status = models.CharField(
        max_length=25, choices=status_choices, default="available", verbose_name="Стату"
    )
    genre_choices = [
        ("fiction", "Художественная литература"),
        ("non-fiction", "Документальная литература"),
        ("classic", "Классическая литература"),
    ]
    genre = models.CharField(max_length=25, choices=genre_choices, verbose_name="Жанр")
    published_year = models.PositiveSmallIntegerField(verbose_name="Год публикации")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} книга с инвентарным номером: {self.inventory_number}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BorrowRecord(models.Model):
    """Сохраняет одну запись о выдачи книг, связанно с:models:`Book`, `User`,"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    @property
    def due_date(self):
        """Вычисляемая дата возврата."""
        return self.borrow_date + timedelta(days=10)

    def __str__(self):
        return f"{self.user.full_name} - {self.book.title}"

    class Meta:
        verbose_name = "Выдача книг"
        verbose_name_plural = "Выдачи книги"
