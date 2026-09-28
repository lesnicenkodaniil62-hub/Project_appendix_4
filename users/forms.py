from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации нового пользователя."""

    # Дополнительные поля пароля (не из модели)
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "country", "avatar"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иван"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иванов"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 999 123-45-67"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Россия"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Стилизация полей формы."""
        super().__init__(*args, **kwargs)
        # Применяем form-control ко всем полям модели
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get("class", "")
            if "form-control" not in existing_class:
                if isinstance(field.widget, forms.ClearableFileInput):
                    field.widget.attrs["class"] = f"{existing_class} form-control".strip()

    def clean_password2(self):
        """Проверка совпадения паролей."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают. Попробуйте ещё раз.")

        return password2

    def save(self, commit=True):
        """Сохранение пользователя с хешированным паролем."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Форма авторизации пользователя по email и паролю."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
    )


class UserProfileForm(forms.ModelForm):
    """Форма редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone", "country", "avatar"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@mail.com",
                    "readonly": True,  # Email нельзя менять — это логин
                }
            ),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иван"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иванов"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 999 123-45-67"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Россия"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Стилизация полей формы."""
        super().__init__(*args, **kwargs)
        # Применяем form-control ко всем полям
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get("class", "")
            if "form-control" not in existing_class:
                field.widget.attrs["class"] = f"{existing_class} form-control".strip()
