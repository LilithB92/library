import io
import os
import urllib.request
import urllib.parse

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw, ImageFont

from library.models import Author, Book

AUTHORS_DATA = [
    {
        "full_name": "Лев Толстой",
        "date_of_birth": "1828-09-09",
        "date_of_death": "1910-11-20",
        "nationality": "RU",
    },
    {
        "full_name": "Фёдор Достоевский",
        "date_of_birth": "1821-11-11",
        "date_of_death": "1881-01-28",
        "nationality": "RU",
    },
    {
        "full_name": "Антон Чехов",
        "date_of_birth": "1860-01-29",
        "date_of_death": "1904-07-15",
        "nationality": "RU",
    },
    {
        "full_name": "Максим Горький",
        "date_of_birth": "1868-03-28",
        "date_of_death": "1936-06-18",
        "nationality": "RU",
    },
    {
        "full_name": "Иван Тургенев",
        "date_of_birth": "1818-11-09",
        "date_of_death": "1883-09-03",
        "nationality": "RU",
    },
    {
        "full_name": "Николай Гоголь",
        "date_of_birth": "1809-04-01",
        "date_of_death": "1852-03-04",
        "nationality": "UA",
    },
    {
        "full_name": "Александр Пушкин",
        "date_of_birth": "1799-06-06",
        "date_of_death": "1837-02-10",
        "nationality": "RU",
    },
    {
        "full_name": "Михаил Булгаков",
        "date_of_birth": "1891-05-15",
        "date_of_death": "1940-03-10",
        "nationality": "UA",
    },
]

BOOKS_DATA = [
    {
        "title": "Война и мир",
        "authors": ["Лев Толстой"],
        "inventory_number": 1001,
        "genre": "classic",
        "published_year": 1869,
        "pages": 1225,
    },
    {
        "title": "Анна Каренина",
        "authors": ["Лев Толстой"],
        "inventory_number": 1002,
        "genre": "classic",
        "published_year": 1877,
        "pages": 864,
    },
    {
        "title": "Преступление и наказание",
        "authors": ["Фёдор Достоевский"],
        "inventory_number": 1003,
        "genre": "classic",
        "published_year": 1866,
        "pages": 672,
    },
    {
        "title": "Братья Карамазовы",
        "authors": ["Фёдор Достоевский"],
        "inventory_number": 1004,
        "genre": "classic",
        "published_year": 1880,
        "pages": 1096,
    },
    {
        "title": "Идиот",
        "authors": ["Фёдор Достоевский"],
        "inventory_number": 1005,
        "genre": "classic",
        "published_year": 1869,
        "pages": 596,
    },
    {
        "title": "Вишнёвый сад",
        "authors": ["Антон Чехов"],
        "inventory_number": 1006,
        "genre": "classic",
        "published_year": 1904,
        "pages": 120,
    },
    {
        "title": "Чайка",
        "authors": ["Антон Чехов"],
        "inventory_number": 1007,
        "genre": "classic",
        "published_year": 1896,
        "pages": 96,
    },
    {
        "title": "Мать",
        "authors": ["Максим Горький"],
        "inventory_number": 1008,
        "genre": "fiction",
        "published_year": 1906,
        "pages": 544,
    },
    {
        "title": "Отцы и дети",
        "authors": ["Иван Тургенев"],
        "inventory_number": 1009,
        "genre": "classic",
        "published_year": 1862,
        "pages": 368,
    },
    {
        "title": "Мёртвые души",
        "authors": ["Николай Гоголь"],
        "inventory_number": 1010,
        "genre": "classic",
        "published_year": 1842,
        "pages": 352,
    },
    {
        "title": "Евгений Онегин",
        "authors": ["Александр Пушкин"],
        "inventory_number": 1011,
        "genre": "classic",
        "published_year": 1833,
        "pages": 224,
    },
    {
        "title": "Мастер и Маргарита",
        "authors": ["Михаил Булгаков"],
        "inventory_number": 1012,
        "genre": "fiction",
        "published_year": 1967,
        "pages": 480,
    },
    {
        "title": "Собачье сердце",
        "authors": ["Михаил Булгаков"],
        "inventory_number": 1013,
        "genre": "fiction",
        "published_year": 1925,
        "pages": 224,
    },
    {
        "title": "Двенадцать стульев",
        "authors": ["Илья Ильф", "Евгений Петров"],
        "inventory_number": 1014,
        "genre": "fiction",
        "published_year": 1928,
        "pages": 416,
    },
    {
        "title": "Тихий Дон",
        "authors": ["Михаил Шолохов"],
        "inventory_number": 1015,
        "genre": "fiction",
        "published_year": 1940,
        "pages": 896,
    },
]

COVER_COLORS = [
    (45, 106, 79),
    (26, 35, 50),
    (128, 0, 0),
    (0, 51, 102),
    (85, 85, 0),
    (60, 60, 120),
    (100, 50, 50),
    (30, 80, 60),
    (70, 40, 90),
    (50, 70, 80),
    (110, 60, 30),
    (40, 60, 90),
    (80, 30, 60),
    (50, 90, 50),
    (90, 70, 40),
]


def fetch_cover_from_open_library(title):
    """Ищет обложку на Open Library по названию книги."""
    try:
        query = urllib.parse.quote(title)
        url = f"https://openlibrary.org/search.json?title={query}&limit=1"
        req = urllib.request.Request(url, headers={"User-Agent": "LibraryProject/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            import json

            data = json.loads(resp.read().decode())

        if data.get("docs"):
            cover_id = data["docs"][0].get("cover_i")
            if cover_id:
                cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                req = urllib.request.Request(
                    cover_url, headers={"User-Agent": "LibraryProject/1.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as img_resp:
                    return img_resp.read()
    except Exception:
        pass
    return None


def generate_fallback_cover(title, author_name, inventory_number):
    """Генерирует заглушку если не удалось скачать обложку."""
    width, height = 400, 560
    bg_color = COVER_COLORS[inventory_number % len(COVER_COLORS)]

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    border_color = tuple(min(c + 40, 255) for c in bg_color)
    draw.rectangle([10, 10, width - 10, height - 10], outline=border_color, width=3)
    draw.rectangle([20, 20, width - 20, height - 20], outline=border_color, width=1)

    try:
        font_title = ImageFont.truetype("arial.ttf", 32)
        font_author = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        try:
            font_title = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32
            )
            font_author = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20
            )
        except OSError:
            font_title = ImageFont.load_default()
            font_author = ImageFont.load_default()

    text_color = (255, 255, 255)

    lines = []
    words = title.split()
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] > width - 60:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    if current_line:
        lines.append(current_line)

    total_text_height = len(lines) * 40
    y_start = (height - total_text_height) // 2 - 40

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = y_start + i * 40
        draw.text((x, y), line, fill=text_color, font=font_title)

    author_bbox = draw.textbbox((0, 0), author_name, font=font_author)
    author_width = author_bbox[2] - author_bbox[0]
    author_y = y_start + len(lines) * 40 + 30
    draw.text(
        ((width - author_width) // 2, author_y),
        author_name,
        fill=text_color,
        font=font_author,
    )

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()


class Command(BaseCommand):
    help = "Заполнить базу данных авторами и книгами с обложками"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очистить существующие данные перед заполнением",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Очистка данных...")
            Book.objects.all().delete()
            Author.objects.all().delete()
            self.stdout.write(self.style.WARNING("Все книги и авторы удалены."))

        self.stdout.write("Создание авторов...")
        authors_map = {}
        for data in AUTHORS_DATA:
            author, created = Author.objects.get_or_create(
                full_name=data["full_name"],
                defaults={
                    "date_of_birth": data["date_of_birth"],
                    "date_of_death": data["date_of_death"],
                    "nationality": data["nationality"],
                },
            )
            authors_map[data["full_name"]] = author
            status = "создан" if created else "уже есть"
            self.stdout.write(f"  {author.full_name} — {status}")

        os.makedirs(os.path.join(settings.MEDIA_ROOT, "book_covers"), exist_ok=True)

        self.stdout.write("\nСоздание книг с обложками...")
        self.stdout.write("Загрузка обложек с Open Library...\n")
        books_created = 0
        books_skipped = 0
        covers_downloaded = 0
        covers_fallback = 0

        for data in BOOKS_DATA:
            if Book.objects.filter(inventory_number=data["inventory_number"]).exists():
                books_skipped += 1
                self.stdout.write(f"  {data['title']} — уже есть (пропуск)")
                continue

            author_names = ", ".join(data["authors"])
            self.stdout.write(f"  {data['title']} — загрузка обложки...")

            cover_bytes = fetch_cover_from_open_library(data["title"])
            if cover_bytes:
                cover_file = ContentFile(cover_bytes)
                filename = f"cover_{data['inventory_number']}.jpg"
                covers_downloaded += 1
                source = "Open Library"
            else:
                fallback = generate_fallback_cover(
                    data["title"], author_names, data["inventory_number"]
                )
                cover_file = ContentFile(fallback)
                filename = f"cover_{data['inventory_number']}.jpg"
                covers_fallback += 1
                source = "заглушка"

            book = Book(
                title=data["title"],
                inventory_number=data["inventory_number"],
                genre=data["genre"],
                published_year=data["published_year"],
                pages=data["pages"],
            )
            book.book_cover.save(filename, cover_file, save=False)
            book.save()

            for author_name in data["authors"]:
                if author_name in authors_map:
                    book.authors.add(authors_map[author_name])

            books_created += 1
            self.stdout.write(f"    -> {source}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nГотово! Книг создано: {books_created}, пропущено: {books_skipped}\n"
                f"Обложек скачано: {covers_downloaded}, заглушек: {covers_fallback}"
            )
        )
