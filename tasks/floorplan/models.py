from django.db import models
from django.conf import settings
from django.db.models import JSONField
# Create your models here.

class FloorPlan(models.Model):
    household = models.OneToOneField(
        'main.Household',
        on_delete=models.CASCADE,
        related_name='floorplan'
    )
    # stores an array of room‐objects: {id, type, x, y, width, height, props…}
    layout = JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.household.name} floorplan"