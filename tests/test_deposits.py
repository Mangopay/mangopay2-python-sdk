import unittest

from mangopay.resources import Deposit
from tests.test_base import BaseTestLive


class DepositsTest(BaseTestLive):

    def test_create(self):
        deposit = self.create_new_deposit()
        self.assertIsNotNone(deposit)

    def test_get(self):
        deposit = self.create_new_deposit()
        fetched_deposit = Deposit.get(deposit.id)

        self.assertIsNotNone(fetched_deposit)
        self.assertEqual(deposit.id, fetched_deposit.id)

    @unittest.skip("can't be tested yet")
    def test_cancel(self):
        deposit = self.create_new_deposit()

        dto = {
            "payment_status": "CANCELED"
        }

        canceled_deposit_dict = deposit.update(deposit.get_pk(), **dto).execute()
        canceled_deposit = Deposit(**canceled_deposit_dict)

        self.assertIsNotNone(canceled_deposit)
        self.assertEqual("CANCELED", canceled_deposit.payment_status)
