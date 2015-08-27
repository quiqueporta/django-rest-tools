# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.gis.geos import Point
from django.core.urlresolvers import reverse
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.test import APITestCase

from django_rest_tools.fields import datetime_to_timestamp
from django_rest_tools_app.serializers import LocationListSerializer

from .models import Location
from .views import LocationsList

MAX_DISTANCE = 20
MY_LONGITUDE = -0.3680616
MY_LATITUDE = 39.4910202

ZARAGOZA = 'Zaragoza'
HUESCA = 'Huesca'
BARCELONA = 'Barcelona'
VALENCIA = 'Valencia'

class TestFactory(object):

    @staticmethod
    def create_location(name, longitude, latitude, date=None, date_time=None):
        if date is None:
            date = datetime.now().date()

        if date_time is None:
            date_time = datetime.now()

        location = Location(
            name=name,
            location=Point(longitude, latitude),
            date=date,
            date_time=date_time
        )

        location.save()

        return location



class NearToPointFilterTest(APITestCase):

    def setUp(self):

        self.location_in_valencia = TestFactory.create_location(VALENCIA, -0.362286, 39.494427)
        self.location_in_barcelona = TestFactory.create_location(BARCELONA, 2.1487679, 41.39479)
        self.location_in_huesca = TestFactory.create_location(HUESCA, -0.4058484, 42.1359063)
        self.location_in_zaragoza = TestFactory.create_location(ZARAGOZA, -0.9270592, 41.6915748)

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


class DateToTimeStampFieldTest(APITestCase):

    def setUp(self):
        self.my_date = datetime.strptime("2015-08-27", "%Y-%m-%d").date()
        self.my_date_in_timestamp = datetime_to_timestamp(self.my_date)

    def test_the_representation_of_date_field_is_a_timestamp(self):

        location_in_valencia = TestFactory.create_location(VALENCIA, -0.362286, 39.494427, date=self.my_date)
        location_serializer = LocationListSerializer(location_in_valencia)

        self.assertIsInstance(location_serializer.data['date'], int)
        self.assertEqual(self.my_date_in_timestamp, location_serializer.data['date'])

    def test_serializer_receive_timestamp_and_stores_date_into_database(self):

        data = {
            'name': VALENCIA,
            'location': Point(0, 0),
            'date': self.my_date_in_timestamp
        }

        location_serializer = LocationListSerializer(data=data)

        self.assertTrue(location_serializer.is_valid())

        location_serializer.save()

        location = Location.objects.get(id=location_serializer.data['id'])
        self.assertEqual(self.my_date, location.date)

    def test_serializer_fails_if_no_integer_is_assigned(self):

        data = {
            'name': VALENCIA,
            'location': Point(0, 0),
            'date': 'FAIL'
        }

        location_serializer = LocationListSerializer(data=data)

        self.assertFalse(location_serializer.is_valid())

    def test_serializer_returns_none_if_no_value_in_date_field(self):

        location_in_valencia = TestFactory.create_location(VALENCIA, -0.362286, 39.494427)
        location_in_valencia.date = None
        location_in_valencia.save()
        location_serializer = LocationListSerializer(location_in_valencia)

        self.assertIsNone(location_serializer.data['date'])


class DateTimeToTimeStampFieldTest(APITestCase):

    def setUp(self):
        self.my_date = datetime.strptime("2015-08-27", "%Y-%m-%d")
        self.my_date_in_timestamp = datetime_to_timestamp(self.my_date)

    def test_the_representation_of_datetime_field_is_a_timestamp(self):

        location_in_valencia = TestFactory.create_location(VALENCIA, -0.362286, 39.494427, date_time=self.my_date)
        location_serializer = LocationListSerializer(location_in_valencia)

        self.assertIsInstance(location_serializer.data['date'], int)
        self.assertEqual(self.my_date_in_timestamp, location_serializer.data['date'])

    def test_serializer_receive_timestamp_and_stores_datetime_into_database(self):

        data = {
            'name': VALENCIA,
            'location': Point(0, 0),
            'date_time': self.my_date_in_timestamp
        }

        location_serializer = LocationListSerializer(data=data)

        self.assertTrue(location_serializer.is_valid())

        location_serializer.save()

        location = Location.objects.get(id=location_serializer.data['id'])
        self.assertEqual(self.my_date, location.date_time)

    def test_serializer_fails_if_no_integer_is_assigned(self):

        data = {
            'name': VALENCIA,
            'location': Point(0, 0),
            'date': 'FAIL'
        }

        location_serializer = LocationListSerializer(data=data)

        self.assertFalse(location_serializer.is_valid())

    def test_serializer_returns_none_if_no_value_in_datetime_field(self):

        location_in_valencia = TestFactory.create_location(VALENCIA, -0.362286, 39.494427)
        location_in_valencia.date_time = None
        location_in_valencia.save()
        location_serializer = LocationListSerializer(location_in_valencia)

        self.assertIsNone(location_serializer.data['date_time'])
