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
from mangopay.resources import BankAccount, Document, ReportTransactions, UboDeclaration, Ubo, Deposit, DirectPayIn, \
    VirtualAccount, NaturalUserSca, LegalUserSca
from mangopay.utils import Address, ReportTransactionsFilters, Birthplace, BrowserInfo, LegalRepresentative
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
            'cardNumber': '4970107111111119',
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
            'cardNumber': '4970107111111119',
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
            'cardNumber': '4970107111111119',
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

    @staticmethod
    def get_browser_info():
        browser = BrowserInfo()
        browser.accept_header = "text/html, application/xhtml+xml, application/xml;q=0.9, /;q=0.8"
        browser.java_enabled = True
        browser.language = "FR-FR"
        browser.color_depth = 4
        browser.screen_width = 400
        browser.screen_height = 1800
        browser.javascript_enabled = True
        browser.timezone_offset = "+60"
        browser.user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"

        return browser


class BaseTestLive(unittest.TestCase):
    _john = None
    _john_sca_payer = None
    _john_sca_owner = None
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
    _user_legal_sca_payer = None
    _user_legal_sca_owner = None
    _ubo_declaration = None
    _ubo = None

    _client_account = None

    def setUp(self):
        BaseTestLive.get_john()
        BaseTestLive.get_user_legal()
        BaseTestLive.get_john_sca_payer()
        BaseTestLive.get_john_sca_owner()
        BaseTestLive.get_user_legal_sca_payer()
        BaseTestLive.get_user_legal_sca_owner()

    @staticmethod
    def get_user_legal(recreate=False, terms=False):
        if BaseTestLive._user_legal is None or recreate:
            legal = BaseTestLive.get_user_legal_instance(terms)
            BaseTestLive._user_legal = LegalUser(**legal.save())
        return BaseTestLive._user_legal

    @staticmethod
    def get_user_legal_instance(terms=False):
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
        return legal

    @staticmethod
    def get_user_legal_sca_payer(recreate=False, terms=True):
        if BaseTestLive._user_legal_sca_payer is None or recreate:
            user = BaseTestLive.get_user_legal_sca_payer_instance(terms)
            BaseTestLive._user_legal_sca_payer = LegalUserSca(**user.save())
        return BaseTestLive._user_legal_sca_payer

    @staticmethod
    def get_user_legal_sca_payer_instance(terms=True):
        user = LegalUserSca()
        user.name = 'Alex Smith'
        user.email = 'alex.smith.services@example.com'
        user.legal_person_type = "SOLETRADER"
        user.terms_and_conditions_accepted = terms
        user.legal_representative = LegalRepresentative(first_name='Alex', last_name='Smith',
                                                        email='alex.smith.services@example.com',
                                                        phone_number='0611111111',
                                                        phone_number_country='FR')
        user.user_category = 'PAYER'
        user.legal_representative_address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                                    city='City', region='Region',
                                                    postal_code='11222', country='FR')
        return user

    @staticmethod
    def get_user_legal_sca_owner(recreate=False, terms=True):
        if BaseTestLive._user_legal_sca_owner is None or recreate:
            user = LegalUserSca()
            user.name = 'Alex Smith'
            user.email = 'alex.smith.services@example.com'
            user.legal_person_type = "SOLETRADER"
            user.terms_and_conditions_accepted = terms
            user.legal_representative = LegalRepresentative(first_name='Alex', last_name='Smith',
                                                             email='alex.smith.services@example.com',
                                                             phone_number='0611111111',
                                                             phone_number_country='FR',
                                                             birthday=652117514,
                                                             nationality='FR',
                                                             country_of_residence='FR')
            user.headquarters_address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                                 city='City', region='Region',
                                                 postal_code='11222', country='FR')
            user.legal_representative_address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                                         city='City', region='Region',
                                                         postal_code='11222', country='FR')
            user.company_number = '123456789'
            user.user_category = 'OWNER'
            BaseTestLive._user_legal_sca_owner = LegalUserSca(**user.save())
        return BaseTestLive._user_legal_sca_owner

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
            user = BaseTestLive.get_john_instance(terms)
            BaseTestLive._john = NaturalUser(**user.save())
        return BaseTestLive._john

    @staticmethod
    def get_john_instance(terms=False):
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
        return user

    @staticmethod
    def get_john_sca_payer(recreate=False, terms=True):
        if BaseTestLive._john_sca_payer is None or recreate:
            user = BaseTestLive.get_john_sca_payer_instance(terms)
            BaseTestLive._john_sca_payer = NaturalUserSca(**user.save())
        return BaseTestLive._john_sca_payer

    @staticmethod
    def get_john_sca_payer_instance(terms=True):
        user = NaturalUserSca()
        user.first_name = 'John SCA'
        user.last_name = 'Doe SCA Review'
        user.email = "john.doe.sca@sample.org"
        user.terms_and_conditions_accepted = terms
        user.user_category = 'PAYER'
        user.phone_number = '+33611111111'
        user.phone_number_country = 'FR'
        user.address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                               city='City', region='Region',
                               postal_code='11222', country='FR')
        return user

    @staticmethod
    def get_john_sca_owner(recreate=False, terms=True):
        if BaseTestLive._john_sca_owner is None or recreate:
            user = NaturalUserSca()
            user.first_name = 'John SCA'
            user.last_name = 'Doe SCA Review'
            user.birthday = 188352000
            user.email = "john.doe.sca@sample.org"
            user.address = Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                   city='City', region='Region',
                                   postal_code='11222', country='FR')
            user.nationality = 'FR'
            user.country_of_residence = 'FR'
            user.occupation = 'programmer'
            user.income_range = '1'
            user.terms_and_conditions_accepted = terms
            user.user_category = 'OWNER'
            user.phone_number = '+33611111111'
            user.phone_number_country = 'FR'
            BaseTestLive._john_sca_owner = NaturalUserSca(**user.save())
        return BaseTestLive._john_sca_owner

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
            BaseTestLive._johns_wallet = BaseTestLive.create_new_wallet(BaseTestLive._john)
        return BaseTestLive._johns_wallet

    @staticmethod
    def get_johns_wallet_with_money(user, recreate=False):
        if BaseTestLive._johns_wallet is None or recreate:
            BaseTestLive._johns_wallet = BaseTestLive.create_new_wallet_with_money(user)
        return BaseTestLive._johns_wallet

    @staticmethod
    def create_new_wallet(user):
        wallet = Wallet()
        wallet.owners = (user,)
        wallet.currency = 'EUR'
        wallet.description = 'WALLET IN EUR'
        return Wallet(**wallet.save())

    @staticmethod
    def create_new_wallet_with_money(user):
        wallet = Wallet()
        wallet.owners = (user,)
        wallet.currency = 'EUR'
        wallet.description = 'WALLET IN EUR'
        wallet = Wallet(**wallet.save())

        card_registration = CardRegistration()
        card_registration.user = user
        card_registration.currency = 'EUR'

        saved_registration = card_registration.save()
        data = {
            'cardNumber': '4970107111111119',
            'cardCvx': '123',
            'cardExpirationDate': '1229',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        registration_data_response = requests.post(card_registration.card_registration_url, data=data, headers=headers)
        saved_registration['registration_data'] = registration_data_response.text
        updated_registration = CardRegistration(**saved_registration).save()
        card_id = updated_registration['card_id']

        direct_payin = DirectPayIn(author=user,
                                   debited_funds=Money(amount=10000, currency='EUR'),
                                   fees=Money(amount=0, currency='EUR'),
                                   credited_wallet_id=wallet,
                                   card_id=card_id,
                                   secure_mode="DEFAULT",
                                   ip_address="2001:0620:0000:0000:0211:24FF:FE80:C12C",
                                   browser_info=BaseTest.get_browser_info(),
                                   secure_mode_return_url="https://www.ulule.com/")

        direct_payin.save()
        return direct_payin.credited_wallet

    @staticmethod
    def get_johns_transfer(recreate=False):
        if BaseTestLive._johns_transfer is None or recreate:
            john = BaseTestLive.get_john()
            wallet1 = BaseTestLive.get_johns_wallet()
            wallet2 = BaseTestLive.create_new_wallet(john)

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
    def get_johns_transfer_sca(sca_context, amount):
        valid_john_sca_id = 'user_m_01JRG5WE99JYRCEBHZ8EKBRE8Y'
        valid_matrix_sca_id = 'user_m_01JRG4ZWZ85RNZDKKTSFRMG6ZW'
        john_sca = NaturalUserSca.get(valid_john_sca_id)
        matrix_sca = LegalUserSca.get(valid_matrix_sca_id)

        debited_wallet = BaseTestLive.create_new_wallet_with_money(john_sca)
        credited_wallet = BaseTestLive.create_new_wallet(matrix_sca)

        transfer = Transfer()
        transfer.author = john_sca
        transfer.credited_user = matrix_sca
        transfer.debited_funds = Money(amount=amount, currency='EUR')
        transfer.fees = Money(amount=0, currency='EUR')
        transfer.debited_wallet = debited_wallet
        transfer.credited_wallet = credited_wallet
        transfer.sca_context = sca_context
        return Transfer(**transfer.save())

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

            data = {
                'data': card_registration.preregistration_data,
                'accessKeyRef': card_registration.access_key,
                'cardNumber': '4970107111111119',
                'cardExpirationDate': '1229',
                'cardCvx': '123'
            }
            headers = {
                'content-type': 'application/x-www-form-urlencoded'
            }
            registration_data_response = requests.post(card_registration.card_registration_url, data=data,
                                                       headers=headers)
            card_registration.registration_data = registration_data_response.text
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

            data = {
                'data': card_registration.preregistration_data,
                'accessKeyRef': card_registration.access_key,
                'cardNumber': '4970107111111119',
                'cardExpirationDate': '1229',
                'cardCvx': '123'
            }
            headers = {
                'content-type': 'application/x-www-form-urlencoded'
            }
            registration_data_response = requests.post(card_registration.card_registration_url, data=data,
                                                       headers=headers)
            card_registration.registration_data = registration_data_response.text
            card_registration.save()
            BaseTestLive._johns_card = card_registration.card
        return BaseTestLive._johns_card

    @staticmethod
    def get_oauth_manager():
        return BaseTestLive._oauth_manager

    @staticmethod
    def create_new_deposit():
        user = BaseTestLive.get_john()
        debited_funds = Money(amount=1000, currency='EUR')
        card_registration = BaseTestLive.create_new_card_registration_for_deposit()

        params = {
            "author_id": user.id,
            "debited_funds": debited_funds,
            "card_id": card_registration.card_id,
            "secure_mode_return_url": "http://lorem",
            "ip_address": "2001:0620:0000:0000:0211:24FF:FE80:C12C",
            "browser_info": BaseTest.get_browser_info()
        }

        deposit = Deposit(**params)

        return Deposit(**deposit.save())

    @staticmethod
    def create_new_card_registration_for_deposit():
        card_params = {
            "user": BaseTestLive.get_john(),
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        data = {
            'data': card_registration.preregistration_data,
            'accessKeyRef': card_registration.access_key,
            'cardNumber': '4970107111111119',
            'cardExpirationDate': '1229',
            'cardCvx': '123'
        }
        headers = {
            'content-type': 'application/x-www-form-urlencoded'
        }
        registration_data_response = requests.post(card_registration.card_registration_url, data=data,
                                                   headers=headers)
        card_registration.registration_data = registration_data_response.text

        return CardRegistration(**card_registration.save())

    @staticmethod
    def create_new_virtual_account():
        BaseTestLive.get_john()
        wallet = BaseTestLive.get_johns_wallet()

        virtual_account = VirtualAccount()
        virtual_account.wallet_id = wallet.id
        virtual_account.country = 'FR'
        virtual_account.virtual_account_purpose = 'COLLECTION'

        return VirtualAccount(**virtual_account.save())

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
