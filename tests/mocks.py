# -*- coding: utf-8 -*-
import unittest

from datetime import date

import json
import time
import sys
import re
import os

import responses

from tests import settings


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
            'url': settings.MANGOPAY_API_SANDBOX_URL+'oauth/token',
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
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/natural',
            'body': get_fixture('natural_user') % time.mktime(date.today().timetuple()),
            'status': 200
        })

    def mock_legal_user(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/legal',
            'body': get_fixture('legal_user') % time.mktime(date.today().timetuple()),
            'status': 200
        })

    def mock_user_wallet(self):
        self.register_mock({
            'method': responses.POST,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
            'body': get_fixture('user_wallet'),
            'status': 200
        })

    def mock_natural_user_wallet(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': get_fixture('natural_user_wallet'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169420',
                'body': get_fixture('natural_user_wallet'),
                'status': 200
            }])

    def mock_legal_user_wallet(self):
        return self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': get_fixture('legal_user_wallet'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169421',
                'body': get_fixture('legal_user_wallet'),
                'status': 200
            }])

    def mock_natural_user_wallet_9(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': get_fixture('natural_user_wallet_9'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169420',
                'body': get_fixture('natural_user_wallet_9'),
                'status': 200
            }])

    def mock_legal_user_wallet_89(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': get_fixture('legal_user_wallet_89'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169421',
                'body': get_fixture('legal_user_wallet_89'),
                'status': 200
            }])

    def mock_legal_user_wallet_99(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets',
                'body': get_fixture('legal_user_wallet_99'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169421',
                'body': get_fixture('legal_user_wallet_99'),
                'status': 200
            }])

    def mock_card(self):
        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/cardregistrations',
                'body': get_fixture('cardregistrations'),
                'status': 200
            },
            {
                'method': responses.PUT,
                'url': re.compile(r''+settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/cardregistrations/\d+'),
                'body': get_fixture('cardregistrations_update'),
                'status': 200
            },
            {
                'method': responses.GET,
                'url': re.compile(r''+settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/cards/\d+'),
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
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users',
            'body': get_fixture('user_list_full'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_2_per_page_page1(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users?page=1&per_page=2',
            'body': get_fixture('user_list_2_per_page_page1'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_3_per_page_page2(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users?page=2&per_page=3',
            'body': get_fixture('user_list_3_per_page_page2'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_page1(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users?page=1',
            'body': get_fixture('user_list_page1'),
            'status': 200,
            'match_querystring': True
        })

    def mock_user_list_2_per_page(self):
        self.register_mock({
            'method': responses.GET,
            'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users?per_page=2',
            'body': get_fixture('user_list_2_per_page'),
            'status': 200,
            'match_querystring': True
        })
