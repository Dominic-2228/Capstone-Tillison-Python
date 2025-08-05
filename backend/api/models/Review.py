from django.db import models
from django.conf import settings
from .Package import Package

class Review(models.Model):
  description = models.CharField(max_length=255)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  rating  = models.IntegerField()
  package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return f"{self.user.first_name} - {self.rating}/5"