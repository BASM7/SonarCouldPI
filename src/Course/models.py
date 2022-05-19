from django.db import models


# Create your models here.
class Course(models.Model):
    """Model for the User"""
    university = models.CharField(max_length=50)
    course_name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    
    def __str__(self):
        return self.course_name
