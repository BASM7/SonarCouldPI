from django.urls import path
from . import views

urlpatterns = [
    path('add_resource', views.AddResource.as_view(), name="add_resource"),
    path('edit_resource', views.EditResource.as_view(), name='edit_resource'),
    path(r'edit_resource/<int:resource>', views.EditResource.as_view(), name='edit_resource'),
]
