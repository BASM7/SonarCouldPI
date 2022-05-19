from django import template
import urllib.parse

from Tutorship.models import RequestNotification
from Chat.models import MessageNotification
from UserAuthentication.models import User

register = template.Library()


@register.inclusion_tag('showNotifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    user = User.objects.get(id=request_user.id)
    notifications = RequestNotification.objects.filter(to_user=user, seen=False).order_by('-date')
    return {'notifications': notifications}


@register.inclusion_tag('showMessageNotifications.html', takes_context=True)
def show_message_notifications(context):
    request_user = context['request'].user
    user = User.objects.get(id=request_user.id)
    notifications = MessageNotification.objects.filter(to_user=user, seen=False).order_by('-date')
    return {'notifications': notifications}


@register.filter
def toggle_value(request, arg):
    url_parts = list(urllib.parse.urlparse(request.get_full_path()))
    query = dict(urllib.parse.parse_qsl(url_parts[4], keep_blank_values=True))
    query["pagina"] = arg
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


@register.filter
def delete_value(request, arg):
    url_parts = list(urllib.parse.urlparse(request.get_full_path()))
    query = list(urllib.parse.parse_qsl(url_parts[4], keep_blank_values=True))

    for value in query:
        if value[1] == str(arg):
            query.remove(value)
            break

    url_parts[4] = urllib.parse.urlencode(query)

    return urllib.parse.urlunparse(url_parts)



@register.simple_tag
def get_context_reciever(user, room):
    return room.context_reciever(user)


@register.filter
def get_name(context):
    request_user = context.user
    user = User.objects.get(id=request_user.id)

    return user.name
