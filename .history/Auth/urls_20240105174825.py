# pylint: disable=trailing-whitespace
from django.urls import path

from . import views


urlpatterns = [
    path("", views.homePage, name="home"),
    path("auth/login/", views.loginUser, name="login"),
    path("auth/register/", views.RegisterUser.as_view(), name="register"),
    path("auth/logout/", views.logoutUser, name="logout"),
]
