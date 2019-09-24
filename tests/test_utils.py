# -*- coding: utf-8 -*-

from datetime import datetime
import pytz

from tests.test_base import BaseTest

from mangopay.utils import Address, Money, timestamp_from_datetime


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

    def test_camelcase_aliases_on_Money(self):
        m = Money(10, 'EUR')
        self.assertEqual(m.Amount, 10)
        self.assertEqual(m.Currency, 'EUR')
        m.Amount = 5
        m.Currency = 'USD'
        self.assertEqual(m.amount, 5)
        self.assertEqual(m.currency, 'USD')

    def test_camelcase_aliases_on_Address(self):
        addr = Address('line1', 'line2', 'city', 'region', 'postal code', 'country')
        self.assertIs(addr.AddressLine1, addr.address_line_1)
        self.assertIs(addr.AddressLine2, addr.address_line_2)
        self.assertIs(addr.City, addr.city)
        self.assertIs(addr.Region, addr.region)
        self.assertIs(addr.PostalCode, addr.postal_code)
        self.assertIs(addr.Country, addr.country)
        addr.AddressLine2 = None
        self.assertIs(addr.address_line_2, None)
        addr.region = None
        self.assertIs(addr.Region, None)
