from django.urls import path
from rest_framework import routers

from library.apps import LibraryConfig
from library.views import (AuthorViewSet, BookViewSet, BorrowBookApiView,
                           BorrowBookListAPIView, ReturnBookAPIView)

app_name = LibraryConfig.name

router = routers.SimpleRouter()
router.register(r"author", AuthorViewSet, basename="author")
router.register(r"book", BookViewSet, basename="book")


urlpatterns = [
    path("borrow/<int:pk>/book/", BorrowBookApiView.as_view(), name="borrow_book"),
    path("return/<int:pk>/book/", ReturnBookAPIView.as_view(), name="return_book"),
    path(
        "borrow/records/", BorrowBookListAPIView.as_view(), name="list_borrowed_records"
    ),
]

urlpatterns += router.urls
