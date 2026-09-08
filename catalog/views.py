from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Product


def index(request: HttpRequest) -> HttpResponse:
    """Контроллер для отображения домашней страницы."""
    # Выборка всех товаров
    products = Product.objects.all()

    # Выборка последних 5 созданных продуктов (для вывода в консоль)
    latest_products = Product.objects.order_by("-created_at")[:5]

    # Вывод в консоль
    print("\n=== Последние 5 продуктов ===")
    for product in latest_products:
        print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price}")
    print("==============================\n")

    context = {
        "products": products,
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
