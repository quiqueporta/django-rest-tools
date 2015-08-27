# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import datetime
import time

from django.utils import six

from rest_framework.fields import IntegerField


def datetime_to_timestamp(value):
    return int(time.mktime(value.timetuple()) * 1000)

def datetime_from_timestamp(value):
    return datetime.datetime.fromtimestamp(value / 1e3)


class DateToTimeStampField(IntegerField):

    def to_internal_value(self, data):
        if isinstance(data, six.text_type) and len(data) > self.MAX_STRING_LENGTH:
            self.fail('max_string_length')

        try:
            data = int(self.re_decimal.sub('', str(data)))
        except (ValueError, TypeError):
            self.fail('invalid')

        return datetime_from_timestamp(data).date()

    def to_representation(self, value):
        if not value:
            return None

        assert not isinstance(value, datetime.datetime), (
            'Expected a `date`, but got a `datetime`. Refusing to coerce, '
            'as this may mean losing timezone information. Use a custom '
            'read-only field and deal with timezone issues explicitly.'
        )

        return datetime_to_timestamp(value)


class DateTimeToTimeStampField(IntegerField):

    def to_internal_value(self, data):
        if isinstance(data, six.text_type) and len(data) > self.MAX_STRING_LENGTH:
            self.fail('max_string_length')

        try:
            data = int(self.re_decimal.sub('', str(data)))
        except (ValueError, TypeError):
            self.fail('invalid')

        return datetime_from_timestamp(data)

    def to_representation(self, value):
        if not value:
            return None

        return datetime_to_timestamp(value)
