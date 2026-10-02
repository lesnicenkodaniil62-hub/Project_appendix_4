from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BlogPostForm
from .models import BlogPost


class BlogPostListView(ListView):
    """Список публикаций — ПУБЛИЧНАЯ страница."""

    model = BlogPost
    template_name = "blogs/post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        """Возвращаем все публикации."""
        return BlogPost.objects.all()


class BlogPostDetailView(DetailView):
    """Детальная страница публикации — ПУБЛИЧНАЯ."""

    model = BlogPost
    template_name = "blogs/post_detail.html"
    context_object_name = "post"


class ContentManagerRequiredMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Миксин: доступ только для контент-менеджеров.

    🔒 Требует право can_manage_blog_posts.
    """

    permission_required = "blogs.can_manage_blog_posts"
    raise_exception = True  # 403 Forbidden вместо редиректа на login


class BlogPostCreateView(ContentManagerRequiredMixin, CreateView):
    """Создание публикации.

    🔒 Доступ только для контент-менеджеров.
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogs/post_form.html"

    def form_valid(self, form: BlogPostForm) -> HttpResponse:
        """Автоматически устанавливаем author = текущий пользователь."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """После создания — редирект на список публикаций."""
        return reverse("blogs:post_list")


class BlogPostUpdateView(ContentManagerRequiredMixin, UpdateView):
    """Редактирование публикации.

    🔒 Доступ только для контент-менеджеров.
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blogs/post_form.html"

    def get_success_url(self) -> str:
        """После редактирования — редирект на страницу публикации."""
        return reverse("blogs:post_detail", kwargs={"pk": self.object.pk})


class BlogPostDeleteView(ContentManagerRequiredMixin, DeleteView):
    """Удаление публикации.

    🔒 Доступ только для контент-менеджеров.
    """

    model = BlogPost
    template_name = "blogs/post_confirm_delete.html"

    def get_success_url(self) -> str:
        """После удаления — редирект на список публикаций."""
        return reverse("blogs:post_list")
