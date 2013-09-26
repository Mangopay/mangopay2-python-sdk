from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.types.money import Money
from mangopaysdk.entities.wallet import Wallet
from mangopaysdk.entities.transaction import Transaction
from mangopaysdk.tools.enums import *
from mangopaysdk.tools.filtertransactions import FilterTransactions
from tests.testbase import TestBase


class Test_ApiWallets(TestBase):

    def test_Wallets_Create(self):
        john = self.getJohn()
        wallet = self.getJohnsWallet()
        
        self.assertTrue(int(wallet.Id) > 0)
        self.assertTrue(john.Id in wallet.Owners)
    
    def test_Wallets_Get(self):
        john = self.getJohn()
        wallet = self.getJohnsWallet()        
        getWallet = self.sdk.wallets.Get(wallet.Id)
        
        self.assertEqual(wallet.Id, getWallet.Id)
        self.assertTrue(john.Id in getWallet.Owners)
    
    def test_Wallets_Update(self):
        wallet = self.getJohnsWallet()
        wallet.Description = 'New description to test'
        updatedWallet = self.sdk.wallets.Update(wallet)
        
        self.assertEqual(wallet.Id, updatedWallet.Id)
        self.assertEqual('New description to test', updatedWallet.Description)
    
    
    def test_Wallets_Transactions(self):
        john = self.getJohn()
        wallet = self.getJohnsWallet()
        payIn = self.getJohnsPayInCardWeb()

        pagination = Pagination(1, 1)
        filter = FilterTransactions()
        filter.Type = TransactionType.PAYIN
        transactions = self.sdk.wallets.GetTransactions(wallet.Id, pagination, filter)

        self.assertEqual(len(transactions), 1)
        self.assertIsInstance(transactions[0], Transaction)
        self.assertEqual(transactions[0].AuthorId, john.Id)
        self.assertEqualInputProps(transactions[0], payIn)
