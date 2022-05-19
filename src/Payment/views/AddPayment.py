from django.shortcuts import render, redirect
from Payment import models
from Payment.forms import AddPaymentForm
from django.views import generic
from django.contrib import messages
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def create_context(form):
    return {'form': form, 'title_page' : "Retribuciones", 'select_navbar_payments' : 1}

class AddPayment(generic.View):
    """This is the view for the add payment admin page."""
    def get(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form = AddPaymentForm
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return redirect('index')

    def post(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form: AddPaymentForm = AddPaymentForm(request.POST or None)

            if form.is_valid():
                payment: models.Payment = models.Payment(
                    name=form.cleaned_data['name'],
                    description=form.cleaned_data['description'],
                )
                payment.save()
                messages.add_message(request, messages.SUCCESS, 'Tipo de pago agregado exitosamente')
            else:
                messages.add_message(request, messages.ERROR, 'Ocurrió un error, por favor, intente más tarde')
            
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return render(request, 'UserAuthentication/index.html')