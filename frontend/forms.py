from django import forms


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
