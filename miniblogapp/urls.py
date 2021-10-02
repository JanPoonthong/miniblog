from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("function_login", views.function_login, name="function_login"),
    path("login_page", views.login_page, name="login_page"),
    path("home", views.home, name="home"),
    path("register", views.register, name="register"),
    path("function_logout", views.function_logout, name="function_logout"),
    path("my_blog", views.my_blog, name="my_blog"),
    path("create_blog", views.create_blog, name="create_blog"),
]
