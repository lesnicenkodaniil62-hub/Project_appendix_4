from typing import Any, cast

from django.core.cache import cache

from .models import Product


def get_products_by_category(category_id: int) -> list[dict[str, Any]]:
    """
    Сервис для получения товаров категории с низкоуровневым кэшированием в Redis.

    :param category_id: ID категории
    :return: Список словарей с данными товаров
    """
    # Критерий: Ключ category_{id}
    cache_key = f"category_{category_id}"

    # 1. Пытаемся получить данные из Redis
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        # Данные найдены в кэше, возвращаем их (cast нужен для mypy)
        return cast(list[dict[str, Any]], cached_data)

    # 2. Если в кэше нет, запрашиваем из БД (только опубликованные)
    # Используем .values() для получения словарей, а не объектов моделей (быстрее и легче для кэша)
    products_qs = Product.objects.filter(category_id=category_id, is_published=True).values(
        "id", "name", "description", "price", "image"
    )

    # Преобразуем QuerySet в обычный список словарей
    # Decimal нужно преобразовать в строку для безопасной сериализации в Redis
    product_list: list[dict[str, Any]] = []
    for p in products_qs:
        product_list.append(
            {
                "id": p["id"],
                "name": p["name"],
                "description": p["description"],
                "price": str(p["price"]),  # Decimal -> str
                "image": p["image"] if p["image"] else None,
            }
        )

    # 3. Сохраняем в Redis с заданным TTL (время хранения)
    # Критерий: TTL задан (3600 секунд = 1 час)
    cache.set(cache_key, product_list, timeout=3600)

    return product_list
