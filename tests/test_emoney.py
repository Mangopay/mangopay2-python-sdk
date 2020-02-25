# -*- coding: utf-8 -*-
from mangopay.resources import EMoney
from tests.test_base import BaseTestLive


class EMoneyTest(BaseTestLive):

    def test_retrieve_emoney(self):
        john = self.get_john()
        emoney = john.get_emoney()
        self.assertIsNotNone(emoney)

    def test_retrieve_emoney_for_year(self):
        john = self.get_john()
        emoney = john.get_emoney(**{'year': 2019})
        self.assertIsNotNone(emoney)

    def test_retrieve_emoney_for_month(self):
        john = self.get_john()
        emoney = john.get_emoney(**{'year': 2019, 'month': 4})
        self.assertIsNotNone(emoney)
