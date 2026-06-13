from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создать суперпользователя"

    def handle(self, *args, **options):
        user = User.objects.create(full_name="Супер пользователь", email="admin@gmail.com")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password("admin1111")
        user.save()

        if user:
            self.stdout.write(self.style.SUCCESS(f"Successfully added superuser: {user.__str__()}"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser already exists: {user.__str__()}"))
