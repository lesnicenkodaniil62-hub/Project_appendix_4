from django.conf import settings
from django.db import models


class BlogPost(models.Model):
    """Модель публикации в блоге."""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок публикации",
    )
    content = models.TextField(
        verbose_name="Содержание",
        help_text="Введите содержание публикации",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Если отмечено — публикация видна всем",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_posts",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-created_at"]
        # Кастомные права для контент-менеджеров
        permissions = [
            ("can_manage_blog_posts", "Может управлять публикациями в блоге"),
        ]

    def __str__(self) -> str:
        return self.title
