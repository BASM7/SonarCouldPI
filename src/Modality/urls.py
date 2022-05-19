from django.urls import path
from . import views

urlpatterns = [
    path('add_modality', views.AddModality.as_view(), name="add_modality"),
    path('edit_modality', views.EditModality.as_view(), name='edit_modality'),
    path(r'edit_modality/<int:modality>', views.EditModality.as_view(), name='edit_modality'),
]
