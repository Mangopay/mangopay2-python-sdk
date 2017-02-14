# -*- coding: utf-8 -*-
import unittest

from mangopay.resources import DirectDebitDirectPayIn, Mandate
from tests import settings
from .resources import (Wallet, PayIn, DirectPayIn, BankWirePayIn,
                        CardWebPayIn, DirectDebitWebPayIn)
from .test_base import BaseTest, BaseTestLive

from mangopay.utils import Money

from datetime import date

import responses
import time


class PayInsTest(BaseTest):
    @responses.activate
    def test_create_direct_payins(self):
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
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payins/6784288',
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
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169421',
                'body': {
                    "Owners": ["6784283"],
                    "Description":"Wallet of Victor Hugo",
                    "Balance":{"Currency": "EUR", "Amount": 9900},
                    "Currency": "EUR",
                    "Id": "6784284",
                    "Tag": "My custom tag",
                    "CreationDate": 1432046584
                },
                'status': 200
            }])

        direct_payin_params = {
            "author": self.card.user,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "credited_wallet": self.legal_user_wallet,
            "card": self.card,
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "http://www.ulule.com/"
        }
        direct_payin = DirectPayIn(**direct_payin_params)

        self.assertIsNone(direct_payin.get_pk())
        direct_payin.save()
        self.assertIsInstance(direct_payin, DirectPayIn)
        self.assertEqual(direct_payin.status, 'SUCCEEDED')
        self.assertEqual(direct_payin.secure_mode_needed, False)

        self.assertEqual(direct_payin.secure_mode_return_url, None)
        direct_payin_params.pop('secure_mode_return_url')

        self.assertEqual(direct_payin.debited_funds.amount, 10000)
        direct_payin_params.pop('debited_funds')

        self.assertEqual(direct_payin.fees.amount, 100)
        direct_payin_params.pop('fees')

        for key, value in direct_payin_params.items():
            self.assertEqual(getattr(direct_payin, key), value)

        self.assertIsNotNone(direct_payin.get_pk())

        # test_retrieve_payins
        payin = PayIn.get(direct_payin.get_pk())

        self.assertIsNotNone(payin.get_pk())
        self.assertIsInstance(payin, PayIn)

        self.assertEqual(getattr(payin, 'id'), direct_payin.get_pk())

        legal_user_wallet = Wallet.get(self.legal_user_wallet.get_pk())
        self.assertEqual(legal_user_wallet.balance.amount, 9900)

    @responses.activate
    def test_create_bank_wire_payins(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payins/bankwire/direct',
            'body': {
                "Id": "117609",
                "Tag": "Custom data",
                "CreationDate": 1387805409,
                "ResultCode": None,
                "ResultMessage": None,
                "AuthorId": "95897",
                "CreditedUserId": "95897",
                "DebitedFunds": None,
                "CreditedFunds": None,
                "Fees": None,
                "Status": "CREATED",
                "ExecutionDate": None,
                "Type": "PAYIN",
                "Nature": "REGULAR",
                "CreditedWalletId": "95898",
                "DebitedWalletId": None,
                "PaymentType": "BANK_WIRE",
                "ExecutionType": "DIRECT",
                "DeclaredDebitedFunds": {
                    "Currency": "EUR",
                    "Amount": 1000
                },
                "DeclaredFees": {
                    "Currency": "EUR",
                    "Amount": 100
                },
                "WireReference": "071c9ac581",
                "BankAccount": {
                    "Type": "IBAN",
                    "OwnerName": "MangoPay Euro global",
                    "OwnerAddress": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    },
                    "IBAN": "CRLYFRPP",
                    "BIC": "FR70 3000 2005 5000 0015 7845 Z02"
                }
            },
            'status': 200
        })

        bank_wire_payin_params = {
            "author": self.natural_user,
            "tag": "Custom data",
            "credited_user": self.legal_user,
            "credited_wallet": self.legal_user_wallet,
            "declared_debited_funds": Money(amount=1000, currency='EUR'),
            "declared_fees": Money(amount=100, currency='EUR')
        }
        bank_wire_payin = BankWirePayIn(**bank_wire_payin_params)

        self.assertIsNone(bank_wire_payin.get_pk())
        bank_wire_payin.save()
        self.assertIsInstance(bank_wire_payin, BankWirePayIn)
        self.assertEqual(bank_wire_payin.status, 'CREATED')

        self.assertEqual(bank_wire_payin.declared_debited_funds.amount, 1000)
        bank_wire_payin_params.pop('declared_debited_funds')

        self.assertEqual(bank_wire_payin.declared_fees.amount, 100)
        bank_wire_payin_params.pop('declared_fees')

        for key, value in bank_wire_payin_params.items():
            self.assertEqual(getattr(bank_wire_payin, key), value)

        self.assertIsNotNone(bank_wire_payin.get_pk())

    @responses.activate
    def test_create_card_via_web_interface_payin(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payins/card/web',
            'body': {
                "Id": "1169430",
                "Tag": "Custom tag",
                "CreationDate": 1383467581,
                "AuthorId": "1167492",
                "CreditedUserId": "1167495",
                "DebitedFunds": {
                    "Currency": "EUR",
                    "Amount": 10000
                },
                "CreditedFunds": {
                    "Currency": "EUR",
                    "Amount": 900
                },
                "Fees": {
                    "Currency": "EUR",
                    "Amount": 100
                },
                "Status": "CREATED",
                "ResultCode": None,
                "ResultMessage": None,
                "ExecutionDate": None,
                "Type": "PAYIN",
                "Nature": "REGULAR",
                "CreditedWalletId": "1167496",
                "DebitedWalletId": None,
                "PaymentType": "CARD",
                "ExecutionType": "WEB",
                "RedirectURL": "https://homologation-secure-p.payline.com/webpayment/?reqCode=prepareStep2&stepCode=step2&token=1b4VBuRxmwWCYYw81Er51383467582768",
                "ReturnURL": "http://www.ulule.com/?transactionId=1169430",
                "TemplateURL": "https://www.ulule.com/payline_template/?transactionId=1169430",
                "Culture": "FR",
                "SecureMode": "DEFAULT"
            },
            'status': 200
        })

        params = {
            "author": self.natural_user,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "credited_wallet": self.legal_user_wallet,
            "return_url": "http://www.ulule.com/",
            "template_url_options": {
                "PAYLINE": "https://www.mysite.com/payline_template/"
            },
            "culture": "FR",
            "card_type": "CB_VISA_MASTERCARD",
            "secure_mode": "DEFAULT"
        }
        card_payin = CardWebPayIn(**params)

        self.assertIsNone(card_payin.get_pk())
        card_payin.save()
        self.assertIsInstance(card_payin, CardWebPayIn)

        self.assertTrue(card_payin.return_url.startswith('http://www.ulule.com/?transactionId='))
        params.pop('return_url')

        self.assertEqual(card_payin.debited_funds.amount, 10000)
        params.pop('debited_funds')

        self.assertEqual(card_payin.fees.amount, 100)
        params.pop('fees')

        for key, value in params.items():
            self.assertEqual(getattr(card_payin, key), value)

        self.assertIsNotNone(card_payin.get_pk())
        self.assertEqual(card_payin.status, 'CREATED')

    @responses.activate
    def test_create_direct_debit_via_web_interface_payin(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payins/directdebit/web',
            'body': {
                "Id": "1169430",
                "Tag": "Custom tag",
                "CreationDate": 1383467581,
                "AuthorId": "1167492",
                "CreditedUserId": "1167495",
                "DebitedFunds": {
                    "Currency": "EUR",
                    "Amount": 10000
                },
                "CreditedFunds": {
                    "Currency": "EUR",
                    "Amount": 900
                },
                "Fees": {
                    "Currency": "EUR",
                    "Amount": 100
                },
                "Status": "CREATED",
                "ResultCode": None,
                "ResultMessage": None,
                "ExecutionDate": None,
                "Type": "PAYIN",
                "Nature": "REGULAR",
                "CreditedWalletId": "1167496",
                "DebitedWalletId": None,
                "PaymentType": "DIRECT_DEBIT",
                "ExecutionType": "WEB",
                "RedirectURL": "https://homologation-secure-p.payline.com/webpayment/?reqCode=prepareStep2&stepCode=step2&token=1b4VBuRxmwWCYYw81Er51383467582768",
                "ReturnURL": "http://www.ulule.com/?transactionId=1169430",
                "TemplateURL": "https://www.ulule.com/payline_template/?transactionId=1169430",
                "Culture": "FR",
                "DirectDebitType": "GIROPAY"
            },
            'status': 200
        })

        params = {
            "author": self.natural_user,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "credited_wallet": self.legal_user_wallet,
            "return_url": "http://www.ulule.com/",
            "template_url_options": {
                "PAYLINE": "https://www.mysite.com/payline_template/"
            },
            "culture": "FR",
            "direct_debit_type": "GIROPAY"
        }
        card_payin = DirectDebitWebPayIn(**params)

        self.assertIsNone(card_payin.get_pk())
        card_payin.save()
        self.assertIsInstance(card_payin, DirectDebitWebPayIn)

        self.assertTrue(card_payin.return_url.startswith('http://www.ulule.com/?transactionId='))
        params.pop('return_url')

        self.assertEqual(card_payin.debited_funds.amount, 10000)
        params.pop('debited_funds')

        self.assertEqual(card_payin.fees.amount, 100)
        params.pop('fees')

        for key, value in params.items():
            self.assertEqual(getattr(card_payin, key), value)

        self.assertIsNotNone(card_payin.get_pk())
        self.assertEqual(card_payin.status, 'CREATED')
        self.assertEqual(card_payin.payment_type, 'DIRECT_DEBIT')

    def test_using_api_names_as_payin_attributes(self):
        payin = BankWirePayIn(
            AuthorId=1,
            declared_debited_funds=Money(100, 'EUR'),
            DeclaredFees=Money(1, 'EUR'),
            credited_wallet=Wallet(Id=1),
        )
        self.assertEqual(payin.AuthorId, 1)
        self.assertIs(payin.declared_debited_funds, payin.DeclaredDebitedFunds)
        self.assertIs(payin.DeclaredFees, payin.declared_fees)
        self.assertEqual(payin.credited_wallet.id, payin.CreditedWalletId)
        payin.Tag = 'x'
        self.assertIs(payin.Tag, payin.tag)


class PayInsTestLive(BaseTestLive):
    @unittest.skip('Set a breakpoint after creating the mandate, navigate to mandate.redirect_url and confirm')
    def test_PayIns_DirectDebitDirect_Create(self):
        # create wallet
        wallet = Wallet()
        wallet.owners = (BaseTestLive.get_john(),)
        wallet.currency = 'EUR'
        wallet.description = 'WALLET IN EUR'
        wallet = Wallet(**wallet.save())

        mandate = Mandate()
        mandate.bank_account_id = BaseTestLive.get_johns_account().id
        mandate.return_url = 'http://test.test'
        mandate.culture = 'FR'
        mandate = Mandate(**mandate.save())

        #       ! IMPORTANT NOTE !
        #       In order to make this test pass, at this place you have to set a breakpoint,
        #       navigate to URL the mandate.RedirectURL property points to and click "CONFIRM" button.

        post = DirectDebitDirectPayIn()
        post.author = BaseTestLive.get_john()
        post.credited_wallet = wallet
        post.debited_funds = Money('1000', 'EUR')
        post.fees = Money('0', 'EUR')
        post.mandate = mandate

        result = post.save()

        self.assertIsNotNone(result)
        self.assertFalse('FAILED' == result['status'],
                         'In order to make this test pass, after creating mandate and before creating the payin you have\
                          to navigate to URL the mandate.redirect_url property points to and click CONFIRM button.')
        self.assertTrue(result['id'])
        self.assertEqual(wallet.id, result['credited_wallet_id'])
        self.assertEqual('DIRECT_DEBIT', result['payment_type'])
        self.assertEqual('DIRECT', result['execution_type'])
        self.assertEqual(BaseTestLive.get_john().id, result['author_id'])
        self.assertEqual('CREATED', result['status'])
        self.assertEqual('PAYIN', result['type'])
        self.assertIsNotNone(result['mandate_id'])
        self.assertEqual(mandate.id, result['mandate_id'])
