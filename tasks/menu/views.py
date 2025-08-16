from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuPlan, MenuEntry
from .forms import MenuPlanForm, MenuEntryFormSet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.models import Household
from datetime import timedelta, date
from django.forms import inlineformset_factory

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
    if not household.meal_count:
        if request.method == 'POST':
            count = int(request.POST.get('meal_count'))
            household.meal_count = count
            household.save()
            return redirect('menu:menu_dashboard')
        return render(request, 'menu/set_meal_count.html')

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
        meal_count = household.meal_count
        initial_entries = []
        for i in range((end - start).days + 1):
            d = start + timedelta(days=i)
            for meal_number in range(1, meal_count + 1):
                initial_entries.append({'date': d, 'meal_type': f'meal_{meal_number}'})

        formset = MenuEntryFormSet(queryset=MenuEntry.objects.none(),
                                initial=initial_entries)

    existing_plans = MenuPlan.objects.filter(household=household).order_by('-start_date')
    return render(request, 'menu/menu_dashboard.html', {
        'plan_form': plan_form,
        'formset': formset,
        'existing_plans': existing_plans,
    })

MenuEntryFormSet = inlineformset_factory(
    MenuPlan,
    MenuEntry,
    fields=['date','meal_type','description'],
    extra=0,
    can_delete=True
)

@login_required
def edit_menu_plan(request, pk):
    plan = get_object_or_404(MenuPlan, pk=pk, household__members=request.user)
    formset = MenuEntryFormSet(request.POST or None, instance=plan)
    if request.method == 'POST' and formset.is_valid():
        formset.save()
        messages.success(request, "Plan updated.")
        return redirect('menu:menu_dashboard')
    return render(request, 'menu/edit_menu_plan.html', {'plan': plan, 'formset': formset})

@login_required
def delete_menu_plan(request, pk):
    plan = get_object_or_404(MenuPlan, pk=pk, household__members=request.user)
    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Plan deleted.")
        return redirect('menu:menu_dashboard')
    return render(request, 'menu/confirm_delete.html', {'plan': plan})

