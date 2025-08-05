from django.db import models

class Service(models.Model):
  description = models.CharField(max_length=255)

  def __str__(self):
    return self.description