from django.db import models
from apps.master.models import BaseClass
from apps.managers.models import Manager

# Create your models here.
#  Artist - details
	# - profile, name[stage-name], artist fields,contact, insta profile, spotify link, artist-charge, description

class Artist(BaseClass):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='artist_profile_pictures/')
    stage_name = models.CharField(max_length=200)
    artist_fields = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)
    instagram_profile = models.URLField(max_length=200)
    spotify_link = models.URLField(max_length=200)
    artist_charge = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        return self.stage_name
    