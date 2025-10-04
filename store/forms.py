from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'gender']
        labels = {
            "first_name": "Imię ",
            "last_name":"Nazwisko ",
            "gender":"Płeć"
        }
        widgets = {
            'gender': forms.Select(choices=Profile.GENDER_CHOICES),
        }