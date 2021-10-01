from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("function_login", views.function_login, name="function_login"),
    path("login_page", views.login_page, name="login_page"),
    path("home", views.home, name="home"),
    path("register", views.register, name="register"),
    path("function_logout", views.function_logout, name="function_logout"),
]
