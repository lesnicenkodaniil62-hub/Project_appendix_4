from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    """Кастомная команда для добавления тестовых продуктов."""

    help = "Добавляет тестовые продукты в базу данных (с предварительной очисткой)"

    def handle(self, *args, **kwargs):
        # Очистка существующих данных
        self.stdout.write("Очистка базы данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✓ База данных очищена"))

        # Создание категорий
        self.stdout.write("Создание категорий...")
        cat1 = Category.objects.create(
            name="Электроника",
            description="Смартфоны, ноутбуки, планшеты",
        )
        cat2 = Category.objects.create(
            name="Одежда",
            description="Мужская и женская одежда",
        )
        cat3 = Category.objects.create(
            name="Книги",
            description="Художественная и учебная литература",
        )
        cat4 = Category.objects.create(
            name="Товары для дома",
            description="Мебель, посуда, декор",
        )
        self.stdout.write(self.style.SUCCESS(f"✓ Создано категорий: {Category.objects.count()}"))

        # Создание продуктов
        self.stdout.write("Создание продуктов...")
        Product.objects.create(
            name="Смартфон XYZ Pro",
            description="Флагманский смартфон с отличной камерой",
            category=cat1,
            price=50000,
        )
        Product.objects.create(
            name="Ноутбук ABC Ultra",
            description="Мощный игровой ноутбук",
            category=cat1,
            price=120000,
        )
        Product.objects.create(
            name="Футболка классическая",
            description="Хлопковая футболка белого цвета",
            category=cat2,
            price=1500,
        )
        Product.objects.create(
            name="Джинсы синие",
            description="Классические джинсы прямого кроя",
            category=cat2,
            price=3500,
        )
        Product.objects.create(
            name="Война и мир",
            description="Роман Л.Н. Толстого в двух томах",
            category=cat3,
            price=800,
        )
        Product.objects.create(
            name="Мастер и Маргарита",
            description="Роман М.А. Булгакова",
            category=cat3,
            price=650,
        )
        Product.objects.create(
            name="Набор кастрюль",
            description="Набор из 5 кастрюль разного объёма",
            category=cat4,
            price=4500,
        )
        Product.objects.create(
            name="Гантели разборные",
            description="Пара разборных гантелей до 20 кг",
            category=cat4,
            price=7500,
        )
        self.stdout.write(self.style.SUCCESS(f"✓ Создано продуктов: {Product.objects.count()}"))
        self.stdout.write(self.style.SUCCESS("\n✓ Тестовые данные успешно добавлены!"))
