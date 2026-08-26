from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Контроллер для отображения домашней страницы."""
    # render автоматически возвращает HttpResponse, mypy это знает благодаря django-stubs
    return render(request, "catalog/home.html")


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
