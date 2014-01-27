from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.entities.cardpreauthorization import CardPreAuthorization
from mangopaysdk.tools.enums import *
from tests.testbase import TestBase

class Test_CardPreAuthorization(TestBase):
    """Tests methods for card preauthorization"""
    
    def test_CardPreAuthorization_Create(self):
        cardPreAuthorization = self.getJohnsCardPreAuthorization()
        self.assertTrue(int(cardPreAuthorization.Id) > 0)
        self.assertEqual(cardPreAuthorization.Status, TransactionStatus.SUCCEEDED)
        self.assertEqual(cardPreAuthorization.PaymentStatus, CardPreAuthorizationStatus.WAITING)
        self.assertEqual(cardPreAuthorization.ExecutionType, ExecutionType.DIRECT)
        self.assertIsNone(cardPreAuthorization.PayInId)
       
    def test_CardPreAuthorization_Get(self):
        cardPreAuthorization = self.getJohnsCardPreAuthorization()
        getCardPreAuthorization = self.sdk.cardPreAuthorizations.Get(cardPreAuthorization.Id)      
        self.assertEqual(int(cardPreAuthorization.Id), int(getCardPreAuthorization.Id))
        self.assertEqual(getCardPreAuthorization.ResultCode, '000000')
        self.assertEqual(getCardPreAuthorization.Status, cardPreAuthorization.Status)
        self.assertEqual(getCardPreAuthorization.PaymentStatus, cardPreAuthorization.PaymentStatus)

    def test_CardPreAuthorization_Update(self):
        cardPreAuthorization = self.getJohnsCardPreAuthorization()
        cardPreAuthorization.PaymentStatus = CardPreAuthorizationStatus.CANCELED
        resultCardPreAuthorization = self.sdk.cardPreAuthorizations.Update(cardPreAuthorization)      
        self.assertEqual(resultCardPreAuthorization.Status, TransactionStatus.SUCCEEDED)
        self.assertEqual(resultCardPreAuthorization.PaymentStatus, CardPreAuthorizationStatus.CANCELED)