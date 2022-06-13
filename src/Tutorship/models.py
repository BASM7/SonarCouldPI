from django.db import models
from Course.models import Course
from Student.models import Request
from UserAuthentication.models import User
from django.utils import timezone


# Create your models here.
class Tutorship(models.Model):
    """Model for the Tutorship"""

    APPROVED = 'AP'
    DONE = 'DN'
    STATUS_CHOICES = (
        (APPROVED, 'Aprobada'),
        (DONE, 'Realizada'),
    )

    max_people = models.IntegerField()
    url = models.URLField(blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATUS_CHOICES, default=APPROVED)
    name = models.CharField(max_length=80, null=True)
    description = models.CharField(max_length=500, null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True)

    def set_done(self):
        self.state = self.DONE
        self.save()

    def remaining_capacity(self):
        return self.max_people - self.request.num_requesters


class TutorshipScore(models.Model):
    """Model for the TutorshipScore"""
    tutorship = models.ForeignKey(Tutorship, on_delete=models.CASCADE)
    score = models.IntegerField()
    student_comment = models.TextField(null=True)


class RequestNotification(models.Model):
    """Model for the notifications."""
    NEW_REQUEST = 'RE'
    ACCEPTED_REQUEST = 'AR'
    REJECTED_REQUEST = 'RR'
    TYPES = (
        (NEW_REQUEST, 'Nueva solicitud'),
        (ACCEPTED_REQUEST, 'Solicitud aceptada'),
        (REJECTED_REQUEST, 'Solicitud rechazada'),
    )
    notification_type = models.CharField(max_length=2, choices=TYPES)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)

#     def is_new_request(self):
#         return self.notification_type == self.NEW_REQUEST

#     def is_accepted_request(self):
#         return self.notification_type == self.ACCEPTED_REQUEST

#     def is_rejected_request(self):
#         return self.notification_type == self.REJECTED_REQUEST



