from django.shortcuts import render, redirect
from Session.forms import AddSessionForm
from django.views import generic
from Session.models import Session
from django.contrib import messages
# noinspection PyUnresolvedReferences


class EditSession(generic.View):
    template_name = 'adminEditSession.html'
    form_class: AddSessionForm = AddSessionForm

    def get(self, request, session=None):

        form = self.form_class()
        selected_session = None

        if request.GET.get('accion') == 'editar':
            session_to_edit = Session.objects.get(pk=session)
            form = self.form_class(instance=session_to_edit)
            selected_session = session_to_edit

        context = {
            'form': form,
            'sessions': Session.objects.all(),
            'selected_session': selected_session,
            'title_page' : "Sesiones",
            'select_navbar_sessions' : 1
        }
        return render(request, self.template_name, context)

    def post(self, request, session=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            if session is not None:
                session_to_edit = Session.objects.get(pk=session)
                session_to_edit.name = form.cleaned_data['name']
                session_to_edit.description = form.cleaned_data['description']
                session_to_edit.save()
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados exitosamente')
            else:
                messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')
        return redirect('edit_session') 