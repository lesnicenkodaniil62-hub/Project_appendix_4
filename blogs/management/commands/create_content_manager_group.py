from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from blogs.models import BlogPost


class Command(BaseCommand):
    """Создание группы 'Контент-менеджер' с правами на блог."""

    help = "Создание группы 'Контент-менеджер' с правами на управление блогом"

    def handle(self, *args, **options) -> None:
        group_name = "content_managers"
        group_display_name = "Контент-менеджер"

        # Создаём или получаем группу
        group, created = Group.objects.get_or_create(name=group_name)

        if not created:
            self.stdout.write(self.style.WARNING(f"Группа '{group_display_name}' уже существует"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Группа '{group_display_name}' создана"))

        # Получаем ContentType для модели BlogPost
        content_type = ContentType.objects.get_for_model(BlogPost)

        # 1. Кастомное право: can_manage_blog_posts
        manage_perm, _ = Permission.objects.get_or_create(
            codename="can_manage_blog_posts",
            content_type=content_type,
            defaults={
                "name": "Может управлять публикациями в блоге",
                "content_type": content_type,
            },
        )

        # 2. Стандартные права Django для BlogPost
        add_perm, _ = Permission.objects.get_or_create(
            codename="add_blogpost",
            content_type=content_type,
            defaults={
                "name": "Can add blog post",
                "content_type": content_type,
            },
        )

        change_perm, _ = Permission.objects.get_or_create(
            codename="change_blogpost",
            content_type=content_type,
            defaults={
                "name": "Can change blog post",
                "content_type": content_type,
            },
        )

        delete_perm, _ = Permission.objects.get_or_create(
            codename="delete_blogpost",
            content_type=content_type,
            defaults={
                "name": "Can delete blog post",
                "content_type": content_type,
            },
        )

        view_perm, _ = Permission.objects.get_or_create(
            codename="view_blogpost",
            content_type=content_type,
            defaults={
                "name": "Can view blog post",
                "content_type": content_type,
            },
        )

        # Назначаем все права группе
        group.permissions.add(manage_perm, add_perm, change_perm, delete_perm, view_perm)

        self.stdout.write(
            self.style.SUCCESS(
                f"Группе '{group_display_name}' назначены права:\n"
                f"   • can_manage_blog_posts\n"
                f"   • add_blogpost\n"
                f"   • change_blogpost\n"
                f"   • delete_blogpost\n"
                f"   • view_blogpost"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(f"Итого в группе '{group_display_name}': " f"{group.permissions.count()} прав(а)")
        )
