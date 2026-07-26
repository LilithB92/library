from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers, status, viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from library.models import Author, Book, BorrowRecord
from library.permissions import IsLibrarian, is_librarian
from library.serializers import AuthorSerializer, BookSerializer, BorrowRecordSerializer
from library.services import (
    send_already_borrowed_email,
    send_borrow_email,
    send_return_email,
)
from users.models import User


class AuthorViewSet(viewsets.ModelViewSet):
    """CRUD для авторов книг"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by("pk")
    permission_classes = (IsAuthenticated, IsLibrarian)


class BookViewSet(viewsets.ModelViewSet):
    """CRUD и фильтрация для книг"""

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("pk")
    filterset_fields = ["genre", "published_year", "title"]
    permission_classes = (IsAuthenticated, IsLibrarian)


class BorrowBookApiView(CreateAPIView):
    """Выдача книги. Библиотекарь может выдать за любого пользователя."""

    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        book_pk = self.kwargs.get("pk")
        book = get_object_or_404(Book, pk=book_pk)
        user = self.request.user

        if is_librarian(user):
            target_user_id = self.request.data.get("user")
            if target_user_id:
                target_user = get_object_or_404(User, pk=target_user_id)
            else:
                target_user = user
        else:
            target_user = user

        with transaction.atomic():
            if book.status == "borrowed":
                active_record = BorrowRecord.objects.filter(
                    book=book, is_returned=False
                ).first()
                if active_record:
                    send_already_borrowed_email(
                        target_user.email,
                        book.title,
                        active_record.due_date,
                    )
                    raise serializers.ValidationError(
                        {
                            "error": (
                                f"Книга уже выдана. "
                                f"Срок возврата: {active_record.due_date}."
                            )
                        }
                    )

            borrow_record = serializer.save(
                user=target_user,
                book=book,
                borrowed_by=user,
            )

            book.status = "borrowed"
            book.save()

        send_borrow_email(
            target_user.email, book.title, borrow_record.due_date
        )

        self._borrow_record_id = borrow_record.id

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            return Response(
                {
                    "message": "Книга успешно выдана.",
                    "record_id": self._borrow_record_id,
                },
                status=status.HTTP_201_CREATED,
            )
        return response


class ReturnBookApiView(UpdateAPIView):
    """Возврат книги по book pk. Библиотекарь может вернуть за любого."""

    queryset = BorrowRecord.objects.filter(is_returned=False)
    serializer_class = BorrowRecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        book_pk = self.kwargs.get("pk")
        book = get_object_or_404(Book, pk=book_pk)
        user = self.request.user

        if is_librarian(user):
            record = BorrowRecord.objects.filter(
                book=book, is_returned=False
            ).first()
        else:
            record = BorrowRecord.objects.filter(
                book=book, user=user, is_returned=False
            ).first()

        if not record:
            raise serializers.ValidationError(
                {"error": "Активная запись выдачи не найдена."}
            )
        return record

    def perform_update(self, serializer):
        with transaction.atomic():
            record = serializer.save(
                is_returned=True,
                return_date=timezone.now(),
            )
            record.book.status = "available"
            record.book.save()

        send_return_email(record.user.email, record.book.title)

        self._return_message = (
            f"Книга «{record.book.title}» успешно возвращена."
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": self._return_message},
            status=status.HTTP_200_OK,
        )


class BorrowBookListAPIView(ListAPIView):
    """Список записей выдачи. Пользователь — свои, библиотекарь — все."""

    serializer_class = BorrowRecordSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        queryset = BorrowRecord.objects.select_related("book", "user")

        if not is_librarian(user):
            queryset = queryset.filter(user=user)

        filter_status = self.request.query_params.get("status")
        if filter_status == "active":
            queryset = queryset.filter(is_returned=False)
        elif filter_status == "returned":
            queryset = queryset.filter(is_returned=True)
        elif filter_status == "overdue":
            queryset = queryset.filter(
                is_returned=False, borrow_date__lt=timezone.now() - timezone.timedelta(days=10)
            )

        return queryset.order_by("-borrow_date")
