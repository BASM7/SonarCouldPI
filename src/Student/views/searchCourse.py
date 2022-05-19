from django.db.models.query_utils import PathInfo
from django.views import generic
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q

from Course.models import Course
from Session.models import Session
from Modality.models import Modality
from Payment.models import Payment
from Student.models import Request, Requesters
from UserAuthentication.models import User
from Tutor.models import Tutor
from Resource.models import Resource
from Region.models import Regions
from Student.filtersModels import ListTypeSearch, ListFilter, ListScore


def create_context(search_query, page_number, type_search, filters, user):
    try:

        results, list_search = handlers_results(search_query, type_search, filters, user)
        page_display = get_paginator_results(results, page_number)

        list_filter = get_list_filters(filters)

        regions = Regions.objects.all()

        if type_search == None:
            type_search = "cursos"

        diplay_sessions_link = 0
        if type_search == "tutor":
            diplay_sessions_link = 1

        context = {
                'latest_search': search_query,
                'results': page_display,
                'types_searches': list_search,
                'sessions': list_filter[0].list,   
                'modals': list_filter[1].list,
                'retributions' : list_filter[2].list, 
                'scores' : list_filter[3].list,
                'regions' : list_filter[4].list,
                'last_type': type_search, 
                'diplay_sessions_link': diplay_sessions_link,
                'title_page' : "Búsqueda"
            }
    except Exception as e:
        print(e)
        raise Exception ("Error en la busqueda")

    return context


def get_paginator_results(results, page_number):
    if results is not None:

        if page_number is None:
            page_number = 1

        paginator = Paginator(results, settings.PAGE_SIZE)
        page_display = paginator.get_page(page_number)
        return page_display
    return results


def get_results_course(search_query):
    if search_query == "all" or search_query == "":
        results = Course.objects.all().order_by('course_name')
    else:
        results = Course.objects.filter(course_name__icontains=search_query).order_by('course_name')

    return results


def get_results_university(search_query):
    if search_query == "all" or search_query == "":
        results = Course.objects.all().order_by('course_name')
    else:
        results = Course.objects.filter(university=search_query).order_by('course_name')

    return results


def get_results_tutor(search_query, filters):
    try:
        if search_query == "all" or search_query == "":
            results = User.objects.filter(type=2).order_by('name', 'lastname')
        else:
            fullname = search_query.split(' ')
            if len(fullname) == 2:
                results = User.objects.filter(name__icontains=fullname[0], lastname__icontains=fullname[1], type=2).order_by('name', 'lastname')
            else:
                results = User.objects.filter(name__icontains=fullname[0], type=2).order_by('name', 'lastname')

        results = do_filters(results, filters)
        return results
    except:
        raise ValueError("Error in getting the results")
    

def get_results_resources(search_query):
    if search_query == "all" or search_query == "":
        results = Resource.objects.filter(is_public=1).order_by('name')
    else:
        results = Resource.objects.filter(is_public=1, name=search_query).order_by('name')

    return results


def get_results_open_groups(search_query, user):
    my_requests = Requesters.objects.filter(user_requester=user).values_list('request', flat=True)
    if search_query == "all" or search_query == "":
        results = Request.objects.filter(session_requested__name="Grupal - Pública", state="AP").filter(~Q(id__in=my_requests)).filter(~Q(user_requester=user)).order_by('course_requested__course_name')
    else:
        results = Request.objects.filter(session_requested__name="Grupal - Pública", state="AP", course_requested__course_name__icontains=search_query).filter(~Q(id__in=my_requests)).filter(~Q(user_requester=user)).order_by('course_requested__course_name')
    
    return results


def handlers_results(search_query, type_search, filters, user):
    try:
        if type_search == "universidad":
            type_list = get_list_type_search(1)
            results = get_results_university(search_query)
        elif type_search == "tutor":
            type_list = get_list_type_search(2)
            results = get_results_tutor(search_query, filters)
        elif type_search == "recursos-publicos":
            type_list = get_list_type_search(3)
            results = get_results_resources(search_query)
        elif type_search == "sesiones-publicas":
            type_list = get_list_type_search(4)
            results = get_results_open_groups(search_query, user)
        else:
            type_list = get_list_type_search(0)
            results = get_results_course(search_query)
            
        return results, type_list
    except:
        raise ValueError("Error in getting the results")


def get_list_type_search(selected_type_search):
    list_type_search = ListTypeSearch([0,0,0,0,0], ['cursos', 'universidad', 'tutor', 'recursos-publicos', 'sesiones-publicas'])
    list_type_search.list[selected_type_search].selected = 1
    return list_type_search.list


def get_list_filters(filters):
    
    try:
        list_filters = []

        if 'sessions' in filters:     
            list_filters.append(ListFilter(Session.objects.all(), filters['sessions']))
        else:
            list_filters.append(ListFilter(Session.objects.all()))
        
        if 'modals' in filters:   
            list_filters.append(ListFilter(Modality.objects.all(), filters['modals']))
        else:
            list_filters.append(ListFilter(Modality.objects.all()))

        if 'payments' in filters:  
            list_filters.append(ListFilter(Payment.objects.all(), filters['payments']))
        else:
            list_filters.append(ListFilter(Payment.objects.all()))

        if 'score' in filters:
            list_filters.append(ListScore(filters['score']))
        else:
            list_filters.append(ListScore())

        if 'region' in filters:
            list_filters.append(ListFilter(Regions.objects.all(), filters['region']))
        else:
            list_filters.append(ListFilter(Regions.objects.all()))
        
        return list_filters

    except Exception as e:
        print(e)
        raise ValueError("Error in list filters")

    


def do_filters(results, filters):
    try:
        filtered_results = results

        if 'sessions' in filters:        
            filtered_results = filter_session(filtered_results, filters['sessions'])

        if 'modals' in filters:
            filtered_results = filter_modality(filtered_results, filters['modals'])

        if 'payments' in filters:
            filtered_results = filter_payment(filtered_results, filters['payments'])

        if 'score' in filters:
            filtered_results = filter_score(filtered_results, filters['score'])

        if 'region' in filters:
            filtered_results = filter_region(filtered_results, filters['region'])
        
        return filtered_results

    except:
        raise ValueError("Error in filtering the results")


def filter_session(last_query, session_names):
    try:
        sessions = Session.objects.filter(name__in=session_names).values_list('id', flat=True)
        all_tutors = Tutor.objects.filter(session_type__in=sessions).values_list('user', flat=True)
        filtered_results = last_query.filter(id__in=all_tutors)
        
        return filtered_results
    except:
        raise ValueError("Error in filtering the sesssion")


def filter_modality(last_query, modality_names):
    try:
        modalities = Modality.objects.filter(name__in=modality_names).values_list('id', flat=True)
        all_tutors = Tutor.objects.filter(modality_type__in=modalities).values_list('user', flat=True)
        filtered_results = last_query.filter(id__in=all_tutors)

        return filtered_results
    except:
        raise ValueError("Error in filtering the modality")


def filter_payment(last_query, payment_names):
    try:
        payments = Payment.objects.filter(name__in=payment_names).values_list('id', flat=True)
        all_tutors = Tutor.objects.filter(payment_type__in=payments).values_list('user', flat=True)
        filtered_results = last_query.filter(id__in=all_tutors)
        
        return filtered_results
    except:
        raise ValueError("Error in filtering the payment")


def filter_score(last_query, scores):
    try:
        
        all_tutors = Tutor.objects.filter(average_rating__in=scores).values_list('user', flat=True)

        filtered_results = last_query.filter(id__in=all_tutors)
        
        return filtered_results
    except:
        raise ValueError("Error in filtering the payment")


def filter_region(last_query, region_names):
    try:
        regions = Regions.objects.filter(region_name__in=region_names).values_list('id', flat=True)
        all_tutors = Tutor.objects.filter(region__in=regions).values_list('user', flat=True)

        filtered_results = last_query.filter(id__in=all_tutors)

        return filtered_results
    except:
        raise ValueError("Error in filtering the region")


def get_filters(request):
    filters = {}

    if request.GET.getlist('sesion'):
        filters['sessions'] = request.GET.getlist('sesion')
    
    if request.GET.getlist('modalidad'):
        filters['modals'] = request.GET.getlist('modalidad')

    if request.GET.getlist('retribucion'):
        filters['payments'] = request.GET.getlist('retribucion')

    if request.GET.getlist('calificacion'):
        filters['score'] = request.GET.getlist('calificacion')
        filters['score'].append('0')

    if request.GET.getlist('region'):
        filters['region'] = request.GET.getlist('region')

    return filters


class searchCourse(generic.View):

    def get(self, request, type_search):
        
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            if user.is_student():
                try:
                    
                    search_query = request.GET.get('buscar')
                    page_number = request.GET.get('pagina') 

                    if search_query is None:
                        return redirect('index')

                    filters = get_filters(request)

                    context = create_context(search_query, page_number, type_search, filters, user)      
                except:
                    context = {}

                if type_search == "tutor":
                    return render(request, 'Student/searchTutor.html', context)
                elif type_search == "recursos-publicos":
                    return render(request, 'Student/searchResources.html', context)
                elif type_search == "sesiones-publicas":
                    return render(request, 'Student/searchOpenSessions.html', context)
                else:
                    return render(request, "Student/search.html", context)
        return redirect('index')
