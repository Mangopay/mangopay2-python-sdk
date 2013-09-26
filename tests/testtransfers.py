import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.transfer import Transfer


class Test_Transfers(TestBase):
    "Tests basic methods for transfers"
     
    def test_Transfers_Create(self):
       john = self.getJohn()
       transfer = self.getJohnsTransfer()
       creditedWallet = self.sdk.wallets.Get(transfer.CreditedWalletId)
       self.assertTrue(int(transfer.Id) > 0)
       self.assertEqual(transfer.AuthorId, john.Id)
       self.assertEqual(100, creditedWallet.Balance.Amount)   
    
    def test_Transfers_Get(self):
       john = self.getJohn()
       transfer = self.getJohnsTransfer()
       getTransfer = self.sdk.transfers.Get(transfer.Id)
       self.assertEqual(transfer.Id, getTransfer.Id)
       self.assertEqual(getTransfer.AuthorId, john.Id)
       self.assertEqual(getTransfer.CreditedUserId, john.Id)
       self.assertEqualInputProps(transfer, getTransfer)

    def test_Transfers_CreateRefund(self):
        # will create 2 wallets
        transfer = self.getJohnsTransfer()
        walletCredited = self.sdk.wallets.Get(transfer.CreditedWalletId)
        walletDebited = self.sdk.wallets.Get(transfer.DebitedWalletId)
        self.assertTrue(int(transfer.Id) > 0)
        self.assertEqual(walletCredited.Balance.Amount, int(transfer.DebitedFunds.Amount))

        refund = self.getJohnsRefundForTransfer(transfer)
        self.assertTrue(int(refund.Id) > 0)
        self.assertTrue(refund.DebitedFunds.Amount, transfer.DebitedFunds.Amount)
        self.assertTrue(walletCredited.Balance.Amount, 0)
        self.assertEqual('TRANSFER', refund.Type)
        self.assertEqual('REFUND', refund.Nature)
