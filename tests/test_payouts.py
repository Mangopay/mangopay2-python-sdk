# -*- coding: utf-8 -*-
from tests import settings
from tests.resources import BankAccount, BankWirePayOut, PayOutEligibility
from tests.test_base import BaseTest

from mangopay.utils import Money, Address

import responses


class PayOutsTest(BaseTest):
    @responses.activate
    def test_create_bank_wire_payout(self):
        self.mock_legal_user()
        self.mock_user_wallet()

        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/users/1169420/bankaccounts/IBAN',
                'body': {
                    "UserId": "1169420",
                    "Type": "IBAN",
                    "OwnerName": "MangoPay",
                    "OwnerAddress": {
                        "AddressLine1": "AddressLine1",
                        "AddressLine2": "AddressLine2",
                        "City": "City",
                        "Region": "Region",
                        "PostalCode": "11222",
                        "Country": "FR"
                    },
                    "IBAN": "FR7630004000031234567890143",
                    "BIC": "BNPAFRPP",
                    "Id": "1169675",
                    "Tag": "custom tag",
                    "CreationDate": 1383561267
                },
                'status': 200
            },
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payouts/bankwire',
                'body': {
                    "Id": 30047,
                    "CreditedFunds": None,
                    "BankWireRef": "John Doe's trousers",
                    "PayoutModeRequested": "STANDARD",
                    "DebitedFunds": {"Currency": "EUR", "Amount": 1000},
                    "BankAccountId": 6784645,
                    "AuthorId": 6784642,
                    "Tag": "Custom data",
                    "Fees": {"Currency": "EUR", "Amount": 100},
                    "DebitedWalletId": 6784644
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/payouts/30047',
                'body': {
                    "Id": 30047,
                    "Tag": "custom tag",
                    "CreationDate": 1374232891,
                    "AuthorId": "20164",
                    "CreditedUserId": None,
                    "DebitedFunds": {
                        "Currency": "EUR",
                        "Amount": 100
                    },
                    "CreditedFunds": {
                        "Currency": "EUR",
                        "Amount": "1000"
                    },
                    "Fees": {
                        "Currency": "EUR",
                        "Amount": "100"
                    },
                    "Status": "SUCCEEDED",
                    "ResultCode": "00000",
                    "ExecutionDate": 1374233532,
                    "Type": "PAY_OUT",
                    "Nature": "NORMAL",
                    "DebitedWalletId": "30025",
                    "BankAccountId": "30027",
                    "BankWireRef": "John Doe's trousers",
                    "PayoutModeRequested": "STANDARD"
                },
                'status': 200
            }])

        params = {
            "owner_name": "Victor Hugo",
            "user": self.legal_user,
            "type": "IBAN",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "iban": "FR7630004000031234567890143",
            "bic": "BNPAFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)
        bankaccount.save()

        bank_wire_payout_params = {
            "tag": "Custom data",
            "author": self.legal_user,
            "debited_funds": Money(amount=1000, currency='EUR'),
            "fees": Money(amount=100, currency='EUR'),
            "debited_wallet": self.legal_user_wallet,
            "bank_account": bankaccount,
            "bank_wire_ref": "John Doe's trousers",
            "payout_mode_requested": "STANDARD"
        }
        bank_wire_payout = BankWirePayOut(**bank_wire_payout_params)

        self.assertIsNone(bank_wire_payout.get_pk())
        bank_wire_payout.save()
        self.assertIsInstance(bank_wire_payout, BankWirePayOut)
        self.assertEqual(bankaccount, bank_wire_payout.bank_account)
        self.assertEqual(bank_wire_payout.debited_funds.amount, 1000)
        bank_wire_payout_params.pop('debited_funds')

        self.assertEqual(bank_wire_payout.fees.amount, 100)
        bank_wire_payout_params.pop('fees')

        for key, value in bank_wire_payout_params.items():
            self.assertEqual(getattr(bank_wire_payout, key), value)

        self.assertIsNotNone(bank_wire_payout.get_pk())
        # test_retrieve_payouts
        retrieved_payout = BankWirePayOut.get(bank_wire_payout.get_pk())
        self.assertIsNotNone(retrieved_payout.get_pk())
        self.assertIsInstance(retrieved_payout, BankWirePayOut)

        self.assertEqual(getattr(retrieved_payout, 'id'), bank_wire_payout.get_pk())

        # get_bank_wire = BankWirePayOut.get_bankwire(109791242)

    def test_check_eligibility(self):
        params = {
            "owner_name": "Victor Hugo",
            "user": self.legal_user,
            "type": "IBAN",
            "owner_address": Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                     city='City', region='Region',
                                     postal_code='11222', country='FR'),
            "iban": "FR7630004000031234567890143",
            "bic": "BNPAFRPP",
            "tag": "custom tag"
        }
        bankaccount = BankAccount(**params)
        bankaccount.save()

        eligibility = {
            "author": self.legal_user,
            "debited_funds": Money(amount=10, currency='EUR'),
            "debited_wallet": self.legal_user_wallet,
            "bank_account": bankaccount,
            "payout_mode_requested": "INSTANT_PAYMENT"
        }

        check_eligibility = PayOutEligibility(**eligibility)
        result = check_eligibility.check_eligibility()
        self.assertIsNotNone(result)
        instant_payout = result.get('instant_payout')
        self.assertIsNotNone(instant_payout)
