import unittest

from mangopay.resources import VirtualAccount, \
    VirtualAccountAvailability
from tests.test_base import BaseTestLive


class VirtualAccountTest(BaseTestLive):

    def test_create_virtual_account(self):
        virtual_account = BaseTestLive.create_new_virtual_account()

        self.assertIsNotNone(virtual_account)
        self.assertEqual(virtual_account.status, 'ACTIVE')

    def test_get_virtual_account(self):
        virtual_account = BaseTestLive.create_new_virtual_account()
        wallet = BaseTestLive.get_johns_wallet()
        fetched = VirtualAccount.get(virtual_account.id, **{'wallet_id': wallet.id})

        self.assertIsNotNone(fetched)
        self.assertEqual(virtual_account.id, fetched.id)

    def test_get_all_virtual_accounts(self):
        BaseTestLive.create_new_virtual_account()
        wallet = BaseTestLive.get_johns_wallet()
        fetched = VirtualAccount.all(**{'wallet_id': wallet.id})

        self.assertIsNotNone(fetched)
        self.assertTrue(len(fetched) > 0)

    def test_deactivate_virtual_account(self):
        virtual_account = BaseTestLive.create_new_virtual_account()
        wallet = BaseTestLive.get_johns_wallet()

        result_dict = VirtualAccount.update(virtual_account.id, **{'wallet_id': wallet.id}).execute()
        deactivated = VirtualAccount(**result_dict)

        self.assertIsNotNone(deactivated)
        self.assertEqual(virtual_account.id, deactivated.id)
        self.assertEqual(deactivated.status, "CLOSED")

    # TODO
    @unittest.skip('API issue. To be re-enable once it is fixed')
    def test_get_availabilities(self):
        availabilities = VirtualAccountAvailability.all()
        self.assertIsNotNone(availabilities)
        self.assertEqual(1, len(availabilities))

