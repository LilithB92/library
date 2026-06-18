from datetime import date

from rest_framework import serializers

from library.models import Author, Book, BorrowRecord


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели «Автор».

    Обрабатывает преобразование экземпляров автора в формат JSON и выполняет валидацию
    входящие данные для удаления, создания или обновления авторов.
    """

    class Meta:
        model = Author
        fields = ("pk", "full_name", "date_of_birth", "date_of_death", "nationality")

    def validate(self, data):
        # 1. Проверка: дата рождения < дата смерти
        if data.get("date_of_birth") and data.get("date_of_death"):
            if data.get("date_of_birth") >= data.get("date_of_death"):
                raise serializers.ValidationError(
                    "Не может дата рождения быть после даты смерти."
                )
        return data


class BookSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели «Книг».

    Обрабатывает преобразование экземпляров книг в формат JSON и выполняет валидацию
    входящие данные для удаления, создания или обновления книг.
    """

    class Meta:
        model = Book
        # authors = AuthorSerializer(many=True, read_only=True)
        fields = (
            "pk",
            "title",
            "authors",
            "inventory_number",
            "status",
            "genre",
            "published_year",
            "created_at",
            "updated_at",
        )
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, data):
        """Валидация атрибутов(data:{get}) модели Книг"""
        # 1. Проверка: У книги есть автор
        if not data.get("authors"):
            raise serializers.ValidationError("Книга не может быть без автора.")
        # 2. Проверка: год публикации
        current_year = date.today().year
        if (data.get("published_year") > current_year) or (
            data.get("published_year") < 868
        ):
            raise serializers.ValidationError(
                "Год публикации не может быть меньше чем год публикации первой книги(868) и не больше текущего года."
            )
        return data


class BorrowRecordSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели «Запись выдачи».

    Обрабатывает преобразование экземпляров «Запись выдачи» в формат JSON и выполняет валидацию
    входящие данные для создания или обновления записи.
    """

    class Meta:
        model = BorrowRecord
        fields = [
            "pk",
            "book",
            "user",
            "borrow_date",
            "due_date",
            "return_date",
            "is_returned",
        ]
        read_only_fields = ["due_date", "borrow_date", "is_returned"]
        extra_kwargs = {"book": {"required": False}, "user": {"required": False}}
