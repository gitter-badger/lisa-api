from django.db import models


class Plugin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=100, blank=True)
