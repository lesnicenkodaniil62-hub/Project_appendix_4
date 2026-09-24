from django.urls import path

from .views import (ContactView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductListView,
                    ProductUpdateView)

app_name = "catalog"

urlpatterns = [
    path("home/", ProductListView.as_view(), name="index"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/add/", ProductCreateView.as_view(), name="add_product"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
