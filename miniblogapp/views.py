from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Blog, Category
from .forms import CreateBlog


def remove_blog(request, blog_id):
    if request.user.is_authenticated:
        Blog.objects.get(pk=blog_id).delete()
        return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponseRedirect(reverse("login_page"))


def edit_update(request, blog_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST["name"]
            content = request.POST["content"]
            category = request.POST["category"]
            Blog.objects.filter(pk=blog_id).update(
                name=name,
                content=content,
                category=category,
                author=request.user,
            )
            return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponseRedirect(reverse("login_page"))


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
    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, pk=blog_id)
        if request.user == blog.author:
            return render(request, "miniblogapp/edit.html", {"blog": blog})
        else:
            return HttpResponse("<h3>You're not the author of this blog</h3>")
    else:
        return HttpResponseRedirect(reverse("login_page"))


def create_blog(request):
    if request.user.is_authenticated:
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
            return render(
                request, "miniblogapp/create_blog.html", {"form": form}
            )
    else:
        return HttpResponseRedirect(reverse("login_page"))


def my_blog(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=request.user)
        is_user_blogs_exist = blogs.exists()
        return render(
            request,
            "miniblogapp/my_blog.html",
            {"blogs": blogs, "is_user_blogs_exist": is_user_blogs_exist},
        )
    else:
        return HttpResponseRedirect(reverse("login_page"))


def login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("home")
    else:
        return render(request, "miniblogapp/login.html", {})


def home(request):
    if request.user.is_authenticated:
        create_category()
        blogs = Blog.objects.filter(open_at=True).exclude(author=request.user)
        author_blogs = Blog.objects.filter(author=request.user)
        is_blogs_exist = Blog.objects.exists()
        print(is_blogs_exist)
        return render(
            request,
            "miniblogapp/home.html",
            {
                "blogs": blogs,
                "author_blogs": author_blogs,
                "is_blogs_exist": is_blogs_exist,
            },
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
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect("login_page")
    else:
        return HttpResponse(
            "<h3>You can not logout because you're not login yet</h3>"
        )
