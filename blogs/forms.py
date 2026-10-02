from django import forms

from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Форма для создания и редактирования публикации."""

    class Meta:
        model = BlogPost
        fields = ["title", "content", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Заголовок публикации"}),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Содержание публикации",
                    "rows": 10,
                }
            ),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
