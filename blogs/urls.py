from django.urls import path

from .views import BlogPostCreateView, BlogPostDeleteView, BlogPostDetailView, BlogPostListView, BlogPostUpdateView

app_name = "blogs"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="post_list"),
    path("<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
    path("create/", BlogPostCreateView.as_view(), name="post_create"),
    path("<int:pk>/update/", BlogPostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", BlogPostDeleteView.as_view(), name="post_delete"),
]
