from django.shortcuts import render


def index(request):
    """Контроллер для отображения домашней страницы."""
    return render(request, "catalog/home.html")


def contacts(request):
    """Контроллер для отображения страницы с контактной информацией."""
    context = {"success": False}

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Получено сообщение от {name} ({phone}): {message}")
        context["success"] = True

    return render(request, "catalog/contacts.html", context)
