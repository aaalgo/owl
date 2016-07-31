from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Image (models.Model):
    path = models.CharField(max_length=500)
    meta = models.TextField()
    done = models.BooleanField(default = False)
    viewed = models.BooleanField(default = False)

class Log (models.Model):
    CREATE, UPDATE, DELETE = 1, 2, 3
    METHOD_CHOICES = ((CREATE, "CREATE"),
                      (UPDATE, "UPDATE"),
                      (DELETE, "DELETE"))
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=False)
    method = models.IntegerField(choices=METHOD_CHOICES, null=False)
    anno = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()

class Annotation (models.Model):
    signature = models.CharField(max_length=250, primary_key=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=False)
    anno = models.TextField()
    log = models.ForeignKey(Log, on_delete=models.SET_NULL, null=True)
    deleted = models.BooleanField(default = False)

