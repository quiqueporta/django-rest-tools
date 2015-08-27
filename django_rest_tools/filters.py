# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

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

        latitude = self._parse_param_to_float(value=latitude, param_name='latitude')
        longitude = self._parse_param_to_float(value=longitude, param_name='longitude')

        location = Point(float(longitude), float(latitude))

        if max_distance is not None:
            queryset = queryset.filter(
                Q(**{'{}__distance_lte'.format(point_field): (location, D(**{NearToPointFilter.UNITS: max_distance}))})
            )

        return queryset.distance(location, field_name=point_field).order_by('distance')

    def _parse_param_to_float(self, value, param_name):
        try:
            value = float(value)
        except ValueError:
            raise ParseError('Invalid {} string supplied for parameter {}'.format(param_name, value))
        return value
