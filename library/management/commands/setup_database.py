from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Полная настройка базы данных: миграции, группа, пользователи, книги"

    def add_arguments(self, parser):
        parser.add_argument(
            "--skip-migrate",
            action="store_true",
            help="Пропустить миграции",
        )
        parser.add_argument(
            "--skip-data",
            action="store_true",
            help="Пропустить заполнение книгами и авторами",
        )
        parser.add_argument(
            "--superuser-email",
            default="admin@gmail.com",
            help="Email суперпользователя (по умолчанию: admin@gmail.com)",
        )
        parser.add_argument(
            "--superuser-password",
            default="admin1111",
            help="Пароль суперпользователя (по умолчанию: admin1111)",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=" * 50))
        self.stdout.write(self.style.MIGRATE_HEADING("  Настройка базы данных"))
        self.stdout.write(self.style.MIGRATE_HEADING("=" * 50))

        if not options["skip_migrate"]:
            self.stdout.write("\n[1/4] Миграции...")
            call_command("migrate", verbosity=0)
            self.stdout.write(self.style.SUCCESS("  Готово"))
        else:
            self.stdout.write("\n[1/4] Миграции... пропущено")

        self.stdout.write("\n[2/4] Группа Librarian...")
        group, created = Group.objects.get_or_create(name="Librarian")
        status = "создана" if created else "уже есть"
        self.stdout.write(self.style.SUCCESS(f"  {status}"))

        self.stdout.write("\n[3/4] Пользователи...")
        self._create_superuser(
            options["superuser_email"], options["superuser_password"]
        )
        self._create_librarian()

        if not options["skip_data"]:
            self.stdout.write("\n[4/4] Книги и авторы...")
            call_command("populate_library", verbosity=0)
            self.stdout.write(self.style.SUCCESS("  Готово"))
        else:
            self.stdout.write("\n[4/4] Книги и авторы... пропущено")

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("  База данных готова!"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"\n  Суперпользователь: {options['superuser_email']}")
        self.stdout.write(f"  Пароль: {options['superuser_password']}")
        self.stdout.write("  Группа: Librarian\n")

    def _create_superuser(self, email, password):
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"  Суперпользователь {email} уже есть"))
            return

        user = User.objects.create(
            full_name="Администратор",
            email=email,
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"  Создан: {email} / {password}"))

    def _create_librarian(self):
        email = "librarian@gmail.com"
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"  Библиотекарь {email} уже есть"))
            return

        user = User.objects.create(
            full_name="Библиотекарь",
            email=email,
        )
        user.is_active = True
        user.set_password("librarian1111")
        user.save()
        group = Group.objects.get(name="Librarian")
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS(f"  Создан: {email} / librarian1111"))
