# -*- coding: utf-8 -*-
from mangopay.utils import Address
from tests import settings
from tests.resources import BankAccount
from tests.test_base import BaseTest, BaseTestLive

from datetime import date

import responses
import time


class BankAccountsTest(BaseTest):
    @responses.activate
    def test_create_bankaccount_iban(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/IBAN',
            'body': {
                "UserId": "1169419",
                "Type": "IBAN",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": {
                    "AddressLine1": "AddressLine1",
                    "AddressLine2": "AddressLine2",
                    "City": "City",
                    "Region": "Region",
                    "PostalCode": "11222",
                    "Country": "FR"
                },
                "IBAN": "FR7630004000031234567890143",
                "BIC": "BNPAFRPP",
                "Id": "1169675",
                "Tag": "custom tag",
                "CreationDate": 1383561267
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "IBAN",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "iban": "FR7630004000031234567890143",
            "bic": "BNPAFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_gb(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/GB',
            'body': {
                "UserId": "1169419",
                "Type": "GB",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": {
                    "AddressLine1": "AddressLine1",
                    "AddressLine2": "AddressLine2",
                    "City": "City",
                    "Region": "Region",
                    "PostalCode": "11222",
                    "Country": "FR"
                },
                "AccountNumber": "62136016",
                "SortCode": "404865",
                "Id": "38290008",
                "Tag": "custom tag",
                "CreationDate": 1383561267
            },
            'status': 200
        })

        params = {
            "tag": "custom tag",
            "user": self.natural_user,
            "type": "GB",
            "owner_name": "Victor Hugo",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "account_number": "62136016",
            "sort_code": "404865"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_us(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/US',
            'body': {
                "UserId": "1169419",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": {
                    "AddressLine1": "AddressLine1",
                    "AddressLine2": "AddressLine2",
                    "City": "City",
                    "Region": "Region",
                    "PostalCode": "11222",
                    "Country": "FR"
                },
                "Type": "US",
                "Id": "6775383",
                "Tag": "custom tag",
                "CreationDate": 1431964711,
                "AccountNumber": "123",
                "ABA": "123456789",
                "DepositAccountType": "CHECKING"
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "US",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "tag": "custom tag",
            "account_number": "123",
            "aba": "123456789",
            "deposit_account_type": "CHECKING"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_ca(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/CA',
            'body': {
                "UserId": "1169419",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": {
                    "AddressLine1": "AddressLine1",
                    "AddressLine2": "AddressLine2",
                    "City": "City",
                    "Region": "Region",
                    "PostalCode": "11222",
                    "Country": "FR"
                },
                "Type": "CA",
                "Id": "6775449",
                "Tag": "custom tag",
                "CreationDate": 1431964854,
                "AccountNumber": "123",
                "InstitutionNumber": "1234",
                "BranchCode": "12345",
                "BankName": "banque nationale of canada"
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "CA",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "tag": "custom tag",
            "bank_name": "banque nationale of canada",
            "institution_number": "1234",
            "branch_code": "12345",
            "account_number": "123"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_create_bankaccount_other(self):
        self.mock_natural_user()
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/OTHER',
            'body': {
                "UserId": "1169419",
                "OwnerName": "Victor Hugo",
                "OwnerAddress": {
                    "AddressLine1": "AddressLine1",
                    "AddressLine2": "AddressLine2",
                    "City": "City",
                    "Region": "Region",
                    "PostalCode": "11222",
                    "Country": "FR"
                },
                "Type": "OTHER",
                "Id": "6775453",
                "Tag": "custom tag",
                "CreationDate": 1431964920,
                "AccountNumber": "123",
                "BIC": "BNPAFRPP",
                "Country": "FR"
            },
            'status': 200
        })

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "OTHER",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "country": "FR",
            "bic": "BNPAFRPP",
            "tag": "custom tag",
            "account_number": "123"
        }
        bankaccount = BankAccount(**params)

        self.assertIsNone(bankaccount.get_pk())
        bankaccount.save()
        self.assertIsInstance(bankaccount, BankAccount)

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

        self.assertIsNotNone(bankaccount.get_pk())

    @responses.activate
    def test_retrieve_bankaccount_iban(self):
        self.mock_natural_user()
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/IBAN',
                'body': {
                    "UserId": "1169419",
                    "Type": "IBAN",
                    "OwnerName": "Victor Hugo",
                    "OwnerAddress": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    },
                    "IBAN": "FR7630004000031234567890143",
                    "BIC": "BNPAFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/1169675',
                'body': {
                    "UserId": "1169419",
                    "Type": "IBAN",
                    "OwnerName": "Victor Hugo",
                    "OwnerAddress": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    },
                    "IBAN": "FR7630004000031234567890143",
                    "BIC": "BNPAFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts',
                'body': [
                    {
                        "UserId": "1169419",
                        "Type": "IBAN",
                        "OwnerName": "Victor Hugo",
                        "OwnerAddress": {
                            "AddressLine1": "AddressLine1",
                            "AddressLine2": "AddressLine2",
                            "City": "City",
                            "Region": "Region",
                            "PostalCode": "11222",
                            "Country": "FR"
                        },
                        "IBAN": "FR7630004000031234567890143",
                        "BIC": "BNPAFRPP",
                        "Id": "1169675",
                        "Tag": "custom tag",
                        "CreationDate": 1383561267
                    }
                ],
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419',
                'body': {
                    "Id": '1169419',
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
                    "PersonType": "NATURAL",
                    "Email": "victor@hugo.com",
                    "Tag": "custom tag"
                },
                'status': 200
            }])

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "IBAN",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "iban": "FR7630004000031234567890143",
            "bic": "BNPAFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)
        bankaccount.save()

        self.assertIsNotNone(bankaccount.get_pk())

        pk = bankaccount.get_pk()

        bankaccount = BankAccount.get(bankaccount.get_pk(), **{'user_id': self.natural_user.get_pk()})

        self.assertIsNotNone(bankaccount.get_pk())

        self.assertEqual(self.natural_user.bankaccounts.get(pk, **{'user_id': self.natural_user.get_pk()}), bankaccount)
        self.assertEqual(self.natural_user.bankaccounts.all(), [bankaccount])

        for key, value in params.items():
            self.assertEqual(getattr(bankaccount, key), value)

    @responses.activate
    def test_retrieve_users_all_bankaccounts(self):
        self.mock_natural_user()
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts/IBAN',
                'body': {
                    "UserId": "1167502",
                    "Type": "IBAN",
                    "OwnerName": "Victor Hugo",
                    "OwnerAddress": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    },
                    "IBAN": "FR7630004000031234567890143",
                    "BIC": "BNPAFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/bankaccounts',
                'body': [
                    {
                        "UserId": "1167502",
                        "Type": "IBAN",
                        "OwnerName": "Victor Hugo",
                        "OwnerAddress": {
                            "AddressLine1": "AddressLine1",
                            "AddressLine2": "AddressLine2",
                            "City": "City",
                            "Region": "Region",
                            "PostalCode": "11222",
                            "Country": "FR"
                        },
                        "IBAN": "FR7630004000031234567890143",
                        "BIC": "BNPAFRPP",
                        "Id": "1169675",
                        "Tag": "custom tag",
                        "CreationDate": 1383561267
                    }
                ],
                'status': 200
            }])

        params = {
            "owner_name": "Victor Hugo",
            "user": self.natural_user,
            "type": "IBAN",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "iban": "FR7630004000031234567890143",
            "bic": "BNPAFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)
        bankaccount.save()
        self.assertIsNotNone(bankaccount.get_pk())

        self.assertIsInstance(self.natural_user.bankaccounts.all(), list)

        for bankaccount in self.natural_user.bankaccounts.all():
            self.assertIsInstance(bankaccount, BankAccount)


class BankAccountTestLive(BaseTestLive):

    def test_deactivateBankAccount(self):
        john = BaseTestLive.get_john()
        account = BaseTestLive.get_johns_account()

        self.assertTrue(account.id)
        self.assertTrue(john.id == account.user_id)

        result = BankAccount(**account.deactivate())

        self.assertIsNotNone(result)
        self.assertEqual(account.id, result.id)
        self.assertFalse(result.active)

    def test_BankAccount_getTransactions(self):
        account = BaseTestLive.get_johns_account()

        transactions_page = account.get_transactions()

        self.assertIsNotNone(transactions_page.data)
        self.assertIsInstance(transactions_page.data, list)

    def test_GetBankAccount(self):
        account = BaseTestLive.get_johns_account()

        get_account = BaseTestLive.get_john().bankaccounts.get(account.id)

        self.assertIsNotNone(get_account)
        self.assertEqual(account.id, get_account.id)
