from django.db import models
from .Package import Package
from .Service import Service

class Package_Service(models.Model):
  service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
  package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return f"{self.service} - {self.package}"