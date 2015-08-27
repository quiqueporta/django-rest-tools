# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from django_rest_tools.fields import DateToTimeStampField, DateTimeToTimeStampField
from .models import Location


class LocationListSerializer(serializers.ModelSerializer):

    date = DateToTimeStampField(required=False)
    date_time = DateTimeToTimeStampField(required=False)

    class Meta:
        model = Location
        fields = ('id', 'name', 'date', 'date_time')
