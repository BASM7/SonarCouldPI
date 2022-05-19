from django.urls import path
from . import views

urlpatterns = [
    path('add_session', views.AddSession.as_view(), name="add_session"),
    path('edit_session', views.EditSession.as_view(), name='edit_session'),
    path(r'edit_session/<int:session>', views.EditSession.as_view(), name='edit_session'),
]
