from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.entities.temporarypaymentcard import TemporaryPaymentCard
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
    
    
        cardRegistration.RegistrationData = 'test RegistrationData'
        getCardRegistration = self.sdk.cardRegistrations.Update(cardRegistration)
        self.assertEqual('test RegistrationData', getCardRegistration.RegistrationData)

    def test_CardRegistrations_Update(self):
        cardRegistration = self.getJohnsCardRegistration()
        registrationData = self.getPaylineCorrectRegistartionData(cardRegistration)
        cardRegistration.RegistrationData = registrationData
        
        getCardRegistration = self.sdk.cardRegistrations.Update(cardRegistration)
        self.assertEqual(registrationData, getCardRegistration.RegistrationData)
        self.assertTrue(getCardRegistration.CardId != None)
        self.assertEqual('VALIDATED', getCardRegistration.Status)
        self.assertEqual('000000', getCardRegistration.ResultCode)
    
        # def test_Cards_CheckCardExisting(self):
        cardRegistration = self.sdk.cardRegistrations.Get(cardRegistration.Id)
        card = self.sdk.cards.Get(cardRegistration.CardId)
        self.assertTrue(int(card.Id) > 0)


    # The two tests below are added to cover temporary use cases, which will be removed in future.

    def test_TemporaryPaymentCard_Create(self):
        user = self.getJohn()
        paymentCard = TemporaryPaymentCard()
        paymentCard.UserId = user.Id
        paymentCard.Tag = 'Test tag'
        paymentCard.Culture = 'FR'
        paymentCard.ReturnURL = 'http://test.com/test'
        paymentCard.TemplateURL = 'https://test.com/test'
                       
        paymentCardCreated = self.sdk.cardRegistrations.CreateTemporaryPaymentCard(paymentCard)
        
        self.assertTrue(int(paymentCardCreated.Id) > 0)
        self.assertEquals(paymentCardCreated.UserId, user.Id)

    def test_TemporaryPaymentCard_Get(self):
        user = self.getJohn()
        paymentCard = TemporaryPaymentCard()
        paymentCard.UserId = user.Id
        paymentCard.Tag = 'Test tag'
        paymentCard.Culture = 'FR'
        paymentCard.ReturnURL = 'http://test.com/test'
        paymentCard.TemplateURL = 'https://test.com/test'

        paymentCardCreated = self.sdk.cardRegistrations.CreateTemporaryPaymentCard(paymentCard)

        paymentCardGet = self.sdk.cardRegistrations.GetTemporaryPaymentCard(paymentCardCreated.Id)

        self.assertTrue(int(paymentCardGet.Id) > 0)
        self.assertEquals(paymentCardGet.Id, paymentCardCreated.Id)
