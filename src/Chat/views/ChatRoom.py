from django.views.generic import View
from django.shortcuts import render, redirect

from UserAuthentication.models import User
from Chat.models import Room, Message


class ChatRoom(View):
    template_name = 'chatLobby.html'
    user: User = None

    def get(self, request, user_receiver_pk=None):
        user = User.objects.get(pk=request.user.id)
        user_to = User.objects.get(pk=user_receiver_pk)

        if not list(Room.objects.filter(original_user_sender=user, original_user_receiver=user_to) |
                    Room.objects.filter(original_user_sender=user_to, original_user_receiver=user)):
            room = Room(original_user_sender=user, original_user_receiver=user_to)
            room.save()

        room = list(Room.objects.filter(original_user_sender=user, original_user_receiver=user_to) |
                    Room.objects.filter(original_user_sender=user_to, original_user_receiver=user))[0]

        return redirect('chatlobby', room_pk=room.id)
