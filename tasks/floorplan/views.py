import json
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Household
from .models import FloorPlan

class Builder3D(LoginRequiredMixin, TemplateView):
    template_name = 'floorplan/builder3d.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        household = get_object_or_404(Household, pk=kwargs['pk'])
        # ensure user is in this household
        if self.request.user.household_id != household.pk:
            return redirect('main:household_landing')
        plan, _ = FloorPlan.objects.get_or_create(household=household)
        ctx.update({
            'household_pk': household.pk,
            'layout_json': json.dumps(plan.layout or {}),
        })
        return ctx

def save_layout(request, pk):
    # only POST from logged-in users
    if request.method != 'POST' or not request.user.is_authenticated:
        return redirect('floorplan:builder3d', pk=pk)
    household = get_object_or_404(Household, pk=pk)
    plan = get_object_or_404(FloorPlan, household=household)
    # parse JSON body
    data = json.loads(request.body.decode())
    plan.layout = data.get('layout', {})
    plan.save()
    return render(request, status=204, content_type='application/json')
