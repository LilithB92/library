from django.contrib import admin

from library.models import Author, Book, BorrowRecord


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Администрирование модели Авторами(Author).
    Супер позволяет управлять авторами книг.
    """

    list_display = (
        "pk",
        "full_name",
        "date_of_birth",
        "date_of_death",
        "nationality",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
     Администрирование модели Книг(Book).
    Супер позволяет управлять книгами.
    """

    list_display = (
        "pk",
        "title",
        "inventory_number",
        "status",
        "genre",
        "published_year",
    )

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    """
     Администрирование модели ВыдачаКниг(BorrowRecord).
    Супер позволяет управлять выдачами книг.
    """

    list_display = (
        "pk",
        "book",
        "user",
        "borrow_date",
        "return_date",
        "is_returned",
        "due_date"
    )
