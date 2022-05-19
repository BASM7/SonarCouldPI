from django.views.generic import View
from django.shortcuts import render, redirect

from UserAuthentication.models import User
from Student.models import Request
from Student.models import Requesters
from Tutorship.models import Tutorship
from Resource.models import ResourceTutorship
from Resource.models import Resource
from django.db.models import Q


class StudentTutorshipView(View):
    template_name = 'Student/tutorshipView.html'
    user: User = None

    def get(self, request, request_pk=None):
        user = User.objects.get(pk=request.user.id)
        if user.is_student():
            tutorship_request = Request.objects.get(pk=request_pk)
            tutorship = Tutorship.objects.get(request=tutorship_request)
            tutorship_resources = list(ResourceTutorship.objects.filter(tutorship=tutorship))
            requesters = list(Requesters.objects.filter(request=tutorship_request))
            context = {
                'request_info': tutorship_request,
                'tutorship_request': tutorship_request,
                'tutorship': tutorship,
                'resources': tutorship_resources,
                'requesters': requesters,
                'select_navbar_tutorships' : 1,
                'title_page': 'Información de Tutoría'
            }
            return render(request, self.template_name, context)
        else:
            return redirect('index')
