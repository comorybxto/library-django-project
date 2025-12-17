from django.db import models
from django.conf import settings

class Book(models.Model):
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('romance', 'Romance'),
        ('thriller', 'Thriller'),
        ('self-help', 'Self-Help'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    year = models.IntegerField(help_text="Year published")
    description = models.TextField(blank=True, null=True, help_text="Book description")
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books_book'
        ordering = ['title']

class ReadBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='read_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, help_text="Rating from 1 to 5")

    class Meta:
        db_table = 'books_readbook'
        unique_together = ('user', 'book')
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.rating}★)"