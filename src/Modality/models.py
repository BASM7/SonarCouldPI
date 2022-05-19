from django.db import models


# Create your models here.
class Modality(models.Model):
    """Model for the Modality."""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
