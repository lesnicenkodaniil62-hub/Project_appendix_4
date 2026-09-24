import os

from django import forms
from django.core.exceptions import ValidationError

from .constants import ALLOWED_IMAGE_EXTENSIONS, FORBIDDEN_WORDS, MAX_IMAGE_SIZE
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для добавления и редактирования товара."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        """Стилизация всех полей формы через __init__."""
        super().__init__(*args, **kwargs)

        # Проходим по всем полям формы и применяем стили
        for field_name, field in self.fields.items():
            css_class = "form-control"

            # Для полей выбора (Select) используем form-select
            if isinstance(field.widget, forms.Select):
                css_class = "form-select"
            # Для чекбоксов используем form-check-input
            elif isinstance(field.widget, forms.CheckboxInput):
                css_class = "form-check-input"

            # Применяем класс к виджету
            existing_class = field.widget.attrs.get("class", "")
            if existing_class:
                field.widget.attrs["class"] = f"{existing_class} {css_class}"
            else:
                field.widget.attrs["class"] = css_class

        # Дополнительные атрибуты для конкретных полей
        self.fields["name"].widget.attrs.update({"placeholder": "Введите название товара"})
        self.fields["description"].widget.attrs.update({"placeholder": "Введите описание товара", "rows": 4})
        self.fields["price"].widget.attrs.update({"placeholder": "Укажите цену", "step": "0.01", "min": "0"})
        # Подсказка для поля изображения
        self.fields["image"].help_text = (
            f"Допустимые форматы: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}. "
            f"Максимальный размер: {MAX_IMAGE_SIZE // (1024 * 1024)} МБ."
        )

    def _check_forbidden_words(self, text: str) -> None:
        """Проверка текста на наличие запрещённых слов (регистронезависимо)."""
        if not text:
            return

        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word in text_lower:
                raise ValidationError(
                    f"В тексте обнаружено запрещённое слово: '{word}'. " f"Пожалуйста, удалите его и попробуйте снова."
                )

    def clean_name(self) -> str:
        """Валидация поля name — проверка на запрещённые слова."""
        name = self.cleaned_data.get("name", "")
        self._check_forbidden_words(name)
        return name

    def clean_description(self) -> str:
        """Валидация поля description — проверка на запрещённые слова."""
        description = self.cleaned_data.get("description", "")
        self._check_forbidden_words(description)
        return description

    def clean_price(self) -> float:
        """Валидация поля price — цена не может быть отрицательной."""
        price = self.cleaned_data.get("price")

        if price is None:
            raise ValidationError("Пожалуйста, укажите цену товара.")

        if price < 0:
            raise ValidationError(
                f"Цена не может быть отрицательной. "
                f"Вы указали: {price} ₽. "
                f"Пожалуйста, введите корректную стоимость товара (0 или больше)."
            )

        return price

    def clean_image(self):
        """Валидация загружаемого изображения.

        Проверяет:
        - Формат файла (только JPEG и PNG)
        - Размер файла (не более 5 МБ)
        """
        image = self.cleaned_data.get("image")

        # Если изображение не загружено — пропускаем валидацию
        # (поле может быть необязательным)
        if not image:
            return image

        # === Проверка 1: Формат файла ===
        # Получаем расширение файла в нижнем регистре
        _, ext = os.path.splitext(image.name)
        ext_lower = ext.lower()

        if ext_lower not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError(
                f"Недопустимый формат изображения: '{ext}'. "
                f"Разрешены только форматы: "
                f"{', '.join(ALLOWED_IMAGE_EXTENSIONS)}."
            )

        # === Проверка 2: Размер файла ===
        # image.size — размер в байтах
        if image.size > MAX_IMAGE_SIZE:
            size_mb = image.size / (1024 * 1024)
            max_mb = MAX_IMAGE_SIZE // (1024 * 1024)
            raise ValidationError(
                f"Размер изображения слишком большой: {size_mb:.2f} МБ. "
                f"Максимально допустимый размер: {max_mb} МБ. "
                f"Пожалуйста, сожмите изображение и попробуйте снова."
            )

        return image
