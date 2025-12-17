from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerView, name='register'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('users/', views.userListView, name='userlist'),
    path('users/<int:user_id>/', views.userProfileView, name='userprofile'),
]