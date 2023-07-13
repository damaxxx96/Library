from django.contrib import admin

from books.models import Book, BookHistory, Bookshelf


class BookHistoryAdmin(admin.ModelAdmin):
    list_display = ["book", "user", "action_date", "action"]


# Register your models here.
admin.site.register(Book)

admin.site.register(BookHistory, BookHistoryAdmin)

admin.site.register(Bookshelf)
