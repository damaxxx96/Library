from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # ex: 127.0.0.1/books/bookshelf/create/
    path("bookshelf/create/", views.create_bookshelf, name="create_bookshelf"),
    path("book/create/", views.create_book, name="create_book"),
    path("borrow/", views.borrow_book, name="borrow_book"),
    path("return/", views.return_book, name="return_book"),
]
