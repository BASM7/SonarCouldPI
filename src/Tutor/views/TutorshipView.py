from django.views.generic import View
from django.shortcuts import render, redirect

from UserAuthentication.models import User
from Student.models import Request
from Student.models import Requesters
from Tutorship.models import Tutorship
from Resource.models import ResourceTutorship
from Resource.models import Resource
from Tutor.forms import EditTutorshipInfo, TutorResourceForm
from Resource.forms import ResourceForm
from django.db.models import Q
from django.contrib import messages


class TutorshipView(View):
    template_name = 'Tutor/tutorshipView.html'
    user: User = None
    form_info_class = EditTutorshipInfo
    form_resource_class = TutorResourceForm

    def get(self, request, request_pk=None, resource_pk=None):
        user = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            if request.GET.get('accion') == 'eliminar':
                resource = Resource.objects.get(pk=resource_pk)
                tutorship_resource = ResourceTutorship.objects.get(resource=resource)
                tutorship_resource.delete()
                if resource.uploader_id == user.id:
                    resource.delete()

                messages.add_message(request, messages.SUCCESS, 'Recurso eliminado exitosamente')
                return redirect('tutor_tutorship_view', request_pk=request_pk)

            tutorship_request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
            tutorship = Tutorship.objects.get(request=tutorship_request)
            tutorship_resources = list(ResourceTutorship.objects.filter(tutorship=tutorship))
            requesters = list(Requesters.objects.filter(request=tutorship_request))

            public_resources = list(
                (Resource.objects.filter(is_public=True) | Resource.objects.filter(uploader=user))
                .filter(~Q(id__in=[resource.resource_id for resource in tutorship_resources]))
            )

            form_info = EditTutorshipInfo(instance=tutorship)
            form_resource = self.form_resource_class()
            context = {
                'request_info': tutorship_request,
                'form_info': form_info,
                'form_resource': form_resource,
                'tutorship_request': tutorship_request,
                'tutorship': tutorship,
                'resources': tutorship_resources,
                'requesters': requesters,
                'public_resources': public_resources,
                'title_page' : "Tutoría"
            }
            return render(request, self.template_name, context)
        else:
            return redirect('index')
        return redirect('index')

    def post(self, request, request_pk=None):
        form_info = self.form_info_class(request.POST)
        form_resource = self.form_resource_class(request.POST)
        user = User.objects.get(pk=request.user.id)

        list(messages.get_messages(request))

        selected_resources = request.POST.getlist('select_resource')
        if selected_resources:
            tutorship_request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
            tutorship = Tutorship.objects.get(request=tutorship_request)
            for resource_id in selected_resources:
                resource = Resource.objects.get(pk=resource_id)
                ResourceTutorship.objects.create(resource=resource, tutorship=tutorship)
            messages.add_message(request, messages.SUCCESS, 'Recursos guardados exitosamente')

        elif form_resource.is_valid():
            tutorship_request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
            tutorship = Tutorship.objects.get(request=tutorship_request)

            # Check if it is a new resource.
            if request.POST.get('resource') == '':
                # Create the resource.
                resource = Resource(
                    name=form_resource.cleaned_data['resource_name'],
                    is_public=form_resource.cleaned_data['is_public'],
                    description=form_resource.cleaned_data['resource_description'],
                    url=form_resource.cleaned_data['resource_url'],
                    author=form_resource.cleaned_data['author'],
                    uploader=user
                )
                resource.save()

                # Link the resource to the tutorship.
                resource_tutorship = ResourceTutorship(
                    tutorship=tutorship,
                    resource=resource
                )
                resource_tutorship.save()
                messages.add_message(request, messages.SUCCESS, 'Recurso guardado exitosamente')

            else:
                resource = Resource.objects.get(pk=request.POST.get('resource'))
                resource.name = form_resource.cleaned_data['resource_name']
                resource.is_public = form_resource.cleaned_data['is_public']
                resource.description = form_resource.cleaned_data['resource_description']
                resource.url = form_resource.cleaned_data['resource_url']
                resource.author = form_resource.cleaned_data['author']
                resource.save()
                messages.add_message(request, messages.SUCCESS, 'Recurso editado exitosamente')

        elif form_info.is_valid():
            tutorship_request = Request.objects.get(pk=request_pk, tutor_requested_id=user)
            tutorship = Tutorship.objects.get(request=tutorship_request)
            tutorship.name = form_info.cleaned_data['name']
            tutorship.description = form_info.cleaned_data['description']
            tutorship.url = form_info.cleaned_data['url']
            tutorship.save()
            messages.add_message(request, messages.SUCCESS, 'Información editada exitosamente')

        return redirect('tutor_tutorship_view', request_pk=request_pk)

