# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from .models import Location


class LocationListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'name',)
