import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from main.models import Household
from core.constants import CURRENCY_CHOICES
from .utils import get_cached_rate
from decimal import Decimal, getcontext


User = get_user_model()

def generate_expense_code():
    return uuid.uuid4().hex[:8]

class Expense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name='shared_expenses',
        null=True, blank=True,
        help_text='If set, this expense is shared with the household.'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    code = models.CharField(
        max_length=8,
        unique=True,
        default=generate_expense_code
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='CHF',
    )
    converted_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    SCOPE_CHOICES = [
        ('private', 'Private'),
        ('shared',  'Shared'),
    ]
    scope = models.CharField(
        max_length=7,
        choices=SCOPE_CHOICES,
        default='private'
    )

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        # 1) Ensure currency defaults to user preference
        if not self.currency:
            self.currency = self.user.default_currency

        # 2) Convert into the user’s default currency
        base = self.household.default_currency if self.household else self.user.default_currency
        
        if self.currency != base:
            print(f"Converting {self.amount} {self.currency} → {base}")
            try:
                rate = get_cached_rate(self.currency, base)
                getcontext().prec = 12
                self.converted_amount = self.amount * Decimal(str(rate))
            except Exception:
                # On error, just use the raw amount
                self.converted_amount = self.amount
        else:
            self.converted_amount = self.amount

        super().save(*args, **kwargs)

    def __str__(self):
        scope = "(shared)" if self.household else "(private)"
        return f"{self.user}: {self.amount} {self.currency} on {self.date} {scope}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ExpenseItem(models.Model):
    expense = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} – {self.amount}"
