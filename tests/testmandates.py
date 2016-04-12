import unittest
from tests.testbase import TestBase
from mangopaysdk.tools.enums import *
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.tools.sorting import Sorting
from mangopaysdk.entities.mandate import Mandate

class Test_Mandates(TestBase):
    """Test methods for mandates."""


    def test_Mandate_Create(self):
        bankAccountId = self.getJohnsAccount().Id
        returnUrl = 'http://test.test'

        mandatePost = Mandate()
        mandatePost.BankAccountId = bankAccountId
        mandatePost.Culture = 'EN'
        mandatePost.ReturnURL = returnUrl

        mandate = self.sdk.mandates.Create(mandatePost)

        self.assertIsNotNone(mandate);
    
    def test_Mandate_Get(self):
        bankAccountId = self.getJohnsAccount().Id
        returnUrl = 'http://test.test'

        mandatePost = Mandate()
        mandatePost.BankAccountId = bankAccountId
        mandatePost.Culture = 'EN'
        mandatePost.ReturnURL = returnUrl

        mandateCreated = self.sdk.mandates.Create(mandatePost)

        mandate = self.sdk.mandates.Get(mandateCreated.Id)

        self.assertIsNotNone(mandate)
        self.assertFalse(mandate.Id == '')
        self.assertTrue(mandate.Id == mandateCreated.Id)
    
    def test_Mandate_Cancel(self):
        bankAccountId = self.getJohnsAccount().Id
        returnUrl = 'http://test.test'

        mandatePost = Mandate()
        mandatePost.BankAccountId = bankAccountId
        mandatePost.Culture = 'EN'
        mandatePost.ReturnURL = returnUrl

        mandate = self.sdk.mandates.Create(mandatePost)

        	
		#	! IMPORTANT NOTE !
		#	
		#	In order to make this test pass, at this place you have to set a breakpoint,
		#	navigate to URL the mandate.RedirectURL property points to and click "CONFIRM" button.


        mandate = self.sdk.mandates.Get(mandate.Id)
        self.assertEquals(mandate.Status, 'SUBMITTED', 'In order to make this test pass, after creating mandate and before cancelling it you have to navigate to URL the mandate.RedirectURL property points to and click CONFIRM button.')

        mandate = self.sdk.mandates.Cancel(mandate)

        self.assertIsNotNone(mandate)
        self.assertEquals(mandate.Status, 'FAILED')
    
    def test_Mandates_Get_All(self):
        mandates = self.sdk.mandates.GetAll()

        self.assertIsNotNone(mandates)

    def test_Mandates_Get_For_User(self):
        user = self.getJohn()
        bankAccountId = self.getJohnsAccount().Id
        returnUrl = 'http://test.test'

        mandatePost = Mandate()
        mandatePost.BankAccountId = bankAccountId
        mandatePost.Culture = 'EN'
        mandatePost.ReturnURL = returnUrl

        mandateCreated = self.sdk.mandates.Create(mandatePost)

        sorting = Sorting()
        sorting.AddField("CreationDate", SortDirection.DESC)
        mandates = self.sdk.mandates.GetForUser(user.Id, Pagination(), sorting)

        self.assertIsNotNone(mandates)
        self.assertIsNotNone(mandates[0])
        self.assertTrue(mandateCreated.Id == mandates[0].Id)

    def test_Mandates_Get_For_Bank_Account(self):
        user = self.getJohn()
        bankAccountId = self.getJohnsAccount().Id
        returnUrl = 'http://test.test'

        mandatePost = Mandate()
        mandatePost.BankAccountId = bankAccountId
        mandatePost.Culture = 'EN'
        mandatePost.ReturnURL = returnUrl

        mandateCreated = self.sdk.mandates.Create(mandatePost)

        sorting = Sorting()
        sorting.AddField("CreationDate", SortDirection.DESC)
        mandates = self.sdk.mandates.GetForBankAccount(user.Id, bankAccountId, Pagination(), sorting)

        self.assertIsNotNone(mandates)
        self.assertIsNotNone(mandates[0])
        self.assertTrue(mandateCreated.Id == mandates[0].Id)