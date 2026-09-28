from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()

        # проверка существования
        if User.objects.filter(email="lesnicenkodaniil62@gmail.com").exists():
            self.stdout.write(self.style.WARNING("Пользователь уже существует"))
            return

        user = User.objects.create(
            email="lesnicenkodaniil62@gmail.com",
            first_name="Admin",
            last_name="Adminex",
        )
        user.set_password("93x85v71z")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f"Успешно создан суперпользователь с email {user.email}."))
