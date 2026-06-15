from rest_framework.serializers import ModelSerializer

from library.models import Author


class AuthorSerializer(ModelSerializer):
    """
    Сериалайзер для модели «Автор».

    Обрабатывает преобразование экземпляров курса в формат JSON и выполняет валидацию
    входящие данные для удаления, создания или обновления курсов.
    """

    class Meta:
        model = Author
        fields = ("pk", "full_name", "date_of_birth", "date_of_death", "nationality")
