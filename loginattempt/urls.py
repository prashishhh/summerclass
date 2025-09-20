# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.fake_admin_login, name="fake_admin"),
]
