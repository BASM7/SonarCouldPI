from django.views import generic
from django.shortcuts import redirect, render
from django.core.cache import cache

from UserAuthentication.models import User
from Tutor.models import TutorAvailableSchedule

def get_context_view_calendar(tutor_email):
    try:

        tutor = User.objects.get(email=tutor_email)

        cache.set('tutor', tutor_email)
        events = TutorAvailableSchedule.objects.filter(
            user=tutor
        ).order_by('start_time')
        event_list = []
        for event in events:
            event_list.append(
                {
                    'message': event.start_time.strftime("%H:%M") + " - " + event.end_time.strftime("%H:%M"),
                    'start': event.start_time.strftime("%Y-%m-%d %H:%M"),
                    'end': event.end_time.strftime("%Y-%m-%d %H:%M"),
                    'id' : event.id,
                }
            )

        context = {
            'events': event_list,
            'calendar_title': tutor.name + " " + tutor.lastname,
            'tutor_email' : tutor_email,
            'title_page' : "Calendario"
        }

        return context
    except Exception as e:
        print(e)
        raise Exception("Error in get_context_view_calendar")

class DisplayTutorDetail(generic.View):
    def get(self, request, tutor):
        if request.user.is_authenticated:
            try:
                context = get_context_view_calendar(tutor)
            except:
                context = {'error' : 1}
            return render(request, "Student/tutorDetail.html", context)
        else:
            return redirect('index')