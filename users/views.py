from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    """Контроллер главной страницы со списком товаров и пагинацией.

    ДОСТУПНА всем (в том числе анонимным пользователям).
    """

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 6

    def get_queryset(self):
        """Возвращаем все товары."""
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        """Добавляем вывод последних 5 товаров в консоль."""
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.order_by("-created_at")[:5]
        print("\n=== Последние 5 продуктов ===")
        for product in latest_products:
            print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price}")
        print("==============================\n")
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Контроллер детальной страницы товара.

    Доступ только для авторизованных пользователей.
    """

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер добавления нового товара.

    Доступ только для авторизованных пользователей.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:index")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования товара.

    Доступ только для авторизованных пользователей.
    """

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"

    def get_success_url(self):
        """После редактирования — редирект на страницу товара."""
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Контроллер удаления товара.

    Доступ только для авторизованных пользователей.
    """

    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("catalog:index")


class ContactView(TemplateView):
    """Контроллер страницы контактов на TemplateView.

    ДОСТУПНА всем (в том числе анонимным пользователям).
    """

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        """Добавляем переменную success в контекст для GET-запросов."""
        context = super().get_context_data(**kwargs)
        context["success"] = False
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Обработка POST-запроса."""
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Получено сообщение от {name} ({phone}): {message}")

        context = self.get_context_data(**kwargs)
        context["success"] = True
        return render(request, self.template_name, context)
