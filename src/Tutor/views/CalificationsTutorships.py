from django.views import generic
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.conf import settings

from UserAuthentication.models import User
from Tutorship.models import TutorshipScore


def get_paginator_results(results, page_number):
    if results is not None:

        if page_number is None:
            page_number = 1

        paginator = Paginator(results, settings.PAGE_SIZE)
        page_display = paginator.get_page(page_number)
        return page_display
    return results


def create_context(query_set, average, quantity):
    return {'results': query_set, 'average': average, 'quantity': quantity, 'title_page' : "Calificaciones"}


class CalificationsTutorships(generic.View):

    def get(self, request, request_pk):
        user = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            query_set = list(TutorshipScore.objects.filter(tutorship_id=request_pk).order_by('id'))
            
            page_number = request.GET.get("pagina")
            page_display = get_paginator_results(query_set, page_number)

            total_calification = 0

            for item in query_set:
                total_calification += item.score

            average_calification = total_calification / len(query_set)

            context = create_context(query_set, average_calification, len(query_set))

            return render(request, "Tutor/tutorCalifications.html", context)
        else:
            return redirect('index')