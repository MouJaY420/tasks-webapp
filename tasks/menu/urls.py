# menu/urls.py
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('dashboard/', views.menu_dashboard, name='menu_dashboard'),
    
]
