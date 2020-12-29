# -*- coding: utf-8 -*-
from tests import settings
from tests.resources import BankingAliasIBAN, BankingAlias
from tests.test_base import BaseTest, BaseTestLive

import responses


class BankingAliasesTest(BaseTest):

    @responses.activate
    def test_banking_alias(self):
        self.mock_natural_user()
        self.mock_natural_user_wallet()

        self.register_mock([
            {
                'method': responses.POST,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169420/bankingaliases/iban',
                'body': {
                    "OwnerName": "Victor",
                    "IBAN": "LU32062DZDP2JLJU9RP3",
                    "BIC": "MPAYFRP1EMI",
                    "CreditedUserId":"25337926",
                    "Country":"LU",
                    "Tag": "null",
                    "CreationDate":1494384060,
                    "Active": True,
                    "Type":"IBAN",
                    "Id":"25337928",
                    "WalletId":"1169420"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/bankingaliases/25337928',
                'body': {
                    "OwnerName": "Victor",
                    "IBAN": "LU32062DZDP2JLJU9RP3",
                    "BIC": "MPAYFRP1EMI",
                    "CreditedUserId":"25337926",
                    "Country":"LU",
                    "Tag": "null",
                    "CreationDate":1494384060,
                    "Active": True,
                    "Type":"IBAN",
                    "Id":"25337928",
                    "WalletId":"1169420"
                },
                'status': 200
            },
            {
                'method': responses.GET,
                'url': settings.MANGOPAY_API_SANDBOX_URL+settings.MANGOPAY_CLIENT_ID+'/wallets/1169420/bankingaliases',
                'body': [
                    {
                    "OwnerName": "Victor",
                    "IBAN": "LU32062DZDP2JLJU9RP3",
                    "BIC": "MPAYFRP1EMI",
                    "CreditedUserId":"25337926",
                    "Country":"LU",
                    "Tag": "null",
                    "CreationDate":1494384060,
                    "Active": True,
                    "Type":"IBAN",
                    "Id":"25337928",
                    "WalletId":"1169420"
                }
                ],
                'status': 200
            }])

        bankingAlias = BankingAliasIBAN(
            wallet = self.natural_user_wallet,
            credited_user = self.natural_user,
            owner_name = self.natural_user.first_name,
            country ='LU'
        )
        bankingAlias.save()

        self.assertEqual(bankingAlias.country, 'LU')
        self.assertEqual(bankingAlias.iban, 'LU32062DZDP2JLJU9RP3')

        walletBankingAliases = BankingAlias(
            wallet = self.natural_user_wallet
        )
        allBankingAliases = walletBankingAliases.all()

        self.assertEqual(allBankingAliases[0].id, bankingAlias.id)
        self.assertEqual(allBankingAliases[0].wallet_id, bankingAlias.wallet_id)