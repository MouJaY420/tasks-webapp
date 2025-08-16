# menu/urls.py
from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('dashboard/', views.menu_dashboard, name='menu_dashboard'),
    path('plan/<int:pk>/edit/', views.edit_menu_plan, name='edit_menu_plan'),
    path('plan/<int:pk>/delete/', views.delete_menu_plan, name='delete_menu_plan'),
    
]
