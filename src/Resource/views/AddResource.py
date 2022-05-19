from django.shortcuts import render, redirect
from django.contrib import messages

from Resource import models
from Resource.forms import ResourceForm
from django.views import generic

# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def create_context(form):
    return {'form': form, 'title_page' : "Recursos", 'select_navbar_resources' : 1}


class AddResource(generic.View):
    """This is the view for the add resource admin page."""
    def get(self, request):

        user: User = User.objects.get(pk=request.user.id)
        
        if user.type == 3:
            form = ResourceForm()
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return redirect('index')

    def post(self, request):
        user: User = User.objects.get(pk=request.user.id)

        if user.type == 3:
            form: ResourceForm = ResourceForm(request.POST or None)

            if form.is_valid():
                resource: models.Resource = models.Resource(
                    name=form.cleaned_data['name'],
                    is_public=form.cleaned_data['is_public'],
                    description=form.cleaned_data['description'],
                    url=form.cleaned_data['url'],
                    author=form.cleaned_data['author']
                )
                resource.save()
                messages.add_message(request, messages.SUCCESS, 'Recurso agregado exitosamente')
            else:
                messages.add_message(request, messages.ERROR, 'Ocurrió un error, por favor, intente más tarde')

            context = create_context(form)
            
            return render(request, 'adminCrudForm.html', context)

        else:
            return render(request, 'UserAuthentication/index.html')