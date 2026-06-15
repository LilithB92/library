from rest_framework import serializers

from library.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели «Автор».

    Обрабатывает преобразование экземпляров курса в формат JSON и выполняет валидацию
    входящие данные для удаления, создания или обновления курсов.
    """

    class Meta:
        model = Author
        fields = ("pk", "full_name", "date_of_birth", "date_of_death", "nationality")

    def validate(self, data):
        # 1. Проверка: дата рождения < дата смерти
        if  data.get("date_of_birth") and data.get("date_of_death"):
            if data.get("date_of_birth") >= data.get("date_of_death"):
                raise serializers.ValidationError("Не может дата рождения быть после даты смерти.")
        return data
