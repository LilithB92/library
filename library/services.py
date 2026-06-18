from django.core.mail import send_mail

from config import settings


def send_email_to_readers(book_borrower, book_returner, book_id, request):
    """
    Обеспечивает обмен книг читателями с почтой
    """
    return_url = f"{request.get_host()}/library/return/{book_id}/book/"
    borrow_url = f"{request.get_host()}/library/borrow/{book_id}/book/"
    reader_emails = [book_borrower, book_returner]
    for email in reader_emails:
        if email == book_returner:
            subject = "Возврат книг"
            message = (
                f"Здравствуйте! Если Вы хотите сдать книгу свяжитесь с почтой({book_borrower}). "
                f"Если Вы оба согласны авторизуйтесь и откройте ссылку: {return_url}"
            )
        else:
            subject = "Выдача книг"
            message = (
                f"Здравствуйте! Если Вы хотите брать книгу свяжитесь с почтой({book_returner}). "
                f"Если Вы оба согласны авторизуйтесь и откройте ссылку: {borrow_url}"
            )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],  # Список адресов
            fail_silently=False,
        )
