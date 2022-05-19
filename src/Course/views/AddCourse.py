from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages

from Course import models
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User

from Course.forms import AddCourseForm
from django.views import generic


def create_context(form):
    return {'form': form, 'title_page': "Cursos", 'select_navbar_courses' : 1}


class AddCourse(generic.View):

    def get(self, request):
        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():

            form = AddCourseForm()
            context = create_context(form)

            return render(request, "adminCrudForm.html", context)
        else:
            return redirect('index')

    def post(self, request):
        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form = AddCourseForm(request.POST or None)

            if form.is_valid():
                course = models.Course(university=form.cleaned_data['university'],
                                    course_name=form.cleaned_data['course_name'],
                                    description=form.cleaned_data['description'])
                if models.Course.objects.filter(university=course.university).exists() and models.Course.objects.filter(
                        course_name=course.course_name).exists():
                    return HttpResponse("El curso \"" + course.course_name + "\" ya estaba registrado")
                course.save()
                messages.add_message(request, messages.SUCCESS, 'Curso agregado exitosamente')
            else:
                messages.add_message(request, messages.ERROR, 'Ocurrió un error, por favor, intente más tarde')
            context = create_context(form)
            return render(request, "adminCrudForm.html", context)

        else:
            return render(request, 'UserAuthentication/index.html')

