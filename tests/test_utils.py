# -*- coding: utf-8 -*-

from datetime import datetime
import pytz

from tests.test_base import BaseTest

from mangopay.utils import timestamp_from_datetime


class UtilsTest(BaseTest):

    def test_timestamp_from_datetime_timezone_unaware(self):
        """
        The timestamp should be correctly calculated on a timezone unaware datetime.
        """
        unaware_datetime = datetime(2016, 1, 1, 10, 0, 0, 0)
        self.assertEqual(timestamp_from_datetime(unaware_datetime), 1451642400)

    def test_timestamp_from_datetime_timezone_aware(self):
        """
        The timestamp should be calculated on a timezone aware datetime by first
        converting the datetime to UTC timezone.
        """
        eastern = pytz.timezone('US/Eastern')
        aware_datetime = eastern.localize(datetime(2016, 1, 1, 5, 0, 0, 0))
        self.assertEqual(timestamp_from_datetime(aware_datetime), 1451642400)
