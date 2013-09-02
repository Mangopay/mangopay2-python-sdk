import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.types.exceptions.responseexception import ResponseException


class Test_PayOuts(TestBase):
    "Tests methods for pay-outs"

    def test_PayOuts_Create_BankWire_FailsCauseNotEnoughMoney(self):
        "Cannot test anything else here: have no pay-ins with sufficient status?"

        with self.assertRaises(ResponseException) as cm:
            payIn = self.getJohnsPayInCardWeb()
            payOut = self.getJohnsPayOutBankWire()

        self.assertEqual(400, cm.exception.Code)
        self.assertTrue("The amount you wish to spend must be smaller than the amount left in your collection" in cm.exception.Message)

if __name__ == '__main__':
    unittest.main()
