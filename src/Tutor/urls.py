from django.urls import path
from . import views
from Tutorship.views import RequestNotificationView

urlpatterns = [
    path('calendario', views.CalendarView.as_view(), name='tutor_calendar'),
    path('perfil', views.ProfileView.as_view(), name='tutor_profile'),
    path('cursos', views.CourseView.as_view(), name='tutor_courses'),
    path('pendientes', views.PendingRequestView.as_view(), name='tutor_pending_requests'),
    path(r'pendientes/<int:request_pk>', views.PendingRequestView.as_view(), name='tutor_pending_requests'),
    path('aceptadas', views.AcceptedRequestView.as_view(), name='tutor_accepted_requests'),
    path(r'aceptadas/<int:request_pk>', views.AcceptedRequestView.as_view(), name='tutor_accepted_requests'),
    path('notificacion/<int:notification_pk>/solicitud/<int:request_pk>',
         RequestNotificationView.as_view(), name='request_notification'),

    path('aceptadas/<int:request_pk>/tutoria',
         views.TutorshipView.as_view(), name='tutor_tutorship_view'),
    path(r'aceptadas/<int:request_pk>/tutoria/<int:resource_pk>',
         views.TutorshipView.as_view(), name='tutor_tutorship_view'),

    path('ganancias', views.ProfitView.as_view(), name='tutor_profit'),
    path('historial', views.DoneTutorships.as_view(), name='tutor_done_requests'),
    path('calificación/<int:request_pk>', views.CalificationsTutorships.as_view(), name='tutorship_califications')
]
