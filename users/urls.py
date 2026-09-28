from django.urls import path

from .views import LoginView, LogoutView, ProfileUpdateView, ProfileView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),  # ← НОВОЕ
    path("profile/update/", ProfileUpdateView.as_view(), name="profile_update"),  # ← НОВОЕ
]
