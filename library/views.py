from rest_framework import viewsets

from library.models import Author, Book
from library.serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """CRUD для авторов книг"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by("pk")


class BookViewSet(viewsets.ModelViewSet):
    """CRUD для книг"""

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("pk")
