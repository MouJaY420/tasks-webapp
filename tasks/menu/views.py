from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuPlan, MenuEntry
from .forms import MenuPlanForm, MenuEntryFormSet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Household
from datetime import timedelta, date
from main.models import Household

@login_required
def create_menu_plan(request):
    user = request.user
    household = Household.objects.filter(members=user).first()

    if request.method == 'POST':
        plan_form = MenuPlanForm(request.POST)
        formset = MenuEntryFormSet(request.POST)

        if plan_form.is_valid() and formset.is_valid():
            menu_plan = plan_form.save(commit=False)
            menu_plan.household = household
            menu_plan.save()

            for form in formset:
                entry = form.save(commit=False)
                entry.menu_plan = menu_plan
                entry.save()

            return redirect('menu:view_menu_plan', pk=menu_plan.pk)
    else:
        # Default: start today, end in 6 days
        start = date.today()
        end = start + timedelta(days=6)
        plan_form = MenuPlanForm(initial={'start_date': start, 'end_date': end})

        # Build initial formset (7 days x 3 meals = 21 entries)
        initial_entries = []
        for i in range(7):
            d = start + timedelta(days=i)
            for meal in ['breakfast', 'lunch', 'dinner']:
                initial_entries.append({'date': d, 'meal_type': meal})

        formset = MenuEntryFormSet(queryset=MenuEntry.objects.none(), initial=initial_entries)

    return render(request, 'menu/single_page_menu_plan.html', {
        'plan_form': plan_form,
        'formset': formset
    })

@login_required
def menu_dashboard(request):
    user = request.user
    household = Household.objects.filter(members=user).first()

    if request.method == 'POST':
        plan_form = MenuPlanForm(request.POST)
        formset = MenuEntryFormSet(request.POST)
        if plan_form.is_valid() and formset.is_valid():
            menu_plan = plan_form.save(commit=False)
            menu_plan.household = household
            menu_plan.save()
            for form in formset:
                entry = form.save(commit=False)
                entry.menu_plan = menu_plan
                entry.save()
            messages.success(request, "Menu plan created.")
            return redirect('menu:menu_dashboard')
    else:
        # default: a 7‑day plan starting today
        start = date.today()
        end = start + timedelta(days=6)
        plan_form = MenuPlanForm(initial={'start_date': start, 'end_date': end})
        initial_entries = []
        for i in range(7):
            d = start + timedelta(days=i)
            for meal in ['breakfast', 'lunch', 'dinner']:
                initial_entries.append({'date': d, 'meal_type': meal})
        formset = MenuEntryFormSet(queryset=MenuEntry.objects.none(),
                                initial=initial_entries)

    existing_plans = MenuPlan.objects.filter(household=household).order_by('-start_date')
    return render(request, 'menu/menu_dashboard.html', {
        'plan_form': plan_form,
        'formset': formset,
        'existing_plans': existing_plans,
    })