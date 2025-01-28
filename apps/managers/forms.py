from django import forms
from apps.managers.models import Manager, Venue, RequiredThing

class ManagerRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        max_length=255,
        required=True,
    )

    class Meta:
        model = Manager
        fields = ("first_name", "last_name", "email", "phone", "password")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password and confirm password do not match")

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = [
            'name', 'party_name', 'party_contact', 'address', 
            'city', 'pincode', 'state', 'country', 
            'venue_charge', 'public_strength'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Venue Name'}),
            'party_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Party Name'}),
            'party_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Party Contact'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'venue_charge': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Venue Charge'}),
            'public_strength': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Public Strength'}),
        }


class RequiredThingForm(forms.ModelForm):
    class Meta:
        model = RequiredThing
        fields = ['name', 'price_per_qty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thing Name'}),
            'price_per_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price (per Quantity)'}),
        }