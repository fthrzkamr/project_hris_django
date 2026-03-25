from django import forms
from .models import EmployeeProfile

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = [
            'phone_number',
            'email_personal',
            'address',
            'birth_date',
            'gender',
            'photo'
        ]
