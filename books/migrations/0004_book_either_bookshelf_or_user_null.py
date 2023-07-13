# Generated by Django 4.2.2 on 2023-07-04 19:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0003_book_user_alter_book_bookshelf"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="book",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(("bookshelf__isnull", False), ("user__isnull", True)),
                    models.Q(("bookshelf__isnull", True), ("user__isnull", False)),
                    _connector="OR",
                ),
                name="either_bookshelf_or_user_null",
            ),
        ),
    ]
