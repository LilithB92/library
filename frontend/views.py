from django.core.paginator import Paginator
from django.views.generic import TemplateView

from library.models import Book

from .forms import BookSearchForm
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
