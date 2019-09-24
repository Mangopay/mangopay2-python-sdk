# -*- coding: utf-8 -*-
from tests import settings
from tests.resources import (Transfer, TransferRefund,
                             PayInRefund, DirectPayIn, Refund,
                             Wallet)
from tests.test_base import BaseTest

from mangopay.utils import Money

from datetime import date

import responses
import time


class RefundsTest(BaseTest):
    @responses.activate
    def test_create_transfer_refunds(self):
        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1167495',
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
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/card/direct',
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
            }])

        # Add money on legal_user_wallet
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_legal_user_wallet_99()
        self.mock_card()

        direct_payin_params = {
            "author": self.legal_user,
            "debited_funds": Money(amount=100, currency='EUR'),
            "fees": Money(amount=1, currency='EUR'),
            "credited_wallet": self.legal_user_wallet,
            "card": self.legal_user_card,
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "http://www.ulule.com/"
        }
        direct_payin = DirectPayIn(**direct_payin_params)
        direct_payin.save()

        legal_user_wallet = Wallet.get(self.legal_user_wallet.get_pk())
        self.assertEqual(legal_user_wallet.balance.amount, 9900)

        # Create a transfer (from legal_user_wallet to natural_user_wallet)
        responses.reset()
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_natural_user_wallet_9()
        self.mock_legal_user_wallet_89()

        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/transfers',
                'body': {
                    "Id": "1169434",
                    "Tag": "DefaultTag",
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
            }])

        params = {
            "author": self.legal_user,
            "credited_user": self.natural_user,
            "debited_funds": Money(amount=10, currency='EUR'),
            "fees": Money(amount=1, currency='EUR'),
            "debited_wallet": self.legal_user_wallet,
            "credited_wallet": self.natural_user_wallet,
            "tag": "custom tag"
        }
        transfer = Transfer(**params)
        transfer.save()
        self.assertEqual(transfer.status, 'SUCCEEDED')

        natural_user_wallet = Wallet.get(self.natural_user_wallet.get_pk())
        self.assertEqual(natural_user_wallet.balance.amount, 900)

        legal_user_wallet = Wallet.get(self.legal_user_wallet.get_pk())
        self.assertEqual(legal_user_wallet.balance.amount, 8900)

        # Test transfer refund
        responses.reset()
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_natural_user_wallet()
        self.mock_legal_user_wallet_99()

        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/refunds/123456708',
                'body': {
                    "Id": "123456708",
                    "Tag": None,
                    "CreationDate": 1384514520,
                    "AuthorId": "1167472",
                    "CreditedUserId": None,
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": 1100
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": -100
                    },
                    "Status": "SUCCEEDED",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "ExecutionDate": 1384514520,
                    "Type": "TRANSFER",
                    "Nature": "REFUND",
                    "InitialTransactionId": "1173371",
                    "InitialTransactionType": "PAYIN",
                    "DebitedWalletId": "1167473",
                    "CreditedWalletId": None,
                    "RefundReason": {
                        "RefusedReasonMessage": None,
                        "RefusedReasonType": "INITIALIZED_BY_CLIENT"
                    }
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/transfers/1169434/refunds',
                'body': {
                    "Id": "123456708",
                    "Tag": None,
                    "CreationDate": 1375437162,
                    "AuthorId": "123456775",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": "400"
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": "500"
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": "-100"
                    },
                    "Status": "SUCCEEDED",
                    "ResultCode": "00000",
                    "ExecutionDate": 1375437162,
                    "Type": "TRANSFER",
                    "Nature": "REFUND",
                    "InitialTransactionId": "1311279",
                    "InitialTransactionType": "TRANSFER",
                    "DebitedWalletId": "1311241",
                    "CreditedWalletId": "1311125",
                    "RefundReason": {
                        "RefusedReasonMessage": None,
                        "RefusedReasonType": "INITIALIZED_BY_CLIENT"
                    }
                },
                'status': 200
            }])

        params = {
            "author": self.legal_user,
            "transfer": transfer
        }
        transfer_refund = TransferRefund(**params)

        self.assertIsNone(transfer_refund.get_pk())
        transfer_refund.save()
        self.assertIsInstance(transfer_refund, TransferRefund)
        self.assertEqual(transfer_refund.status, 'SUCCEEDED')

        natural_user_wallet = Wallet.get(self.natural_user_wallet.get_pk())
        self.assertEqual(natural_user_wallet.balance.amount, 0)

        legal_user_wallet = Wallet.get(self.legal_user_wallet.get_pk())
        self.assertEqual(legal_user_wallet.balance.amount, 9900)

        for key, value in params.items():
            self.assertEqual(getattr(transfer_refund, key), value)

        self.assertIsNotNone(transfer_refund.get_pk())

        # test_retrieve_refunds
        refund = Refund.get(transfer_refund.get_pk())

        self.assertIsNotNone(refund.get_pk())
        self.assertIsInstance(refund, Refund)

        self.assertEqual(getattr(refund, 'id'), transfer_refund.get_pk())
        self.assertEqual(refund.type, 'TRANSFER')
        self.assertEqual(refund.nature, 'REFUND')

    @responses.activate
    def test_create_payin_refund(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_legal_user_wallet_99()
        self.mock_card()

        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1167495',
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
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/card/direct',
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
            }])

        direct_payin_params = {
            "author": self.card.user,
            "debited_funds": Money(amount=100, currency='EUR'),
            "fees": Money(amount=1, currency='EUR'),
            "credited_wallet": self.legal_user_wallet,
            "card": self.card,
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "http://www.ulule.com/"
        }
        direct_payin = DirectPayIn(**direct_payin_params)
        direct_payin.save()
        self.assertEqual(direct_payin.status, 'SUCCEEDED')

        legal_user_wallet = Wallet.get(self.legal_user_wallet.get_pk())
        self.assertEqual(legal_user_wallet.balance.amount, 9900)

        responses.reset()
        self.mock_legal_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/6784288/refunds',
            'body': {
                "Id": "1632606",
                "Tag": None,
                "CreationDate": 1393421901,
                "AuthorId": "1584635",
                "CreditedUserId": None,
                "DebitedFunds": {
                    "Currency": "EUR",
                    "Amount": 3300
                },
                "CreditedFunds": {
                    "Currency": "EUR",
                    "Amount": 3300
                },
                "Fees": {
                    "Currency": "EUR",
                    "Amount": 0
                },
                "Status": "SUCCEEDED",
                "ResultCode": "000000",
                "ResultMessage": "Success",
                "ExecutionDate": 1393421902,
                "Type": "PAYOUT",
                "Nature": "REFUND",
                "InitialTransactionId": "1632604",
                "InitialTransactionType": "PAYIN",
                "DebitedWalletId": "1584636",
                "CreditedWalletId": None,
                "RefundReason": {
                    "RefusedReasonMessage": None,
                    "RefusedReasonType": "INITIALIZED_BY_CLIENT"
                }
            },
            'status': 200
        })

        params = {
            "author": self.card.user,
            "payin": direct_payin
        }
        payin_refund = PayInRefund(**params)

        self.assertIsNone(payin_refund.get_pk())
        payin_refund.save()
        self.assertIsInstance(payin_refund, PayInRefund)
        self.assertEqual(payin_refund.status, 'SUCCEEDED')

        legal_user_wallet = Wallet.get(self.legal_user_wallet.get_pk())
        self.assertEqual(legal_user_wallet.balance.amount, 0)

        for key, value in params.items():
            self.assertEqual(getattr(payin_refund, key), value)

        self.assertIsNotNone(payin_refund.get_pk())
