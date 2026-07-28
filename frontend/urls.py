from django.urls import path

from . import views

app_name = "frontend"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("books/create/", views.BookCreateView.as_view(), name="book_create"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book_detail"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book_delete"),
    path("authors/", views.AuthorListView.as_view(), name="author_list"),
    path("authors/create/", views.AuthorCreateView.as_view(), name="author_create"),
    path("authors/<int:pk>/", views.AuthorDetailView.as_view(), name="author_detail"),
    path("authors/<int:pk>/delete/", views.AuthorDeleteView.as_view(), name="author_delete"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("verify/<str:token>/", views.VerifyView.as_view(), name="verify"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
