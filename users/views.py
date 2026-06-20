import secrets

from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from library.permissions import IsLibrarian
from users.models import User
from users.serializers import UserSerializer
from users.services import EmailVerification


class UserRegisterAPIView(CreateAPIView):
    """Регистрация пользователя с верификацией почтой"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = secrets.token_hex(16)
        user.verification_token = token
        user.set_password(user.password)
        user.save()
        request = self.request
        EmailVerification.authentication_by_email(
            request=request, token=token, user_email=user.email
        )


class VerifyEmailView(APIView):
    """Проверяет адрес электронной почты, связанный с предоставленным ключом.
    Принимает следующий GET-параметр: key (token): Уникальный ключ активации/проверки,
    отправляемый на электронную почту пользователя.
    Возвращает:
    При успешном выполнении (HTTP 200): {"message": "Email verified successfully. You can now log in."}.
    При неудачном выполнении (HTTP 400): {"error": "Invalid verification token."}
    """

    permission_classes = (AllowAny,)

    def get(self, request, token, *args, **kwargs):
        try:
            user = User.objects.filter(verification_token=token).first()
            if user:
                user.is_active = True
                user.verification_token = None
                user.save()
            return Response(
                {"message": "Email verified successfully. You can now log in."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid verification token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserListAPIView(ListAPIView):
    """Показывает список пользователей"""

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsLibrarian)
