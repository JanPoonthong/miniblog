from django.contrib import admin

from .models import Blog, Category


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "content",
        "category",
        "create_at",
        "open_at",
        "author",
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


# admin.site.register(User)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
