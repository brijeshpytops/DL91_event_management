from django.db import models

from apps.master.models import BaseClass
from apps.managers.models import Manager
# Create your models here.


class Wine(BaseClass):
    WINE_TYPES = [
        ('Red', 'Red'),
        ('White', 'White'),
        ('Rosé', 'Rosé'),
        ('Sparkling', 'Sparkling'),
        ('Dessert', 'Dessert'),
        ('Fortified', 'Fortified'),
    ]
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    wine_name = models.CharField(max_length=100, unique=True)
    wine_price = models.DecimalField(max_digits=10, decimal_places=2)
    wine_type = models.CharField(max_length=20, choices=WINE_TYPES)
    alcohol_content = models.FloatField(help_text="Percentage of alcohol content")
    wine_qty_ml = models.PositiveIntegerField(help_text="Quantity in milliliters (ml)")

    def __str__(self):
        return f"{self.wine_name} - {self.wine_qty_ml}ml"

    