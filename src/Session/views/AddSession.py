from django.shortcuts import render, redirect
from Session import models
from Session.forms import AddSessionForm
from django.views import generic
from django.contrib import messages
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def create_context(form):
    return {'form': form, 'title_page' : "Sesiones", 'select_navbar_sessions' : 1}

class AddSession(generic.View):
    """This is the view for the add session admin page."""
    def get(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form = AddSessionForm
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return redirect('index')

    def post(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form: AddSessionForm = AddSessionForm(request.POST or None)

            if form.is_valid():
                session: models.Session = models.Session(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                )
                session.save()
                messages.add_message(request, messages.SUCCESS, 'Tipo de sesión agregada exitosamente')
            else:
                messages.add_message(request, messages.ERROR, 'Ocurrió un error, por favor, intente más tarde')
            
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return render(request, 'UserAuthentication/index.html')