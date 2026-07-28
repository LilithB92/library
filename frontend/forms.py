from django import forms

from library.models import Author, Book
from users.models import User


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


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("full_name", "date_of_birth", "date_of_death", "nationality")
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ФИО автора"}
            ),
            "date_of_birth": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "date_of_death": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "nationality": forms.Select(attrs={"class": "form-select"}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )
    password_confirm = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
        ),
    )

    class Meta:
        model = User
        fields = ("full_name", "email", "phone_number", "address")
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ФИО"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Телефон (необязательно)"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Адрес (необязательно)"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("full_name", "email", "phone_number", "address", "avatar")
        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ФИО"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Телефон"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Адрес"}
            ),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class BorrowForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).order_by("full_name"),
        label="Читатель",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, show_user_select=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not show_user_select:
            self.fields["user"].widget = forms.HiddenInput()
        else:
            self.fields["user"].required = True
            self.fields["user"].empty_label = "-- Выберите читателя --"
