# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db import models
from django.contrib.gis.db.models import GeoManager, PointField


class Location(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    location = PointField(null=True, blank=False, geography=True)
    date = models.DateField(blank=True, null=True)
    date_time = models.DateTimeField(blank=True, null=True)

    objects = GeoManager()

    def __unicode__(self):
        return self.name
