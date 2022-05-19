from . import models
from django import forms


class AddRegionForm(forms.ModelForm):
    class Meta:
        model = models.Regions
        fields = [
            'region_name',
            'country'
        ]

        labels = {
            'region_name': 'Región',
            'Country': 'País'
        }

        widgets = {
            'region_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'})
        }
