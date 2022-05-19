from . import models
from django import forms


class AddModalityForm(forms.ModelForm):
    class Meta:
        model = models.Modality
        fields = [
            'name',
            'description',
        ]

        labels = {
            'name': 'Nombre de la modalidad',
            'description': 'Descripción',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
