import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.entities.payin import PayIn
from mangopaysdk.types.exceptions.responseexception import ResponseException
from mangopaysdk.types.payoutpaymentdetailsbankwire import PayOutPaymentDetailsBankWire


class Test_PayOuts(TestBase):
    """Tests methods for pay-outs"""

    def test_PayOuts_Create_BankWire_FailsCauseNotEnoughMoney(self):
        TestBase._johnsWallet = None
        payOut = self.getJohnsPayOutBankWire()
        self.assertEqual('001001', payOut.ResultCode)

    def test_PayOuts_Create_BankWire(self):
        payIn = self.getJohnsPayInCardWeb()
        payOut = self.getJohnsPayOutBankWire()

        self.assertTrue(payOut.Id != '')
        self.assertEquals(payOut.PaymentType, "BANK_WIRE")
        self.assertIsInstance(payOut.MeanOfPaymentDetails, PayOutPaymentDetailsBankWire)