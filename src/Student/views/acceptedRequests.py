from django.views import generic
from django.shortcuts import redirect, render

from UserAuthentication.models import User
from Student.models import Request, Requesters

def create_context(query_set):
    return {'requests': query_set, 'title_page' : "Aceptadas", 'select_navbar_tutorships' : 1}


class acceptedRequests(generic.View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        if user.is_student():
            join_request  = Requesters.objects.filter(user_requester=user).values_list('request', flat=True)
            query_set = list((Request.objects.filter(user_requester=user, state='AP') | Request.objects.filter(id__in=join_request, state='AP')).order_by('date_start'))
            context = create_context(query_set)
            return render(request, "Student/studentRequest.html", context)
        else:
            return redirect('index')