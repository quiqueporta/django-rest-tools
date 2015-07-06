# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import LocationsList

urlpatterns = [
    url(r'^locations/$', LocationsList.as_view(), name='location-list'),
]