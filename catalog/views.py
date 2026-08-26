from django.shortcuts import render


def index(request):
    """Контроллер для отображения домашней страницы."""
    return render(request, "catalog/home.html")


def contacts(request):
    """Контроллер для отображения страницы с контактной информацией."""
    return render(request, "catalog/contacts.html")
