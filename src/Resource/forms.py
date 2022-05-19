from django.forms import RadioSelect

from . import models
from django import forms


class ResourceForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = [
            'name',
            'is_public',
            'description',
            'url',
            'author',
        ]

        labels = {
            'name': 'Nombre del recurso',
            'is_public': 'Es público',
            'description': 'Descripción',
            'url': 'URL',
            'author': 'Autor',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_public': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
        }
