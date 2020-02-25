# -*- coding: utf-8 -*-
import responses

from tests import settings
from tests.resources import ClientWallet
from tests.test_base import BaseTest, BaseTestLive


class ClientWalletsTest(BaseTest):

    @responses.activate
    def test_client_wallet(self):
        self.register_mock([
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/clients/wallets',
                'body': [
                    {
                        "Balance": {
                            "Currency": "EUR",
                            "Amount": 1422
                        },
                        "Currency": "EUR",
                        "FundsType": "FEES",
                        "Id": "FEES_EUR",
                        "Tag": None,
                        "CreationDate": 1463495506
                    },
                    {
                        "Balance": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Currency": "EUR",
                        "FundsType": "CREDIT",
                        "Id": "CREDIT_EUR",
                        "Tag": None,
                        "CreationDate": 1463496443
                    },
                    {
                        "Balance": {
                            "Currency": "PLN",
                            "Amount": 0
                        },
                        "Currency": "PLN",
                        "FundsType": "CREDIT",
                        "Id": "CREDIT_PLN",
                        "Tag": None,
                        "CreationDate": 1465283852
                    }
                ],
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/clients/wallets/FEES/EUR/',
                'body':
                    {
                        "Balance": {
                            "Currency": "EUR",
                            "Amount": 1422
                        },
                        "Currency": "EUR",
                        "FundsType": "FEES",
                        "Id": "FEES_EUR",
                        "Tag": None,
                        "CreationDate": 1463495506
                    },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/clients/wallets/CREDIT',
                'body': [
                    {
                        "Balance": {
                            "Currency": "EUR",
                            "Amount": 0
                        },
                        "Currency": "EUR",
                        "FundsType": "CREDIT",
                        "Id": "CREDIT_EUR",
                        "Tag": None,
                        "CreationDate": 1463496443
                    },
                    {
                        "Balance": {
                            "Currency": "PLN",
                            "Amount": 0
                        },
                        "Currency": "PLN",
                        "FundsType": "CREDIT",
                        "Id": "CREDIT_PLN",
                        "Tag": None,
                        "CreationDate": 1465283852
                    }
                ],
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL + settings.MANGOPAY_CLIENT_ID + '/clients/wallets/FEES',
                'body': [
                    {
                        "Balance": {
                            "Currency": "EUR",
                            "Amount": 1422
                        },
                        "Currency": "EUR",
                        "FundsType": "FEES",
                        "Id": "FEES_EUR",
                        "Tag": None,
                        "CreationDate": 1463495506
                    }
                ],
                'status': 200
            }
        ])

        wallet_params = {
            "currency": "EUR",
            "funds_type": "FEES",
            "id": "FEES_EUR"
        }

        wallet = ClientWallet(**wallet_params)
        
        #found_wallet = ClientWallet.get('FEES', 'EUR')
        #self.assertEqual(wallet, found_wallet)
        #self.assertEqual(wallet.funds_type, found_wallet.funds_type)

        wallets_page = ClientWallet.all()
        all_wallets = wallets_page.data

        fees_wallets_page = ClientWallet.all_by_funds_type('FEES')

        default_wallets_page = ClientWallet.all_by_funds_type('DEFAULT')

        credit_wallets_page = ClientWallet.all_by_funds_type('CREDIT')

        self.assertEqual(all_wallets[:1], fees_wallets_page.data)

        self.assertEqual(all_wallets[1:], credit_wallets_page.data)

        self.assertEqual(default_wallets_page.data, all_wallets)


class ClientWalletsLiveTest(BaseTestLive):

    def test_ViewAllClientWallets(self):
        wallets = None
        try:
            wallets = ClientWallet.all()
        except Exception as ex:
            self.assertIsNone(ex)

        if not wallets:
            self.assertFalse("Cannot test getting client's wallet because there is no any wallet for client.")

    def test_ViewClientWalletsByFunds(self):
        credit_wallets = None
        fees_wallets = None
        default_wallets = None

        try:
            credit_wallets = ClientWallet.all_by_funds_type('CREDIT')
            fees_wallets = ClientWallet.all_by_funds_type('FEES')
            default_wallets = ClientWallet.all_by_funds_type('DEFAULT')
        except Exception as ex:
            self.assertisNone(ex)

        wallet = None
        result = None

        if not credit_wallets:
            self.assertFalse("Cannot test client's credit wallets because there is none.")
        else:
            wallet = credit_wallets[0]
        if not fees_wallets:
            self.assertFalse("Cannot test client's fees wallets because there is none.")
        else:
            wallet = fees_wallets[0]
        if not default_wallets:
            self.assertFalse("Cannot test client's default wallets because there is none.")
        else:
            wallet = default_wallets[0]

        if wallet is not None:
            result = ClientWallet.get(wallet.funds_type, wallet.currency)
            self.assertIsNotNone(result)
            self.assertTrue(result.funds_type == wallet.funds_type)
            self.assertTrue(result.currency == wallet.currency)
