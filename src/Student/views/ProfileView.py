from django.views import generic
from django.views.generic.edit import CreateView
from django import forms
from django.contrib import messages

from Student.forms import ProfileForm
from UserAuthentication.models import User
from django.shortcuts import render, redirect


class ProfileView(generic.View):
    template_name = 'Student/studentProfile.html'
    form_class: ProfileForm = ProfileForm

    def get(self, request):

        form = self.form_class()

        user_to_edit = User.objects.get(id=request.user.id)
        form = self.form_class(instance=user_to_edit)
            

        context = {
            'form': form,
            'user_info': user_to_edit,
            'title_page' : "Perfil",
            'select_navbar_profile': 1
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_to_edit = User.objects.get(id=request.user.id)
            user_to_edit.name = form.cleaned_data['name']
            user_to_edit.lastname = form.cleaned_data['lastname']
            user_to_edit.save()
            messages.add_message(request, messages.SUCCESS, 'Perfil actualizado exitosamente')
        else:
            messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')
        return redirect('student_profile') 


