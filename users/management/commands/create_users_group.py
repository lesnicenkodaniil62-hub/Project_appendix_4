from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from blogs.models import BlogPost
from catalog.models import Product


class Command(BaseCommand):
    """Создание группы 'Пользователи' с базовыми правами."""

    help = "Создание группы 'Пользователи' с правами на просмотр и добавление товаров"

    def handle(self, *args, **options) -> None:
        group_name = "users"
        group_display_name = "Пользователи"

        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name=group_name)

        if not created:
            self.stdout.write(self.style.WARNING(f"Группа '{group_display_name}' уже существует"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_display_name}' создана"))

        # Получаем ContentType для моделей
        product_ct = ContentType.objects.get_for_model(Product)
        blogpost_ct = ContentType.objects.get_for_model(BlogPost)

        # 1. Право view_product — видеть товары
        view_product, _ = Permission.objects.get_or_create(
            codename="view_product",
            content_type=product_ct,
            defaults={
                "name": "Can view product",
                "content_type": product_ct,
            },
        )

        # 2. Право add_product — добавлять товары
        add_product, _ = Permission.objects.get_or_create(
            codename="add_product",
            content_type=product_ct,
            defaults={
                "name": "Can add product",
                "content_type": product_ct,
            },
        )

        # 3. Право view_blogpost — видеть публикации блога
        view_blogpost, _ = Permission.objects.get_or_create(
            codename="view_blogpost",
            content_type=blogpost_ct,
            defaults={
                "name": "Can view blog post",
                "content_type": blogpost_ct,
            },
        )

        # Назначаем права группе
        group.permissions.add(view_product, add_product, view_blogpost)

        self.stdout.write(
            self.style.SUCCESS(
                f"Группе '{group_display_name}' назначены права:\n"
                f"   • view_product (видеть товары)\n"
                f"   • add_product (добавлять товары)\n"
                f"   • view_blogpost (видеть публикации блога)"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(f"Итого в группе '{group_display_name}': " f"{group.permissions.count()} прав(а)")
        )
