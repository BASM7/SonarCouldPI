from django.views import generic
from django.views.generic.edit import CreateView
from django import forms
from django.contrib import messages

from Tutor.forms import ProfileForm, TutorProfileForm
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from Tutor.models import Tutor
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment
from Region.models import Regions


def create_context(modality_form):
    context = {
        'modality_form': modality_form
    }
    return context


class ProfileView(generic.View):
    template_name = 'Tutor/tutorProfile.html'
    user: User = None
    form_class: TutorProfileForm = TutorProfileForm

    def get(self, request):
        user: User = User.objects.get(pk=request.user.id)
        profile_form = ProfileForm(request.GET or None, **{'user': user})

        user_to_edit = User.objects.get(id=request.user.id)
        form = self.form_class(instance=user_to_edit)
        selected_user = user_to_edit

        region = Tutor.objects.get(user_id=user.id).region
        tutorship_price = Tutor.objects.get(user_id=user.id).amount_per_person
        increment_half_hour = Tutor.objects.get(user_id=user.id).increment_per_half_hour
        session = Tutor.objects.get(user_id=user.id).session_type.all()
        modality = Tutor.objects.get(user_id=user.id).modality_type.all()
        payment = Tutor.objects.get(user_id=user.id).payment_type.all()

        context = {
            'form': profile_form,
            'tutor_form': form,
            'selected_user': selected_user,
            'region': region,
            'tutorship_price': tutorship_price,
            'increment_half_hour': increment_half_hour,
            'session': session,
            'modality': modality,
            'payment': payment,
            'user': user,
            'title_page': "Perfil",
            'select_navbar_profile': 1
        }

        if user.is_tutor():
            return render(request, self.template_name, context)
        else:
            return redirect('index')

    def post(self, request):
        profile_form = ProfileForm(request.POST or None)
        form = self.form_class(request.POST)
        
        if form.is_valid():
            user_to_edit = User.objects.get(id=request.user.id)
            user_to_edit.name = form.cleaned_data['name']
            user_to_edit.lastname = form.cleaned_data['lastname']
            user_to_edit.save()
            messages.add_message(request, messages.SUCCESS, 'Perfil actualizado exitosamente')        
        elif profile_form.is_valid():
            tutor = Tutor.objects.get(user_id=request.user.id)
            tutor.region = Regions.objects.get(
                region_name=profile_form.cleaned_data['choices_region'])
            tutor.amount_per_person = profile_form.cleaned_data['tutorship_price']
            tutor.increment_per_half_hour = profile_form.cleaned_data['increment_half_hour']

            tutor.payment_type.add(*profile_form.cleaned_data['choices_payment'])
            tutor.session_type.add(*profile_form.cleaned_data['choices_session'])
            tutor.modality_type.add(*profile_form.cleaned_data['choices_modality'])
            tutor.save()
            messages.add_message(request, messages.SUCCESS, 'Perfil actualizado exitosamente')
        else:
            messages.add_message(request, messages.ERROR, 'El perfil no ha sido actualizado')

        return redirect('tutor_profile')
