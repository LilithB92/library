from django.core.mail import send_mail

from config import settings

BORROW_SUBJECT = "Выдача книги"
BORROW_MESSAGE = (
    "Здравствуйте!\n\n"
    "Книга «{book_title}» выдана вам до {due_date}.\n"
    "Пожалуйста, верните книгу вовремя.\n\n"
    "С уважением,\nБиблиотека"
)

RETURN_SUBJECT = "Возврат книги"
RETURN_MESSAGE = (
    "Здравствуйте!\n\n"
    "Книга «{book_title}» успешно возвращена.\n"
    "Спасибо, что пользуетесь библиотекой!\n\n"
    "С уважением,\nБиблиотека"
)

OVERDUE_SUBJECT = "Просрочка возврата книги"
OVERDUE_MESSAGE = (
    "Здравствуйте!\n\n"
    "Срок возврата книги «{book_title}» истёк {due_date}.\n"
    "Пожалуйста, верните книгу как можно скорее.\n\n"
    "С уважением,\nБиблиотека"
)

ALREADY_BORROWED_SUBJECT = "Книга занята"
ALREADY_BORROWED_MESSAGE = (
    "Здравствуйте!\n\n"
    "Вы пытаетесь взять книгу «{book_title}», но она уже выдана другому читателю.\n"
    "Срок возврата: {due_date}.\n\n"
    "С уважением,\nБиблиотека"
)


def send_borrow_email(user_email, book_title, due_date):
    """Отправляет email при выдаче книги."""
    send_mail(
        subject=BORROW_SUBJECT,
        message=BORROW_MESSAGE.format(
            book_title=book_title, due_date=due_date.strftime("%d.%m.%Y")
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )


def send_return_email(user_email, book_title):
    """Отправляет email при возврате книги."""
    send_mail(
        subject=RETURN_SUBJECT,
        message=RETURN_MESSAGE.format(book_title=book_title),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )


def send_overdue_email(user_email, book_title, due_date):
    """Отправляет email при просрочке."""
    send_mail(
        subject=OVERDUE_SUBJECT,
        message=OVERDUE_MESSAGE.format(
            book_title=book_title, due_date=due_date.strftime("%d.%m.%Y")
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )


def send_already_borrowed_email(user_email, book_title, due_date):
    """Уведомляет, что книга уже занята."""
    send_mail(
        subject=ALREADY_BORROWED_SUBJECT,
        message=ALREADY_BORROWED_MESSAGE.format(
            book_title=book_title, due_date=due_date.strftime("%d.%m.%Y")
        ),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=True,
    )
