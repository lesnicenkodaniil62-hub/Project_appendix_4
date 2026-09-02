from django.db import models


class Category(models.Model):
    """Модель категории товара."""

    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите название категории",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Модель товара."""

    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите название продукта",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
        help_text="Введите описание продукта",
    )
    image = models.ImageField(
        upload_to="photos/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
        verbose_name="Категория",
        help_text="Выберите категорию продукта",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Укажите цену продукта",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category"]

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"

class Contact(models.Model):
    """Модель контактных данных."""

    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите название контакта",
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Email",
        help_text="Введите email",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите номер телефона",
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name="Адрес",
        help_text="Введите адрес",
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name