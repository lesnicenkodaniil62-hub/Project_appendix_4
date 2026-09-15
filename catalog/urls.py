from django.urls import path

from .views import ContactView, ProductCreateView, ProductDetailView, ProductListView

app_name = "catalog"

urlpatterns = [
    path("home/", ProductListView.as_view(), name="index"),
    path("contacts/", ContactView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("product/add/", ProductCreateView.as_view(), name="add_product"),
]
