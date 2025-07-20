from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    share_with_household = forms.BooleanField(
        required=False,
        label="Share with my household",
        help_text="Uncheck to keep this expense private."
    )

    class Meta:
        model = Expense
        fields = ['amount', 'currency', 'description', 'household']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.Select(attrs={'class':'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'household': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'household': 'Select your household if sharing.',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow the user’s own household
        if user and user.household:
            self.fields['household'].queryset = user.household.__class__.objects.filter(pk=user.household.pk)
        else:
            # If no household, hide the field entirely
            self.fields['household'].widget = forms.HiddenInput()
        # Default to private
        self.fields['share_with_household'].initial = False

    def clean(self):
        cleaned = super().clean()
        share = cleaned.get('share_with_household')
        household = cleaned.get('household')
        if share:
            if not household:
                raise forms.ValidationError("You must have a household to share with.")
        else:
            # force private
            cleaned['household'] = None
        return cleaned
    
class SharedExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'currency', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }