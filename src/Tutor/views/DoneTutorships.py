from django.views import generic
from django.shortcuts import redirect, render

from UserAuthentication.models import User
from Tutorship.models import Tutorship, TutorshipScore
from Student.models import Request

from Tutor.tutorshipHistoryModels import ListTutorshipHistory


def create_context(query_set):
    return {'results': query_set.list, "title_page" : "Historial", 'select_navbar_tutorships' : 1}


class DoneTutorships(generic.View):

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            query_set = list(Request.objects.filter(tutor_requested=user, state='DN').order_by('date_start'))
            list_tutorship_history = ListTutorshipHistory(query_set)
            context = create_context(list_tutorship_history)
            return render(request, "Tutor/tutorHistory.html", context)
        else:
            return redirect('index')