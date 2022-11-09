# -*- coding: utf-8 -*-
import responses

from mangopay.resources import CountryAuthorization
from tests import settings
from tests.test_base import BaseTest


class CountryAuthorizationsTest(BaseTest):
    @responses.activate
    def test_get_specific_country_authorizations(self):
        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + 'countries/FR/authorizations',
                'body': {
                    "CountryCode": "FR",
                    "CountryName": "France",
                    "Authorization": {
                        "BlockUserCreation": False,
                        "BlockBankAccountCreation": False,
                        "BlockPayout": False
                    },
                    "LastUpdate": 1644574249
                },
                'status': 200
            }])

        authorizations = CountryAuthorization.get_country_authorizations("FR")

        self.assertIsNotNone(authorizations)

    @responses.activate
    def test_get_all_countries_authorizations(self):
        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + 'countries/authorizations',
                'body': [
                    {
                        "CountryCode": "FR",
                        "CountryName": "France",
                        "Authorization": {
                            "BlockUserCreation": False,
                            "BlockBankAccountCreation": False,
                            "BlockPayout": False
                        },
                        "LastUpdate": 1644574249
                    }
                ],
                'status': 200
            }])

        authorizations = CountryAuthorization.get_all_countries_authorizations()

        self.assertIsNotNone(authorizations)
        self.assertIsNotNone(authorizations.data[0])
