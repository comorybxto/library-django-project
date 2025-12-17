from django.contrib import admin
from .models import Book, ReadBook

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year']
    search_fields = ['title', 'author']
    list_filter = ['year']

@admin.register(ReadBook)
class ReadBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'date_added']
    search_fields = ['user__username', 'book__title']
    list_filter = ['date_added']