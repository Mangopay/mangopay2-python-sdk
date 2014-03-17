import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.refund import Refund
from mangopaysdk.tools.enums import TransactionType, TransactionStatus


class Test_Refunds(TestBase):
    """
    Tests basic methods for refunds
    """
    
    def test_Refund_GetForTransfer(self):
        transfer = self.getJohnsTransfer()
        refund = self.getJohnsRefundForTransfer(transfer)        
        user = self.getJohn()        
        getRefund = self.sdk.refunds.Get(refund.Id)
        self.assertEqual(getRefund.Id, refund.Id)
        self.assertEqual(getRefund.InitialTransactionId, transfer.Id)
        self.assertEqual(getRefund.AuthorId, user.Id)
        self.assertEqual(getRefund.Type, TransactionType.TRANSFER)
    
    def test_Refund_GetForPayIn(self):
        payIn = self.getJohnsPayInCardDirect()
        refund = self.getJohnsRefundForPayIn(payIn)
        user = self.getJohn()
        getRefund = self.sdk.refunds.Get(refund.Id)
        self.assertEqual(getRefund.Id, refund.Id)
        self.assertEqual(getRefund.InitialTransactionId, payIn.Id)
        self.assertEqual(getRefund.AuthorId, user.Id)
        self.assertEqual(getRefund.Type, TransactionType.PAYOUT)
