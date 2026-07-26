from datetime import timedelta

from django.db import models
from django.utils import timezone
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
    pages = models.PositiveIntegerField(verbose_name="страницы", default=5)
    book_cover = models.ImageField(verbose_name="обложка книг", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} книга с инвентарным номером: {self.inventory_number}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BorrowRecord(models.Model):
    """Сохраняет одну запись о выдаче книг, связанную с Book и User."""

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrow_records"
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrow_records"
    )
    borrowed_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issued_records",
        verbose_name="Кто выдал",
    )
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    @property
    def due_date(self):
        """Вычисляемая дата возврата (10 дней от выдачи)."""
        return self.borrow_date + timedelta(days=10)

    @property
    def is_overdue(self):
        """Проверка просрочки: не возвращена и срок вышел."""
        if self.is_returned:
            return False
        return timezone.now() > self.due_date

    def __str__(self):
        return f"{self.user.full_name} — {self.book.title}"

    class Meta:
        verbose_name = "Выдача книг"
        verbose_name_plural = "Выдачи книг"
        ordering = ["-borrow_date"]
