from django.shortcuts import render

from .models import Contact, Product


def index(request):
    """Контроллер для отображения домашней страницы."""
    # Выборка последних 5 созданных продуктов
    latest_products = Product.objects.order_by("-created_at")[:5]

    # Вывод в консоль
    print("\n=== Последние 5 продуктов ===")
    for product in latest_products:
        print(f"ID: {product.id} | Название: {product.name} | Цена: {product.price} | Категория: {product.category}")
    print("==============================\n")

    return render(request, "catalog/home.html")


def contacts(request):
    """Контроллер для отображения страницы с контактной информацией."""
    # Получение всех контактных данных из БД
    contacts_list = Contact.objects.all()
    context = {
        "success": False,
        "contacts_list": contacts_list,
    }

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Получено сообщение от {name} ({phone}): {message}")
        context["success"] = True

    return render(request, "catalog/contacts.html", context)
