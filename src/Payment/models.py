from django.db import models


# Create your models here.
class Payment(models.Model):
    """Model for the Payment."""
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name
