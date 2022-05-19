from django.views.generic import TemplateView
from django import forms
from Tutor.forms import TutorScheduleForm
from Tutor import models
from UserAuthentication.models import User
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages


def create_context(user: User, form: TutorScheduleForm):
    events = models.TutorAvailableSchedule.objects.filter(
        user=user
    ).order_by('start_time')
    event_list = []
    for event in events:
        event_list.append(
            {
                'message': event.start_time.strftime("%H:%M") + " - " + event.end_time.strftime("%H:%M"),
                'start': event.start_time.strftime("%Y-%m-%d %H:%M"),
                'end': event.end_time.strftime("%Y-%m-%d %H:%M"),
            }
        )
    context = {
        'form': form,
        'events': event_list,
        'title_page': "Calendario",
        'select_navbar_calendar' : 1
    }
    return context


class CalendarView(TemplateView):
    template_name = 'Tutor/tutorCalendar.html'
    user: User = None
    form_class: TutorScheduleForm = TutorScheduleForm

    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        form = self.form_class()
        if user.is_tutor():
            return render(request, self.template_name, create_context(user, form))
        else:
            redirect('index')

    def post(self, request):
        form = self.form_class(request.POST)
        user: User = User.objects.get(pk=request.user.id)
        if form.is_valid():
            scheduled_block = models.TutorAvailableSchedule(
                user_id=user.id,
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
            )

            current_date = datetime.now()
            clean_current_date = current_date.strftime("%Y-%m-%d %H:%M")
            form_start_date = form.cleaned_data['start_time']
            clean_form_start_date = form_start_date.strftime("%Y-%m-%d %H:%M")
            form_end_date = form.cleaned_data['end_time']
            clean_form_end_date = form_end_date.strftime("%Y-%m-%d %H:%M")
            if clean_form_start_date == clean_form_end_date:
                messages.add_message(request, messages.WARNING, 'No se ha agendado su horario, por favor, elija una hora final diferente a la hora de inicio')
            elif clean_form_start_date >= clean_current_date:
                scheduled_block.save()
                messages.add_message(request, messages.SUCCESS, 'Horario agendado exitosamente')
            else:
                messages.add_message(request, messages.WARNING, 'No se ha agendado su horario, por favor, elija una hora mayor a la actual')
        return render(request, self.template_name, create_context(user, form))
