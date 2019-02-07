from django.urls import path
from . import views

app_name = "Users"
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
