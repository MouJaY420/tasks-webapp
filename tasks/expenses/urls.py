from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('household/<int:pk>/expenses/', views.household_expenses, name='household_expenses'),
    path('upload-receipt/', views.upload_receipt, name='upload_receipt'),
    path('qr-code/', views.qr_code_view, name='qr_code'),
]
