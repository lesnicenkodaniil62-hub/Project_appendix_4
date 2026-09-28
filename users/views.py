from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import UserLoginForm, UserRegistrationForm

User = get_user_model()


class RegisterView(CreateView):
    """Представление регистрации нового пользователя."""

    form_class = UserRegistrationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """Сохраняем пользователя и отправляем приветственное письмо."""
        # Сохраняем пользователя (пароль хешируется в форме через set_password)
        user = form.save()

        # Отправляем приветственное письмо
        self._send_welcome_email(user)

        # Сообщение об успешной регистрации
        messages.success(
            self.request,
            "Регистрация прошла успешно! Теперь вы можете войти в систему.",
        )

        return redirect(self.success_url)

    def _send_welcome_email(self, user: User) -> None:
        """Отправка приветственного письма после регистрации."""
        if not settings.EMAIL_HOST_USER:
            print("Email не настроен — письмо не отправлено")
            return

        subject = f"Добро пожаловать, {user.first_name or user.email}!"
        message = (
            f"Здравствуйте, {user.first_name or user.email}!\n\n"
            f"Спасибо за регистрацию в нашем интернет-магазине.\n\n"
            f"Ваш email: {user.email}\n"
            f"Теперь вы можете:\n"
            f"• Просматривать товары\n"
            f"• Оставлять отзывы\n"
            f"• Делать заказы\n\n"
            f"Если у вас есть вопросы — ответим на это письмо.\n\n"
            f"С уважением,\n"
            f"Команда интернет-магазина"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            print(f"Приветственное письмо отправлено на {user.email}")
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")


class LoginView(View):
    """Представление авторизации пользователя по email и паролю."""

    template_name = "users/login.html"

    def get(self, request):
        """Отображение формы входа."""
        # Если пользователь уже авторизован — редирект на главную
        if request.user.is_authenticated:
            return redirect("catalog:index")

        form = UserLoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        """Обработка формы входа."""
        form = UserLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Аутентификация пользователя
            # ⚠️ ВАЖНО: username=email — это особенность Django,
            # функция authenticate всегда ожидает параметр username,
            # даже если у нас поле называется email
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Добро пожаловать, {user.email}!")
                    return redirect("catalog:index")
                else:
                    messages.error(
                        request, "Ваш аккаунт деактивирован. Обратитесь в поддержку."
                    )
            else:
                messages.error(
                    request, "Неверный email или пароль. Попробуйте ещё раз."
                )

        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    """Представление выхода из системы."""

    def get(self, request):
        """Выход из системы и редирект на страницу входа."""
        logout(request)
        messages.success(request, "Вы успешно вышли из системы.")
        return redirect("users:login")