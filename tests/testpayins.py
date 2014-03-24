import unittest
from tests.testbase import TestBase
from mangopaysdk.tools.enums import PayInPaymentType, ExecutionType, TransactionType, TransactionStatus, TransactionNature
from mangopaysdk.entities.payin import PayIn
from mangopaysdk.types.payinexecutiondetailsdirect import PayInExecutionDetailsDirect
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from mangopaysdk.types.payinexecutiondetailsweb import PayInExecutionDetailsWeb
from mangopaysdk.types.payinpaymentdetailsbankwire import PayInPaymentDetailsBankWire
from mangopaysdk.types.payinpaymentdetailspreauthorized import PayInPaymentDetailsPreAuthorized
from mangopaysdk.types.money import Money


class Test_PayIns(TestBase):
    "Tests methods for pay-ins"
    
    def test_PayIns_Create_CardWeb(self):
       payIn = self.getJohnsPayInCardWeb()
       self.assertTrue(len(payIn.Id) > 0)
       self.assertEqual(payIn.PaymentType, PayInPaymentType.CARD)
       self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
       self.assertEqual(payIn.ExecutionType, ExecutionType.WEB)
       self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsWeb)
    
    def test_PayIns_Get_CardWeb(self):
       payIn = self.getJohnsPayInCardWeb()
       getPayIn = self.sdk.payIns.Get(payIn.Id)
        
       self.assertEqual(payIn.Id, getPayIn.Id)
       self.assertEqual(payIn.PaymentType, PayInPaymentType.CARD)
       self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
       self.assertEqual(payIn.ExecutionType, ExecutionType.WEB)
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
        self.assertTrue(len(payIn.Id) > 0)
        self.assertEqual(wallet.Id, payIn.CreditedWalletId)
        self.assertEqual(PayInPaymentType.CARD, payIn.PaymentType)
        self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
        self.assertEqual(ExecutionType.DIRECT, payIn.ExecutionType)
        self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsDirect)
        self.assertIsInstance(payIn.DebitedFunds, Money)
        self.assertIsInstance(payIn.CreditedFunds, Money)
        self.assertIsInstance(payIn.Fees, Money)
        self.assertEqual(user.Id, payIn.AuthorId)
        self.assertEqual(wallet.Balance.Amount, beforeWallet.Balance.Amount + payIn.CreditedFunds.Amount)
        self.assertEqual(TransactionStatus.SUCCEEDED, payIn.Status)
        self.assertEqual(TransactionType.PAYIN, payIn.Type)
    
    def test_PayIns_Get_CardDirect(self):
        payIn = self.getJohnsPayInCardDirect()        
        getPayIn = self.sdk.payIns.Get(payIn.Id)        
        self.assertEqual(payIn.Id, getPayIn.Id)
        self.assertEqual(payIn.PaymentType, PayInPaymentType.CARD)
        self.assertIsInstance(payIn.PaymentDetails, PayInPaymentDetailsCard)
        self.assertEqual(payIn.ExecutionType, ExecutionType.DIRECT)
        self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsDirect)
        self.assertEqual(payIn.Id, getPayIn.Id)
        self.assertIsNotNone(getPayIn.ExecutionDetails.CardId)
        self.assertEqual(payIn.ResultCode, '000000')
    
    def test_PayIns_CreateRefund_CardDirect(self):
        wallet = self.getJohnsWallet()
        payIn = self.getJohnsPayInCardDirect(wallet)
        walletAfterPayIn = self.sdk.wallets.Get(wallet.Id)
        self.assertEqual(walletAfterPayIn.Balance.Amount, payIn.DebitedFunds.Amount)
        self.assertTrue(len(payIn.Id) > 0)

        refund = self.getJohnsRefundForPayIn(payIn)
        walletAfterRefund = self.sdk.wallets.Get(wallet.Id)
        self.assertTrue(len(refund.Id) > 0)
        self.assertTrue(refund.DebitedFunds.Amount, payIn.DebitedFunds.Amount)
        self.assertEqual(walletAfterRefund.Balance.Amount, walletAfterPayIn.Balance.Amount - payIn.DebitedFunds.Amount)
        self.assertEqual(TransactionType.PAYOUT, refund.Type)
        self.assertEqual(TransactionNature.REFUND, refund.Nature)

    def test_PayIns_PreAuthorizedDirect(self):
        cardPreAuthorization = self.getJohnsCardPreAuthorization()
        wallet = self.getJohnsWalletWithMoney()
        user = self.getJohn()
        # create pay-in PRE-AUTHORIZED DIRECT
        payIn = PayIn()
        payIn.CreditedWalletId = wallet.Id
        payIn.AuthorId = user.Id
        payIn.DebitedFunds = Money()
        payIn.DebitedFunds.Amount = 1000
        payIn.DebitedFunds.Currency = 'EUR'
        payIn.Fees = Money()
        payIn.Fees.Amount = 0
        payIn.Fees.Currency = 'EUR'
        # payment type as CARD
        payIn.PaymentDetails = PayInPaymentDetailsPreAuthorized()
        payIn.PaymentDetails.PreauthorizationId = cardPreAuthorization.Id
        # execution type as DIRECT
        payIn.ExecutionDetails = PayInExecutionDetailsDirect()
        payIn.ExecutionDetails.SecureModeReturnURL = 'http://test.com'
        
        createPayIn = self.sdk.payIns.Create(payIn)
        
        self.assertTrue(len(createPayIn.Id) > 0)
        self.assertEqual(wallet.Id, createPayIn.CreditedWalletId)
        self.assertEqual('PREAUTHORIZED', createPayIn.PaymentType)
        self.assertIsInstance(createPayIn.PaymentDetails, PayInPaymentDetailsPreAuthorized)
        self.assertEqual('DIRECT', createPayIn.ExecutionType)
        self.assertIsInstance(createPayIn.ExecutionDetails, PayInExecutionDetailsDirect)
        self.assertIsInstance(createPayIn.DebitedFunds, Money)
        self.assertIsInstance(createPayIn.CreditedFunds, Money)
        self.assertIsInstance(createPayIn.Fees, Money)
        self.assertEqual(user.Id, createPayIn.AuthorId)
        self.assertEqual('SUCCEEDED', createPayIn.Status)
        self.assertEqual('PAYIN', createPayIn.Type)
    

    def test_PayIns_Create_BankWireDirect(self):
        payIn = self.getJohnsPayInBankWireDirect()
        self.assertTrue(len(payIn.Id) > 0)
        self.assertEqual(payIn.PaymentType, PayInPaymentType.BANK_WIRE)
        self.assertIsInstance(payIn.PaymentDetails,  PayInPaymentDetailsBankWire)
        self.assertEqual(payIn.ExecutionType, ExecutionType.DIRECT)
        self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsDirect)
        self.assertEqual(payIn.CreditedUserId, payIn.AuthorId)
        self.assertEqual(payIn.Status, TransactionStatus.CREATED)
        self.assertEqual(payIn.Nature, TransactionNature.REGULAR)
        self.assertTrue(len(payIn.PaymentDetails.WireReference) == 10)
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount)
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount.Type)
        self.assertEqual(payIn.PaymentDetails.BankAccount.Type, 'IBAN')
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount.Details.IBAN)
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount.Details.BIC)

    def test_PayIns_Get_BankWireDirect(self):
        payIn = self.getJohnsPayInBankWireDirect()
        getPayIn = self.sdk.payIns.Get(payIn.Id)
        self.assertTrue(len(payIn.Id) > 0)
        self.assertEqual(payIn.PaymentType, PayInPaymentType.BANK_WIRE)
        self.assertIsInstance(payIn.PaymentDetails,  PayInPaymentDetailsBankWire)
        self.assertEqual(payIn.ExecutionType, ExecutionType.DIRECT)
        self.assertIsInstance(payIn.ExecutionDetails, PayInExecutionDetailsDirect)
        self.assertEqual(payIn.CreditedUserId, payIn.AuthorId)
        self.assertEqual(payIn.Status, TransactionStatus.CREATED)
        self.assertEqual(payIn.Nature, TransactionNature.REGULAR)
        self.assertTrue(len(payIn.PaymentDetails.WireReference) == 10)
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount)
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount.Type)
        self.assertEqual(payIn.PaymentDetails.BankAccount.Type, 'IBAN')
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount.Details.IBAN)
        self.assertIsNotNone(payIn.PaymentDetails.BankAccount.Details.BIC)  