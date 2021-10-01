from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError

from .models import User


def function_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(type(user), user is not None)
        if user is not None:
            login(request, user)
        else:
            return render(
                request,
                "miniblogapp/login.html",
                {"message": "Invalid username and/or password."},
            )
    return render(request, "miniblogapp/home.html", {})


def login_page(request):
    return render(request, "miniblogapp/login.html", {})


def home(request):
    return render(request, "miniblogapp/home.html", {})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(
                request,
                "miniblogapp/register.html",
                {"message": "Passwords must match."},
            )
        try:
            user = User.objects.create_user(username, password)
            user.save()
            print(f"register {type(user)}")
        except ValueError:
            return render(
                request,
                "miniblogapp/register.html",
                {"message": "Fill up the form."},
            )
        except IntegrityError:
            return render(
                request,
                "miniblogapp/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect("home")
    return render(request, "miniblogapp/register.html")


def function_logout(request):
    logout(request)
    return HttpResponseRedirect("login_page")
