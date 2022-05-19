from django.db import models

class Regions(models.Model):
    """Models for the regions of the tutor"""
    region_name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    def __str__(self):
        return self.region_name