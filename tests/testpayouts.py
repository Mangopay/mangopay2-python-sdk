import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.types.exceptions.responseexception import ResponseException


class Test_PayOuts(TestBase):
    "Tests methods for pay-outs"

    def test_PayOuts_Create_BankWire_FailsCauseNotEnoughMoney(self):
        "Cannot test anything else here: have no pay-ins with sufficient status?"

        TestBase._johnsWallet = None
        payOut = self.getJohnsPayOutBankWire()
        self.assertEqual('001001', payOut.ResultCode)