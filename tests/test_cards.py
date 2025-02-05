# -*- coding: utf-8 -*-
import time

from tests import settings

try:
    import urllib.parse as urlrequest
except ImportError:
    import urllib as urlrequest

from mangopay.resources import Card, CardRegistration, CardValidation
from tests.test_base import BaseTest
from tests.test_base import BaseTestLive

import requests
import responses


class CardsTest(BaseTest):
    @responses.activate
    def test_cards_registration(self):
        """
        Card registration process:
        - Create a CardRegistration object
        - Receive a CardRegistration object
        - Send card details to the Tokenization server
        - Receive RegistrationData
        - Edit the CardRegistration with received RegistrationData
        """

        self.mock_natural_user()
        self.mock_card()
        self.mock_tokenization_request()
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1169419/cards',
            'body': [
                {
                    "ExpirationDate": "1214",
                    "Alias": "497010XXXXXX4406",
                    "CardType": "CB",
                    "Country": "",
                    "Product": "",
                    "BankCode": "",
                    "Active": True,
                    "Currency": "XXX",
                    "Validity": "VALID",
                    "UserId": "1167495",
                    "Id": "1167507",
                    "Tag": None,
                    "CreationDate": 1382608428
                }
            ],
            'status': 200
        })

        # Create a CardRegistration object
        card_params = {
            "user": self.natural_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        for key, value in card_params.items():
            self.assertEqual(getattr(card_registration, key), value)

        self.assertIsNotNone(card_registration.get_pk())

        # Send card details to the Tokenization server
        response = requests.post(card_registration.card_registration_url, urlrequest.urlencode({
            'cardNumber': '4970107111111119',
            'cardCvx': '123',
            'cardExpirationDate': '0128',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        }))

        # Edit the CardRegistration with received RegistrationData
        previous_pk = card_registration.get_pk()

        card_registration.registration_data = response.text
        card_registration.save()

        self.assertEqual(previous_pk, card_registration.get_pk())
        self.assertIsNotNone(card_registration.registration_data)
        self.assertEqual(card_registration.registration_data, response.text)
        self.assertEqual(card_registration.status, 'VALIDATED')
        self.assertEqual(card_registration.result_message, 'Success')
        self.assertEqual(card_registration.result_code, '000000')
        self.assertIsNotNone(card_registration.card_id)  # We now have a card id!

        # Fetch the new card thanks to card_id
        self.assertIsNotNone(card_registration.card_id)

        card = Card.get(card_registration.card_id)
        self.assertIsNotNone(card.get_pk())
        self.assertEqual(card.get_pk(), card_registration.card_id)

        # Retrieve user's cards
        self.assertEqual(len(self.natural_user.cards.all()), 1)
        self.assertEqual(self.natural_user.cards.all()[0], card)
        self.assertEqual(self.natural_user.cards.get(card.id), card)

    @responses.activate
    def test_cards_for_fingerprint(self):
        self.mock_natural_user()
        self.mock_card()
        self.mock_tokenization_request()
        self.register_mock([{
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1169419/cards',
            'body': [
                {
                    "ExpirationDate": "1214",
                    "Alias": "497010XXXXXX4406",
                    "CardType": "CB",
                    "Country": "",
                    "Product": "",
                    "BankCode": "",
                    "Active": True,
                    "Currency": "XXX",
                    "Validity": "VALID",
                    "UserId": "1167495",
                    "Id": "1167507",
                    "Tag": None,
                    "CreationDate": 1382608428
                }
            ],
            'status': 200
        }, {
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/cards/fingerprints/c188a617d3ed42169a7d91f7485c65f3',
            'body': [
                {
                    "ExpirationDate": "1214",
                    "Alias": "497010XXXXXX4406",
                    "CardType": "CB",
                    "Country": "",
                    "Product": "",
                    "BankCode": "",
                    "Active": True,
                    "Currency": "XXX",
                    "Validity": "VALID",
                    "UserId": "1167495",
                    "Id": "1167507",
                    "Tag": None,
                    "CreationDate": 1382608428,
                    "Fingerprint": "c188a617d3ed42169a7d91f7485c65f3"
                }
            ],
            'status': 200
        }])

        card_params = {
            "user": self.natural_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        for key, value in card_params.items():
            self.assertEqual(getattr(card_registration, key), value)

        self.assertIsNotNone(card_registration.get_pk())

        response = requests.post(card_registration.card_registration_url, urlrequest.urlencode({
            'cardNumber': '4970107111111119',
            'cardCvx': '123',
            'cardExpirationDate': '0128',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        }))

        card_registration.registration_data = response.text
        card_registration.save()

        card = Card.get(card_registration.card_id)
        cards = Card.get_by_fingerprint(card.fingerprint)

        self.assertTrue(len(cards) > 0)

        for c in cards:
            self.assertEqual(c.fingerprint, card.fingerprint)

    @responses.activate
    def test_desactive_card(self):
        self.mock_natural_user()
        self.mock_card()
        self.mock_tokenization_request()
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/1169419/cards',
            'body': [
                {
                    "ExpirationDate": "1214",
                    "Alias": "497010XXXXXX4406",
                    "CardType": "CB",
                    "Country": "",
                    "Product": "",
                    "BankCode": "",
                    "Active": True,
                    "Currency": "XXX",
                    "Validity": "VALID",
                    "UserId": "1167495",
                    "Id": "1167507",
                    "Tag": None,
                    "CreationDate": 1382608428
                }
            ],
            'status': 200
        })
        self.register_mock({
            'method': responses.PUT,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/cards/1167507',
            'body': {
                "ExpirationDate": "1214",
                "Alias": "497010XXXXXX4406",
                "CardType": "CB",
                "Country": "",
                "Product": "",
                "BankCode": "",
                "Active": False,
                "Currency": "XXX",
                "Validity": "VALID",
                "UserId": "1167495",
                "Id": "1167507",
                "Tag": None,
                "CreationDate": 1382608428
            },
            'status': 200
        })

        # Create a CardRegistration object
        card_params = {
            "user": self.natural_user,
            "currency": 'EUR'
        }
        card_registration = CardRegistration(**card_params)
        card_registration.save()

        # Send card details to the Tokenization server
        response = requests.post(card_registration.card_registration_url, urlrequest.urlencode({
            'cardNumber': '4970107111111119',
            'cardCvx': '123',
            'cardExpirationDate': '0128',
            'accessKeyRef': card_registration.access_key,
            'data': card_registration.preregistration_data
        }))

        # Edit the CardRegistration with received RegistrationData
        previous_pk = card_registration.get_pk()

        card_registration.registration_data = response.text
        card_registration.save()

        card = Card.get(card_registration.card_id)

        card.active = False
        card.save()

        self.assertIs(card.active, False)


class CardsLiveTest(BaseTestLive):

    def test_getCardPreAuthorizations(self):
        card = BaseTestLive.get_johns_card()

        preauthorizations_page = card.get_pre_authorizations()

        self.assertIsNotNone(preauthorizations_page.data)
        self.assertIsInstance(preauthorizations_page.data, list)

    def test_getCardTransactions(self):
        card = BaseTestLive.get_johns_card()

        time.sleep(2)
        transactions_page = card.get_transactions()

        self.assertIsNotNone(transactions_page.data)
        self.assertIsInstance(transactions_page.data, list)

    def test_cardValidation(self):
        user = BaseTestLive.get_john()

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

        card_validation = CardValidation()
        card_validation.author = user
        card_validation.tag = "test"
        card_validation.secure_mode_return_url = "http://www.example.com/"
        card_validation.ip_address = "2001:0620:0000:0000:0211:24FF:FE80:C12C"
        card_validation.browser_info = BaseTest.get_browser_info()
        card_validation.payment_category = 'TelephoneOrder'

        validation_response = card_validation.validate(card_id)

        self.assertIsNotNone(validation_response)
        self.assertIsNotNone(validation_response['id'])
        self.assertEqual('TelephoneOrder', validation_response['payment_category'])

    def test_getCardValidation(self):
        user = BaseTestLive.get_john()

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

        card_validation = CardValidation()
        card_validation.author = user
        card_validation.tag = "test"
        card_validation.secure_mode_return_url = "http://www.example.com/"
        card_validation.ip_address = "2001:0620:0000:0000:0211:24FF:FE80:C12C"
        card_validation.browser_info = BaseTest.get_browser_info()

        validation_response = card_validation.validate(card_id)

        get_card_validation = CardValidation()
        get_card_validation.id = validation_response['id']
        get_card_validation_response = get_card_validation.get_card_validation(card_id)

        self.assertIsNotNone(get_card_validation_response.data[0])
        self.assertIsNotNone(get_card_validation_response.data[0].id)
        self.assertEqual(get_card_validation_response.data[0].id, validation_response['id'])
