from django.urls import path
from . import views

urlpatterns = [
    path("members/", views.members, name="members"),
    path("user-list/", views.user_list_view, name="user_list"),
    path("user-book/", views.user_books_view, name="user_book"),
]
