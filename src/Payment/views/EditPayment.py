from django.shortcuts import render, redirect
from Payment.forms import AddPaymentForm
from django.views import generic
from Payment.models import Payment
from django.contrib import messages
# noinspection PyUnresolvedReferences


class EditPayment(generic.View):
    template_name = 'adminEditPayment.html'
    form_class: AddPaymentForm = AddPaymentForm

    def get(self, request, payment=None):

        form = self.form_class()
        selected_payment = None

        if request.GET.get('accion') == 'editar':
            payment_to_edit = Payment.objects.get(pk=payment)
            form = self.form_class(instance=payment_to_edit)
            selected_payment = payment_to_edit

        context = {
            'form': form,
            'payments': Payment.objects.all(),
            'selected_payment': selected_payment,
            'title_page' : "Retribuciones",
            'select_navbar_payments' : 1
        }
        return render(request, self.template_name, context)

    def post(self, request, payment=None):
        form = self.form_class(request.POST)
        if form.is_valid():
            if payment is not None:
                payment_to_edit = Payment.objects.get(pk=payment)
                payment_to_edit.name = form.cleaned_data['name']
                payment_to_edit.description = form.cleaned_data['description']
                payment_to_edit.save()
                messages.add_message(request, messages.SUCCESS, 'Cambios guardados exitosamente')
            else:
                form.save()
                messages.add_message(request, messages.ERROR, 'No se han realizado los cambios')
        return redirect('edit_payment') 