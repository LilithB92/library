from django import forms

from library.models import Book


class BookSearchForm(forms.Form):
    title = forms.CharField(
        required=False,
        label="Название",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Поиск по названию..."}
        ),
    )
    genre = forms.ChoiceField(
        required=False,
        label="Жанр",
        choices=[("", "Все жанры")] + [
            ("fiction", "Художественная"),
            ("non-fiction", "Документальная"),
            ("classic", "Классическая"),
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    status = forms.ChoiceField(
        required=False,
        label="Статус",
        choices=[("", "Все"), ("available", "Доступна"), ("borrowed", "Выдана")],
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = (
            "title", "authors", "inventory_number",
            "genre", "published_year", "pages", "book_cover",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название книги"}
            ),
            "authors": forms.SelectMultiple(attrs={"class": "form-select"}),
            "inventory_number": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Инвентарный номер"}
            ),
            "genre": forms.Select(attrs={"class": "form-select"}),
            "published_year": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Год публикации"}
            ),
            "pages": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Количество страниц"}
            ),
            "book_cover": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
