from . import models
from django import forms
from UserAuthentication.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'lastname'
        ]

        labels = {
            'name': 'Nombre',
            'lastname': 'Apellido'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'})
        }