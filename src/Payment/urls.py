from django.urls import path
from . import views

urlpatterns = [
    path('add_payment', views.AddPayment.as_view(), name="add_payment"),
    path('edit_payment', views.EditPayment.as_view(), name='edit_payment'),
    path(r'edit_payment/<int:payment>', views.EditPayment.as_view(), name='edit_payment'),
]
