from datetime import datetime, timedelta
from django.views import generic
from django.shortcuts import redirect, render
from django.core.cache import cache

from Student.models import Request, Requesters
from UserAuthentication.models import User
from Session.models import Session
from Modality.models import Modality
from Course.models import Course
from Tutor.models import TutorAvailableSchedule, Tutor, TutorCourse
from Payment.models import Payment
from Tutorship.models import RequestNotification


def save_values_post(request):
    dict_values = {}

    dict_values['user_requester'] = request.user

    if request.POST.get('fecha'):
        dict_values['fecha'] = request.POST.get('fecha')

    if request.POST.get('tutor'):
        dict_values['tutor'] = request.POST.get('tutor')

    if request.POST.get('sesion'):
        dict_values['sesion'] = request.POST.get('sesion')

    if request.POST.get('modalidad'):
        dict_values['modalidad'] = request.POST.get('modalidad')

    if request.POST.get('inicial'):
        dict_values['inicial'] = request.POST.get('inicial')

    if request.POST.get('final'):
        dict_values['final'] = get_added_hours(request.POST.get('final'))

    if request.POST.getlist('invitados'):
        dict_values['invitados'] = request.POST.getlist('invitados')

    if request.POST.get('curso'):
        dict_values['curso'] = request.POST.get('curso')

    if valid_comment(request.POST.get('comentario')):
        dict_values['comentario'] = request.POST.get('comentario')


    return dict_values


def check_dict_value(dict_values):
    valid_keys = ('tutor', 'sesion', 'modalidad', 'inicial', 'final', 'fecha')
    return all(key in dict_values for key in valid_keys)


def valid_comment(comment: str):
    if comment is not None and comment.replace(" ", "") != "":
        return True
    return False


def get_added_hours(added_hours):
    if added_hours == "1":
        return 1, 30
    elif added_hours == "2":
        return 2, 0
    return 1, 0


def set_all_guests_request(dict_values, tutor, request_tutorship):
    new_num_requesters = 1
    if check_guests(dict_values, tutor):
        for guest in dict_values['invitados']:
            resquester = Requesters()
            resquester.request = request_tutorship
            resquester.user_requester = User.objects.get(id=guest)
            resquester.save()
            new_num_requesters += 1
    return new_num_requesters

# Cambiar 50
def check_guests(dict_values, tutor):
    if dict_values['sesion'] == "Grupal - Privada" or dict_values['sesion'] == "Grupal - Pública":
        if 'invitados' in dict_values:
            if 50 >= len(dict_values['invitados']):
                return True
    return False


def request_maker(dict_values, course_name=None):
    try:
        schedule_selected = cache.get('schedule_selected')

        user_requester = User.objects.get(id=dict_values['user_requester'].id)
        tutor_requested = User.objects.get(id=dict_values['tutor'])

        session_requested = Session.objects.get(name=dict_values['sesion'])
        modality_requested = Modality.objects.get(name=dict_values['modalidad'])
        if course_name is not None:
            course_requested = Course.objects.get(course_name=course_name)
        else:
            course_requested = Course.objects.get(course_name=dict_values['curso'])

        start_date = datetime.strptime(dict_values['fecha'], "%Y-%m-%d")
        initial_hour, initial_minutes = dict_values['inicial'].split(":")

        start_date = start_date.replace(hour=int(initial_hour), minute=int(initial_minutes))

        final_hour, final_minutes = dict_values['final']
        time_added = timedelta(hours=final_hour, minutes=final_minutes)

        end_date = start_date + time_added

        do_requesters = check_guests(dict_values, tutor_requested)

        request_builder = Request.objects.create(user_requester=user_requester,
                                                 tutor_requested=tutor_requested,
                                                 session_requested=session_requested,
                                                 modality_requested=modality_requested,
                                                 course_requested=course_requested,
                                                 date_start=start_date,
                                                 date_end=end_date,
                                                 date_request=start_date)

        if 'comentario' in dict_values:
            request_builder.student_comment = dict_values['comentario']

        num_requesters = set_all_guests_request(dict_values, tutor_requested, request_builder)
        request_builder.num_requesters = num_requesters

        request_builder.save()

        # add the notification here.
        notification = RequestNotification(
            notification_type='RE',
            to_user=request_builder.tutor_requested,
            from_user=request_builder.user_requester,
            request=request_builder
        )
        notification.save()

    except Exception as e:
        print(e)
        raise Exception("Unknown exception")

# Cambiar 50
def create_context(schedule_id, user, tutor=None, get_courses=False, last_page = None):
    try:
        context = {}
        schedule_selected = TutorAvailableSchedule.objects.get(id=schedule_id)

        cache.set('schedule_selected', schedule_selected)

        tutor = Tutor.objects.get(user=schedule_selected.user)
        all_students = User.objects.filter(type=1).exclude(id=user.id).order_by('name')

        courses = None
        if get_courses:
            courses = TutorCourse.objects.filter(user=tutor.user).values("course")
            courses = Course.objects.filter(id__in=courses)

        # Para la integración de varias sesiones se debe tener una lista de sesiones id y hacer id__in
        sessions = tutor.session_type.all()
        modals = tutor.modality_type.all()
        payments = tutor.payment_type.all()

        min_time = schedule_selected.start_time.strftime('%H:%M')
        max_time = schedule_selected.end_time - timedelta(hours=1, minutes=0)
        max_time = max_time.strftime('%H:%M')

        

        if last_page is None:
            last_page = 'http://127.0.0.1:8000/'

        context.update({
            'tutor': tutor,
            'students': all_students,
            'sessions': sessions,
            'modals': modals,
            'payments': payments,
            'min_time': min_time,
            'max_time': max_time,
            'value_tutorship_person': tutor.amount_per_person,
            'increment': tutor.increment_per_half_hour,
            'date': str(schedule_selected.start_time.date()),
            'students': all_students,
            'max_people': 50,
            'courses': courses,
            'title_page' : "Agendar",
            'last_page': last_page
        })

        return context
    except schedule_selected.DoesNotExist:
        raise Exception("Schedule selected id is not in the database")
    except Exception as e:
        print(e)
        raise Exception("Unknown exception")


class RequestTutorship(generic.View):

    def get(self, request, course_name):
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:
                schedule_id = request.GET.get('schedule_number')
                context = create_context(schedule_id, user, last_page=request.META.get('HTTP_REFERER'))
                print()
                return render(request, "Student/formRequestTutorship.html", context)
            except Exception as e:
                print(e)
        return redirect('index')

    def post(self, request, course_name):
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:
                dict_values = save_values_post(request)

                if check_dict_value(dict_values):
                    request_maker(dict_values, course_name)
                    return render(request, "Student/reportRequest.html", {'success': True, 'title_page' : "Solicitud"})
                return render(request, "Student/reportRequest.html", {'success': False, 'title_page' : "Solicitud"})
            except:
                return render(request, "Student/reportRequest.html", {'success': False, 'title_page' : "Solicitud"})
        return redirect('index')


class RequestTutorshipTutor(generic.View):
    
    def get(self, request, tutor):
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:
                schedule_id = request.GET.get('schedule_number')
                context = create_context(schedule_id, user, tutor, True, request.META.get('HTTP_REFERER'))
                return render(request, "Student/formRequestTutor.html", context)
            except Exception as e:
                print(e)
        return redirect('index')
    
    def post(self, request, tutor):
        user = User.objects.get(id=request.user.id)
        if request.user.is_authenticated and user.is_student():
            try:
                dict_values = save_values_post(request)

                if check_dict_value(dict_values):
                    request_maker(dict_values)
                    return render(request, "Student/reportRequest.html", {'success': True, 'title_page' : "Solicitud"})
                return render(request, "Student/reportRequest.html", {'success': False, 'title_page' : "Solicitud"})
            except:
                return render(request, "Student/reportRequest.html", {'success': False, 'title_page' : "Solicitud"})
        return redirect('index')
