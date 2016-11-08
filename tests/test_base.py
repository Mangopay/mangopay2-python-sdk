# -*- coding: utf-8 -*-
import requests

from datetime import date
from exam.decorators import fixture

from mangopay.utils import Address, ReportFilters
from . import settings
from .mocks import RegisteredMocks
from .resources import (NaturalUser, LegalUser, Wallet,
                        CardRegistration, Card)

import responses
import time
import unittest

from mangopay import get_default_handler
from mangopay.auth import AuthorizationTokenManager, StaticStorageStrategy
from mangopay.resources import BankAccount, Document, Report

_activate = responses.activate


def override_activate(func):
    if getattr(settings, 'MOCK_TESTS_RESPONSES', True):
        return _activate(func)
    return func


responses.activate = override_activate


class BaseTest(RegisteredMocks):
    @fixture
    def natural_user(self):
        natural_user_params = {
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": time.mktime(date.today().timetuple()),
            "nationality": "FR",
            "country_of_residence": "FR",
            "occupation": "Writer",
            "income_range": 6,
            "proof_of_identity": None,
            "proof_of_address": None,
            "person_type": "NATURAL",
            "email": "victor@hugo.com",
            "tag": "custom tag",
        }
        natural_user = NaturalUser(**natural_user_params)
        natural_user.save()

        return natural_user

    @fixture
    def legal_user(self):
        legal_user_params = {
            "name": "MangoPay",
            "legal_person_type": "BUSINESS",
            "headquarters_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                            city='City', region='Region',
                                            postal_code='11222', country='FR'),
            "legal_representative_first_name": "Mango",
            "legal_representative_last_name": "Pay",
            "legal_representative_email": "mango@mangopay.com",
            "legal_representative_birthday": time.mktime(date.today().timetuple()),
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
        legal_user = LegalUser(**legal_user_params)
        legal_user.save()

        return legal_user

    @fixture
    def legal_user_wallet(self):
        legal_user_wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.legal_user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }

        legal_user_wallet = Wallet(**legal_user_wallet_params)
        legal_user_wallet.save()

        return legal_user_wallet

    @fixture
    def natural_user_wallet(self):
        natural_user_wallet_params = {
            'tag': 'My custom tag',
            'owners': [self.natural_user],
            'description': 'Wallet of Victor Hugo',
            'currency': 'EUR'
        }

        natural_user_wallet = Wallet(**natural_user_wallet_params)
        natural_user_wallet.save()

        return natural_user_wallet

    @fixture
    def card(self):
        card_params = {
            "user": self.natural_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        self.mock_tokenization_request()

        response = requests.post(card_registration.card_registration_url, data={
            'cardNumber': '4970100000000154',
            'cardCvx': '123',
            'cardExpirationDate': '0120',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        })

        card_registration.registration_data = response.content
        card_registration.save()

        card = Card.get(card_registration.card.get_pk())

        return card

    @fixture
    def natural_user_card(self):
        card_params = {
            "user": self.natural_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        self.mock_tokenization_request()

        response = requests.post(card_registration.card_registration_url, data={
            'cardNumber': '4970101122334422',
            'cardCvx': '123',
            'cardExpirationDate': '0120',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        })

        card_registration.registration_data = response.content
        card_registration.save()

        card = Card.get(card_registration.card.get_pk())

        return card

    @fixture
    def legal_user_card(self):
        card_params = {
            "user": self.legal_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        self.mock_tokenization_request()

        response = requests.post(card_registration.card_registration_url, data={
            'cardNumber': '4970101122334406',
            'cardCvx': '123',
            'cardExpirationDate': '0120',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        })

        card_registration.registration_data = response.content
        card_registration.save()

        card = Card.get(card_registration.card.get_pk())

        return card


class BaseTestLive(unittest.TestCase):
    _john = None
    _johns_account = None
    _johns_wallet = None
    _johns_kyc_document = None
    _oauth_manager = AuthorizationTokenManager(get_default_handler(), StaticStorageStrategy())
    _johns_report = None

    def setUp(self):
        BaseTestLive.get_john()

    @staticmethod
    def get_johns_report(recreate=False):
        if BaseTestLive._johns_report is None or recreate:
            report = Report()
            report.report_type = 'TRANSACTION'
            report.filters = ReportFilters()
            report.filters.author_id = BaseTestLive._john.id
            BaseTestLive._johns_report = Report(**report.save())
        return BaseTestLive._johns_report

    @staticmethod
    def get_johns_account(recreate=False):
        if BaseTestLive._johns_account is None or recreate:
            account = BankAccount()
            account.owner_name = BaseTestLive._john.first_name + ' ' + BaseTestLive._john.last_name
            account.user = BaseTestLive._john
            account.type = 'IBAN'
            account.owner_address = BaseTestLive._john.address
            account.iban = 'FR7618829754160173622224154'
            account.bic = 'CMBRFR2BCME'
            BaseTestLive._johns_account = BankAccount(**account.save())
        return BaseTestLive._johns_account

    @staticmethod
    def get_john(recreate=False):
        if BaseTestLive._john is None or recreate:
            user = NaturalUser()
            user.first_name = 'John'
            user.last_name = 'Doe'
            user.birthday = 188352000
            user.email = "john.doe@sample.org"
            user.address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                   city='City', region='Region',
                                   postal_code='11222', country='FR')
            user.nationality = 'FR'
            user.country_of_residence = 'FR'
            user.occupation = 'programmer'
            user.income_range = '1'
            user.person_type = 'NATURAL'
            BaseTestLive._john = NaturalUser(**user.save())
        return BaseTestLive._john

    @staticmethod
    def get_johns_kyc_document(recreate=False):
        if BaseTestLive._johns_kyc_document is None or recreate:
            document = Document()
            document.type = 'IDENTITY_PROOF'
            document.user_id = BaseTestLive.get_john().id
            BaseTestLive._johns_kyc_document = Document(**document.save())
        return BaseTestLive._johns_kyc_document

    @staticmethod
    def get_johns_wallet(recreate=False):
        if BaseTestLive._johns_wallet is None or recreate:
            wallet = Wallet()
            wallet.owners = (BaseTestLive._john, )
            wallet.currency = 'EUR'
            wallet.description = 'WALLET IN EUR'
            BaseTestLive._johns_wallet = Wallet(**wallet.save())
        return BaseTestLive._johns_wallet

    @staticmethod
    def get_oauth_manager():
        return BaseTestLive._oauth_manager