from django import forms
from django.forms import ModelForm

from .models import Blog


class CreateBlog(ModelForm):
    class Meta:
        model = Blog
        fields = [
            "name",
            "content",
            "category",
        ]
