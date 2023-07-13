from datetime import datetime
from django.db import models
from django.db.models import CheckConstraint, Q
from django.contrib.auth.models import User


class Bookshelf(models.Model):
    shelf_number = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)

    class Meta:
        constraints = [CheckConstraint(check=Q(capacity__lte=5), name="max_capacity")]


class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=20)
    pub_date = models.DateTimeField("date published")
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(bookshelf__isnull=False, user__isnull=True)
                | Q(bookshelf__isnull=True, user__isnull=False),
                name="either_bookshelf_or_user_null",
            )
        ]


class BookHistory(models.Model):
    ACTION_CHOICES = [
        ("BORROWED", "Borrowed"),
        ("RETURNED", "Returned"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    action_date = models.DateTimeField("action date")
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)


class BookQueue(models.Model):
    users = models.ManyToManyField(User)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    queue_date = models.DateTimeField("queue date", default=datetime.now())
