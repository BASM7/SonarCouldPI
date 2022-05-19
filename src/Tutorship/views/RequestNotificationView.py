from django.views.generic import View
from UserAuthentication.models import User
from Tutorship.models import RequestNotification
from Student.models import Request
from django.shortcuts import redirect, render


class RequestNotificationView(View):
    def get(self, request, notification_pk, request_pk):
        notification = RequestNotification.objects.get(pk=notification_pk)

        notification.seen = True
        notification.save()

        if notification.is_new_request():
            return redirect('tutor_pending_requests', request_pk=request_pk)
        elif notification.is_accepted_request():
            return redirect('student_accepted_request')
        elif notification.is_rejected_request():
            return redirect('student_rejected_request')

