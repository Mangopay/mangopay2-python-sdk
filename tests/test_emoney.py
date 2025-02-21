# -*- coding: utf-8 -*-
from tests.test_base import BaseTestLive


class EMoneyTest(BaseTestLive):

    def test_retrieve_emoney(self):
        john = self.get_john()
        emoney = john.get_emoney()
        self.assertResponse(emoney)

    def test_retrieve_emoney_for_year(self):
        john = self.get_john()
        emoney = john.get_emoney(**{'year': 2019})
        self.assertResponse(emoney)

    def test_retrieve_emoney_for_month(self):
        john = self.get_john()
        emoney = john.get_emoney(**{'year': 2019, 'month': 4})
        self.assertResponse(emoney)

    def assertResponse(self, emoney_response):
        self.assertIsNotNone(emoney_response)
        self.assertTrue(len(emoney_response.data) > 0)
        self.assertIsNotNone(emoney_response.data[0].credited_emoney)
        self.assertIsNotNone(emoney_response.data[0].debited_emoney)
