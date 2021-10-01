from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.models import User


def function_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
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
    if request.user.is_authenticated:
        return render(request, "miniblogapp/home.html", {})
    else:
        return render(request, "miniblogapp/login.html", {})


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
            user = User.objects.create_user(
                username=username, password=password
            )
            user.save()
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
        return HttpResponseRedirect("login_page")
    return render(request, "miniblogapp/register.html")


def function_logout(request):
    logout(request)
    return HttpResponseRedirect("login_page")
