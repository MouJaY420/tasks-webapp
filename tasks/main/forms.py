# main/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import User, Household

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Household Name'})
        }

class CustomUserChangeForm(UserChangeForm):
    password = None  # hide password field

    class Meta:
        model = User
        fields = ('display_name', 'email', 'gamification_enabled', 'receive_notifications')
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'gamification_enabled': forms.CheckboxInput(),
            'receive_notifications': forms.CheckboxInput(),
        }

class HouseholdSettingsForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ['name', 'default_currency', 'default_language', 'household_shop', 'gamification_enabled']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'default_currency': forms.Select(attrs={'class':'form-select'}),
            'default_language': forms.Select(attrs={'class':'form-select'}),
            'household_shop': forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'gamification_enabled': forms.CheckboxInput(attrs={'class':'form-check-input'}),

        }