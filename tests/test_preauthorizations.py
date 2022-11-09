# -*- coding: utf-8 -*-
from tests import settings
from tests.resources import (PreAuthorization, PreAuthorizedPayIn, CardRegistration, Card)
from tests.test_base import BaseTest, BaseTestLive

try:
    import urllib.parse as urlrequest
except ImportError:
    import urllib as urlrequest

from mangopay.utils import Money, Billing, Address, SecurityInfo

from datetime import date

import requests
import responses
import time


class PreAuthorizationsTest(BaseTest):
    @responses.activate
    def test_create_preauthorization(self):
        self.mock_natural_user()
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
                    "Id": "1169419",
                    "Tag": "custom tag",
                    "CreationDate": 1383321421,
                    "KYCLevel": "LIGHT"
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/card/direct',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 10000
                    },
                    "RemainingFunds": {
                        "Currency": "EUR",
                        "Amount": 500
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "WAITING",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "DEFAULT",
                    "CardId": "1208983",
                    "SecureModeReturnURL": None,
                    "SecureModeRedirectURL": "https://api-test.mangopay.com:443/Redirect/ACSWithoutValidation?token=8139ca555fd74fbbba14a50b7151a3e9",
                    "SecureModeNeeded": True,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/1209003',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "RemainingFunds": {
                        "Currency": "EUR",
                        "Amount": 500
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "CREATED",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "FORCE",
                    "CardId": "1208983",
                    "SecureModeReturnURL": "https://www.mysite.com/secure?preAuthorizationId=1209003",
                    "SecureModeRedirectURL": "https://api-test.mangopay.com:443/Redirect/ACSWithoutValidation?token=8139ca555fd74fbbba14a50b7151a3e9",
                    "SecureModeNeeded": None,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.PUT,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/1209003',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "RemainingFunds": {
                        "Currency": "EUR",
                        "Amount": 500
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "CANCELED",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "FORCE",
                    "CardId": "1208983",
                    "SecureModeReturnURL": "https://www.mysite.com/secure?preAuthorizationId=1209003",
                    "SecureModeRedirectURL": "https://api-test.mangopay.com:443/Redirect/ACSWithoutValidation?token=8139ca555fd74fbbba14a50b7151a3e9",
                    "SecureModeNeeded": None,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.PUT,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/1209003',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "RemainingFunds": {
                        "Currency": "EUR",
                        "Amount": 500
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "CREATED",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "FORCE",
                    "CardId": "1208983",
                    "SecureModeReturnURL": "https://www.mysite.com/secure?preAuthorizationId=1209003",
                    "SecureModeRedirectURL": "https://api-test.mangopay.com:443/Redirect/ACSWithoutValidation?token=8139ca555fd74fbbba14a50b7151a3e9",
                    "SecureModeNeeded": None,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/1209003',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 1000
                    },
                    "RemainingFunds": {
                        "Currency": "EUR",
                        "Amount": 500
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "CREATED",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "FORCE",
                    "CardId": "1208983",
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            }])

        params = {
            "author": self.card.user,
            "card": self.card,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "remaining_funds": Money(amount=500, currency='EUR'),
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "http://www.ulule.com/",
            "requested_3ds_version": "V1"
        }
        preauthorization = PreAuthorization(**params)

        self.assertIsNone(preauthorization.get_pk())
        preauthorization.save()
        self.assertIsInstance(preauthorization, PreAuthorization)

        self.assertEqual(preauthorization.status, 'SUCCEEDED')
        self.assertEqual(preauthorization.payment_status, 'WAITING')

        self.assertEqual(preauthorization.secure_mode_return_url, None)
        params.pop('secure_mode_return_url')

        self.assertEqual(preauthorization.debited_funds.amount, 10000)
        params.pop('debited_funds')

        for key, value in params.items():
            self.assertEqual(getattr(preauthorization, key), value)

        self.assertIsNotNone(preauthorization.get_pk())
        self.assertIsNotNone(preauthorization.remaining_funds)

        # Test update
        previous_pk = preauthorization.get_pk()

        preauthorization.payment_status = 'CANCELED'
        preauthorization.save()

        self.assertEqual(previous_pk, preauthorization.get_pk())

        self.assertEqual(preauthorization.payment_status, 'CANCELED')

    @responses.activate
    def test_retrieve_preauthorization(self):
        self.mock_natural_user()
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
                    "KYCLevel": "LIGHT",
                    "IpAdress": "2001:0620:0000:0000:0211:24FF:FE80:C12C"
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/card/direct',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 10000
                    },
                    "RemainingFunds": {
                        "Currency": "EUR",
                        "Amount": 500
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "WAITING",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "DEFAULT",
                    "CardId": "1208983",
                    "SecureModeRedirectURL": "https://api.sandbox.mangopay.com:443/Redirect/ACSWithoutValidation?token=8139ca555fd74fbbba14a50b7151a3e9",
                    "SecureModeNeeded": True,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/1209003',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1167495",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 10000
                    },
                    "RemainingFunds": {
                        "Currency": "EUR",
                        "Amount": 500
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "CREATED",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "DEFAULT",
                    "CardId": "1208983",
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/1209004',
                'body': {"errors": []},
                'status': 404
            }])

        params = {
            "author": self.card.user,
            "card": self.card,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "remaining_funds": Money(amount=500, currency='EUR'),
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "https://www.mysite.com/secure?preAuthorizationId=1209003"
        }
        preauthorization = PreAuthorization(**params)
        preauthorization.save()

        self.assertRaises(PreAuthorization.DoesNotExist, PreAuthorization.get, int(preauthorization.get_pk()) + 1)

        self.assertIsNotNone(preauthorization.get_pk())

        preauthorization = PreAuthorization.get(preauthorization.get_pk())

        self.assertIsNotNone(preauthorization.get_pk())
        self.assertIsNotNone(preauthorization.remaining_funds)

        self.assertEqual(preauthorization.secure_mode_return_url, None)
        params.pop('secure_mode_return_url')

        self.assertEqual(preauthorization.debited_funds.amount, 10000)
        params.pop('debited_funds')

        for key, value in params.items():
            self.assertEqual(getattr(preauthorization, key), value)

    @responses.activate
    def test_create_succeeded_preauthorized_payin(self):
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
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/card/direct',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 10000
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "WAITING",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "DEFAULT",
                    "CardId": "1208983",
                    "SecureModeRedirectURL": "https://api-test.mangopay.com:443/Redirect/ACSWithoutValidation?token=8139ca555fd74fbbba14a50b7151a3e9",
                    "SecureModeNeeded": True,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payins/PreAuthorized/direct',
                'body': {
                    "Id": "1209008",
                    "Tag": None,
                    "CreationDate": 1388653621,
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "AuthorId": "1208974",
                    "CreditedUserId": "1208974",
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
                    "Status": "SUCCEEDED",
                    "ExecutionDate": 1388653622,
                    "Type": "PAYIN",
                    "Nature": "REGULAR",
                    "CreditedWalletId": "1208991",
                    "DebitedWalletId": None,
                    "PaymentType": "PREAUTHORIZED",
                    "ExecutionType": "DIRECT",
                    "PreauthorizationId": "1209003"
                },
                'status': 200
            }])

        params = {
            "author": self.card.user,
            "card": self.card,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "remaining_funds": Money(amount=500, currency='EUR'),
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "https://www.mysite.com/secure?preAuthorizationId=1209003"
        }
        preauthorization = PreAuthorization(**params)
        preauthorization.save()

        params = {
            "author": self.card.user,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "fees": Money(amount=1, currency='EUR'),
            "credited_wallet": self.legal_user_wallet,
            "preauthorization": preauthorization,
            "secure_mode_return_url": "https://www.mysite.com/secure?preAuthorizationId=1209003"
        }
        preauthorized_payin = PreAuthorizedPayIn(**params)

        self.assertIsNone(preauthorized_payin.get_pk())
        preauthorized_payin.save()
        self.assertIsInstance(preauthorized_payin, PreAuthorizedPayIn)

        self.assertTrue(preauthorized_payin.secure_mode_return_url, "https://www.mysite.com/secure?preAuthorizationId=")
        params.pop('secure_mode_return_url')

        self.assertEqual(preauthorized_payin.debited_funds.amount, 10000)
        params.pop('debited_funds')

        self.assertEqual(preauthorized_payin.fees.amount, 100)
        params.pop('fees')

        for key, value in params.items():
            self.assertEqual(getattr(preauthorized_payin, key), value)

        self.assertIsNotNone(preauthorized_payin.get_pk())
        self.assertEqual(preauthorized_payin.status, 'SUCCEEDED')
        self.assertEqual(preauthorized_payin.payment_type, 'PREAUTHORIZED')

    @responses.activate
    def test_create_failed_preauthorized_payin(self):
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
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/preauthorizations/card/direct',
                'body': {
                    "Id": "1209003",
                    "Tag": None,
                    "CreationDate": 1388653234,
                    "AuthorId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 10000
                    },
                    "AuthorizationDate": 1388653377,
                    "Status": "SUCCEEDED",
                    "PaymentStatus": "WAITING",
                    "ExpirationDate": 1389258177,
                    "PayInId": "1209008",
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "SecureMode": "DEFAULT",
                    "CardId": "1208983",
                    "SecureModeRedirectURL": "https://api-test.mangopay.com:443/Redirect/ACSWithoutValidation?token=8139ca555fd74fbbba14a50b7151a3e9",
                    "SecureModeNeeded": True,
                    "PaymentType": "CARD",
                    "ExecutionType": "DIRECT"
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payins/PreAuthorized/direct',
                'body': {
                    "Id": "1209008",
                    "Tag": None,
                    "CreationDate": 1388653621,
                    "ResultCode": "000000",
                    "ResultMessage": "Success",
                    "AuthorId": "1208974",
                    "CreditedUserId": "1208974",
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 30000
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": 900
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": 100
                    },
                    "Status": "FAILED",
                    "ExecutionDate": 1388653622,
                    "Type": "PAYIN",
                    "Nature": "REGULAR",
                    "CreditedWalletId": "1208991",
                    "DebitedWalletId": None,
                    "PaymentType": "PREAUTHORIZED",
                    "ExecutionType": "DIRECT",
                    "PreauthorizationId": "1209003"
                },
                'status': 200
            }])

        params = {
            "author": self.card.user,
            "card": self.card,
            "debited_funds": Money(amount=10000, currency='EUR'),
            "remaining_funds": Money(amount=500, currency='EUR'),
            "secure_mode": "DEFAULT",
            "secure_mode_return_url": "http://www.ulule.com/"
        }
        preauthorization = PreAuthorization(**params)
        preauthorization.save()

        self.assertEqual(preauthorization.status, 'SUCCEEDED')
        self.assertEqual(preauthorization.payment_status, 'WAITING')

        params = {
            "author": self.card.user,
            "debited_funds": Money(amount=30000, currency='EUR'),  # Amount is too high
            "fees": Money(amount=1, currency='EUR'),
            "credited_wallet": self.legal_user_wallet,
            "preauthorization": preauthorization,
            "secure_mode_url": "http://www.ulule.com/"
        }
        preauthorized_payin = PreAuthorizedPayIn(**params)
        preauthorized_payin.save()

        self.assertEqual(preauthorized_payin.status, 'FAILED')
        self.assertEqual(preauthorized_payin.payment_type, 'PREAUTHORIZED')


class PreAuthorizationsTestLive(BaseTestLive):

    def test_PreAuthorizations_CreateWithAvs(self):
        user = BaseTestLive.get_john()
        card_registration = CardRegistration()
        card_registration.user = user
        card_registration.currency = "EUR"

        saved_registration = card_registration.save()
        data = {
            'cardNumber': '4970105191923460',
            'cardCvx': '123',
            'cardExpirationDate': '1224',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        registration_data_response = requests.post(card_registration.card_registration_url, data=data, headers=headers)
        saved_registration['registration_data'] = registration_data_response.text
        updated_registration = CardRegistration(**saved_registration).save()

        card = Card.get(updated_registration['card_id'])
        pre_authorization = PreAuthorization()
        pre_authorization.card = card
        pre_authorization.author = user
        pre_authorization.debited_funds = Money()
        pre_authorization.debited_funds.currency = "EUR"
        pre_authorization.debited_funds.amount = 100
        pre_authorization.remaining_funds = Money()
        pre_authorization.remaining_funds.currency = "EUR"
        pre_authorization.remaining_funds.amount = 100
        pre_authorization.secure_mode_return_url = "http://www.example.com/"
        pre_authorization.ip_address = "2001:0620:0000:0000:0211:24FF:FE80:C12C"
        pre_authorization.browser_info = BaseTest.get_browser_info()

        billing = Billing()
        billing.address = Address()
        billing.address.address_line_1 = "Main Street"
        billing.address.address_line_2 = "no. 5 ap. 6"
        billing.address.country = "FR"
        billing.address.city = "Lyon"
        billing.address.postal_code = "65400"
        billing.last_name = "Doe"
        billing.first_name = "John"
        pre_authorization.billing = billing

        saved_pre_authorization = pre_authorization.save()

        self.assertIsNotNone(saved_pre_authorization)
        security_info = saved_pre_authorization['security_info']
        self.assertIsInstance(security_info, SecurityInfo)
        self.assertEqual(security_info.avs_result, "NO_CHECK")

    def test_PreAuthorizations_CreateDirect(self):
        user = BaseTestLive.get_john()
        card_registration = CardRegistration()
        card_registration.user = user
        card_registration.currency = "EUR"

        saved_registration = card_registration.save()
        data = {
            'cardNumber': '4970105191923460',
            'cardCvx': '123',
            'cardExpirationDate': '1224',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        registration_data_response = requests.post(card_registration.card_registration_url, data=data, headers=headers)
        saved_registration['registration_data'] = registration_data_response.text
        updated_registration = CardRegistration(**saved_registration).save()

        card = Card.get(updated_registration['card_id'])
        pre_authorization = PreAuthorization()
        pre_authorization.card = card
        pre_authorization.author = user
        pre_authorization.debited_funds = Money()
        pre_authorization.debited_funds.currency = "EUR"
        pre_authorization.debited_funds.amount = 500
        pre_authorization.remaining_funds = Money()
        pre_authorization.remaining_funds.currency = "EUR"
        pre_authorization.remaining_funds.amount = 500
        pre_authorization.secure_mode_return_url = "http://www.example.com/"
        pre_authorization.ip_address = "2001:0620:0000:0000:0211:24FF:FE80:C12C"
        pre_authorization.browser_info = BaseTest.get_browser_info()

        billing = Billing()
        billing.address = Address()
        billing.address.address_line_1 = "Main Street"
        billing.address.address_line_2 = "no. 5 ap. 6"
        billing.address.country = "FR"
        billing.address.city = "Lyon"
        billing.address.postal_code = "65400"
        billing.last_name = "Doe"
        billing.first_name = "John"
        pre_authorization.billing = billing

        saved_pre_authorization = pre_authorization.save()

        wallet = BaseTestLive.get_johns_wallet()

        payin = PreAuthorizedPayIn()
        payin.author = BaseTestLive.get_john()
        payin.debited_funds = Money(amount=500, currency='EUR')
        payin.credited_wallet = wallet
        payin.secure_mode_return_url = "http://test.com"
        payin.secure_mode = 'DEFAULT'
        payin.preauthorization = pre_authorization
        payin.fees = Money(amount=0, currency='EUR')
        payin.culture = 'fr'
        BaseTestLive._johns_payin = PreAuthorizedPayIn(**payin.save())

        transactions = pre_authorization.get_transactions()

        self.assertIsNotNone(saved_pre_authorization)
        security_info = saved_pre_authorization['security_info']
        self.assertIsInstance(security_info, SecurityInfo)
        self.assertEqual(security_info.avs_result, "NO_CHECK")
        self.assertEqual(payin.status, "SUCCEEDED")
        self.assertEqual(transactions[0].status, "SUCCEEDED")
