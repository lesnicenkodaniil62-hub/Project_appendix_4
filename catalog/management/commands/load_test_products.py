from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Кастомная команда для добавления тестовых продуктов."""

    help = "Добавляет тестовые продукты из фикстуры (с предварительной очисткой)"

    def handle(self, *args: Any, **kwargs: Any) -> None:
        # Предварительное удаление данных (критерий!)
        self.stdout.write("Очистка базы данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✓ База данных очищена"))

        # Загрузка из существующей фикстуры (критерий!)
        self.stdout.write("Загрузка данных из фикстуры fixtures.json...")
        call_command("loaddata", "fixtures.json", format="json")

        self.stdout.write(self.style.SUCCESS(f"✓ Загружено категорий: {Category.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"✓ Загружено продуктов: {Product.objects.count()}"))
        self.stdout.write(self.style.SUCCESS("\n✓ Тестовые данные успешно добавлены!"))
