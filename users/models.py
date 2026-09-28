from typing import Any, cast

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя с email в качестве USERNAME_FIELD."""

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any) -> "CustomUser":
        """Создание обычного пользователя."""
        if not email:
            raise ValueError("Email обязателен для создания пользователя")

        email = self.normalize_email(email)
        # Используем cast, чтобы mypy знал, что это CustomUser, а не абстрактный тип
        user = cast("CustomUser", self.model(email=email, **extra_fields))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: Any) -> "CustomUser":
        """Создание суперпользователя."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Кастомная модель пользователя с email в качестве USERNAME_FIELD."""

    # Отключаем стандартное поле username
    username = None  # type: ignore

    # Email как основное поле для авторизации
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите email для входа в систему",
    )

    # Дополнительные поля по заданию
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите изображение профиля",
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Страна",
        help_text="Введите страну проживания",
    )

    # Указываем email как поле для авторизации
    # Простой type: ignore надёжно подавляет все предупреждения mypy для этих строк
    USERNAME_FIELD = "email"  # type: ignore
    REQUIRED_FIELDS: list[str] = []  # type: ignore

    # Кастомный менеджер
    objects = CustomUserManager()  # type: ignore

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined"]

    def __str__(self) -> str:
        return self.email
