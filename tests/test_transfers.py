# -*- coding: utf-8 -*-
from tests import settings
from tests.resources import Transfer, Wallet, DirectPayIn
from tests.test_base import BaseTest, BaseTestLive

from mangopay.utils import Money

from datetime import date

import responses
import time


class TransfersTest(BaseTest):
    @responses.activate
    def test_create_transfers(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()
        self.mock_card()

        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1167495',
                'body': {
                    "FirstName": "Victor",
                    "LastName": "Hugo",
                    "Address": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    },
                    "Birthday": int(time.mktime(date.today().timetuple())),
                    "Nationality": "FR",
                    "CountryOfResidence": "FR",
                    "Occupation": "Writer",
                    "IncomeRange": 6,
                    "ProofOfIdentity": None,
                    "ProofOfAddress": None,
                    "PersonType": "NATURAL",
                    "Email": "victor@hugo.com",
                    "Id": "1167495",
                    "Tag": "custom tag",
                    "CreationDate": 1383321421,
                    "KYCLevel": "LIGHT"
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payins/card/direct',
                'body': {
                    "Id": "6784288",
                    "Tag": None,
                    "CreationDate": 1432046586,
                    "AuthorId": "6784285",
                    "CreditedUserId": "6784283",
                    "DebitedFunds": {"Currency": "EUR", "Amount": 10000},
                    "CreditedFunds": {"Currency": "EUR", "Amount": 9900},
                    "Fees": {"Currency": "EUR", "Amount": 100},
                    "Status": "SUCCEEDED",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "ExecutionDate": 1432046588,
                    "Type": "PAYIN",
                    "Nature": "REGULAR",
                    "CreditedWalletId": "6784284",
                    "DebitedWalletId": None,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT",
                    "SecureMode": "DEFAULT",
                    "CardId": "6784287",
                    "SecureModeReturnURL": None,
                    "SecureModeRedirectURL": None,
                    "SecureModeNeeded": False
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/transfers',
                'body': {
                    "Id": "1169434",
                    "Tag": "custom tag",
                    "CreationDate": 1431648000,
                    "AuthorId": "1167495",
                    "CreditedUserId": "1167502",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": 900
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": 100
                    },
                    "Status": "SUCCEEDED",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "ExecutionDate": int(time.mktime(date.today().timetuple())),
                    "Type": "TRANSFER",
                    "Nature": "REGULAR",
                    "DebitedWalletId": "1167496",
                    "CreditedWalletId": "1167504"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/transfers/1169434',
                'body': {
                    "Id": "1169434",
                    "Tag": "DefaultTag",
                    "CreationDate": 1383556653,
                    "AuthorId": "1167495",
                    "CreditedUserId": "1167502",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": 900
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": 100
                    },
                    "Status": "SUCCEEDED",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "ExecutionDate": 1383556653,
                    "Type": "TRANSFER",
                    "Nature": "REGULAR",
                    "DebitedWalletId": "1167496",
                    "CreditedWalletId": "1167504"
                },
                'status': 200
            }])

        wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.card.user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }
        wallet = Wallet(**wallet_params)
        wallet.save()

        direct_payin_params = {
            "author": self.card.user,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "credited_wallet": wallet,
            "card": self.card,
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "http://www.ulule.com/"
        }
        direct_payin = DirectPayIn(**direct_payin_params)
        direct_payin.save()

        params = {
            "author": self.card.user,
            "credited_user": self.legal_user,
            "debited_funds": Money(amount=1000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "debited_wallet": wallet,
            "credited_wallet": self.legal_user_wallet,
            "tag": "custom tag"
        }
        transfer = Transfer(**params)

        self.assertIsNone(transfer.get_pk())
        transfer.save()
        self.assertIsInstance(transfer, Transfer)

        self.assertEqual(transfer.status, 'SUCCEEDED')

        self.assertEqual(direct_payin.debited_funds.amount, 10000)
        direct_payin_params.pop('debited_funds')

        self.assertEqual(direct_payin.fees.amount, 100)
        direct_payin_params.pop('fees')

        for key, value in params.items():
            self.assertEqual(getattr(transfer, key), value)

        self.assertIsNotNone(transfer.get_pk())

        # test_retrieve_transfers
        retrieved_transfer = Transfer.get(transfer.get_pk())

        self.assertIsNotNone(retrieved_transfer.get_pk())
        self.assertIsInstance(retrieved_transfer, Transfer)

        self.assertEqual(getattr(retrieved_transfer, 'id'), transfer.get_pk())


class Transfers(BaseTestLive):
    def test_Transfer_GetRefunds(self):
        transfer = BaseTestLive.get_johns_transfer()

        refunds_page = transfer.get_refunds()

        self.assertIsNotNone(refunds_page.data)
        self.assertIsInstance(refunds_page.data, list)
