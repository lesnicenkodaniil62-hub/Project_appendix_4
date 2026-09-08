from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для добавления нового товара."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Название товара"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Описание товара"}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Цена", "step": "0.01"}),
        }
