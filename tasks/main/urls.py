from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView, LoginView
from .views import HouseholdSettingsView

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/",
        LoginView.as_view(next_page="main:home"),
        name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="main:home"),
        name="logout"
    ),
    path('household/', views.household_landing, name='household_landing'),
    path('household/<int:pk>/', views.HouseholdDetailView.as_view(), name='household_detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('household/<int:pk>/dashboard/', views.HouseholdDashboardView.as_view(), name='household_dashboard'),
    path(
        'household/<int:pk>/settings/',
        HouseholdSettingsView.as_view(),
        name='household_settings'
    ),
]