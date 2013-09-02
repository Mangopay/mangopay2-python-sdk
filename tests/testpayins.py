import unittest
from tests.testbase import TestBase
from mangopaysdk.entities.payin import PayIn
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
       self.assertIsNotNone(getPayIn.PaymentDetails.RedirectURL)
       self.assertIsNotNone(getPayIn.PaymentDetails.ReturnURL)

if __name__ == '__main__':
    unittest.main()