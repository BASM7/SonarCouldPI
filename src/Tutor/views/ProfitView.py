from django.views import generic
from django.shortcuts import render, redirect
from django import forms
from datetime import timedelta, datetime

from UserAuthentication.models import User
from Tutor.models import Tutor
from Student.models import Request
from Tutor.forms import ProfitForm


class ProfitView(generic.View):
    template_name = 'Tutor/tutorProfit.html'
    user: User = None

    def get(self, request):
        user: User = User.objects.get(pk=request.user.id)
        profit_form = ProfitForm(request.GET or None)
        
        if user.is_tutor():
            return render(request, self.template_name, {'form': profit_form, "title_page" : "Ganancias", 'select_navbar_profit' : 1})
        else:
            return redirect('index')

    def post(self, request):
        user: User = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            profit_form = ProfitForm(request.POST or None)
            if profit_form.is_valid():
                tutor = Tutor.objects.get(user_id=request.user.id) 
                date = profit_form.cleaned_data['date']
                clean_date = date.strftime("%Y-%m-%d %H:%M")
                next_month = datetime(date.year + int(date.month / 12), ((date.month % 12) + 1), 1)
                clean_next_month = next_month.strftime("%Y-%m-%d %H:%M")

                half_hour_increment = timedelta(hours=1, minutes=30)
                hour_increment = timedelta(hours=2)
                without_increment = timedelta(hours=1)

                profit = 0
                time = timedelta(hours=0)
 
                requests = list(Request.objects.filter(tutor_requested_id = user, state = 'DN', date_start__gte = clean_date, date_start__lte = clean_next_month))
                for tutorship in requests:
                    if tutorship.date_end - half_hour_increment == tutorship.date_start:
                        profit += tutorship.num_requesters * tutor.amount_per_person + tutor.increment_per_half_hour
                        time += half_hour_increment
                    elif tutorship.date_end - hour_increment == tutorship.date_start:
                        profit += (tutorship.num_requesters * tutor.amount_per_person) + (tutor.increment_per_half_hour * 2)
                        time += hour_increment
                    else:
                        profit += tutorship.num_requesters * tutor.amount_per_person
                        time += without_increment


                context = {
                    'form': profit_form,
                    'profit': profit,
                    'time': new_time,
                    'title_page': "Ganancias",
                    'select_navbar_profit': 1
                }

            return render(request, self.template_name, context)

        return render(request, self.template_name)