from django.db import models


class BlogPost(models.Model):
    """Модель блоговой записи."""

    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок записи",
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите содержимое записи",
    )
    preview = models.ImageField(
        upload_to="blogs/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите изображение для превью",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Признак публикации",
        help_text="Отметьте, если запись опубликована",
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name="Количество просмотров",
        help_text="Количество просмотров записи",
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
