from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.template.loader import get_template

from UserAuthentication.models import User
from Chat.models import Room, Message
import json


class SendMessage(View):
    template_name = 'chatLobby.html'
    user: User = None

    def get(self, request):
        pass

    def post(self, request):
        if request.is_ajax():
            user = User.objects.get(pk=request.user.id)

            print(request.POST['room'])
            print(request.POST['message'])

            room = Room.objects.get(pk=request.POST['room'])

            Message.objects.create(
                room=room,
                user_sender=user,
                content=request.POST['message']
            )

            messages = list(Message.objects.filter(room=room))

            reciever = room.context_reciever(user)
            context = {'chat_messages': messages,
                       'receiver': reciever}
            return HttpResponse(render(request, 'chatMessages.html', context))
