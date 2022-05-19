from django.urls import path, re_path
from . import views

urlpatterns = [
     path("estudiante", views.mainScreen.as_view(), name="index_student"),
     re_path(r'^estudiante/busqueda/(?P<type_search>[^/]+)', views.searchCourse.as_view(), name="search"),

     path('estudiante/curso/<str:course_name>', views.displayCourseDetail.as_view(), name="course_detail"),
     path('estudiante/curso/<str:course_name>/agendar', views.RequestTutorship.as_view(), name="request_tutorship"),
     path('estudiante/tutor/<str:tutor>', views.DisplayTutorDetail.as_view(), name="tutor_detail"),
     path('estudiante/tutor/<str:tutor>/agendar', views.RequestTutorshipTutor.as_view(), name="request_tutorship_tutor"),
     path('estudiante/tutoria/unirse/<int:request_id>', views.JoinRequest.as_view(), name="request_join_tutorship"),

     path('estudiante/tutoria/pendientes', views.pendingRequests.as_view(), name='student_pending_request'),
     path('estudiante/tutoria/aceptadas', views.acceptedRequests.as_view(), name='student_accepted_request'),
     path('estudiante/tutoria/rechazadas', views.rejectedRequests.as_view(), name='student_rejected_request'),
     path('estudiante/tutoria/historial', views.doneTutorships.as_view(), name='student_done_request'),

     path('estudiante/tutoria/pendientes/<int:pk_request>',
          views.pendingRequests.as_view(), name='student_pending_request'),
     path(r'estudiante/tutoria/aceptadas/<int:request_pk>',
          views.StudentTutorshipView.as_view(), name='student_tutorship_view'),
     path('estudiante/tutoria/rechazadas/<int:pk_request>',
          views.rejectedRequests.as_view(), name='student_rejected_request'),
     path('estudiante/tutoria/historial/<int:pk_request>',
          views.doneTutorships.as_view(), name='student_done_request'),
     path('estudiante/perfil', views.ProfileView.as_view(), name='student_profile')
]
    
