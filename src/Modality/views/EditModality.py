from django.shortcuts import render, redirect
from Modality.forms import AddModalityForm
from django.views import generic
from Modality.models import Modality
from django.contrib import messages
# noinspection PyUnresolvedReferences


class EditModality(generic.View):
    template_name = 'adminEditModality.html'
    form_class: AddModalityForm = AddModalityForm

    def get(self, request, modality=None):

        form = self.form_class()
        selected_modality = None

        if request.GET.get('accion') == 'editar':
            modality_to_edit = Modality.objects.get(pk=modality)
            form = self.form_class(instance=modality_to_edit)
            selected_modality = modality_to_edit

        context = {
            'form': form,
            'modalities': Modality.objects.all(),
            'selected_modality': selected_modality,
            'title_page' : "Modalidades",
            'select_navbar_modalities' : 1
        }
        return render(request, self.template_name, context)

    def post(self, request, modality=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            if modality is not None:
                modality_to_edit = Modality.objects.get(pk=modality)
                modality_to_edit.name = form.cleaned_data['name']
                modality_to_edit.description = form.cleaned_data['description']
                modality_to_edit.save()
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados exitosamente')
            else:
                form.save()
                messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')
        return redirect('edit_modality') 