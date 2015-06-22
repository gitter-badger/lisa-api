from django.db import models


class Plugin(models.Model):
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=100, blank=True)


class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    mac = models.CharField(max_length=100, unique=True, null=True)
    zone = models.ForeignKey(Zone, related_name='clients')
