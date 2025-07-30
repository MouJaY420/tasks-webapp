from django.shortcuts import render, redirect
from .models import MenuPlan, MenuEntry
from .forms import MenuPlanForm, MenuEntryFormSet
from django.contrib.auth.decorators import login_required
from main.models import Household
from datetime import timedelta, date

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
