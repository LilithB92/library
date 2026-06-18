from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library.models import Author, Book, BorrowRecord
from library.permissions import IsLibrarian
from library.serializers import (AuthorSerializer, BookSerializer,
                                 BorrowRecordSerializer)
from library.services import send_email_to_readers


class AuthorViewSet(viewsets.ModelViewSet):
    """CRUD для авторов книг"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by("pk")
    permission_classes = (IsAuthenticated, IsLibrarian)


class BookViewSet(viewsets.ModelViewSet):
    """CRUD и фильтрация для книг"""

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("pk")
    # Указываем поля, по которым можно искать (точное совпадение)
    filterset_fields = ["genre", "published_year", "title"]
    permission_classes = (IsAuthenticated, IsLibrarian)


class BorrowBookApiView(CreateAPIView):
    """Создание одной записи выдачи книг"""

    queryset = BorrowRecord.objects.all().select_related("book", "user")
    serializer_class = BorrowRecordSerializer

    def perform_create(self, serializer):
        book_pk = self.kwargs.get("pk")
        user = self.request.user

        try:
            book = get_object_or_404(Book, pk=book_pk)

            with transaction.atomic():
                if book.status != "available":
                    borrowed_book = BorrowRecord.objects.filter(
                        book=book, is_returned=False
                    ).first()
                    if borrowed_book:
                        send_email_to_readers(
                            borrowed_book.user.email, user, book_pk, self.request
                        )
                        # Выбрасываем исключение — DRF автоматически вернёт 400
                        raise serializers.ValidationError(
                            {
                                "error": f"Эта книга уже выдана и будет возвращена {borrowed_book.due_date}."
                            }
                        )

                # Сохраняем запись через сериализатор
                borrow_record = serializer.save(user=user, book=book)

                # Обновляем статус книги
                book.status = "borrowed"
                book.save()

            # Сохраняем record_id в сериализаторе для использования в ответе
            self.borrow_record_id = borrow_record.id

        except Exception as e:
            # Для исключений тоже используем ValidationError
            raise serializers.ValidationError(
                {"error": f"Произошла ошибка при выдаче книги: {str(e)}"}
            )

    def create(self, request, *args, **kwargs):
        # Вызываем стандартный create() для валидации и сохранения
        response = super().create(request, *args, **kwargs)

        # Если сохранение прошло успешно (статус 201), формируем кастомный ответ
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {
                    "message": "Книга успешно выдана читателю.",
                    "record_id": self.borrow_record_id,
                },
                status=status.HTTP_201_CREATED,
            )

        # В случае ошибок возвращаем стандартный ответ DRF
        return response


class BorrowBookListAPIView(ListAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer


class ReturnBookAPIView(UpdateAPIView):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    def perform_update(self, serializer):
        user = self.request.user
        book_pk = self.kwargs.get("pk")
        try:
            book = get_object_or_404(Book, pk=book_pk)
            borrowed_record = get_object_or_404(
                BorrowRecord, user=user, book=book, is_returned=False
            )

            if borrowed_record:
                # borrowed_record = serializer.save(is_returned=True, return_date=returned_date)
                borrowed_record.is_returned = True
                borrowed_record.return_date = timezone.now()
                borrowed_record.save()

                # Обновляем статус книги
                book.status = "available"
                book.save()

            return Response(
                {
                    "message": "Книга успешно возвращена в библиотеку.",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Для исключений тоже используем ValidationError
            raise serializers.ValidationError(
                {"error": f"Произошла ошибка при возврате книг: {str(e)}"}
            )
