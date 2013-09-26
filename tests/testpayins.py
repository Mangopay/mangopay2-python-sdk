import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.payin import PayIn
from mangopaysdk.types.payinexecutiondetailsdirect import PayInExecutionDetailsDirect
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from mangopaysdk.types.payinexecutiondetailsweb import PayInExecutionDetailsWeb


class Test_PayIns(TestBase):
    "Tests methods for pay-ins"
    
    def test_PayIns_Create_CardWeb(self):
       payIn = self.getJohnsPayInCardWeb()
       self.assertTrue(int(payIn.Id) > 0)
       self.assertEqual(payIn.PaymentType, 'CARD')
       self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
       self.assertEqual(payIn.ExecutionType, 'WEB')
       self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsWeb)
    
    def test_PayIns_Get_CardWeb(self):
       payIn = self.getJohnsPayInCardWeb()
       getPayIn = self.sdk.payIns.Get(payIn.Id)
        
       self.assertEqual(payIn.Id, getPayIn.Id)
       self.assertEqual(payIn.PaymentType, 'CARD')
       self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
       self.assertEqual(payIn.ExecutionType, 'WEB')
       self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsWeb)
       self.assertEqualInputProps(payIn, getPayIn)
       self.assertEqual(getPayIn.Status, 'CREATED')
       self.assertIsNone(getPayIn.ExecutionDate)
       self.assertIsNotNone(getPayIn.ExecutionDetails.RedirectURL)
       self.assertIsNotNone(getPayIn.ExecutionDetails.ReturnURL)

       def test_PayIns_Create_CardDirect(self):
        johnWallet = self.getJohnsWallet()
        beforeWallet = self.sdk.wallets.Get(johnWallet.Id)
        payIn = self.getJohnsPayInCardDirect()
        wallet = self.sdk.wallets.Get(johnWallet.Id)
        user = self.getJohn()
        self.assertTrue(int(payIn.Id) > 0)
        self.assertEqual(wallet.Id, payIn.CreditedWalletId)
        self.assertEqual('CARD', payIn.PaymentType)
        self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
        self.assertEqual('DIRECT', payIn.ExecutionType)
        self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsDirect)
        self.assertIsInstance(payIn.DebitedFunds, Money)
        self.assertIsInstance(payIn.CreditedFunds, Money)
        self.assertIsInstance(payIn.Fees, Money)
        self.assertEqual(user.Id, payIn.AuthorId)
        self.assertEqual(wallet.Balance.Amount, beforeWallet.Balance.Amount + payIn.CreditedFunds.Amount)
        self.assertEqual('SUCCEEDED', payIn.Status)
        self.assertEqual('PAYIN', payIn.Type)
    
    def test_PayIns_Get_CardDirect(self):
        payIn = self.getJohnsPayInCardDirect()        
        getPayIn = self.sdk.payIns.Get(payIn.Id)        
        self.assertEqual(payIn.Id, getPayIn.Id)
        self.assertEqual(payIn.PaymentType, 'CARD')
        self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
        self.assertEqual(payIn.ExecutionType, 'DIRECT')
        self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsDirect)
        self.assertEqual(payIn.Id, getPayIn.Id)
        self.assertIsNotNone(getPayIn.ExecutionDetails.CardId)
    
    def test_PayIns_CreateRefund_CardDirect(self):
        wallet = self.getJohnsWallet()
        payIn = self.getJohnsPayInCardDirect(wallet)
        walletAfterPayIn = self.sdk.wallets.Get(wallet.Id)
        self.assertEqual(walletAfterPayIn.Balance.Amount, payIn.DebitedFunds.Amount)
        self.assertTrue(int(payIn.Id) > 0)

        refund = self.getJohnsRefundForPayIn(payIn)
        walletAfterRefund = self.sdk.wallets.Get(wallet.Id)
        self.assertTrue(int(refund.Id) > 0)
        self.assertTrue(refund.DebitedFunds.Amount, payIn.DebitedFunds.Amount)
        self.assertEqual(walletAfterRefund.Balance.Amount, walletAfterPayIn.Balance.Amount - payIn.DebitedFunds.Amount)
        self.assertEqual('PAYOUT', refund.Type)
        self.assertEqual('REFUND', refund.Nature)
