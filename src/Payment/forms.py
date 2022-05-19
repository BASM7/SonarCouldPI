from . import models
from django import forms


class AddPaymentForm(forms.ModelForm):
    class Meta:
        model = models.Payment
        fields = [
            'name',
            'description',
        ]

        labels = {
            'name': 'Nombre de la forma de pago',
            'description': 'Descripción',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
