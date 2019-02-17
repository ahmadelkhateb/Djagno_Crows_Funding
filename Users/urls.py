from django.urls import path
from . import views
from django.conf.urls import url

app_name = "Users"
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('edit/', views.edit, name='edit'),
    path('delete/', views.delete, name='delete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
