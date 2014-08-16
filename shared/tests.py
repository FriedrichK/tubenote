from datetime import datetime

from django.test import TestCase
from django.utils.timezone import utc

from shared.conversion import datetime_to_json


class ConversionTestCase(TestCase):

    def test_returns_expected_json_representation_of_datetime(self):
        dt = datetime(2014, 1, 1).replace(tzinfo=utc)

        actual = datetime_to_json(dt)

        self.assertEqual(actual, {'hour': 0, 'month': 1, 'second': 0, 'year': 2014, 'timezone': 'UTC', 'day': 1, 'minute': 0})

    def test_returns_expected_json_representation_of_datetime_without_timezone_information(self):
        dt = datetime(2014, 1, 1)

        actual = datetime_to_json(dt)

        self.assertEqual(actual, {'hour': 0, 'month': 1, 'second': 0, 'year': 2014, 'timezone': None, 'day': 1, 'minute': 0})
