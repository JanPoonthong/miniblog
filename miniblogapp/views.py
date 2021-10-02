from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User

from .models import Blog, Category
from .forms import CreateBlog


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
        return HttpResponseRedirect("home")


def create_category():
    """First time when user visit the page"""
    if Category.objects.exists() is False:
        default_category = [
            "Programming",
            "Fashion",
            "Christmas",
            "Electronics",
            "Property",
            "Sport",
            "Other",
        ]
        for category in default_category:
            Category.objects.create(name=category)


def edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.user == blog.author:
        return render(request, "miniblogapp/edit.html", {"blog": blog})
    else:
        return HttpResponse("<h3>You're not the author of this blog</h3>")


def create_blog(request):
    if request.method == "POST":
        form = CreateBlog(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["content"]
            category = form.cleaned_data["category"]
            Blog.objects.create(
                name=name,
                content=content,
                category=category,
                author=request.user,
            )
            return HttpResponseRedirect("home")
    else:
        form = CreateBlog()
        return render(request, "miniblogapp/create_blog.html", {"form": form})


def my_blog(request):
    blogs = Blog.objects.filter(author=request.user)
    return render(request, "miniblogapp/my_blog.html", {"blogs": blogs})


def login_page(request):
    return render(request, "miniblogapp/login.html", {})


def home(request):
    create_category()
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(open_at=True).exclude(author=request.user)
        author_blogs = Blog.objects.filter(author=request.user)
        return render(
            request,
            "miniblogapp/home.html",
            {"blogs": blogs, "author_blogs": author_blogs},
        )
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
