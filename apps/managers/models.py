from django.db import models

from apps.master.models import BaseClass
from apps.master.helpers.dynamic_filename import dynamic_filename_for_manager_profile
from apps.managers.constants import *

from datetime import date

class Manager(BaseClass):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, default='324135', null=True, blank=True)

    def __str__(self):
        return f"{self.dl91_id} | {self.first_name} {self.last_name}"
    

class ManagerProfileInfo(BaseClass):
    DIR_NAME=UNIQUE_KEYWORD_MANAGER_PROFILE
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    profile = models.ImageField(
        upload_to=dynamic_filename_for_manager_profile,
        default='default_images/manager_profile.png',
        null=True,
        blank=True
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Other'
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        default=date(2025, 1, 1)
    )

class Venue(BaseClass):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Venue Name")
    party_name = models.CharField(max_length=200, verbose_name="Party Name")
    party_contact = models.CharField(max_length=20, verbose_name="Party Contact")
    address = models.TextField(verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    pincode = models.CharField(max_length=10, verbose_name="Pincode")
    state = models.CharField(max_length=100, verbose_name="State")
    country = models.CharField(max_length=100, verbose_name="Country")
    venue_charge = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Venue Charge"
    )
    public_strength = models.PositiveIntegerField(verbose_name="Public Strength")

    def __str__(self):
        return self.name


class RequiredThing(BaseClass):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Thing Name")
    price_per_qty = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price (per Quantity)"
    )

    def __str__(self):
        return f"{self.name}"
    
