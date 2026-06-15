from rest_framework import viewsets

from library.models import Author
from library.serializers import AuthorSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """CRUD для авторов книг"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all().order_by("pk")
