from rest_framework import serializers

from library.models import Author, Book


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
