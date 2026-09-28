from typing import Any

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import CustomUser


class RegisterView(CreateView):
    """Регистрация нового пользователя."""

    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form: UserRegistrationForm) -> HttpResponse:
        """Сохраняем пользователя и отправляем приветственное письмо."""
        user: CustomUser = form.save()
        self._send_welcome_email(user)
        messages.success(
            self.request,
            "Регистрация прошла успешно! Теперь вы можете войти в систему.",
        )
        return redirect(self.success_url)

    def _send_welcome_email(self, user: CustomUser) -> None:
        """Отправка приветственного письма после регистрации."""
        if not settings.EMAIL_HOST_USER:
            print("Email не настроен — письмо не отправлено")
            return

        display_name = user.first_name or user.email
        subject = f"Добро пожаловать, {display_name}!"
        message = (
            f"Здравствуйте, {display_name}!\n\n"
            f"Спасибо за регистрацию в нашем интернет-магазине.\n\n"
            f"Ваш email: {user.email}\n"
            f"Теперь вы можете:\n"
            f"• Просматривать товары\n"
            f"• Оставлять отзывы\n"
            f"• Делать заказы\n\n"
            f"С уважением,\nКоманда интернет-магазина"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f" Приветственное письмо отправлено на {user.email}")
        except Exception as e:
            print(f" Ошибка отправки письма: {e}")


class LoginView(View):
    """Авторизация пользователя по email и паролю."""

    template_name = "users/login.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Отображение формы входа."""
        if request.user.is_authenticated:
            return redirect("catalog:index")
        form = UserLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Обработка формы входа."""
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)

            # isinstance сужает тип для mypy
            if user is not None and isinstance(user, CustomUser):
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Добро пожаловать, {user.email}!")
                    return redirect("catalog:index")
                messages.error(request, "Ваш аккаунт деактивирован. Обратитесь в поддержку.")
            else:
                messages.error(request, "Неверный email или пароль. Попробуйте ещё раз.")

        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    """Выход из системы."""

    def get(self, request: HttpRequest) -> HttpResponse:
        """Выход и редирект на страницу входа."""
        logout(request)
        messages.success(request, "Вы успешно вышли из системы.")
        return redirect("users:login")


# ==========================================================
# ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ: Профиль пользователя
# ==========================================================


class ProfileView(LoginRequiredMixin, View):
    """Просмотр профиля текущего пользователя.

    🔒 Доступ только для авторизованных пользователей.
    """

    template_name = "users/profile.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Отображение профиля."""
        return render(request, self.template_name, {"user": request.user})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля текущего пользователя.

    Доступ только для авторизованных пользователей.
    """

    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/profile_update.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset: QuerySet[CustomUser] | None = None) -> CustomUser:
        """Возвращаем текущего авторизованного пользователя."""
        # Явно указываем тип возвращаемого объекта для mypy
        user = self.request.user
        if isinstance(user, CustomUser):
            return user
        # На случай, если пользователь не CustomUser (не должно случиться)
        raise ValueError("Пользователь не является экземпляром CustomUser")

    def form_valid(self, form: UserProfileForm) -> HttpResponse:
        """Обработка успешного сохранения формы."""
        messages.success(self.request, "Профиль успешно обновлён!")
        return super().form_valid(form)

    def get_form_kwargs(self) -> dict[str, Any]:
        """Передаём файлы формы (для загрузки аватара)."""
        kwargs = super().get_form_kwargs()
        if self.request.FILES:
            kwargs["files"] = self.request.FILES
        return kwargs
