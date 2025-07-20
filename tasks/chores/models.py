from django.db import models
from main.models import Household

# Create your models here.
class TaskTemplate(models.Model):
    """
    A reusable default task—for initial setup.
    """
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    default_points = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name
    

class HouseholdTask(models.Model):
    """
    An instance of a task for a specific household.
    """
    household   = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='tasks')
    template    = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, null=True)
    quantity    = models.PositiveSmallIntegerField(default=1)
    # status, due_date, assigned_to, etc. can come later
    created_at  = models.DateTimeField(auto_now_add=True)

    @property
    def total_points(self):
        return (self.template.default_points or 0) * self.quantity

    def __str__(self):
        return f"{self.household.name}: {self.template.name} x{self.quantity}"