from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template.loader import get_template

from UserAuthentication.models import User
from Chat.models import Room, Message
import json


class ChatLobby(View):
    template_name = 'chatLobby.html'
    user: User = None

    def get(self, request, room_pk=None):
        user = User.objects.get(pk=request.user.id)
        rooms = list(Room.objects.filter(original_user_sender=user) | Room.objects.filter(original_user_receiver=user))

        current_room = None
        messages = None
        if room_pk:
            current_room = Room.objects.get(pk=room_pk)
            messages = list(Message.objects.filter(room=current_room))

        context = {
            'current_user': user,
            'rooms': rooms,
            'current_room': current_room,
            'chat_messages': messages
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if request.is_ajax():
            user = User.objects.get(pk=request.user.id)

            if request.POST.get('room_id'):
                room = Room.objects.get(pk=request.POST['room_id'])
                messages = list(Message.objects.filter(room=room))

                reciever = room.context_reciever(user)
                context = {'chat_messages': messages,
                           'receiver': reciever}
                return HttpResponse(render(request, 'chatMessages.html', context))

            return HttpResponse(render(request, 'chatMessages.html'))
