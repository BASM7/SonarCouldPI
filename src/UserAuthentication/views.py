from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from . import models
from . import forms
from .forms import NewAdminForm
from .models import User
from Tutor.models import Tutor
from django.contrib import messages


def index(request):
    list(messages.get_messages(request))

    context = {
            "title_page": "Inicio",
            'select_navbar_start': 1
    }

    if models.User.objects.filter(pk=request.user.id).exists():
        user: User = models.User.objects.get(pk=request.user.id)
        if user.is_tutor():
            return render(request, "UserAuthentication/tutorLogin.html", context)
        elif user.is_admin():
            return render(request, "UserAuthentication/adminLogin.html", context)
    return render(request, "Student/index.html", context)


def login(request):
    list(messages.get_messages(request))
    if models.User.objects.filter(pk=request.user.id).exists():
        return redirect('index')
    else:
        form = forms.UserForm(request.POST or None)
        if form.is_valid():
            user = models.User(id=request.user.id, email=request.user.email,
                               name=form.cleaned_data['name'], lastname=form.cleaned_data['lastname'],
                               type=form.cleaned_data['type'])
            user.save()
            if user.is_tutor():
                tutor = Tutor(user=user)
                tutor.save()
        context = {
            'form': form,
            'email': request.user.email
        }
        return render(request, "UserAuthentication/register.html", context)


def add_administrator(request):
    """This is the view for the admin manager."""
    user: User = models.User.objects.get(pk=request.user.id)
    if user.type == 3:
        form: NewAdminForm = forms.NewAdminForm(request.POST or None)
        if form.is_valid():
            try:
                user: User = models.User.objects.get(email=form.cleaned_data['email'])
                user.type = 3
                user.save()
                messages.add_message(request, messages.SUCCESS, 'El usuario ' + user.get_full_name + ' ahora es administrador')
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'El usuario no existe')
        context = {
            'form': form,
            'title_page': "Agregar administrador",
            'select_navbar_admin' : 1
        }
        return render(request, 'adminCrudForm.html', context)
    else:
        return render(request, 'UserAuthentication/index.html')
