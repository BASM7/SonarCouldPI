from django.db.models import fields, query
from django.forms import widgets
from UserAuthentication.models import User
from . import models
from Tutor.models import TutorCourse
from Payment.models import Payment
from Modality.models import Modality
from Session.models import Session
from Tutor.models import Tutor
from Course.models import Course
from Region.models import Regions
from Tutorship.models import Tutorship
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from crispy_forms.bootstrap import PrependedText

import datetime


class TutorScheduleForm(forms.ModelForm):
    class Meta:
        model = models.TutorAvailableSchedule
        fields = ['start_time', 'end_time']
        labels = {
            'start_time': 'Inicio del bloque',
            'end_time': 'Fin del bloque'
        }
        widgets = {
            'start_time': DateTimePickerInput(
                format='%Y-%m-%d %H:%M',
                options={
                    'locale': 'es',
                    'stepping': '30'
                }
            ).start_of('block'),
            'end_time': DateTimePickerInput(
                format='%Y-%m-%d %H:%M',
                options={
                    'locale': 'es',
                    'stepping': '30'
                }
            ).end_of('block'),
        }


class TutorResourceForm(forms.Form):
    resource_name = forms.CharField(widget=forms.TextInput,
                                    initial=None,
                                    label='Nombre:')

    resource_description = forms.CharField(widget=forms.Textarea,
                                           initial=None,
                                           label='Descripción:', )

    is_public = forms.ChoiceField(widget=forms.Select,
                                  choices=((True, 'Pública'), (False, 'Privada')),
                                  initial=True,
                                  label='Visibilidad:')

    resource_url = forms.URLField(widget=forms.TextInput,
                                  initial=None,
                                  label='URL:')

    author = forms.CharField(widget=forms.TextInput,
                             initial=None,
                             label='Fuente:')

    helper = FormHelper()
    helper.use_custom_control = True
    helper.layout = Layout(
        Field('resource_name', css_class='form-control'),
        Field('resource_description', css_class='form-control'),
        Field('is_public', css_class='form-control'),
        Field('resource_url', css_class='form-control'),
        Field('author', css_class='form-control')
    )

    def __init__(self, *args, **kwargs):
        super(TutorResourceForm, self).__init__(*args, **kwargs)
        self.fields['resource_description'].widget.attrs = {'rows': 5}


class ProfileForm(forms.Form):
    choices_region = forms.ModelChoiceField(widget=forms.RadioSelect,
                                             queryset=Regions.objects.all(),
                                             initial=None,
                                             label="Región:")

    tutorship_price = forms.CharField(widget=forms.TextInput,
                                      initial=None,
                                      label="Precio de mis tutorías:")

    increment_half_hour = forms.CharField(widget=forms.TextInput,
                                          initial=None,
                                          label="Precio por el incremento de media hora:")

    choices_session = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             queryset=Session.objects.all(),
                                             initial=None,
                                             label="Tipo de sesión a impartir:")

    choices_modality = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              queryset=Modality.objects.all(),
                                              initial=None,
                                              label="Tipo de modalidad a impartir:")

    choices_payment = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                             queryset=Payment.objects.all(),
                                             initial=None,
                                             label="Método de pago preferido:")

    helper = FormHelper()
    helper.use_custom_control = False
    helper.form_class = 'blueForms'
    helper.layout = Layout(
        Field('choices_region'),
        Div(PrependedText('tutorship_price', '₡', css_class='form-control'),
            css_class='input-group-prepend'),
        Div(PrependedText('increment_half_hour', '₡', css_class='form-control'),
            css_class='input-group-prepend'),
        Field('choices_session'),
        Field('choices_modality'),
        Field('choices_payment'),
        Submit('submit', 'Guardar', css_class='btn btn-primary'),
    )

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            region = Tutor.objects.get(user_id=user.id).region
            tutorship_price = Tutor.objects.get(user_id=user.id).amount_per_person
            increment_half_hour = Tutor.objects.get(user_id=user.id).increment_per_half_hour

            session = Tutor.objects.get(user_id=user.id).session_type.all()
            modality = Tutor.objects.get(user_id=user.id).modality_type.all()
            payment = Tutor.objects.get(user_id=user.id).payment_type.all()

            super(ProfileForm, self).__init__(*args, **kwargs)
            
            self.fields['choices_region'].initial = region
            self.fields['tutorship_price'].initial = tutorship_price
            self.fields['increment_half_hour'].initial = increment_half_hour
            self.fields['choices_session'].initial = session
            self.fields['choices_modality'].initial = modality
            self.fields['choices_payment'].initial = payment

        else:
            super(ProfileForm, self).__init__(*args, **kwargs)


class AddCourseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            user = kwargs.pop('user')
            super(AddCourseForm, self).__init__(*args, **kwargs)

            user_courses = TutorCourse.objects.filter(user_id=user.id).values('course_id')

            if user_courses is not None and user_courses.count() > 0:
                not_added_courses = Course.objects.exclude(id__in=user_courses)
                self.fields['choices'].queryset = not_added_courses
        else:
            super(AddCourseForm, self).__init__(*args, **kwargs)

    fields = ['course_name']

    choices = forms.ModelChoiceField(widget=forms.Select(
        attrs={'class': 'custom-select'}),
        queryset=Course.objects.all(),
        empty_label=None)

    choices.label = ''


class EditTutorshipInfo(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditTutorshipInfo, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Tutorship
        fields = ['name', 'description', 'url']
        labels = {
            'name': 'Nombre:',
            'description': 'Descripción:',
            'url': 'URL:'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '10'}),
            'url': forms.TextInput(attrs={'class': 'form-control'})
        }

class ProfitForm(forms.Form):
    date=forms.DateTimeField(
        input_formats=['%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    ) 

class TutorProfileForm(forms.ModelForm):
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