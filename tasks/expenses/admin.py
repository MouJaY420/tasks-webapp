from django.contrib import admin
from .models import Expense

# Register your models here.

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display   = (
        'user',
        'household',
        'amount',
        'currency',
        'converted_amount',
        'date',
        'scope',
    )
    list_filter    = (
        'household',
        'currency',
        'date',
        'scope',
    )
    search_fields  = (
        'user__username',
        'description',
        'code',
    )