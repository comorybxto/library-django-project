from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.catalogView, name='catalog'),
    path('register-book/', views.registerBookView, name='register-book'),
    path('edit-book/<int:book_id>/', views.editBookView, name='edit-book'),
    path('delete-book/<int:book_id>/', views.deleteBookView, name='delete-book'),
    path('mark-as-read/<int:book_id>/', views.markAsReadView, name='mark-as-read'),
    path('my-profile/', views.myProfileView, name='myprofile'),
    path('remove-read-book/<int:readbook_id>/', views.removeReadBookView, name='remove-read-book'),
]