from django import forms

from .models import CustomUser


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации нового пользователя."""

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "phone", "country", "avatar"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иван"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иванов"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 999 123-45-67"}),
            "country": forms.TextInput(attrs={"class": "form-control", "placeholder": "Россия"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_password2(self) -> str:
        """Проверка совпадения паролей."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают. Попробуйте ещё раз.")
        return password2 or ""

    def save(self, commit: bool = True) -> CustomUser:
        """Сохранение пользователя с хешированным паролем."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    """Форма авторизации пользователя."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
    )


class UserProfileForm(forms.ModelForm):
    """ДОП. ЗАДАНИЕ: Форма редактирования профиля пользователя."""

    class Meta:
        model = CustomUser
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
