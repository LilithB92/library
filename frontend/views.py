import secrets

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView

from library.models import Author, Book
from users.models import User

from .forms import AuthorForm, BookForm, BookSearchForm, LoginForm, ProfileForm, RegisterForm
from .permissions import is_librarian


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.prefetch_related("authors").order_by("-created_at")
        form = BookSearchForm(self.request.GET)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            genre = form.cleaned_data.get("genre")
            status_val = form.cleaned_data.get("status")
            if title:
                books = books.filter(title__icontains=title)
            if genre:
                books = books.filter(genre=genre)
            if status_val:
                books = books.filter(status=status_val)

        paginator = Paginator(books, 4)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        context["form"] = form
        context["is_librarian"] = is_librarian(self.request.user)
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["authors"] = self.object.authors.all()
        context["is_librarian"] = is_librarian(self.request.user)
        return context


class LibrarianRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_librarian(request.user):
            return redirect("frontend:index")
        return super().dispatch(request, *args, **kwargs)


class BookCreateView(LibrarianRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/create.html"
    success_url = "frontend:index"

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class BookDeleteView(LibrarianRequiredMixin, DeleteView):
    model = Book
    template_name = "books/delete.html"
    success_url = "frontend:index"

    def form_valid(self, form):
        self.object.delete()
        return redirect(self.get_success_url())


class AuthorListView(ListView):
    model = Author
    template_name = "authors/list.html"
    context_object_name = "authors"
    ordering = "full_name"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_librarian"] = is_librarian(self.request.user)
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = "authors/detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["books"] = self.object.books.all().order_by("-published_year")
        context["is_librarian"] = is_librarian(self.request.user)
        return context


class AuthorCreateView(LibrarianRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "authors/create.html"
    success_url = "frontend:author_list"

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class AuthorDeleteView(LibrarianRequiredMixin, DeleteView):
    model = Author
    template_name = "authors/delete.html"
    success_url = "frontend:author_list"

    def form_valid(self, form):
        self.object.delete()
        return redirect(self.get_success_url())


class LoginView(FormView):
    form_class = LoginForm
    template_name = "auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("frontend:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(
            self.request,
            username=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            login(self.request, user)
            return redirect(self.request.GET.get("next", "frontend:index"))
        messages.error(self.request, "Неверный email или пароль.")
        return super().form_invalid(form)


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "auth/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("frontend:index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.verification_token = token
        user.set_password(form.cleaned_data["password"])
        user.save()

        from users.services import EmailVerification

        EmailVerification.authentication_by_email(
            request=self.request, token=token, user_email=user.email
        )

        messages.success(
            self.request,
            "Регистрация успешна! Проверьте почту для подтверждения аккаунта.",
        )
        return redirect("frontend:login")


class VerifyView(TemplateView):
    template_name = "auth/verify.html"

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        user = User.objects.filter(verification_token=token).first()
        if user:
            user.is_active = True
            user.verification_token = None
            user.save()
            messages.success(request, "Email подтвержден! Теперь вы можете войти.")
        else:
            messages.error(request, "Неверный токен верификации.")
        return super().get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "users/profile.html"
    success_url = "frontend:profile"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Профиль обновлен.")
        return redirect("frontend:profile")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("frontend:index")
