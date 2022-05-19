from django.shortcuts import render, redirect
from Region import models
from Region.forms import AddRegionForm
from django.views import generic
from django.contrib import messages
# noinspection PyUnresolvedReferences
from UserAuthentication.models import User


def create_context(form):
    return {'form': form, 'title_page' : "Regiones", 'select_navbar_regions' : 1}

class AddRegion(generic.View):
    """This is the view for the admin manager."""
    def get(self, request):
        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form = AddRegionForm
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return redirect('index')

    def post(self, request):

        user: User = User.objects.get(pk=request.user.id)

        if user.is_admin():
            form: AddRegionForm = AddRegionForm(request.POST or None)

            if form.is_valid():
                region: models.Regions = models.Regions(
                    region_name=form.cleaned_data['region_name'],
                    country=form.cleaned_data['country']
                )
                region.save()
                messages.add_message(request, messages.SUCCESS, 'Región agregada exitosamente')
            else:
                messages.add_message(request, messages.ERROR, 'Ocurrió un error, por favor, intente más tarde')
            
            context = create_context(form)

            return render(request, 'adminCrudForm.html', context)

        else:
            return render(request, 'UserAuthentication/index.html')