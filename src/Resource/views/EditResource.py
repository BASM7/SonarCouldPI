from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from Resource import models
from Resource.forms import ResourceForm
from django.views import generic
from Resource.models import Resource
from django.contrib import messages
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


class EditResource(generic.View):
    template_name = 'adminEditResource.html'
    form_class: ResourceForm = ResourceForm

    def get(self, request, resource=None):

        form = self.form_class()
        selected_resource = None

        if request.GET.get('accion') == 'editar':
            resource_to_edit = Resource.objects.get(pk=resource)
            form = self.form_class(instance=resource_to_edit)
            selected_resource = resource_to_edit
        elif request.GET.get('accion') == 'eliminar':
            try:
                resource_to_edit = Resource.objects.get(pk=resource)
                resource_to_edit.delete()
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados exitosamente')
            except:
                messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')

        context = {
            'form': form,
            'resources': Resource.objects.all(),
            'selected_resource': selected_resource,
            'title_page' : "Recursos",
            'select_navbar_resources' : 1
        }
        return render(request, self.template_name, context)

    def post(self, request, resource=None):
        form = self.form_class(request.POST)
        user = User.objects.get(pk=request.user.id)
        if form.is_valid():
            if resource is not None:
                resource_to_edit = Resource.objects.get(pk=resource)
                resource_to_edit.name = form.cleaned_data['name']
                resource_to_edit.is_public = form.cleaned_data['is_public']
                resource_to_edit.description = form.cleaned_data['description']
                resource_to_edit.url = form.cleaned_data['url']
                resource_to_edit.author = form.cleaned_data['author']
                resource_to_edit.save()
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados exitosamente')
            else:
                resource = Resource(
                    name=form_resource.cleaned_data['name'],
                    is_public=form_resource.cleaned_data['is_public'],
                    description=form_resource.cleaned_data['description'],
                    url=form_resource.cleaned_data['url'],
                    author=form_resource.cleaned_data['author'],
                    uploader=user
                )
                resource.save()
                messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')
        return redirect('edit_resource')
