# Generated by Django 4.2.2 on 2023-07-01 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0002_remove_bookshelf_max_capacity_bookshelf_max_capacity"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="bookshelf",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="books.bookshelf",
            ),
        ),
    ]