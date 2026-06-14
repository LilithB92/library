from django.core.mail import send_mail

from config import settings


class EmailVerification:
    """Класс для верификации аккаунта с почтой"""

    @staticmethod
    def authentication_by_email(request, token, user_email):
        """
        Отправление почты для верификации токен пользователя
        :param request:
        :param token: токен пользователя
        :param user_email: почта получателя
        :return: None
        """
        verification_url = f"{request.get_host()}/users/verify/{token}"
        subject = "Verify Your Email Address"
        message = f"Click the link to verify your email: {verification_url}"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
