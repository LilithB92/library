from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView

from library.models import Book

from .forms import BookForm, BookSearchForm
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
