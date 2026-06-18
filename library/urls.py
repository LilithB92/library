from django.urls import path
from rest_framework import routers

from library.apps import LibraryConfig
from library.views import AuthorViewSet, BookViewSet, BorrowBookApiView

app_name = LibraryConfig.name

router = routers.SimpleRouter()
router.register(r"author", AuthorViewSet, basename="author")
router.register(r"book", BookViewSet, basename="book")


urlpatterns = [
    path("borrow/<int:pk>/book/", BorrowBookApiView.as_view(), name="borrow_book"),
]

urlpatterns += router.urls
