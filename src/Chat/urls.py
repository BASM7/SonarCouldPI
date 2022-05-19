# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('mensajes/', views.ChatLobby.as_view(), name='chatlobby'),
    path('mensajes/<int:room_pk>/', views.ChatLobby.as_view(), name='chatlobby'),
    path('mensajes/enviar', views.SendMessage.as_view(), name='send_message'),

    path('mensajes/<int:user_receiver_pk>', views.ChatRoom.as_view(), name='chatroom'),

]
