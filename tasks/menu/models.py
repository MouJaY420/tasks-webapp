from django.db import models
from django.conf import settings
from main.models import Household

class MenuPlan(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Weekly Plan")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"

class MenuEntry(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]

    menu_plan = models.ForeignKey(MenuPlan, related_name='entries', on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.meal_type.capitalize()}: {self.description}"
