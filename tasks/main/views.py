from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, UpdateView, TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Sum

from .forms import CustomUserCreationForm, HouseholdForm, CustomUserChangeForm, HouseholdSettingsForm
from .models import Household, User
from expenses.forms import ExpenseForm
from expenses.models import Expense

# Home and Registration

def home(request):
    return render(request, "main/home.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. You can now log in.")
            return redirect('main:home')
    else:
        form = CustomUserCreationForm()
    return render(request, "main/register.html", {"form": form})

# Household Landing (join/create) view

@login_required
def household_landing(request):
    if request.user.household:
        return redirect('main:household_dashboard', pk=request.user.household.pk)

    form = HouseholdForm(request.POST or None)
    join_error = None

    if request.method == "POST":
        if 'create' in request.POST and form.is_valid():
            h = form.save()
            request.user.household = h
            request.user.save()
            return redirect('main:household_dashboard', pk=h.pk)
        elif 'join' in request.POST:
            code = request.POST.get('household_code')
            try:
                h = Household.objects.get(code=code)
                request.user.household = h
                request.user.save()
                return redirect('main:household_dashboard', pk=h.pk)
            except Household.DoesNotExist:
                join_error = "Invalid join code."

    return render(request, 'main/household_landing.html', {
        'form': form,
        'join_error': join_error,
    })

# Household detail with inline shared expense form



class HouseholdDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Household
    template_name = 'main/household_detail.html'
    context_object_name = 'household'
    form_class = ExpenseForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        # Pre-fill so we don’t need the hidden share checkbox
        kwargs['initial'] = {
            'share_with_household': True,
            'household': self.get_object().pk
        }
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['shared_expenses'] = self.object.shared_expenses.all()
        ctx['expense_form'] = self.get_form()
        return ctx

    def post(self, request, *args, **kwargs):
        # Bind and validate the inline form
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.household = self.object
            exp.save()
            return redirect('main:household_detail', pk=self.object.pk)
        return self.form_invalid(form)


# Profile view with inline private expense form

class ProfileView(LoginRequiredMixin, FormMixin, DetailView):
    model = get_user_model()
    template_name = 'main/profile.html'
    context_object_name = 'user_obj'
    form_class = ExpenseForm
    success_url = reverse_lazy('main:profile')

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['private_expenses'] = Expense.objects.filter(
            user=self.request.user,
            household__isnull=True
        )
        ctx['expense_form'] = self.get_form()
        return ctx

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            exp = form.save(commit=False)
            exp.user = request.user
            exp.household = None
            exp.save()
            return self.form_valid(form)
        return self.form_invalid(form)

# Profile update (edit user info)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = 'main/profile_edit.html'
    success_url = reverse_lazy('main:profile')

    def get_object(self):
        return self.request.user

class HouseholdDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/household_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        household = get_object_or_404(Household, pk=kwargs['pk'])
        ctx['household'] = household
        return ctx
    

class HouseholdSettingsView(LoginRequiredMixin, UpdateView):
    model = Household
    form_class = HouseholdSettingsForm
    template_name = 'main/household_settings.html'
    context_object_name = 'household'

    def get_object(self):
        # only let the current user edit their own household
        return self.request.user.household

    def form_valid(self, form):
        # Save the form and get the updated household
        self.object = form.save()
        # Redirect explicitly to the dashboard for this household
        return redirect(
            'main:household_dashboard',
            pk=self.object.pk
        )