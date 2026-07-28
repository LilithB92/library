from django.urls import path

from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("books/create/", views.BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
]
