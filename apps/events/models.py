from django.db import models

from apps.master.models import BaseClass
from apps.managers.models import Manager, Venue, RequiredThing
from apps.artist.models import Artist
# Create your models here.

class Event(BaseClass):
    EVENT_STATUS_CHOICES = [
        ('Upcoming', 'Upcoming'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)  # Event Image
    event_organizer_name = models.CharField(max_length=255)  # Organizer Name
    event_organizer_contact = models.CharField(max_length=20)  # Organizer Contact
    event_date = models.DateField()  # Event Date
    event_start_time = models.TimeField()
    event_end_time = models.TimeField()
    event_day_of_week = models.CharField(max_length=20)  # Day of the week
    event_description = models.TextField()  # Event Description
    event_status = models.CharField(max_length=20, choices=EVENT_STATUS_CHOICES)  # Event Status
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)  # Artist Name
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)  # Venue Name
    required_thing = models.ManyToManyField(RequiredThing)  # Things Required for the event

    def __str__(self):
        return f"{self.event_name} - {self.artist} on {self.event_date} | {self.event_start_time} - {self.event_end_time}"