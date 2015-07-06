# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import Q

from rest_framework import filters
from rest_framework.exceptions import ParseError


class NearToPointFilter(filters.BaseFilterBackend):

    LATITUDE = 'lat'
    LONGITUDE = 'long'
    MAX_DISTANCE = 'max_distance'
    UNITS = 'km'

    def filter_queryset(self, request, queryset, view):
        point_field = getattr(view, 'point_field_filter', None)

        latitude = request.query_params.get(NearToPointFilter.LATITUDE, None)
        longitude = request.query_params.get(NearToPointFilter.LONGITUDE, None)
        max_distance = request.query_params.get(NearToPointFilter.MAX_DISTANCE, None)

        if not point_field:
            return queryset

        if not longitude and not latitude:
            return queryset

        try:
            latitude = float(latitude)
        except ValueError:
            raise ParseError('Invalid latitude string supplied for parameter {0}'.format(latitude))

        try:
            longitude = float(longitude)
        except ValueError:
            raise ParseError('Invalid longitude string supplied for parameter {0}'.format(longitude))

        location = Point(float(longitude), float(latitude))

        if max_distance is not None:
            queryset = queryset.filter(
                Q(**{'{}__distance_lte'.format(point_field): (location, D(**{NearToPointFilter.UNITS: max_distance}))})
            )

        return queryset.distance(location, field_name=point_field).order_by('distance')
