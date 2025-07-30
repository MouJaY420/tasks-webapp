from django import forms
from .models import MenuPlan, MenuEntry
from django.forms import modelformset_factory

class MenuPlanForm(forms.ModelForm):
    class Meta:
        model = MenuPlan
        fields = ['name', 'start_date', 'end_date']

class MenuEntryForm(forms.ModelForm):
    class Meta:
        model = MenuEntry
        fields = ['date', 'meal_type', 'description']

MenuEntryFormSet = modelformset_factory(
    MenuEntry,
    form=MenuEntryForm,
    extra=0,
    can_delete=False
)
