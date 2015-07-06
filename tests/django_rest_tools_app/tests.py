# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from rest_framework import status

from rest_framework.test import APITestCase

from .models import Location
from .views import LocationsList

MAX_DISTANCE = 20
MY_LONGITUDE = -0.3680616
MY_LATITUDE = 39.4910202

ZARAGOZA = 'Zaragoza'
HUESCA = 'Huesca'
BARCELONA = 'Barcelona'
VALENCIA = 'Valencia'


class NearToPointFilterTest(APITestCase):

    def setUp(self):

        self.location_in_valencia = self._create_location(VALENCIA, -0.362286, 39.494427)
        self.location_in_barcelona = self._create_location(BARCELONA, 2.1487679, 41.39479)
        self.location_in_huesca = self._create_location(HUESCA, -0.4058484, 42.1359063)
        self.location_in_zaragoza = self._create_location(ZARAGOZA, -0.9270592, 41.6915748)

    def _create_location(self, name, long, lat):
        location = Location()
        location.name = name
        location.location = Point(long, lat)
        location.save()
        return location

    def test_filter_is_not_applied_if_no_point_field_filter_provided(self):
        LocationsList.point_field_filter = ''
        response = self.client.get(reverse('location-list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, len(response.data))

    def test_filter_is_not_applied_if_no_lat_and_long_provided(self):
        LocationsList.point_field_filter = 'location'
        response = self.client.get(reverse('location-list'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, len(response.data))

    def test_no_valid_latitude_returns_bad_request(self):
        LocationsList.point_field_filter = 'location'
        response = self.client.get("{}?lat=asdf&long=-0.3".format(reverse('location-list')))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_no_valid_longitude_returns_bad_request(self):
        LocationsList.point_field_filter = 'location'
        response = self.client.get("{}?lat=39.4&long=asdf".format(reverse('location-list')))
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_if_no_max_distance_provided_results_are_only_ordered_by_distance(self):
        LocationsList.point_field_filter = 'location'
        response = self.client.get("{}?lat={}&long={}".format(reverse('location-list'), MY_LATITUDE, MY_LONGITUDE))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(VALENCIA, response.data[0]['name'])
        self.assertEqual(ZARAGOZA, response.data[1]['name'])
        self.assertEqual(HUESCA, response.data[2]['name'])
        self.assertEqual(BARCELONA, response.data[3]['name'])

    def test_if_max_distance_provided_(self):
        LocationsList.point_field_filter = 'location'
        response = self.client.get("{}?lat={}&long={}&max_distance={}".format(
            reverse('location-list'), MY_LATITUDE, MY_LONGITUDE, MAX_DISTANCE)
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(VALENCIA, response.data[0]['name'])
