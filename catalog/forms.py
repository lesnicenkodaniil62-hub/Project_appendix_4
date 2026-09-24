from django import forms
from django.core.exceptions import ValidationError

from .constants import FORBIDDEN_WORDS
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для добавления и редактирования товара."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название товара"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Описание товара"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Цена", "step": "0.01"}),
        }

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
