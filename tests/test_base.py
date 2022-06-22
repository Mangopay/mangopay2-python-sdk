# -*- coding: utf-8 -*-
import time
import unittest
from datetime import date

import requests
import responses
from exam.decorators import fixture

from mangopay import APIRequest
from mangopay import get_default_handler
from mangopay.auth import AuthorizationTokenManager, StaticStorageStrategy
from mangopay.constants import LEGAL_USER_TYPE_CHOICES
from mangopay.resources import BankAccount, Document, ReportTransactions, UboDeclaration, Ubo
from mangopay.utils import Address, ReportTransactionsFilters, Birthplace
from tests import settings
from tests.mocks import RegisteredMocks
from tests.resources import (NaturalUser, LegalUser, Wallet,
                             CardRegistration, Card, BankWirePayOut, CardWebPayIn, Transfer, Money)

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
            "tag": "Python SDK Unit Test",
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
            "legal_representative_birthday": 188301600,
            "legal_representative_nationality": "FR",
            "legal_representative_country_of_residence": "FR",
            "proof_of_registration": None,
            "shareholder_declaration": None,
            "legal_representative_address": None,
            "statute": None,
            "person_type": "LEGAL",
            "email": "info@mangopay.com",
            "tag": "Python SDK Unit Test",
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
            'cardExpirationDate': '0124',
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
            'cardExpirationDate': '0124',
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
            'cardExpirationDate': '0124',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        })

        card_registration.registration_data = response.content
        card_registration.save()

        card = Card.get(card_registration.card.get_pk())

        return card

    @fixture
    def legal_user_ubo_declaration(self):
        self.mock_declarative_user()
        self.mock_ubo_declaration()

        params = {
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": 1231432,
            "nationality": "FR",
            "country_of_residence": "FR",
            "occupation": "Writer",
            "income_range": 6,
            "proof_of_identity": None,
            "proof_of_address": None,
            "person_type": "NATURAL",
            "email": "victor@hugo.com",
            "tag": "Python SDK Unit Test",
            "capacity": "DECLARATIVE"
        }
        user = NaturalUser(**params)
        user.save()

        params = {
            "user": user,
            "creation_date": 1554803756
        }

        ubo_declaration = UboDeclaration(**params)
        ubo_declaration.save()
        return ubo_declaration, user

    @fixture
    def ubo_declaration_ubo(self):
        params = {
            "first_name": "Victor",
            "last_name": "Hugo",
            "address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR'),
            "birthday": 1231432,
            "nationality": "FR",
            "birthplace": Birthplace(city='Paris', country='FR')
        }
        ubo = Ubo(**params)
        return ubo


class BaseTestLive(unittest.TestCase):
    _john = None
    _johns_account = None
    _johns_wallet = None
    _johns_kyc_document = None
    _oauth_manager = AuthorizationTokenManager(get_default_handler(), StaticStorageStrategy())
    _johns_report = None
    _johns_transfer = None
    _johns_payout = None
    _johns_payin = None
    _johns_card = None
    _johns_card_3dsecure = None

    _user_legal = None
    _ubo_declaration = None
    _ubo = None

    _client_account = None

    def setUp(self):
        BaseTestLive.get_john()
        BaseTestLive.get_user_legal()

    @staticmethod
    def get_user_legal(recreate=False, terms=False):
        if BaseTestLive._user_legal is None or recreate:
            legal = LegalUser()
            legal.name = 'MatrixSampleOrg_PythonSDK'
            legal.email = 'mail@test.com'
            legal.legal_person_type = "BUSINESS"
            legal.legal_representative_first_name = "Mango"
            legal.legal_representative_last_name = 'Pay'
            legal.legal_representative_email = 'mango@mangopay.com'
            legal.person_type = 'LEGAL'
            legal.headquarters_address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                                 city='City', region='Region',
                                                 postal_code='11222', country='FR')
            legal.legal_representative_birthday = 1300186358
            legal.legal_representative_nationality = 'FR'
            legal.legal_representative_country_of_residence = 'FR'
            legal.company_number = 123456789
            legal.tag = 'Python SDK Unit Test'
            legal.terms_and_conditions_accepted = terms
            legal.user_category = 'OWNER'
            BaseTestLive._user_legal = LegalUser(**legal.save())
        return BaseTestLive._user_legal

    @staticmethod
    def get_ubo_declaration(recreate=False):
        if BaseTestLive._ubo_declaration is None or recreate:
            legal_user = BaseTestLive.get_user_legal()
            params = {
                "user_id": legal_user.id
            }
            BaseTestLive._ubo_declaration = UboDeclaration(**UboDeclaration().create(**params))
        return BaseTestLive._ubo_declaration

    @staticmethod
    def get_ubo(recreate=False):
        if BaseTestLive._ubo is None or recreate:
            address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                              city='City', region='Region',
                              postal_code='11222', country='FR')
            params = {
                "user": BaseTestLive.get_user_legal(True),
                "ubo_declaration": BaseTestLive.get_ubo_declaration(True),
                "first_name": "Victor",
                "last_name": "Hugo",
                "address": address,
                "birthday": date(1970, 1, 15),
                "nationality": "FR",
                "birthplace": Birthplace(city='Paris', country='FR'),
                "isActive": True
            }
            BaseTestLive._ubo = Ubo.create(**params)
        return BaseTestLive._ubo

    @staticmethod
    def get_johns_report(recreate=False):
        if BaseTestLive._johns_report is None or recreate:
            report = ReportTransactions()
            report.report_type = 'transactions'
            report.filters = ReportTransactionsFilters()
            report.filters.author_id = BaseTestLive._john.id
            BaseTestLive._johns_report = ReportTransactions(**report.save())
        return BaseTestLive._johns_report

    @staticmethod
    def get_johns_account(recreate=False):
        if BaseTestLive._johns_account is None or recreate:
            account = BankAccount()
            account.owner_name = BaseTestLive._john.first_name + ' ' + BaseTestLive._john.last_name
            account.user = BaseTestLive._john
            account.type = 'IBAN'
            account.owner_address = BaseTestLive._john.address
            account.iban = 'FR7630004000031234567890143'
            account.bic = 'BNPAFRPP'
            BaseTestLive._johns_account = BankAccount(**account.save())
        return BaseTestLive._johns_account

    @staticmethod
    def get_client_bank_account(recreate=False):
        if BaseTestLive._client_account is None or recreate:
            account = BankAccount()
            account.owner_name = 'Joe Blogs'
            account.type = 'IBAN'

            account.owner_address = Address()
            account.owner_address.address_line_1 = "Main Street"
            account.owner_address.address_line_2 = "no. 5 ap. 6"
            account.owner_address.country = "FR"
            account.owner_address.city = "Lyon"
            account.owner_address.postal_code = "65400"

            account.iban = 'FR7630004000031234567890143'
            account.bic = 'BNPAFRPP'
            account.tag = 'custom meta'

            account.create_client_bank_account()

            BaseTestLive._client_account = BankAccount(**account.create_client_bank_account())

        return BaseTestLive._client_account

    @staticmethod
    def get_john(recreate=False, terms=False):
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
            user.terms_and_conditions_accepted = terms
            user.user_category = 'OWNER'
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
            BaseTestLive._johns_wallet = BaseTestLive.create_new_wallet()
        return BaseTestLive._johns_wallet

    @staticmethod
    def create_new_wallet():
        wallet = Wallet()
        wallet.owners = (BaseTestLive._john,)
        wallet.currency = 'EUR'
        wallet.description = 'WALLET IN EUR'
        return Wallet(**wallet.save())

    @staticmethod
    def get_johns_transfer(recreate=False):
        if BaseTestLive._johns_transfer is None or recreate:
            john = BaseTestLive.get_john()
            wallet1 = BaseTestLive.get_johns_wallet()
            wallet2 = BaseTestLive.create_new_wallet()

            transfer = Transfer()
            transfer.author = john
            transfer.tag = 'DefaultTag'
            transfer.credited_user = john
            transfer.debited_funds = Money(amount=1, currency='EUR')
            transfer.fees = Money(amount=0, currency='EUR')
            transfer.debited_wallet = wallet1
            transfer.credited_wallet = wallet2
            BaseTestLive._johns_transfer = Transfer(**transfer.save())
        return BaseTestLive._johns_transfer

    @staticmethod
    def get_johns_payout(recreate=False):
        if BaseTestLive._johns_payout is None or recreate:
            john = BaseTestLive.get_john()
            wallet = BaseTestLive.get_johns_wallet()
            account = BaseTestLive.get_johns_account()

            payout = BankWirePayOut()
            payout.debited_wallet = wallet
            payout.author = john
            payout.credited_user = john
            payout.tag = 'DefaultTag'
            payout.debited_funds = Money(amount=10, currency='EUR')
            payout.fees = Money(amount=5, currency='EUR')
            payout.bank_account = account
            payout.bank_wire_ref = 'User payment'
            payout.payment_type = 'BANK_WIRE'
            BaseTestLive._johns_payout = BankWirePayOut(**payout.save())
        return BaseTestLive._johns_payout

    @staticmethod
    def get_johns_payin(recreate=False):
        if BaseTestLive._johns_payin is None or recreate:
            wallet = BaseTestLive.get_johns_wallet()
            payin = CardWebPayIn()
            payin.credited_wallet = wallet
            payin.author = BaseTestLive.get_john()
            payin.debited_funds = Money(amount=10000, currency='EUR')
            payin.fees = Money(amount=0, currency='EUR')
            payin.card_type = 'CB_VISA_MASTERCARD'
            payin.return_url = 'https://test.com'
            payin.template_url = 'https://TemplateURL.com'
            payin.secure_mode = 'DEFAULT'
            payin.culture = 'fr'
            BaseTestLive._johns_payin = CardWebPayIn(**payin.save())
        return BaseTestLive._johns_payin

    @staticmethod
    def get_johns_card(recreate=False):
        if BaseTestLive._johns_card is None or recreate:
            card_params = {
                "user": BaseTestLive.get_john(),
                "currency": 'EUR'
            }
            card_registration = CardRegistration(**card_params)
            card_registration.save()

            params = {
                "data_XXX": card_registration.preregistration_data,
                "accessKeyRef": card_registration.access_key,
                "cardNumber": '4970101122334422',
                "cardExpirationDate": '1224',
                "cardCvx": '123'
            }
            response = APIRequest().custom_request('POST', card_registration.card_registration_url, None, None, False,
                                                   False, **params)
            card_registration.registration_data = response
            card_registration.save()
            BaseTestLive._johns_card = card_registration.card
        return BaseTestLive._johns_card

    @staticmethod
    def get_johns_card_3dsecure(recreate=False):
        if BaseTestLive._johns_card_3dsecure is None or recreate:
            card_params = {
                "user": BaseTestLive.get_john(),
                "currency": 'EUR'
            }
            card_registration = CardRegistration(**card_params)
            card_registration.save()

            params = {
                "data_XXX": card_registration.preregistration_data,
                "accessKeyRef": card_registration.access_key,
                "cardNumber": '4970105191923460',
                "cardExpirationDate": '1224',
                "cardCvx": '123'
            }
            response = APIRequest().custom_request('POST', card_registration.card_registration_url, None, None, False,
                                                   False, **params)
            card_registration.registration_data = response
            card_registration.save()
            BaseTestLive._johns_card = card_registration.card
        return BaseTestLive._johns_card

    @staticmethod
    def get_oauth_manager():
        return BaseTestLive._oauth_manager

    def test_handler(self):
        api_url = "test_api_url"
        sandbox_url = "test_sandbox_url"

        sandbox_handler = APIRequest(
            api_sandbox_url=sandbox_url,
            api_url=api_url,
            sandbox=True)

        non_sandbox_handler = APIRequest(
            api_sandbox_url=sandbox_url,
            api_url=api_url,
            sandbox=False)

        self.assertEqual(api_url, non_sandbox_handler.api_url)
        self.assertEqual(sandbox_url, sandbox_handler.api_url)
