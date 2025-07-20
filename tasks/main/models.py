import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from core.constants import CURRENCY_CHOICES, LANGUAGE_CHOICES


def generate_household_code():
    return uuid.uuid4().hex[:8]


class Household(models.Model):
    """
    Represents a shared household for grouping users, tasks, events, and expenses.
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(
        max_length=8,
        default=generate_household_code,
        unique=True,
        help_text='Invite code for others to join.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    default_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='CHF',
        help_text='Currency for shared expenses.'
    )
    default_language = models.CharField(choices=
                                        LANGUAGE_CHOICES,
                                        max_length=10,
                                        default='en',
                                        help_text='Default language for the household.'
                                        )
    household_shop = models.BooleanField(default=False)
    gamification_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    verbose_name = "Household"
    verbose_name_plural = "Households"




class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser to include
    shared/private scopes, gamification toggles, and household membership.
    Overrides group and permission related names to avoid clashes.
    """
    display_name = models.CharField(max_length=150, blank=True)

    # Override default groups and permissions to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='main_users',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='main_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    household = models.ForeignKey(
        Household,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members',
        help_text='The single household this user belongs to.'
    )

    gamification_enabled = models.BooleanField(
        default=True,
        help_text='Toggle gamification features on/off.'
    )
    points = models.PositiveIntegerField(
        default=0,
        help_text='Accumulated points from completing tasks.'
    )

    receive_notifications = models.BooleanField(
        default=True,
        help_text='Whether user receives email/alert notifications.'
    )

    default_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='CHF',
        help_text='Your preferred currency.'
    )

    def __str__(self):
        return self.display_name or self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    