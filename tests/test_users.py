# -*- coding: utf-8 -*-

import re

import requests
import responses

from mangopay.resources import (User, NaturalUser, Wallet,
                                LegalUser, Transfer, Transaction)
from mangopay.utils import Money, Address
from tests import settings
from tests.mocks import today, today_timestamp
from tests.test_base import BaseTest, BaseTestLive

requests_session = requests.Session()


class UsersTest(BaseTest):
    @responses.activate
    def test_create_natural_user(self):
        self.mock_natural_user()

        self.register_mock({
            "method": responses.PUT,
            "url": re.compile(
                r'' + settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/natural/\d+'),
            "body": {
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
                "Birthday": today_timestamp,
                "Nationality": "FR",
                "CountryOfResidence": "FR",
                "Occupation": "Writer",
                "IncomeRange": 6,
                "PersonType": "NATURAL",
                "Email": "victor@hugo.com",
                "Id": "1169419",
                "Tag": "custom tag",
                "CreationDate": 1383321421,
                "KYCLevel": "LIGHT",
                "UserCategory": "OWNER"
            },
            "status": 200
        })

        params = {
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": today,
            "nationality": "FR",
            "country_of_residence": "FR",
            "occupation": "Writer",
            "income_range": 6,
            "proof_of_identity": None,
            "proof_of_address": None,
            "person_type": "NATURAL",
            "email": "victor@hugo.com",
            "tag": "custom tag",
            "user_category": "OWNER"
        }
        user = NaturalUser(**params)

        self.assertIsNone(user.get_pk())
        user.save()
        self.assertIsInstance(user, NaturalUser)

        for key, value in params.items():
            self.assertEqual(getattr(user, key), value)

        self.assertIsNotNone(user.get_pk())

        previous_pk = user.get_pk()

        user.last_name = 'Claver'
        user.save()

        self.assertEqual(previous_pk, user.get_pk())

        self.assertEqual(user.last_name, 'Claver')

    @responses.activate
    def test_create_legal_user(self):
        self.mock_legal_user()

        self.register_mock({
            'method': responses.PUT,
            'url': re.compile(
                r'' + settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/legal/\d+'),
            'body': {
                "Name": "MangoPay edited",
                "LegalPersonType": "BUSINESS",
                "HeadquartersAddress": {
                    "AddressLine1": "AddressLine1",
                    "AddressLine2": "AddressLine2",
                    "City": "City",
                    "Region": "Region",
                    "PostalCode": "11222",
                    "Country": "FR"
                },
                "LegalRepresentativeFirstName": "Mango",
                "LegalRepresentativeLastName": "Pay",
                "LegalRepresentativeEmail": "mango@mangopay.com",
                "LegalRepresentativeBirthday": today_timestamp,
                "LegalRepresentativeNationality": "FR",
                "LegalRepresentativeCountryOfResidence": "FR",
                "PersonType": "LEGAL",
                "Email": "info@mangopay.com",
                "Id": "1169420",
                "Tag": "custom tag",
                "CreationDate": 1383322502,
                "KYCLevel": "LIGHT",
                "UserCategory": "PAYER"
            },
            'status': 200
        })

        params = {
            "name": "MangoPay",
            "legal_person_type": "BUSINESS",
            "headquarters_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                            city='City', region='Region',
                                            postal_code='11222', country='FR'),
            "legal_representative_first_name": "Mango",
            "legal_representative_last_name": "Pay",
            "legal_representative_email": "mango@mangopay.com",
            "legal_representative_birthday": today,
            "legal_representative_nationality": "FR",
            "legal_representative_country_of_residence": "FR",
            "proof_of_registration": None,
            "shareholder_declaration": None,
            "legal_representative_address": None,
            "statute": None,
            "person_type": "LEGAL",
            "email": "info@mangopay.com",
            "tag": "custom tag",
            "user_category": "PAYER"
            # "creation_date": datetime.now()
        }
        user = LegalUser(**params)

        self.assertIsNone(user.get_pk())
        user.save()
        self.assertIsInstance(user, LegalUser)

        for key, value in params.items():
            self.assertEqual(getattr(user, key), value)

        self.assertIsNotNone(user.get_pk())

        previous_pk = user.get_pk()

        user.last_name = 'Claver'
        user.save()

        self.assertEqual(previous_pk, user.get_pk())

        self.assertEqual(user.last_name, 'Claver')

    @responses.activate
    def test_retrieve_natural_user(self):
        self.mock_natural_user()

        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/natural/1169419',
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
                    "Birthday": today_timestamp,
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
                    "KYCLevel": "LIGHT",
                    "UserCategory": "OWNER"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/natural/1169420',
                'body': {"errors": []},
                'status': 404
            }])

        params = {
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": today,
            "nationality": "FR",
            "country_of_residence": "FR",
            "occupation": "Writer",
            "income_range": 6,
            "proof_of_identity": None,
            "proof_of_address": None,
            "person_type": "NATURAL",
            "email": "victor@hugo.com",
            "tag": "custom tag",
            "user_category": "OWNER"
        }
        user = NaturalUser(**params)
        user.save()

        self.assertRaises(NaturalUser.DoesNotExist, NaturalUser.get, int(user.get_pk()) + 1)

        self.assertIsNotNone(user.get_pk())

        user = NaturalUser.get(user.get_pk())

        self.assertIsNotNone(user.get_pk())

        for key, value in params.items():
            self.assertEqual(getattr(user, key), value)

    @responses.activate
    def test_retrieve_legal_user(self):
        self.mock_legal_user()

        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/legal/1169420',
                'body': {
                    "Name": "MangoPay",
                    "LegalPersonType": "BUSINESS",
                    "HeadquartersAddress": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    },
                    "LegalRepresentativeFirstName": "Mango",
                    "LegalRepresentativeLastName": "Pay",
                    "LegalRepresentativeEmail": "mango@mangopay.com",
                    "LegalRepresentativeBirthday": today_timestamp,
                    "LegalRepresentativeNationality": "FR",
                    "LegalRepresentativeCountryOfResidence": "FR",
                    "ProofOfRegistration": None,
                    "ShareholderDeclaration": None,
                    "LegalRepresentativeAddress": None,
                    "Statute": None,
                    "PersonType": "LEGAL",
                    "Email": "info@mangopay.com",
                    "Id": "1169420",
                    "Tag": "custom tag",
                    "CreationDate": 1383322502,
                    "KYCLevel": "LIGHT"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/legal/1169421',
                'body': {"errors": []},
                'status': 404
            }])

        params = {
            "name": "MangoPay",
            "legal_person_type": "BUSINESS",
            "headquarters_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                            city='City', region='Region',
                                            postal_code='11222', country='FR'),
            "legal_representative_first_name": "Mango",
            "legal_representative_last_name": "Pay",
            "legal_representative_email": "mango@mangopay.com",
            "legal_representative_birthday": today,
            "legal_representative_nationality": "FR",
            "legal_representative_country_of_residence": "FR",
            "proof_of_registration": None,
            "shareholder_declaration": None,
            "legal_representative_address": None,
            "statute": None,
            "person_type": "LEGAL",
            "email": "info@mangopay.com",
            "tag": "custom tag",
            # "creation_date": datetime.now()
        }
        user = LegalUser(**params)
        user.save()

        self.assertRaises(LegalUser.DoesNotExist, LegalUser.get, int(user.get_pk()) + 1)

        self.assertIsNotNone(user.get_pk())

        user = LegalUser.get(user.get_pk())

        self.assertIsNotNone(user.get_pk())

        for key, value in params.items():
            self.assertEqual(getattr(user, key), value)

    @responses.activate
    def test_retrieve_all_users(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users',
            'body': [
                {
                    "PersonType": "NATURAL",
                    "Email": "victor@hugo.com",
                    "Id": "1167495",
                    "Tag": None,
                    "CreationDate": 1382605938,
                    "KYCLevel": "LIGHT",
                    "FirstName": "Victor"
                },
                {
                    "PersonType": "LEGAL",
                    "Email": None,
                    "Id": "1167502",
                    "Tag": None,
                    "CreationDate": 1382607639,
                    "KYCLevel": "LIGHT"
                },
                {
                    "PersonType": "NATURAL",
                    "Email": None,
                    "Id": "1167774",
                    "Tag": "",
                    "CreationDate": 1382627263,
                    "KYCLevel": "REGULAR"
                },
                {
                    "PersonType": "NATURAL",
                    "Email": None,
                    "Id": "1168856",
                    "Tag": None,
                    "CreationDate": 1383143870,
                    "KYCLevel": "LIGHT"
                }
            ],
            'status': 200
        })

        users = User.all()
        self.assertIsInstance(users.data, list)

        self.assertIsInstance(users[0], NaturalUser)
        self.assertEqual(users[0].email, 'victor@hugo.com')
        self.assertIsNotNone(users[0].first_name)

    @responses.activate
    def test_retrieve_paginated_users(self):
        self.mock_user_list_full()
        self.mock_user_list_2_per_page_page1()
        self.mock_user_list_3_per_page_page2()
        self.mock_user_list_page1()
        self.mock_user_list_2_per_page()

        users_page = User.all()
        self.assertEqual(len(users_page), 10)
        for user in users_page:
            if isinstance(user, NaturalUser):
                self.assertIsNotNone(user.first_name)
            else:
                self.assertIsInstance(user, LegalUser)
                self.assertIsNotNone(user.name)

        users_page = User.all(page=1, per_page=2)
        self.assertEqual(len(users_page), 2)

        first_instance = users_page.data[0]

        users_page = User.all(page=2, per_page=3)
        self.assertEqual(len(users_page), 3)
        self.assertFalse(first_instance in users_page)

        # with self.assertRaises(APIError):
        #     users_page = User.all(random_key=1, another_random_key=2)

        users_page = User.all(page=1)
        self.assertEqual(len(users_page), 10)

        users_page = User.all(per_page=2)
        self.assertEqual(len(users_page), 2)

    @responses.activate
    def test_retrieve_specific_natural_user(self):
        self.mock_natural_user()

        self.register_mock({
            'method': responses.GET,
            'url': re.compile(r'' + settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/\d+'),
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
                "Birthday": today_timestamp,
                "Nationality": "FR",
                "CountryOfResidence": "FR",
                "Occupation": "Writer",
                "IncomeRange": 6,
                "PersonType": "NATURAL",
                "Email": "victor@hugo.com",
                "Id": "1167495",
                "CreationDate": 1382605938,
                "KYCLevel": "LIGHT",
                "Tag": "custom tag",
                "UserCategory": "OWNER"
            },
            'status': 200
        })

        params = {
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": today,
            "nationality": "FR",
            "country_of_residence": "FR",
            "occupation": "Writer",
            "income_range": 6,
            "proof_of_identity": None,
            "proof_of_address": None,
            "person_type": "NATURAL",
            "email": "victor@hugo.com",
            "tag": "custom tag",
            "user_category": "OWNER"
        }
        user = NaturalUser(**params)
        user.save()
        self.assertIsNotNone(user.get_pk())

        retrieved_user = User.get(user.get_pk())

        self.assertIsNotNone(retrieved_user.get_pk())

        for key, value in params.items():
            self.assertEqual(getattr(retrieved_user, key), value)

        self.assertIsInstance(retrieved_user, User)

    @responses.activate
    def test_retrieve_specific_legal_user(self):
        self.mock_legal_user()

        self.register_mock({
            'method': responses.GET,
            'url': re.compile(r'' + settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/\d+'),
            'body': {
                "Name": "MangoPay",
                "LegalPersonType": "BUSINESS",
                "HeadquartersAddress": {
                    "AddressLine1": "AddressLine1",
                    "AddressLine2": "AddressLine2",
                    "City": "City",
                    "Region": "Region",
                    "PostalCode": "11222",
                    "Country": "FR"
                },
                "LegalRepresentativeFirstName": "Mango",
                "LegalRepresentativeLastName": "Pay",
                "LegalRepresentativeEmail": "mango@mangopay.com",
                "LegalRepresentativeBirthday": today_timestamp,
                "LegalRepresentativeNationality": "FR",
                "LegalRepresentativeCountryOfResidence": "FR",
                "ProofOfRegistration": None,
                "ShareholderDeclaration": None,
                "LegalRepresentativeAddress": None,
                "Statute": None,
                "PersonType": "LEGAL",
                "Email": "info@mangopay.com",
                "Id": "1169420",
                "Tag": "custom tag",
                "CreationDate": 1383322502,
                "KYCLevel": "LIGHT",
                "UserCategory": "OWNER"
            },
            'status': 200
        })

        params = {
            "name": "MangoPay",
            "legal_person_type": "BUSINESS",
            "headquarters_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                            city='City', region='Region',
                                            postal_code='11222', country='FR'),
            "legal_representative_first_name": "Mango",
            "legal_representative_last_name": "Pay",
            "legal_representative_email": "mango@mangopay.com",
            "legal_representative_birthday": today,
            "legal_representative_nationality": "FR",
            "legal_representative_country_of_residence": "FR",
            "proof_of_registration": None,
            "shareholder_declaration": None,
            "legal_representative_address": None,
            "statute": None,
            "person_type": "LEGAL",
            "email": "info@mangopay.com",
            "tag": "custom tag",
            "user_category": "OWNER"
            # "creation_date": datetime.now()
        }
        user = LegalUser(**params)

        self.assertIsNone(user.get_pk())
        user.save()
        self.assertIsInstance(user, LegalUser)

        for key, value in params.items():
            self.assertEqual(getattr(user, key), value)

        retrieved_user = User.get(user.id)

        for key, value in params.items():
            self.assertEqual(getattr(retrieved_user, key), value)

        self.assertIsInstance(retrieved_user, User)

    @responses.activate
    def test_retrieve_users_transactions(self):
        self.mock_natural_user()
        self.mock_legal_user()
        self.mock_user_wallet()
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
                    "Birthday": today_timestamp,
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
                    "KYCLevel": "LIGHT",
                    "UserCategory": "OWNER"
                },
                'status': 200
            },
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
                    "ExecutionDate": today_timestamp,
                    "Type": "TRANSFER",
                    "Nature": "REGULAR",
                    "DebitedWalletId": "1167496",
                    "CreditedWalletId": "1167504"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1169419/transactions',
                'body': [
                    {
                        "Id": "1174837",
                        "Tag": "my transfer",
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
                        "ExecutionDate": today_timestamp,
                        "Type": "TRANSFER",
                        "Nature": "REGULAR",
                        "CreditedWalletId": "1167496",
                        "DebitedWalletId": "1167504"
                    }
                ],
                'status': 200
            }
        ])

        wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.card.user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }
        wallet = Wallet(**wallet_params)
        wallet.save()

        # Create a transaction:
        params = {
            "author": self.card.user,
            "credited_user": self.legal_user,
            "debited_funds": Money(amount=10, currency='EUR'),
            "fees": Money(amount=1, currency='EUR'),
            "debited_wallet": wallet,
            "credited_wallet": self.legal_user_wallet,
            "tag": "custom tag"
        }
        transfer = Transfer(**params)
        transfer.save()

        # List wallet's transactions
        transactions = Transaction.all(**{"user_id": self.card.user.id})

        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].type, 'TRANSFER')


class UserTestLive(BaseTestLive):
    def test_Users_GetKycDocuments(self):
        user = BaseTestLive.get_john()
        BaseTestLive.get_johns_kyc_document()
        BaseTestLive.get_johns_kyc_document(recreate=True)
        documents = user.documents.all()

        self.assertTrue(documents)


class PayOutsTestLive(BaseTestLive):

    def test_PayOut_GetRefunds(self):
        payout = BaseTestLive.get_johns_payout()

        refunds = payout.get_refunds()

        self.assertIsNotNone(refunds.data)
        self.assertIsInstance(refunds.data, list)


class PayInsTestLive(BaseTestLive):
    def test_PayIn_GetRefunds(self):
        payin = BaseTestLive.get_johns_payin()
        refunds_page = payin.get_refunds()

        self.assertIsNotNone(refunds_page.data)
        self.assertIsInstance(refunds_page.data, list)

    def test_User_GetPreAuthorizationss(self):
        user = BaseTestLive.get_john()

        get_preauthorizations_page = user.get_pre_authorizations()

        self.assertIsNotNone(get_preauthorizations_page.data)
        self.assertIsInstance(get_preauthorizations_page.data, list)

    def test_User_get_block_status(self):
        user = BaseTestLive.get_john()
        block_status = user.get_block_status()

        self.assertIsNotNone(block_status)

    def test_User_get_regulatory(self):
        user = BaseTestLive.get_john()
        regulatory = user.get_regulatory()

        self.assertIsNotNone(regulatory)

    def test_User_natural_terms_and_conditions(self):
        user = BaseTestLive.get_john()
        self.assertFalse(user.terms_and_conditions_accepted)

        user.terms_and_conditions_accepted = True
        user.save()

        self.assertTrue(user.terms_and_conditions_accepted)
        self.assertIsNotNone(user.terms_and_conditions_accepted_date)

        user = BaseTestLive.get_john(recreate=True, terms=True)
        self.assertTrue(user.terms_and_conditions_accepted)
        self.assertIsNotNone(user.terms_and_conditions_accepted_date)

    def test_User_legal_terms_and_conditions(self):
        user = BaseTestLive.get_user_legal()
        self.assertFalse(user.terms_and_conditions_accepted)

        user.legal_representative_address = {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    }
        user.terms_and_conditions_accepted = True
        user.save()

        self.assertTrue(user.terms_and_conditions_accepted)
        self.assertIsNotNone(user.terms_and_conditions_accepted_date)

        user = BaseTestLive.get_user_legal(recreate=True, terms=True)
        self.assertTrue(user.terms_and_conditions_accepted)
        self.assertIsNotNone(user.terms_and_conditions_accepted_date)
