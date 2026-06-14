from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели «Пользователи».

    Обрабатывает преобразование экземпляров пользователи в формат JSON и выполняет валидацию
    входящие данные регистрации пользователи.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email",
            "phone_number",
            "avatar",
            "address",
            "password",
        )
