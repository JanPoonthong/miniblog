# Generated by Django 3.2.7 on 2021-10-02 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("miniblogapp", "0003_blog_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="open_at",
            field=models.BooleanField(default=True, null=True),
        ),
    ]
