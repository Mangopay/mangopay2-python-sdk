# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import unittest
from datetime import datetime

import responses

from mangopay.utils import timestamp_from_date
from tests import settings

#re._pattern_type = re.Pattern

today = datetime.utcnow().date()
today_timestamp = timestamp_from_date(today)


def get_fixture(name):
    path = os.path.abspath(__file__)
    fixtures_path = os.path.join(os.path.dirname(path), 'fixtures')
    filepath = os.path.join(fixtures_path, '%s.json' % name)

    if sys.version_info < (3, 0):
        with open(filepath, 'r') as file:
            return file.read()

    with open(filepath, newline='', encoding='utf-8') as file:
        return file.read()


class RegisteredMocks(unittest.TestCase):

    def setUp(self):
        self.mock_oauth()

    def register_mock(self, data):
        match_querystring = False

        if 'match_querystring' in data:
            match_querystring = data['match_querystring'] or False

        if isinstance(data, list):
            for d in data:
                self.register_mock(d)
        else:
            if isinstance(data['body'], (dict, list)):
                data['body'] = json.dumps(data['body'])

            responses.add(data['method'], data['url'],
                          body=data['body'], status=data['status'],
                          content_type='application/json',
                          match_querystring=match_querystring)

    def mock_oauth(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + 'oauth/token',
            'body': {
                "access_token": "67b036bd007c40378d4be5a934f197e6",
                "token_type": "Bearer",
                "expires_in": 3600
            },
            'status': 200
        })

    def mock_natural_user(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/natural',
            'body': get_fixture('natural_user') % today_timestamp,
            'status': 200
        })

    def mock_legal_user(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/legal',
            'body': get_fixture('legal_user') % today_timestamp,
            'status': 200
        })

    def mock_declarative_user(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/natural',
            'body': get_fixture('declarative_user') % today_timestamp,
            'status': 200
        })

    def mock_user_wallet(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets',
            'body': get_fixture('user_wallet'),
            'status': 200
        })

    def mock_natural_user_wallet(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets',
                'body': get_fixture('natural_user_wallet'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets/1169420',
                'body': get_fixture('natural_user_wallet'),
                'status': 200
            }])

    def mock_legal_user_wallet(self):
        return self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets',
                'body': get_fixture('legal_user_wallet'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets/1169421',
                'body': get_fixture('legal_user_wallet'),
                'status': 200
            }])

    def mock_natural_user_wallet_9(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets',
                'body': get_fixture('natural_user_wallet_9'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets/1169420',
                'body': get_fixture('natural_user_wallet_9'),
                'status': 200
            }])

    def mock_legal_user_wallet_89(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets',
                'body': get_fixture('legal_user_wallet_89'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets/1169421',
                'body': get_fixture('legal_user_wallet_89'),
                'status': 200
            }])

    def mock_legal_user_wallet_99(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets',
                'body': get_fixture('legal_user_wallet_99'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/wallets/1169421',
                'body': get_fixture('legal_user_wallet_99'),
                'status': 200
            }])

    def mock_card(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/cardregistrations',
                'body': get_fixture('cardregistrations'),
                'status': 200
            },
            {
                'method': responses.PUT,
                'url': re.compile(
                    r'' + settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/cardregistrations/\d+'),
                'body': get_fixture('cardregistrations_update'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': re.compile(r'' + settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/cards/\d+'),
                'body': get_fixture('card'),
                'status': 200
            }])

    def mock_tokenization_request(self):
        self.register_mock({
            'method': responses.POST,
            'url': 'https://homologation-webpayment.payline.com/webpayment/getToken',
            'body': "data=gcpSOxwNHZutpFWmFCAYQu1kk25qPfJFdPaHT9kM3gKumDF3GeqSw8f-k8nh-s5OC3GNnhGoFONuAyg1RZQW6rVXooQ_ysKsz09HxQFEJfb-6H4zbY2Nnp1TliwkEFi4",
            'status': 200
        })

    def mock_user_list_full(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users',
            'body': get_fixture('user_list_full'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_2_per_page_page1(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users?page=1&per_page=2',
            'body': get_fixture('user_list_2_per_page_page1'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_3_per_page_page2(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users?page=2&per_page=3',
            'body': get_fixture('user_list_3_per_page_page2'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_page1(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users?page=1',
            'body': get_fixture('user_list_page1'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_2_per_page(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users?per_page=2',
            'body': get_fixture('user_list_2_per_page'),
            'status': 200,
            'match_querystring': True
        })

    def mock_ubo_declaration(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/11694190/kyc/ubodeclarations',
            'body': get_fixture('ubo_declaration') % '"Default Tag"',
            'status': 200
        })

    def mock_list_ubo_declarations(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/11694190/kyc/ubodeclarations',
            'body': get_fixture('list_ubo_declarations') % '"Default Tag"',
            'status': 200
        })

    def mock_get_ubo_declaration(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/11694190/kyc/ubodeclarations/122341',
            'body': get_fixture('ubo_declaration') % '"Default Tag"',
            'status': 200
        })

    def mock_ubo_creation(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/11694190/kyc/ubodeclarations/122341/ubos',
            'body': get_fixture('ubo'),
            'status': 200
        })

    def mock_get_ubo(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/11694190/kyc/ubodeclarations/122341/ubos/1232432',
            'body': get_fixture('ubo'),
            'status': 200
        })

    def mock_submit_ubo_declaration(self):
        self.register_mock({
            'method': responses.PUT,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/11694190/kyc/ubodeclarations/122341',
            'body': get_fixture('ubo_declaration_submit') % '"Default Tag"',
            'status': 200
        })

    def mock_update_ubo(self):
        self.register_mock({
            'method': responses.PUT,
            'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/users/11694190/kyc/ubodeclarations/122341/ubos/1232432',
            'body': get_fixture('ubo_update'),
            'status': 200
        })
