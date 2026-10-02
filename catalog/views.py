from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    """Список товаров — ПУБЛИЧНАЯ страница."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.order_by("-created_at")[:5]
        print("\n=== Последние 5 продуктов ===")
        for product in latest_products:
            print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price}")
        print("==============================\n")
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Детальная страница товара."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание товара.

    При создании автоматически заполняется поле owner.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = "/"

    def form_valid(self, form: ProductForm) -> HttpResponse:
        """Автоматически устанавливаем owner = текущий пользователь."""
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("catalog:index")


class OwnerOrModeratorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Миксин: доступ только для владельца товара ИЛИ модератора."""

    raise_exception = True

    def test_func(self) -> bool:
        """Проверка: пользователь — владелец товара или модератор."""
        product: Product = self.get_object()  # type: ignore[attr-defined]
        user = self.request  # type: ignore[attr-defined]
        user = user.user

        if product.owner_id is not None and product.owner_id == user.pk:
            return True

        if user.has_perm("catalog.can_unpublish_product"):
            return True

        return False


class ProductUpdateView(OwnerOrModeratorMixin, UpdateView):
    """Редактирование товара.

    🔒 Доступ только для владельца или модератора.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"

    def get_success_url(self) -> str:
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(OwnerOrModeratorMixin, DeleteView):
    """Удаление товара.

    🔒 Доступ только для владельца или модератора.
    """

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = "/"

    def get_success_url(self) -> str:
        return reverse("catalog:index")


class ContactView(TemplateView):
    """Контакты — ПУБЛИЧНАЯ страница."""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["success"] = False
        return context

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Получено сообщение от {name} ({phone}): {message}")
        context = self.get_context_data(**kwargs)
        context["success"] = True
        return render(request, self.template_name, context)
