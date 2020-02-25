# -*- coding: utf-8 -*-
from tests import settings
from tests.resources import NaturalUser, Wallet, Transfer
from tests.test_base import BaseTest

from datetime import date

import responses
import time


class WalletsTest(BaseTest):
    @responses.activate
    def test_create_wallet(self):
        self.mock_natural_user()

        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': {
                    "Owners": [
                        "1169419"
                    ],
                    "Description": "Wallet of Victor Hugo",
                    "Balance": {
                        "Currency": "EUR",
                        "Amount": 0
                    },
                    "Currency": "EUR",
                    "Id": "1169421",
                    "Tag": "your custom tag",
                    "CreationDate": 1383323329
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169421',
                'body': {
                    "Owners": [
                        "1169419"
                    ],
                    "Description": "Wallet of Victor Hugo",
                    "Balance": {
                        "Currency": "EUR",
                        "Amount": 0
                    },
                    "Currency": "EUR",
                    "Id": "1169421",
                    "Tag": "My custom tag",
                    "CreationDate": 1383323329
                },
                'status': 200
            },
            {
                'method': responses.PUT,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169421',
                'body': {
                    "Owners": [
                        "1169419"
                    ],
                    "Description": "Wallet of Victor Hugo",
                    "Balance": {
                        "Currency": "EUR",
                        "Amount": 0
                    },
                    "Currency": "EUR",
                    "Id": "1169421",
                    "Tag": "My custom tag",
                    "CreationDate": 1383323329
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/wallets',
                'body': [
                    {
                        "Owners": [
                            "1169419"
                        ],
                        "Description": "Wallet of Victor Hugo",
                        "Balance": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Currency": "EUR",
                        "Id": "1169421",
                        "Tag": "your custom tag",
                        "CreationDate": 1383323329
                    }
                ],
                'status': 200
            }])

        wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.natural_user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }

        wallet = Wallet(**wallet_params)
        wallet.save()

        w = Wallet.get(wallet.get_pk())

        for k, v in wallet_params.items():
            if isinstance(v, list):
                self.assertEqual([self.natural_user], v)  # TODO: Fix this
            else:
                self.assertEqual(getattr(w, k), v)

        self.assertEqual(w.get_pk(), wallet.get_pk())

        previous_pk = wallet.get_pk()

        wallet.description = "Wallet of Victor Claver"
        wallet.save()

        self.assertEqual(previous_pk, wallet.get_pk())

        self.assertEqual(len(self.natural_user.wallets), 1)
        self.assertEqual(self.natural_user.wallets, [wallet])

    @responses.activate
    def test_related_wallet(self):
        self.mock_natural_user()

        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': {
                    "Owners": [
                        "1167492"
                    ],
                    "Description": "A very cool wallet",
                    "Balance": {
                        "Currency": "EUR",
                        "Amount": 0
                    },
                    "Currency": "EUR",
                    "Id": "1169421",
                    "Tag": "your custom tag",
                    "CreationDate": 1383323329
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/natural/1169419',
                'body': {
                    "FirstName": "Victor",
                    "LastName": "Claver",
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
                    "PersonType": "NATURAL",
                    "Email": "victor@hugo.com",
                    "Id": "1169419",
                    "Tag": "custom tag",
                    "CreationDate": 1383321421,
                    "KYCLevel": "LIGHT"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/wallets',
                'body': [
                    {
                        "Owners": [
                            "1167492"
                        ],
                        "Description": "A very cool wallet",
                        "Balance": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Currency": "EUR",
                        "Id": "1169421",
                        "Tag": "your custom tag",
                        "CreationDate": 1383323329
                    }
                ],
                'status': 200
            }])

        wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.natural_user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }
        wallet = Wallet(**wallet_params)
        wallet.save()

        user = NaturalUser.get(self.natural_user.get_pk())

        self.assertEqual(user.wallets, [wallet])

    @responses.activate
    def test_retrieve_wallet_transactions(self):
        self.mock_natural_user()
        self.mock_legal_user()

        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': {
                    "Owners": [
                        "1167492"
                    ],
                    "Description": "A very cool wallet",
                    "Balance": {
                        "Currency": "EUR",
                        "Amount": 0
                    },
                    "Currency": "EUR",
                    "Id": "1169421",
                    "Tag": "your custom tag",
                    "CreationDate": 1383323329
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
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169421/transactions',
                'body': [
                    {
                        "Id": "1169215",
                        "Tag": "my transfer",
                        "CreationDate": 1383156787,
                        "AuthorId": "1167492",
                        "CreditedUserId": "1167502",
                        "DebitedFunds": {
                            "Currency": "EUR",
                            "Amount": 100
                        },
                        "CreditedFunds": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Fees": {
                            "Currency": "EUR",
                            "Amount": 100
                        },
                        "Status": "CREATED",
                        "ResultCode": "000000",
                        "ResultMessage": "Success",
                        "ExecutionDate": 1383156788,
                        "Type": "TRANSFER",
                        "Nature": "REGULAR",
                        "CreditedWalletId": "1167504",
                        "DebitedWalletId": "1167494"
                    }
                ],
                'status': 200
            }])

        # Create a transaction:
        params = {
            "author": self.legal_user,
            "credited_user": self.natural_user,
            "debited_funds": {
                "Currency": "EUR",
                "Amount": 1000
            },
            "fees": {
                "Currency": "EUR",
                "Amount": 100
            },
            "debited_wallet": self.legal_user_wallet,
            "credited_wallet": self.natural_user_wallet,
            "tag": "custom tag"
        }
        transfer = Transfer(**params)
        transfer.save()

        # List wallet's transactions
        transactions = self.legal_user_wallet.transactions.all()

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].type, 'TRANSFER')
