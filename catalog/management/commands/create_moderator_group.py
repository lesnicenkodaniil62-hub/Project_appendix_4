from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from catalog.models import Product

User = get_user_model()


class Command(BaseCommand):
    """Кастомная команда для создания группы 'Модератор продуктов'."""

    help = "Создание группы 'Модератор продуктов' с необходимыми правами"

    def handle(self, *args, **options) -> None:
        group_name = "moderators"
        group_display_name = "Модератор продуктов"

        # Проверка существования группы
        group, created = Group.objects.get_or_create(
            name=group_name,
            defaults={"name": group_name},
        )

        if not created:
            self.stdout.write(self.style.WARNING(f"Группа '{group_display_name}' уже существует"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_display_name}' создана"))

        # Получаем ContentType для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем нужные права
        # 1. Кастомное право: can_unpublish_product
        unpublish_perm, created_unpublish = Permission.objects.get_or_create(
            codename="can_unpublish_product",
            content_type=content_type,
            defaults={
                "name": "Может отменять публикацию продукта",
                "content_type": content_type,
            },
        )
        if created_unpublish:
            self.stdout.write(self.style.SUCCESS("Право 'can_unpublish_product' найдено"))

        # 2. Стандартное право: delete_product (создаётся Django автоматически)
        delete_perm, created_delete = Permission.objects.get_or_create(
            codename="delete_product",
            content_type=content_type,
            defaults={
                "name": "Can delete product",
                "content_type": content_type,
            },
        )
        if created_delete:
            self.stdout.write(self.style.SUCCESS("Право 'delete_product' найдено"))

        # Назначаем права группе
        group.permissions.add(unpublish_perm, delete_perm)

        self.stdout.write(
            self.style.SUCCESS(
                f"Группе '{group_display_name}' назначены права:\n"
                f"   • can_unpublish_product\n"
                f"   • delete_product"
            )
        )

        # Итоговая статистика
        self.stdout.write(
            self.style.SUCCESS(f"\nИтого в группе '{group_display_name}': " f"{group.permissions.count()} прав(а)")
        )
