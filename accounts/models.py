from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('reader', 'Reader'),
        ('librarian', 'Librarian'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='reader')
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    class Meta:
        db_table = 'accounts_user'