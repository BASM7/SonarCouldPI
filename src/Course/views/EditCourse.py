from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from Course import models
from Course.forms import AddCourseForm
from django.views import generic
from Course.models import Course
from django.contrib import messages
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


class EditCourse(generic.View):
    template_name = 'adminEditCourse.html'
    form_class: AddCourseForm = AddCourseForm

    def get(self, request, course=None):

        form = self.form_class()
        selected_course = None

        if request.GET.get('accion') == 'editar':
            course_to_edit = Course.objects.get(pk=course)
            form = self.form_class(instance=course_to_edit)
            selected_course = course_to_edit

        context = {
            'form': form,
            'courses': Course.objects.all(),
            'selected_course': selected_course,
            'title_page' : "Cursos", 
            'select_navbar_courses' : 1
        }
        return render(request, self.template_name, context)

    def post(self, request, course=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            if course is not None:
                course_to_edit = Course.objects.get(pk=course)
                course_to_edit.university = form.cleaned_data['university']
                course_to_edit.course_name = form.cleaned_data['course_name']
                course_to_edit.description = form.cleaned_data['description']
                course_to_edit.save()
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados exitosamente')
            else:
                form.save()
                messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')
        return redirect('edit_course')