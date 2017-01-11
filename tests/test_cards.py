# -*- coding: utf-8 -*-
from tests import settings

try:
    import urllib.parse as urlrequest
except ImportError:
    import urllib as urlrequest

from .resources import Card, CardRegistration
from .test_base import BaseTest

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
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169419/cards',
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
            'cardNumber': '4970100000000154',
            'cardCvx': '123',
            'cardExpirationDate': '0120',
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

    def test_desactive_card(self):
        # self.card.active = False
        # self.card.save()
        pass
