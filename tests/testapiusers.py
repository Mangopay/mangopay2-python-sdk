import random, string, time
from tests.testbase import TestBase
from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.types.exceptions.responseexception import ResponseException
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.entities.kycpage import KycPage
from mangopaysdk.tools.enums import *
import os
from __builtin__ import Exception
from mangopaysdk.types.bankaccountdetailsgb import BankAccountDetailsGB
from mangopaysdk.types.bankaccountdetailsus import BankAccountDetailsUS
from mangopaysdk.types.bankaccountdetailsca import BankAccountDetailsCA
from mangopaysdk.types.bankaccountdetailsother import BankAccountDetailsOTHER


class Test_ApiUsers(TestBase):

    def test_Users_CreateNatural(self):
        john = self.getJohn()
        self.assertTrue(int(john.Id) > 0)
        self.assertEqual(john.PersonType, PersonType.Natural)

    def test_Users_CreateLegal(self):
        matrix = self.getMatrix()
        self.assertTrue(int(matrix.Id) > 0)
        self.assertEqual(matrix.PersonType, PersonType.Legal)

    def test_Users_CreateLegal_FailsIfRequiredPropsNotProvided(self):
        user = UserLegal()
        with self.assertRaises(ResponseException) as cm:
            self.sdk.users.Create(user)
        self.assertEqual(400, cm.exception.Code)
        self.assertTrue('One or several required parameters are missing or incorrect' in cm.exception.Message)

    def test_Users_CreateLegal_PassesIfRequiredPropsProvided(self):
        user = UserLegal()
        user.Name = "SomeOtherSampleOrg"
        user.LegalPersonType = "BUSINESS"
        user.Email = "john.doe@sample.org"
        user.LegalPersonType = "BUSINESS"
        user.LegalRepresentativeFirstName = 'Piter'
        user.LegalRepresentativeLastName = 'Doe'
        user.LegalRepresentativeBirthday = int(time.mktime((1979, 11, 21, 0,0,0, -1, -1, -1)))
        user.LegalRepresentativeNationality = 'FR'
        user.LegalRepresentativeCountryOfResidence = 'FR'
        ret = self.sdk.users.Create(user)

        self.assertTrue(int(ret.Id) > 0, "Created successfully after required props set")
        self.assertEqualInputProps(user, ret)

    def test_Users_GetNatural(self):
        john = self.getJohn()

        user1 = self.sdk.users.Get(john.Id)
        user2 = self.sdk.users.GetNatural(john.Id)

        self.assertEqual(user1.Id, john.Id)
        self.assertEqual(user2.Id, john.Id)
        self.assertEqualInputProps(user1, john)
        self.assertEqualInputProps(user2, john)

    def test_Users_GetNatural_FailsForLegalUser(self):
        matrix = self.getMatrix()
        with self.assertRaises(Exception) as cm:
            user = self.sdk.users.GetNatural(matrix.Id)
        self.assertEqual(404, cm.exception.Code)
        self.assertTrue('The ressource does not exist' in cm.exception.Message)

    def test_Users_GetLegal_FailsForNaturalUser(self):
        john = self.getJohn()
        with self.assertRaises(Exception) as cm:
            user = self.sdk.users.GetLegal(john.Id)
        self.assertEqual(404, cm.exception.Code)
        self.assertTrue('The ressource does not exist' in cm.exception.Message)

    def test_Users_GetLegal(self):
        matrix = self.getMatrix()

        user1 = self.sdk.users.Get(matrix.Id)
        user2 = self.sdk.users.GetLegal(matrix.Id)

        self.assertEqual(user1.Id, matrix.Id)
        self.assertEqual(user2.Id, matrix.Id)
        self.assertEqualInputProps(user1, matrix)
        self.assertEqualInputProps(user2, matrix)

    def test_Users_UpdateNatural(self):
        john = self.getJohn()
        john.LastName += " - CHANGED"

        userUpdated = self.sdk.users.Update(john)
        userFetched = self.sdk.users.Get(john.Id)

        self.assertEqualInputProps(userUpdated, john)
        self.assertEqualInputProps(userFetched, john)

    def test_Users_UpdateLegal(self):
        matrix = self.getMatrix()
        matrix.LegalRepresentativeLastName += " - CHANGED"

        userUpdated = self.sdk.users.Update(matrix)
        userFetched = self.sdk.users.Get(matrix.Id)

        self.assertEqualInputProps(userUpdated, matrix)
        self.assertEqualInputProps(userFetched, matrix)

    def test_Users_CreateBankAccount_IBAN(self):
        john = self.getJohn()
        account = self.getJohnsAccount()

        self.assertTrue(int(account.Id) > 0)
        self.assertEqual(account.UserId, john.Id)

    def test_Users_CreateBankAccount_GB(self):
        john = self.getJohn()
        account = BankAccount()
        account.OwnerName = john.FirstName + ' ' + john.LastName
        account.OwnerAddress = john.Address
        account.Details = BankAccountDetailsGB()
        account.Details.AccountNumber = '234234234234'
        account.Details.SortCode = '234334'
        
        createAccount = self.sdk.users.CreateBankAccount(john.Id, account)
        
        self.assertTrue(len(createAccount.Id) > 0)
        self.assertEqual(createAccount.UserId, john.Id)
        self.assertEqual(createAccount.Type, 'GB')
        self.assertEqual(createAccount.Details.AccountNumber, '234234234234')
        self.assertEqual(createAccount.Details.SortCode, '234334')
    
    
    def test_Users_CreateBankAccount_US(self):
        john = self.getJohn()
        account = BankAccount()
        account.OwnerName = john.FirstName + ' ' + john.LastName
        account.OwnerAddress = john.Address
        account.Details = BankAccountDetailsUS()
        account.Details.AccountNumber = '234234234234'
        account.Details.ABA = '234334789'
        
        createAccount = self.sdk.users.CreateBankAccount(john.Id, account)
        
        self.assertTrue(len(createAccount.Id) > 0)
        self.assertEqual(createAccount.UserId, john.Id)
        self.assertEqual(createAccount.Type, 'US')
        self.assertEqual(createAccount.Details.AccountNumber, '234234234234')
        self.assertEqual(createAccount.Details.ABA, '234334789')
    
    
    def test_Users_CreateBankAccount_CA(self):
        john = self.getJohn()
        account = BankAccount()
        account.OwnerName = john.FirstName + ' ' + john.LastName
        account.OwnerAddress = john.Address
        account.Details = BankAccountDetailsCA()
        account.Details.BankName = 'TestBankName'
        account.Details.BranchCode = '12345'
        account.Details.AccountNumber = '234234234234'
        account.Details.InstitutionNumber = '123'
        
        createAccount = self.sdk.users.CreateBankAccount(john.Id, account)
        
        self.assertTrue(len(createAccount.Id) > 0)
        self.assertEqual(createAccount.UserId, john.Id)
        self.assertEqual(createAccount.Type, 'CA')
        self.assertEqual(createAccount.Details.AccountNumber, '234234234234')
        self.assertEqual(createAccount.Details.BankName, 'TestBankName')
        self.assertEqual(createAccount.Details.BranchCode, '12345')
        self.assertEqual(createAccount.Details.InstitutionNumber, '123')
    
    
    def test_Users_CreateBankAccount_OTHER(self):
        john = self.getJohn()
        account = BankAccount()
        account.OwnerName = john.FirstName + ' ' + john.LastName
        account.OwnerAddress = john.Address
        account.Details = BankAccountDetailsOTHER()
        account.Details.Type = 'OTHER'
        account.Details.Country = 'FR'
        account.Details.AccountNumber = '234234234234'
        account.Details.BIC = 'BINAADADXXX'
        
        createAccount = self.sdk.users.CreateBankAccount(john.Id, account)
        
        self.assertTrue(len(createAccount.Id) > 0)
        self.assertEqual(createAccount.UserId, john.Id)
        self.assertEqual(createAccount.Type, 'OTHER')
        self.assertEqual(createAccount.Details.Type, 'OTHER')
        self.assertEqual(createAccount.Details.Country, 'FR')
        self.assertEqual(createAccount.Details.AccountNumber, '234234234234')
        self.assertEqual(createAccount.Details.BIC, 'BINAADADXXX')
    

    def test_Users_BankAccount(self):
        john = self.getJohn()
        account = self.getJohnsAccount()

        accountFetched = self.sdk.users.GetBankAccount(john.Id, account.Id)
        self.assertEqualInputProps(account, accountFetched)

    def test_Users_BankAccounts(self):
        john = self.getJohn()
        account = self.getJohnsAccount()
        pagination = Pagination(1, 12)

        list = self.sdk.users.GetBankAccounts(john.Id, pagination)

        self.assertIsInstance(list[0], BankAccount)
        self.assertEqual(account.Id, list[0].Id)
        self.assertEqualInputProps(account, list[0])
        self.assertEqual(pagination.Page, 1)
        self.assertEqual(pagination.ItemsPerPage, 12)
        self.assertTrue(pagination.TotalPages > 0)
        self.assertTrue(pagination.TotalItems > 0)

    def test_Users_Cards(self):
       john = self.getJohn()
       payIn = self.getJohnsPayInCardDirect()
       userCards = self.sdk.users.GetCards(john.Id)
       self.assertTrue(len(userCards) == 1)
       self.assertIsNotNone(userCards[0].CardType)
       self.assertIsNotNone(userCards[0].Currency)

    def test_Users_Transactions(self):
       john = self.getJohn()
       transfer = self.getJohnsTransfer()
       userTransfers = self.sdk.users.GetTransactions(john.Id)
       self.assertTrue(len(userTransfers) > 0)
       self.assertIsNotNone(userTransfers[0].Type)
       self.assertIsNotNone(userTransfers[0].Status)

    def test_Users_CreateKycDocument(self):
        kycDoc = self.getUserKycDocument()
        self.assertNotEqual(kycDoc.Id, None)
        self.assertNotEqual(kycDoc.Id, 0)
        self.assertNotEqual(kycDoc.CreationDate, None)
        self.assertEqual(kycDoc.Status, KycDocumentStatus.CREATED)

    def test_Users_GetKycDocument(self):
        john = self.getJohn()
        kycDoc = self.getUserKycDocument()
        kycDocRes = self.sdk.users.GetUserKycDocument(kycDoc.Id, john.Id)
        self.assertEqual(kycDoc.Id, kycDocRes.Id)
        self.assertEqual(kycDoc.Tag, kycDocRes.Tag)
        self.assertEqual(kycDoc.Type, kycDocRes.Type)
        self.assertEqual(kycDoc.Status, kycDocRes.Status)

    def test_Users_UpdateKycDocument(self):
        john = self.getJohn()
        kycDoc = self.getUserKycDocument()
        kycDoc.Status = KycDocumentStatus.VALIDATION_ASKED
        kycDocRes = self.sdk.users.UpdateUserKycDocument(kycDoc, john.Id, kycDoc.Id)
        self.assertEqual(kycDocRes.Status, KycDocumentStatus.VALIDATION_ASKED)

    def test_Users_CreateKycDocumentPage(self):
        john = self.getJohn()
        kycDoc = self.getUserKycDocument()
        kycPage = KycPage().LoadDocumentFromFile(os.path.join(os.path.dirname(__file__),"spacer.gif"))
        kycDocRes = self.sdk.users.CreateUserKycPage(kycPage, john.Id, kycDoc.Id)
        self.assertEqual(kycDocRes, None)

    def test_Users_CreateKycPage_EmptyFileString(self):
        kycDocument = self.getUserKycDocument()
        user = self.getJohn()
        kycPage = KycPage()
        kycPage.File = ''
        kycPageResponse = self.sdk.users.CreateUserKycPage(kycPage, user.Id, kycDocument.Id)    
        self.assertEqual(kycPageResponse, None)
    
    def test_Users_CreateKycPage_WrongFileString(self):
        kycDocument = self.getUserKycDocument()
        user = self.getJohn()
        kycPage = KycPage()
        kycPage.File = 'qqqq'
        kycPageResponse = self.sdk.users.CreateUserKycPage(kycPage, user.Id, kycDocument.Id)
        self.assertEqual(kycPageResponse, None)
    
    def test_Users_CreateKycPage_CorrectFileString(self):
        user = self.getJohn()
        kycDocumentInit = KycDocument()
        kycDocumentInit.Status = KycDocumentStatus.CREATED
        kycDocumentInit.Type = KycDocumentType.IDENTITY_PROOF
        kycDocument = self.sdk.users.CreateUserKycDocument(kycDocumentInit, user.Id)
        kycPage = KycPage()
        kycPage.File = 'dGVzdCB0ZXN0IHRlc3QgdGVzdA=='
        
        kycPageResponse = self.sdk.users.CreateUserKycPage(kycPage, user.Id, kycDocument.Id)
        self.assertEqual(kycPageResponse, None)
    
    def test_Users_CreateKycPage_EmptyFilePath(self):
        user = self.getJohn()
        kycDocumentInit = KycDocument()
        kycDocumentInit.Status = KycDocumentStatus.CREATED
        kycDocumentInit.Type = KycDocumentType.IDENTITY_PROOF
        kycDocument = self.sdk.users.CreateUserKycDocument(kycDocumentInit, user.Id)
        
        try:
            self.sdk.users.CreateKycPageFromFile(user.Id, kycDocument.Id, '')
        except Exception as exc:
            self.assertEqual(exc.message, 'Path of file cannot be empty')
        
    def test_Users_CreateKycPage_WrongFilePath(self) :
        user = self.getJohn()
        kycDocumentInit = KycDocument()
        kycDocumentInit.Status = KycDocumentStatus.CREATED
        kycDocumentInit.Type = KycDocumentType.IDENTITY_PROOF
        kycDocument = self.sdk.users.CreateUserKycDocument(kycDocumentInit, user.Id)
        
        try:
            self.sdk.users.CreateKycPageFromFile(user.Id, kycDocument.Id, 'notExistFileName.tmp')
        except Exception as exc:
            self.assertEqual(exc.message, 'File not exist')
    
    def test_Users_CreateKycPage_CorrectFilePath(self) :
        user = self.getJohn()
        kycDocumentInit = KycDocument()
        kycDocumentInit.Status = KycDocumentStatus.CREATED
        kycDocumentInit.Type = KycDocumentType.IDENTITY_PROOF
        kycDocument = self.sdk.users.CreateUserKycDocument(kycDocumentInit, user.Id)

        self.sdk.users.CreateKycPageFromFile(user.Id, kycDocument.Id, __file__)

if __name__ == '__main__':
     Test_ApiUsers().test_Users_GetKycDocument()