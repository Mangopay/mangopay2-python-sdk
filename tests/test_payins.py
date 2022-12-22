# -*- coding: utf-8 -*-
import json
import time
import unittest
from cmath import rect
from datetime import date

import responses

from mangopay.resources import DirectDebitDirectPayIn, Mandate, ApplepayPayIn, GooglepayPayIn, \
    RecurringPayInRegistration, \
    RecurringPayInCIT, PayInRefund, RecurringPayInMIT, CardPreAuthorizedDepositPayIn
from mangopay.utils import (Money, ShippingAddress, Shipping, Billing, Address, SecurityInfo, ApplepayPaymentData,
                            GooglepayPaymentData, DebitedBankAccount, BrowserInfo)

from tests import settings
from tests.resources import (Wallet, PayIn, DirectPayIn, BankWirePayIn, BankWirePayInExternalInstruction, PayPalPayIn,
                             PayconiqPayIn, CardWebPayIn, DirectDebitWebPayIn, constants)
from tests.test_base import BaseTest, BaseTestLive


class PayInsTest(BaseTest):
    # @responses.activate
    # def test_create_direct_payins(self):
    #     self.mock_natural_user()
    #     self.mock_legal_user()
    #     self.mock_user_wallet()
    #     self.mock_card()
    #
    #     self.register_mock([
    #         {
    #             'method': responses.GET,
    #             'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1167495',
    #             'body': {
    #                 "FirstName": "Victor",
    #                 "LastName": "Hugo",
    #                 "Address": {
    #                     "AddressLine1": "AddressLine1",
    #                     "AddressLine2": "AddressLine2",
    #                     "City": "City",
    #                     "Region": "Region",
    #                     "PostalCode": "11222",
    #                     "Country": "FR"
    #                 },
    #                 "Birthday": int(time.mktime(date.today().timetuple())),
    #                 "Nationality": "FR",
    #                 "CountryOfResidence": "FR",
    #                 "Occupation": "Writer",
    #                 "IncomeRange": 6,
    #                 "ProofOfIdentity": None,
    #                 "ProofOfAddress": None,
    #                 "PersonType": "NATURAL",
    #                 "Email": "victor@hugo.com",
    #                 "Id": "1167495",
    #                 "Tag": "custom tag",
    #                 "CreationDate": 1383321421,
    #                 "KYCLevel": "LIGHT"
    #             },
    #             'status': 200
    #         },
    #         {
    #             'method': responses.POST,
    #             'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/card/direct',
    #             'body': {
    #                 "Id": "6784288",
    #                 "Tag": None,
    #                 "CreationDate": 1432046586,
    #                 "AuthorId": "6784285",
    #                 "CreditedUserId": "6784283",
    #                 "DebitedFunds": {"Currency": "EUR", "Amount": 10000},
    #                 "CreditedFunds": {"Currency": "EUR", "Amount": 9900},
    #                 "Fees": {"Currency": "EUR", "Amount": 100},
    #                 "Status": "SUCCEEDED",
    #                 "ResultCode": "000000",
    #                 "ResultMessage": "Success",
    #                 "ExecutionDate": 1432046588,
    #                 "Type": "PAYIN",
    #                 "Nature": "REGULAR",
    #                 "CreditedWalletId": "6784284",
    #                 "DebitedWalletId": None,
    #                 "PaymentType": "CARD",
    #                 "ExecutionType": "DIRECT",
    #                 "SecureMode": "DEFAULT",
    #                 "CardId": "6784287",
    #                 "SecureModeReturnURL": None,
    #                 "SecureModeRedirectURL": None,
    #                 "Culture": "FR",
    #                 "SecureModeNeeded": False
    #             },
    #             'status': 200
    #         },
    #         {
    #             'method': responses.GET,
    #             'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/6784288',
    #             'body': {
    #                 "Id": "6784288",
    #                 "Tag": None,
    #                 "CreationDate": 1432046586,
    #                 "AuthorId": "6784285",
    #                 "CreditedUserId": "6784283",
    #                 "DebitedFunds": {"Currency": "EUR", "Amount": 10000},
    #                 "CreditedFunds": {"Currency": "EUR", "Amount": 9900},
    #                 "Fees": {"Currency": "EUR", "Amount": 100},
    #                 "Status": "SUCCEEDED",
    #                 "ResultCode": "000000",
    #                 "ResultMessage": "Success",
    #                 "ExecutionDate": 1432046588,
    #                 "Type": "PAYIN",
    #                 "Nature": "REGULAR",
    #                 "CreditedWalletId": "6784284",
    #                 "DebitedWalletId": None,
    #                 "PaymentType": "CARD",
    #                 "ExecutionType": "DIRECT",
    #                 "SecureMode": "DEFAULT",
    #                 "CardId": "6784287",
    #                 "SecureModeReturnURL": None,
    #                 "SecureModeRedirectURL": None,
    #                 "SecureModeNeeded": False
    #             },
    #             'status': 200
    #         },
    #         {
    #             'method': responses.GET,
    #             'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets/1169421',
    #             'body': {
    #                 "Owners": ["6784283"],
    #                 "Description": "Wallet of Victor Hugo",
    #                 "Balance": {"Currency": "EUR", "Amount": 9900},
    #                 "Currency": "EUR",
    #                 "Id": "6784284",
    #                 "Tag": "My custom tag",
    #                 "CreationDate": 1432046584
    #             },
    #             'status': 200
    #         }])
    #
    #     direct_payin_params = {
    #         "author": self.card.user,
    #         "debited_funds": Money(amount=10000, currency='EUR'),
    #         "fees": Money(amount=100, currency='EUR'),
    #         "credited_wallet": self.legal_user_wallet,
    #         "card": self.card,
    #         "secure_mode": "DEFAULT",
    #         "secure_mode_return_url": "http://www.ulule.com/",
    #         "culture": "FR",
    #     }
    #     direct_payin = DirectPayIn(**direct_payin_params)
    #
    #     self.assertIsNone(direct_payin.get_pk())
    #     direct_payin.save()
    #     self.assertIsInstance(direct_payin, DirectPayIn)
    #     self.assertEqual(direct_payin.status, 'SUCCEEDED')
    #     self.assertEqual(direct_payin.secure_mode_needed, False)
    #
    #     self.assertEqual(direct_payin.secure_mode_return_url, None)
    #     direct_payin_params.pop('secure_mode_return_url')
    #
    #     self.assertEqual(direct_payin.debited_funds.amount, 10000)
    #     direct_payin_params.pop('debited_funds')
    #
    #     self.assertEqual(direct_payin.fees.amount, 100)
    #     direct_payin_params.pop('fees')
    #
    #     for key, value in direct_payin_params.items():
    #         self.assertEqual(getattr(direct_payin, key), value)
    #
    #     self.assertIsNotNone(direct_payin.get_pk())
    #
    #     # test_retrieve_payins
    #     payin = PayIn.get(direct_payin.get_pk())
    #
    #     self.assertIsNotNone(payin.get_pk())
    #     self.assertIsInstance(payin, PayIn)
    #
    #     self.assertEqual(getattr(payin, 'id'), direct_payin.get_pk())
    #     self.assertEqual(getattr(payin, 'culture'), direct_payin.culture)
    #
    #     legal_user_wallet = Wallet.get(self.legal_user_wallet.get_pk())
    #     self.assertEqual(legal_user_wallet.balance.amount, 9900)

    @responses.activate
    def test_create_bank_wire_payins(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/bankwire/direct',
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
                    "IBAN": "BNPAFRPP",
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
    def test_get_bank_wire_external_instructions_iban(self):
        debited_bank_account_params = {
                    "owner_name": None,
                    "account_number": None,
                    "iban": "1234567",
                    "bic": None,
                    "type": "IBAN",
                    "country": None
                }
        debited_bank_account = DebitedBankAccount(**debited_bank_account_params)
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/74980101',
            'body': {
                "CreditedUserId": "3171114",
                "AuthorId": "3171114",
                "CreditedWalletId": "3171115",
                "DebitedBankAccount": debited_bank_account_params,
                "BankingAliasId": "3174533",
                "Type": "PAYIN",
                "Status": "SUCCEEDED",
                "ResultCode": "000000",
                "ResultMessage": "Success",
                "Nature": "REGULAR",
                "CreationDate": 1499440747,
                "ExecutionDate": 1499440749,
                "WireReference": "feadza",
                "PaymentType": "BANK_WIRE",
                "ExecutionType": "EXTERNAL_INSTRUCTION",
                "DebitedWalletId": None,
                "Fees": {
                    "Currency": "EUR",
                    "Amount": 0
                },
                "DebitedFunds": {
                    "Currency": "EUR",
                    "Amount": 1000
                },
                "CreditedFunds": {
                    "Currency": "EUR",
                    "Amount": 1000
                },
                "Id": "3174534",
                "Tag": None
            },
            'status': 200
        })

        self.assertIsNone(debited_bank_account.account_number)
        self.assertIsNotNone(debited_bank_account.iban)
        self.assertIs(debited_bank_account.type, "IBAN")

    @responses.activate
    def test_get_bank_wire_external_instructions_account_number(self):
        debited_bank_account_params = {
            "owner_name": None,
            "account_number": "1234567",
            "iban": None,
            "bic": None,
            "type": "OTHER"
        }
        debited_bank_account = DebitedBankAccount(**debited_bank_account_params)
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/74980101',
            'body': {
                "CreditedUserId": "3171114",
                "AuthorId": "3171114",
                "CreditedWalletId": "3171115",
                "DebitedBankAccount": debited_bank_account_params,
                "BankingAliasId": "3174533",
                "Type": "PAYIN",
                "Status": "SUCCEEDED",
                "ResultCode": "000000",
                "ResultMessage": "Success",
                "Nature": "REGULAR",
                "CreationDate": 1499440747,
                "ExecutionDate": 1499440749,
                "WireReference": "feadza",
                "PaymentType": "BANK_WIRE",
                "ExecutionType": "EXTERNAL_INSTRUCTION",
                "DebitedWalletId": None,
                "Fees": {
                    "Currency": "EUR",
                    "Amount": 0
                },
                "DebitedFunds": {
                    "Currency": "EUR",
                    "Amount": 1000
                },
                "CreditedFunds": {
                    "Currency": "EUR",
                    "Amount": 1000
                },
                "Id": "3174534",
                "Tag": None
            },
            'status': 200
        })

        self.assertIsNone(debited_bank_account.iban)
        self.assertIsNotNone(debited_bank_account.account_number)
        self.assertIs(debited_bank_account.type, "OTHER")

    @responses.activate
    def test_create_paypal_payin(self):

        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/paypal/web',
            'body': {
                "Id": "117609",
                "CreationDate": 1387805409,
                "Tag": "Custom data",
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
                "DebitedWalletId": None,
                "CreditedWalletId": "95898",
                "CreditedUserId": "95897",
                "AuthorId": "95897",
                "Nature": "REGULAR",
                "Status": "CREATED",
                "ResultCode": None,
                "ResultMessage": None,
                "ExecutionDate": None,
                "Type": "PAYIN",
                "PaymentType": "PAYPAL",
                "ExecutionType": "DIRECT",
                "ReturnURL": "http://www.ulule.com/?transactionId=1169430",
                "RedirectURL": "https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token=EC-68L249465R9617720",
                "ShippingAddress": {
                    "RecipientName": "Unittests User",
                    "Address": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    }
                }
            },
            'status': 200
        })

        shipping_address = ShippingAddress(recipient_name="Unittests User",
                                           address={"AddressLine1": "AddressLine1", "AddressLine2": "AddressLine2",
                                                    "City": "City", "Region": "Region", "PostalCode": "11222",
                                                    "Country": "FR"})
        paypal_payin_params = {
            "author": self.natural_user,
            "debited_funds": Money(amount=1000, currency='EUR'),
            "fees": Money(amount=100, currency="EUR"),
            "return_url": "http://www.ulule.com/",
            "credited_wallet": self.legal_user_wallet,
            "shipping_address": shipping_address
        }

        paypal_payin = PayPalPayIn(**paypal_payin_params)

        self.assertIsNone(paypal_payin.get_pk())
        paypal_payin.save()
        self.assertIsInstance(paypal_payin, PayPalPayIn)
        self.assertEqual(paypal_payin.status, 'CREATED')
        self.assertEqual(paypal_payin.type, 'PAYIN')
        self.assertEqual(paypal_payin.payment_type, 'PAYPAL')
        self.assertIsNotNone(paypal_payin.get_pk())
        self.assertTrue(paypal_payin.redirect_url.startswith(
            'https://www.sandbox.paypal.com/cgi-bin/webscr?cmd=_express-checkout&token'))

        self.assertTrue(paypal_payin.return_url.startswith('http://www.ulule.com/?transactionId='))
        paypal_payin_params.pop('return_url')

        self.assertEqual(paypal_payin.debited_funds.amount, 1000)
        paypal_payin_params.pop('debited_funds')

        self.assertEqual(paypal_payin.fees.amount, 100)
        paypal_payin_params.pop('fees')

        for key, value in paypal_payin_params.items():
            self.assertEqual(getattr(paypal_payin, key), value)

    @responses.activate
    def test_create_payoniq_payin(self):

        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/payconiq/web',
            'body': {
               "Id": "119683174",
               "Tag": "custom meta",
               "CreationDate" :1632985748,
               "ExpirationDate" :1632986949,
               "AuthorId": "119683166",
               "CreditedUserId": "119683166",
               "DebitedFunds": {
                  "Currency": "EUR",
                  "Amount": 22
               },
               "CreditedFunds": {
                  "Currency": "EUR",
                  "Amount": 12
               },
               "Fees": {
                  "Currency": "EUR",
                  "Amount": 10
               },
               "Status": "CREATED",
               "ResultCode": None,
               "ResultMessage": None,
               "ExecutionDate": None,
               "Type": "PAYIN",
               "Nature": "REGULAR",
               "CreditedWalletId": "119683167",
               "DebitedWalletId": None,
               "PaymentType": "PAYCONIQ",
               "ExecutionType": "WEB",
               "RedirectURL": "https://portal.payconiq.com/qrcode?c=https%3A%2F%2Fpayconiq.com%2Fpay%2F2%2F52e501a43d878e8846470b8f",
               "ReturnURL": "http://www.my-site.com/returnURL",
               "DeepLinkURL": "HTTPS://PAYCONIQ.COM/PAY/2/52E501A43D878E8846470B8F"
            },
            'status': 200
        })

        payconiq_payin_params = {
            "tag": "custom meta",
            "author": self.natural_user,
            "debited_funds": Money(amount=22, currency='EUR'),
            "fees": Money(amount=10, currency="EUR"),
            "return_url": "http://www.my-site.com/returnURL",
            "credited_wallet": self.legal_user_wallet,
            "country": "BE"
        }

        payconiq_payin = PayconiqPayIn(**payconiq_payin_params)

        self.assertIsNone(payconiq_payin.get_pk())
        payconiq_payin.save()
        self.assertIsInstance(payconiq_payin, PayconiqPayIn)
        self.assertEqual(payconiq_payin.status, 'CREATED')
        self.assertEqual(payconiq_payin.type, 'PAYIN')
        self.assertEqual(payconiq_payin.payment_type, 'PAYCONIQ')
        self.assertIsNotNone(payconiq_payin.get_pk())
        self.assertTrue(payconiq_payin.redirect_url.startswith(
            'https://portal.payconiq.com/qrcode'))

        self.assertTrue(payconiq_payin.return_url.startswith('http://www.my-site.com'))

        self.assertTrue(payconiq_payin.deep_link_url.startswith('HTTPS://PAYCONIQ.COM/PAY'))

        self.assertEqual(payconiq_payin.debited_funds.amount, 22)

        self.assertEqual(payconiq_payin.fees.amount, 10)

    @responses.activate
    def test_create_card_via_web_interface_payin(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/card/web',
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
                "PAYLINE": "https://www.mysite.com/payline_template/",
                "PAYLINEV2": "https://www.mysite.com/payline_template/"
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
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/payins/directdebit/web',
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
                "PAYLINE": "https://www.mysite.com/payline_template/",
                "PAYLINEV2": "https://www.mysite.com/payline_template/"

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

    def test_get_paypal_with_account_email(self):
        payin_id = "54088959"
        paypal_buyer_email = "paypal-buyer-user@mangopay.com"
        payin = PayPalPayIn.get(payin_id)

        self.assertIsNotNone(payin, "PayPal pay in is null")
        self.assertEqual(payin.payment_type, "PAYPAL")
        self.assertEqual(payin_id, payin.id)
        self.assertEqual(paypal_buyer_email, payin.buyer_account_email)


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

    def test_PayIns_CardDirect_CreateWithAvs(self):
        user = BaseTestLive.get_john(True)
        debited_wallet = BaseTestLive.get_johns_wallet(True)

        # create wallet
        credited_wallet = Wallet()
        credited_wallet.owners = (user,)
        credited_wallet.currency = 'EUR'
        credited_wallet.description = 'WALLET IN EUR'
        credited_wallet = Wallet(**credited_wallet.save())
        card = BaseTestLive.get_johns_card(True)

        pay_in = DirectPayIn()
        pay_in.author = user
        pay_in.debited_wallet = debited_wallet
        pay_in.credited_wallet = credited_wallet
        pay_in.card = card
        pay_in.fees = Money()
        pay_in.fees.amount = 100
        pay_in.fees.currency = "EUR"
        pay_in.debited_funds = Money()
        pay_in.debited_funds.amount = 1000
        pay_in.debited_funds.currency = "EUR"
        pay_in.secure_mode_return_url = "http://www.example.com/"
        pay_in.ip_address = "2001:0620:0000:0000:0211:24FF:FE80:C12C"
        pay_in.browser_info = BaseTest.get_browser_info()

        address = Address()
        address.address_line_1 = "Big Street"
        address.address_line_2 = "no 2 ap 6"
        address.country = "FR"
        address.city = "Lyon"
        address.postal_code = "68400"
        pay_in.billing = Billing(first_name="John", last_name="Doe", address=address)

        result = pay_in.save()

        self.assertIsNotNone(result)
        security_info = result['security_info']
        self.assertIsNotNone(security_info)
        self.assertIsInstance(security_info, SecurityInfo)
        self.assertEqual(security_info.avs_result, "NO_CHECK")

    def test_RecurringPayment(self):
        user = self.get_john(True)
        wallet = self.get_johns_wallet(True)
        card = BaseTestLive.get_johns_card_3dsecure(True)

        recurring = RecurringPayInRegistration()
        recurring.author = user
        recurring.card = card
        recurring.user = user
        recurring.credited_wallet = wallet
        recurring.first_transaction_fees = Money(1, "EUR")
        recurring.first_transaction_debited_funds = Money(12, "EUR")
        recurring.free_cycles = 0
        address = Address()
        address.address_line_1 = "Big Street"
        address.address_line_2 = "no 2 ap 6"
        address.country = "FR"
        address.city = "Lyon"
        address.postal_code = "68400"
        recurring.billing = Billing(first_name="John", last_name="Doe", address=address)
        recurring.shipping = Shipping(first_name="John", last_name="Doe", address=address)
        recurring.end_date = 1768656033
        recurring.migration = True
        recurring.next_transaction_fees = Money(1, "EUR")
        recurring.next_transaction_debited_funds = Money(12, "EUR")
        result = recurring.save()
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.get('free_cycles'))

        created_recurring = RecurringPayInRegistration.get(result.get('id'))
        self.assertIsNotNone(created_recurring)
        print(created_recurring.id)
        cit = RecurringPayInCIT()
        cit.recurring_payin_registration_id = created_recurring.id
        cit.tag = "custom meta"
        cit.statement_descriptor = "lorem"
        cit.secure_mode_return_url = "http://www.my-site.com/returnurl"
        cit.ip_address = "2001:0620:0000:0000:0211:24FF:FE80:C12C"
        cit.browser_info = BaseTest.get_browser_info()
        cit.debited_funds = Money(12, "EUR")
        cit.fees = Money(1, "EUR")

        created_cit = cit.save()
        self.assertIsNotNone(created_cit)
        cit_id = created_cit.get('id')

        got_cit = RecurringPayInCIT.get(cit_id)
        self.assertIsNotNone(got_cit)
        self.assertIsInstance(got_cit, RecurringPayInCIT)

        mit = RecurringPayInMIT()
        mit.recurring_payin_registration_id = created_recurring.id
        mit.statement_descriptor = "lorem"
        mit.tag = "custom meta"
        mit.debited_funds = Money(10, "EUR")
        mit.fees = Money(1, "EUR")
        created_mit = mit.save()
        self.assertIsNotNone(created_mit)

        got_cit = RecurringPayInCIT.get(cit_id)
        self.assertIsNotNone(got_cit)
        #self.assertIsInstance(got_cit, RecurringPayInCIT)

        params = {
            "author": user,
            "payin": got_cit
        }

        payin_refund = PayInRefund(**params)

        self.assertIsNotNone(payin_refund)
        self.assertIsNone(payin_refund.get_pk())
        payin_refund.save()
        self.assertIsInstance(payin_refund, PayInRefund)
        self.assertEqual(payin_refund.status, 'SUCCEEDED')

        mit_id = created_mit.get('id')
        got_mit = RecurringPayInMIT.get(mit_id)
        self.assertIsNotNone(got_mit)
        self.assertIsInstance(got_mit, RecurringPayInMIT)

        params = {
            "author": user,
            "payin": got_mit
        }

        payin_refund_mit = PayInRefund(**params)

        self.assertIsNotNone(payin_refund_mit)
        self.assertIsNone(payin_refund_mit.get_pk())
        payin_refund_mit.save()
        self.assertIsInstance(payin_refund_mit, PayInRefund)
        self.assertEqual(payin_refund_mit.status, 'SUCCEEDED')

    def test_RecurringPayment_Get(self):
        user = self.get_john(True)
        wallet = self.get_johns_wallet(True)
        card = BaseTestLive.get_johns_card_3dsecure(True)

        recurring = RecurringPayInRegistration()
        recurring.author = user
        recurring.card = card
        recurring.user = user
        recurring.credited_wallet = wallet
        recurring.first_transaction_fees = Money()
        recurring.first_transaction_fees.amount = 1
        recurring.first_transaction_fees.currency = "EUR"
        recurring.first_transaction_debited_funds = Money()
        recurring.first_transaction_debited_funds.amount = 10
        recurring.first_transaction_debited_funds.currency = "EUR"
        address = Address()
        address.address_line_1 = "Big Street"
        address.address_line_2 = "no 2 ap 6"
        address.country = "FR"
        address.city = "Lyon"
        address.postal_code = "68400"
        recurring.billing = Billing(first_name="John", last_name="Doe", address=address)
        recurring.shipping = Shipping(first_name="John", last_name="Doe", address=address)
        result = recurring.save()
        self.assertIsNotNone(result)

        rec_id = result.get("id")

        get = RecurringPayInRegistration.get(rec_id)
        self.assertIsNotNone(get)

    def test_RecurringPayment_Update(self):
        user = self.get_john(True)
        wallet = self.get_johns_wallet(True)
        card = BaseTestLive.get_johns_card_3dsecure(True)

        recurring = RecurringPayInRegistration()
        recurring.author = user
        recurring.card = card
        recurring.user = user
        recurring.credited_wallet = wallet
        recurring.first_transaction_fees = Money()
        recurring.first_transaction_fees.amount = 1
        recurring.first_transaction_fees.currency = "EUR"
        recurring.first_transaction_debited_funds = Money()
        recurring.first_transaction_debited_funds.amount = 10
        recurring.first_transaction_debited_funds.currency = "EUR"
        address = Address()
        address.address_line_1 = "Big Street"
        address.address_line_2 = "no 2 ap 6"
        address.country = "FR"
        address.city = "Lyon"
        address.postal_code = "68400"
        recurring.billing = Billing(first_name="John", last_name="Doe", address=address)
        recurring.shipping = Shipping(first_name="John", last_name="Doe", address=address)
        result = recurring.save()
        self.assertIsNotNone(result)

        rec_id = result.get("id")

        get = RecurringPayInRegistration.get(rec_id)
        self.assertIsNotNone(get)

        params_to_be_updated = {
            "status": "ENDED"
        }

        updated = get.update(get.get_pk(), **params_to_be_updated).execute()
        self.assertIsNotNone(updated)

    def test_ApplePay_Payin(self):
        user = self.get_john(True)
        debited_wallet = self.get_johns_wallet()

        # create wallet
        credited_wallet = Wallet()
        credited_wallet.owners = (user,)
        credited_wallet.currency = 'EUR'
        credited_wallet.description = 'WALLET IN EUR'
        credited_wallet = Wallet(**credited_wallet.save())
        card = BaseTestLive.get_johns_card(True)

        pay_in = ApplepayPayIn()
        pay_in.author = user
        pay_in.credited_user = user
        pay_in.credited_wallet = credited_wallet
        pay_in.fees = Money()
        pay_in.fees.amount = 1
        pay_in.fees.currency = "EUR"
        pay_in.debited_funds = Money()
        pay_in.debited_funds.amount = 199
        pay_in.debited_funds.currency = "EUR"
        payment_data = ApplepayPaymentData()
        payment_data.transaction_id = '061EB32181A2D9CA42AD16031B476EEBAA62A9A095AD660E2759FBA52B51A61'
        payment_data.network = 'VISA'
        payment_data.token_data = "{\"version\":\"EC_v1\",\"data\":\"w4HMBVqNC9ghPP4zncTA\\/0oQAsduERfsx78oxgniynNjZLANTL6+0koEtkQnW\\/K38Zew8qV1GLp+fLHo+qCBpiKCIwlz3eoFBTbZU+8pYcjaeIYBX9SOxcwxXsNGrGLk+kBUqnpiSIPaAG1E+WPT8R1kjOCnGvtdombvricwRTQkGjtovPfzZo8LzD3ZQJnHMsWJ8QYDLyr\\/ZN9gtLAtsBAMvwManwiaG3pOIWpyeOQOb01YcEVO16EZBjaY4x4C\\/oyFLWDuKGvhbJwZqWh1d1o9JT29QVmvy3Oq2JEjq3c3NutYut4rwDEP4owqI40Nb7mP2ebmdNgnYyWfPmkRfDCRHIWtbMC35IPg5313B1dgXZ2BmyZRXD5p+mr67vAk7iFfjEpu3GieFqwZrTl3\\/pI5V8Sxe3SIYKgT5Hr7ow==\",\"signature\":\"MIAGCSqGSIb3DQEHAqCAMIACAQExDzANBglghkgBZQMEAgEFADCABgkqhkiG9w0BBwEAAKCAMIID5jCCA4ugAwIBAgIIaGD2mdnMpw8wCgYIKoZIzj0EAwIwejEuMCwGA1UEAwwlQXBwbGUgQXBwbGljYXRpb24gSW50ZWdyYXRpb24gQ0EgLSBHMzEmMCQGA1UECwwdQXBwbGUgQ2VydGlmaWNhdGlvbiBBdXRob3JpdHkxEzARBgNVBAoMCkFwcGxlIEluYy4xCzAJBgNVBAYTAlVTMB4XDTE2MDYwMzE4MTY0MFoXDTIxMDYwMjE4MTY0MFowYjEoMCYGA1UEAwwfZWNjLXNtcC1icm9rZXItc2lnbl9VQzQtU0FOREJPWDEUMBIGA1UECwwLaU9TIFN5c3RlbXMxEzARBgNVBAoMCkFwcGxlIEluYy4xCzAJBgNVBAYTAlVTMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEgjD9q8Oc914gLFDZm0US5jfiqQHdbLPgsc1LUmeY+M9OvegaJajCHkwz3c6OKpbC9q+hkwNFxOh6RCbOlRsSlaOCAhEwggINMEUGCCsGAQUFBwEBBDkwNzA1BggrBgEFBQcwAYYpaHR0cDovL29jc3AuYXBwbGUuY29tL29jc3AwNC1hcHBsZWFpY2EzMDIwHQYDVR0OBBYEFAIkMAua7u1GMZekplopnkJxghxFMAwGA1UdEwEB\\/wQCMAAwHwYDVR0jBBgwFoAUI\\/JJxE+T5O8n5sT2KGw\\/orv9LkswggEdBgNVHSAEggEUMIIBEDCCAQwGCSqGSIb3Y2QFATCB\\/jCBwwYIKwYBBQUHAgIwgbYMgbNSZWxpYW5jZSBvbiB0aGlzIGNlcnRpZmljYXRlIGJ5IGFueSBwYXJ0eSBhc3N1bWVzIGFjY2VwdGFuY2Ugb2YgdGhlIHRoZW4gYXBwbGljYWJsZSBzdGFuZGFyZCB0ZXJtcyBhbmQgY29uZGl0aW9ucyBvZiB1c2UsIGNlcnRpZmljYXRlIHBvbGljeSBhbmQgY2VydGlmaWNhdGlvbiBwcmFjdGljZSBzdGF0ZW1lbnRzLjA2BggrBgEFBQcCARYqaHR0cDovL3d3dy5hcHBsZS5jb20vY2VydGlmaWNhdGVhdXRob3JpdHkvMDQGA1UdHwQtMCswKaAnoCWGI2h0dHA6Ly9jcmwuYXBwbGUuY29tL2FwcGxlYWljYTMuY3JsMA4GA1UdDwEB\\/wQEAwIHgDAPBgkqhkiG92NkBh0EAgUAMAoGCCqGSM49BAMCA0kAMEYCIQDaHGOui+X2T44R6GVpN7m2nEcr6T6sMjOhZ5NuSo1egwIhAL1a+\\/hp88DKJ0sv3eT3FxWcs71xmbLKD\\/QJ3mWagrJNMIIC7jCCAnWgAwIBAgIISW0vvzqY2pcwCgYIKoZIzj0EAwIwZzEbMBkGA1UEAwwSQXBwbGUgUm9vdCBDQSAtIEczMSYwJAYDVQQLDB1BcHBsZSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTETMBEGA1UECgwKQXBwbGUgSW5jLjELMAkGA1UEBhMCVVMwHhcNMTQwNTA2MjM0NjMwWhcNMjkwNTA2MjM0NjMwWjB6MS4wLAYDVQQDDCVBcHBsZSBBcHBsaWNhdGlvbiBJbnRlZ3JhdGlvbiBDQSAtIEczMSYwJAYDVQQLDB1BcHBsZSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTETMBEGA1UECgwKQXBwbGUgSW5jLjELMAkGA1UEBhMCVVMwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAATwFxGEGddkhdUaXiWBB3bogKLv3nuuTeCN\\/EuT4TNW1WZbNa4i0Jd2DSJOe7oI\\/XYXzojLdrtmcL7I6CmE\\/1RFo4H3MIH0MEYGCCsGAQUFBwEBBDowODA2BggrBgEFBQcwAYYqaHR0cDovL29jc3AuYXBwbGUuY29tL29jc3AwNC1hcHBsZXJvb3RjYWczMB0GA1UdDgQWBBQj8knET5Pk7yfmxPYobD+iu\\/0uSzAPBgNVHRMBAf8EBTADAQH\\/MB8GA1UdIwQYMBaAFLuw3qFYM4iapIqZ3r6966\\/ayySrMDcGA1UdHwQwMC4wLKAqoCiGJmh0dHA6Ly9jcmwuYXBwbGUuY29tL2FwcGxlcm9vdGNhZzMuY3JsMA4GA1UdDwEB\\/wQEAwIBBjAQBgoqhkiG92NkBgIOBAIFADAKBggqhkjOPQQDAgNnADBkAjA6z3KDURaZsYb7NcNWymK\\/9Bft2Q91TaKOvvGcgV5Ct4n4mPebWZ+Y1UENj53pwv4CMDIt1UQhsKMFd2xd8zg7kGf9F3wsIW2WT8ZyaYISb1T4en0bmcubCYkhYQaZDwmSHQAAMYIBizCCAYcCAQEwgYYwejEuMCwGA1UEAwwlQXBwbGUgQXBwbGljYXRpb24gSW50ZWdyYXRpb24gQ0EgLSBHMzEmMCQGA1UECwwdQXBwbGUgQ2VydGlmaWNhdGlvbiBBdXRob3JpdHkxEzARBgNVBAoMCkFwcGxlIEluYy4xCzAJBgNVBAYTAlVTAghoYPaZ2cynDzANBglghkgBZQMEAgEFAKCBlTAYBgkqhkiG9w0BCQMxCwYJKoZIhvcNAQcBMBwGCSqGSIb3DQEJBTEPFw0xOTA1MjMxMTA1MDdaMCoGCSqGSIb3DQEJNDEdMBswDQYJYIZIAWUDBAIBBQChCgYIKoZIzj0EAwIwLwYJKoZIhvcNAQkEMSIEIIvfGVQYBeOilcB7GNI8m8+FBVZ28QfA6BIXaggBja2PMAoGCCqGSM49BAMCBEYwRAIgU01yYfjlx9bvGeC5CU2RS5KBEG+15HH9tz\\/sg3qmQ14CID4F4ZJwAz+tXAUcAIzoMpYSnM8YBlnGJSTSp+LhspenAAAAAAAA\",\"header\":{\"ephemeralPublicKey\":\"MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE0rs3wRpirXjPbFDQfPRdfEzRIZDWm0qn7Y0HB0PNzV1DDKfpYrnhRb4GEhBF\\/oEXBOe452PxbCnN1qAlqcSUWw==\",\"publicKeyHash\":\"saPRAqS7TZ4bAYwzBj8ezDDC55ZolyH1FL+Xc8fd93o=\",\"transactionId\":\"b061eb32181a2d9ca42ad16031b476eebaa62a9a095ad660e2759fba52b51a61\"}}"
        pay_in.payment_data = payment_data
        pay_in.statement_descriptor = 'Python'
        pay_in.payment_type = constants.PAYIN_PAYMENT_TYPE.applepay
        pay_in.execution_type = constants.EXECUTION_TYPE_CHOICES.direct
        result = pay_in.save()
        self.assertIsNotNone(result)

    @unittest.skip("can't be tested yet")
    def test_GooglePay_payIn(self):
        user = self.get_john(True)
        debited_wallet = self.get_johns_wallet()

        # create wallet
        credited_wallet = Wallet()
        credited_wallet.owners = (user,)
        credited_wallet.currency = 'EUR'
        credited_wallet.description = 'WALLET IN EUR'
        credited_wallet = Wallet(**credited_wallet.save())
        card = BaseTestLive.get_johns_card(True)

        pay_in = GooglepayPayIn()
        pay_in.author = user
        pay_in.credited_user = user
        pay_in.credited_wallet = credited_wallet
        pay_in.fees = Money()
        pay_in.fees.amount = 1
        pay_in.fees.currency = "EUR"
        pay_in.debited_funds = Money()
        pay_in.debited_funds.amount = 199
        pay_in.debited_funds.currency = "EUR"
        payment_data = GooglepayPaymentData()
        # can't be tested
        payment_data.transaction_id = "placeholder"
        payment_data.network = 'VISA'
        payment_data.token_data = "placeholder"
        pay_in.payment_data = payment_data
        pay_in.statement_descriptor = 'Python'
        pay_in.payment_type = constants.PAYIN_PAYMENT_TYPE.googlepay
        pay_in.execution_type = constants.EXECUTION_TYPE_CHOICES.direct
        result = pay_in.save()
        self.assertIsNotNone(result)

    @unittest.skip("can't be tested yet")
    def test_card_preauthorized_deposit_payin(self):
        deposit = self.create_new_deposit()

        params = {
            "credited_wallet_id": self.get_johns_wallet().id,
            "debited_funds": Money(amount=1000, currency='EUR'),
            "fees": Money(amount=0, currency='EUR'),
            "deposit_id": deposit.id
        }

        created = CardPreAuthorizedDepositPayIn(**params).save()
        pay_in = CardPreAuthorizedDepositPayIn().get(created.get('id'))

        self.assertIsNotNone(pay_in)
        self.assertEqual("SUCCEEDED", pay_in.status)
        self.assertEqual("REGULAR", pay_in.nature)
        self.assertEqual("DIRECT", pay_in.execution_type)
        self.assertEqual("PREAUTHORIZED", pay_in.payment_type)
        self.assertEqual("PAYIN", pay_in.type)
