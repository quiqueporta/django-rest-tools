# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from django_rest_tools.fields import DateToTimeStampField
from .models import Location


class LocationListSerializer(serializers.ModelSerializer):

    date = DateToTimeStampField()

    class Meta:
        model = Location
        fields = ('id', 'name', 'date')
