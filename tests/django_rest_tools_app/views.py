# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import generics
from django_rest_tools.filters import NearToPointFilter

from .serializers import LocationListSerializer
from .models import Location


class LocationsList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationListSerializer
    filter_backends = (NearToPointFilter,)
    point_field_filter = 'location'
