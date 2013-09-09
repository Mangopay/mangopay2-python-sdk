from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.tools.enums import *
from tests.testbase import TestBase

class Test_CardRegistrations(TestBase):
    """Tests methods for card registrations"""


    def test_CardRegistrations_Create(self):
        cardRegistration = self.getJohnsCardRegistration()
        user = self.getJohn()
        
        self.assertTrue(int(cardRegistration.Id) > 0)
        self.assertNotEqual(cardRegistration.AccessKey, None)
        self.assertNotEqual(cardRegistration.PreregistrationData, None)
        self.assertNotEqual(cardRegistration.CardRegistrationURL, None)
        self.assertEqual(user.Id, cardRegistration.UserId)
        self.assertEqual('EUR', cardRegistration.Currency)
        self.assertEqual('CREATED', cardRegistration.Status)

    def test_CardRegistrations_Get(self):
        cardRegistration = self.getJohnsCardRegistration()
        getCardRegistration = self.sdk.cardRegistrations.Get(cardRegistration.Id)
        self.assertTrue(int(getCardRegistration.Id) > 0)
        self.assertEqual(cardRegistration.Id, getCardRegistration.Id)
    
    def test_CardRegistrations_Update(self):
        cardRegistration = self.getJohnsCardRegistration()
        cardRegistration.RegistrationData = 'test RegistrationData'
        getCardRegistration = self.sdk.cardRegistrations.Update(cardRegistration)
        self.assertEqual('test RegistrationData', getCardRegistration.RegistrationData)
