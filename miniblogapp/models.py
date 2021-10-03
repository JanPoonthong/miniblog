from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Blog(models.Model):
    name = models.CharField(max_length=64)
    content = models.TextField(max_length=300)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=None
    )
    create_at = models.DateTimeField(auto_now_add=True)
    open_at = models.BooleanField(null=True, default=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
