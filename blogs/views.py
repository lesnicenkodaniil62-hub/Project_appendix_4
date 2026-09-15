from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import BlogPost


class BlogPostListView(ListView):
    """Список блоговых записей (только опубликованные)."""

    model = BlogPost
    template_name = "blogs/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        """Возвращаем только опубликованные записи."""
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная страница блоговой записи."""

    model = BlogPost
    template_name = "blogs/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """Увеличиваем счётчик просмотров и отправляем письмо при 100 просмотрах."""
        obj = super().get_object(queryset)
        obj.view_count += 1
        obj.save(update_fields=["view_count"])

        # Проверка достижения 100 просмотров
        if obj.view_count == 100:
            self._send_congratulation_email(obj)

        return obj

    def _send_congratulation_email(self, post: BlogPost) -> None:
        """Отправка поздравительного письма при достижении 100 просмотров."""
        # Проверяем, что email настроен
        if not settings.EMAIL_HOST_USER:
            print("Email не настроен в settings.py")
            return

        subject = f"Поздравляем! Статья '{post.title}' достигла 100 просмотров!"
        message = (
            f"Поздравляем!\n\n"
            f"Ваша статья '{post.title}' достигла замечательной отметки — "
            f"100 просмотров!\n\n"
            f"Дата создания: {post.created_at.strftime('%d.%m.%Y')}\n"
            f"Количество просмотров: {post.view_count}\n\n"
            f"Ссылка на статью: /blogs/{post.pk}/\n\n"
            f"Так держать!"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.EMAIL_HOST_USER]

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            print(f"Письмо отправлено: статья '{post.title}' достигла 100 просмотров!")
        except Exception as e:
            print(f"Ошибка отправки письма: {e}")


class BlogPostCreateView(CreateView):
    """Создание новой блоговой записи."""

    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blogs/post_form.html"
    success_url = reverse_lazy("blogs:post_list")


class BlogPostUpdateView(UpdateView):
    """Редактирование блоговой записи."""

    model = BlogPost
    fields = ["title", "content", "preview", "is_published"]
    template_name = "blogs/post_form.html"

    def get_success_url(self):
        """Перенаправляем на просмотр отредактированной статьи."""
        return reverse_lazy("blogs:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(DeleteView):
    """Удаление блоговой записи."""

    model = BlogPost
    template_name = "blogs/post_confirm_delete.html"
    success_url = reverse_lazy("blogs:post_list")
