from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from .forms import ProductForm
from .models import Product


def index(request: HttpRequest) -> HttpResponse:
    """Контроллер для отображения домашней страницы с пагинацией."""
    # Выборка всех продуктов
    products_list = Product.objects.all()

    # Пагинация: 6 товаров на страницу
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Вывод последних 5 продуктов в консоль (сохраняем из доп. задания)
    latest_products = Product.objects.order_by("-created_at")[:5]
    print("\n=== Последние 5 продуктов ===")
    for product in latest_products:
        print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price}")
    print("==============================\n")

    context = {
        "page_obj": page_obj,
    }

    return render(request, "catalog/home.html", context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Контроллер для отображения страницы с контактной информацией."""
    context = {"success": False}

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Получено сообщение от {name} ({phone}): {message}")
        context["success"] = True

    return render(request, "catalog/contacts.html", context)


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Контроллер для отображения подробной информации о товаре."""
    product = get_object_or_404(Product, pk=pk)

    context = {
        "product": product,
    }

    return render(request, "catalog/product_detail.html", context)


def add_product(request: HttpRequest) -> HttpResponse:
    """Контроллер для добавления нового товара."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("catalog:index")
    else:
        form = ProductForm()

    context = {
        "form": form,
    }

    return render(request, "catalog/add_product.html", context)
