from django.db import models

from apps.master.models import BaseClass
from apps.master.helpers.dynamic_filename import dynamic_filename_for_manager_profile
from apps.managers.constants import *

from datetime import date
# Create your models here.

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
