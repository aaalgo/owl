from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Image (models.Model):
    INIT, DONE = 1, 2
    STATUS_CHOICES = ((INIT, "INIT"),
                      (DONE, "DONE"))
    path = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=INIT)


class Annotation (models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    text = models.TextField()

