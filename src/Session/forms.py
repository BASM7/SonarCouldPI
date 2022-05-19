from . import models
from django import forms


class AddSessionForm(forms.ModelForm):
    class Meta:
        model = models.Session
        fields = [
            'name',
            'description',
        ]

        labels = {
            'name': 'Nombre de la sesión',
            'description': 'Descripción',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
