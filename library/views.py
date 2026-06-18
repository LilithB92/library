from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from library.models import Author, Book, BorrowRecord
from library.serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """CRUD для авторов книг"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by("pk")


class BookViewSet(viewsets.ModelViewSet):
    """CRUD и фильтрация для книг"""

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("pk")
    # Указываем поля, по которым можно искать (точное совпадение)
    filterset_fields = ["genre", "published_year", "title"]


class BorrowBookApiView(CreateAPIView):
    """Создание одной записи выдачи книг"""

    queryset = BorrowRecord.objects.all().select_related("book", "user")
    serializer_class = BorrowRecordSerializer

    def get_serializer_context(self):
        """Добавляем book и request в контекст сериализатора"""
        context = super().get_serializer_context()
        book_pk = self.kwargs.get("pk")
        book = get_object_or_404(Book, pk=book_pk)
        context["book"] = book
        return context

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
