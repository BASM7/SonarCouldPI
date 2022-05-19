from . import models
from django import forms


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            'name',
            'lastname',
            'type'
        ]

        labels = {
            'name': 'Nombre',
            'lastname': 'Apellido',
            'type': 'Registrarse como'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'}),
            'type': forms.Select(choices=[('1', 'Tutorando'), ('2', 'Tutor')], attrs={'class': 'form-select'})
        }


class NewAdminForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = [
            'email'
        ]

        labels = {
            'email': 'Correo'
        }

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': 'true'})
        }
