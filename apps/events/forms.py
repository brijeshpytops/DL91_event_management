from django import forms
from apps.events.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['manager']  # Exclude the manager field, as it is set automatically in the view
        widgets = {
            "event_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter event name"}),
            "event_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "event_organizer_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter organizer name"}),
            "event_organizer_contact": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter organizer contact"}),
            "event_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "event_start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "event_end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "event_day_of_week": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter day of the week"}),
            "event_description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter event description"}),
            "event_status": forms.Select(attrs={"class": "form-control"}),
            "artist": forms.Select(attrs={"class": "form-control"}),
            "venue": forms.Select(attrs={"class": "form-control"}),
            "required_thing": forms.SelectMultiple(attrs={"class": "form-control"}),
        }
