from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('menu_plan/', views.create_menu_plan, name='create_menu_plan'),
]
