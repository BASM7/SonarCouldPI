from django.urls import path
from . import views

urlpatterns = [
    path("add_course", views.AddCourse.as_view(), name="add_course"),
    path('edit_course', views.EditCourse.as_view(), name='edit_course'),
    path(r'edit_course/<int:course>', views.EditCourse.as_view(), name='edit_course'),
]