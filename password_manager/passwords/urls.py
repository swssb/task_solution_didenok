from django.urls import path

from .views import PasswordView

urlpatterns = [
    path("", PasswordView.as_view(), name="password-search"),
    path("<str:service_name>", PasswordView.as_view(), name="password-create-retrieve"),
]
