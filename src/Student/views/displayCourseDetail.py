from django.views import generic
from django.core.cache import cache
from django.shortcuts import redirect, render

from UserAuthentication.models import User
from Tutor.models import TutorCourse, TutorAvailableSchedule
from Course.models import Course

def get_context_view_calendar(tutor: User, course_name: str):
    try:
        course = Course.objects.get(course_name=course_name)
        tutors = TutorCourse.objects.filter(course=course).values("user")
        tutors_display = User.objects.filter(id__in=tutors)

        if tutor is None:
            tutor = tutors_display.first()

        cache.set('tutor', tutor)
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
            'tutors': tutors_display,
            'events': event_list,
            'calendar_title': tutor.name + " " + tutor.lastname,
            'course': course_name,
            'title_page' : "Calendario"
        }

        return context
    except Exception as e:
        print(e)
        raise Exception("Error in get_context_view_calendar")

class displayCourseDetail(generic.View):

    def get(self, request, course_name):

        if request.user.is_authenticated:
            try:
                context = get_context_view_calendar(None, course_name)
            except:
                context = {'error' : 1}
            return render(request, "Student/courseDetail.html", context)
        else:
            return redirect('index')

    def post(self, request, course_name):
        if request.user.is_authenticated:
            requested_tutor = User.objects.get(email=request.POST.get('tutor'))
            context = get_context_view_calendar(requested_tutor, course_name)
            return render(request, "Student/courseDetail.html", context)
        else:
            return redirect('index')
