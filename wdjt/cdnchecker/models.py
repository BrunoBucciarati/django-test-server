# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class cdnurl(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    def __str__(self):
        return self.url
