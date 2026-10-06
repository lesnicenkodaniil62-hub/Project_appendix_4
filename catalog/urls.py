from django.urls import path

from .views import (CategoryProductListView, ContactView, ProductCreateView, ProductDeleteView, ProductDetailView,
                    ProductListView, ProductUpdateView)

app_name = "catalog"

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/add/", ProductCreateView.as_view(), name="product_add"),
    path(
        "product/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path("contacts/", ContactView.as_view(), name="contacts"),
    # ✅ Задание 3: Маршрут для товаров категории по ID
    path(
        "category/<int:category_id>/",
        CategoryProductListView.as_view(),
        name="category_products",
    ),
]
