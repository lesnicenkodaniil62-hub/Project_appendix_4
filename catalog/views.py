from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import ProductForm
from .models import Product


class ProductListView(ListView):
    """Контроллер главной страницы со списком товаров и пагинацией."""

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


class ProductDetailView(DetailView):
    """Контроллер детальной страницы товара."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """Контроллер добавления нового товара."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("catalog:index")


class ContactView(TemplateView):
    """Контроллер страницы контактов на TemplateView."""

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
