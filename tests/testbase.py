import unittest
import logging
import time
from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.entities.wallet import Wallet
from mangopaysdk.entities.usernatural import UserNatural
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.payin import PayIn
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.entities.payout import PayOut
from mangopaysdk.entities.transfer import Transfer
from mangopaysdk.entities.transaction import Transaction
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from mangopaysdk.types.payinexecutiondetailsweb import PayInExecutionDetailsWeb
from mangopaysdk.types.payoutpaymentdetailsbankwire import PayOutPaymentDetailsBankWire
from mangopaysdk.types.money import Money


class TestBase(unittest.TestCase):

    # sdk = None

    _john = None
    _matrix = None
    _johnsAccount = None
    _johnsWallet = None
    _johnsPayInCardWeb = None
    _payInPaymentDetailsCard = None
    _payInExecutionDetailsWeb = None
    _johnsPayOutBankWire = None    
    _johnsTransfer = None

    def __init__(self, methodName='runTest'):
        self.sdk = self.buildNewMangoPayApi()
        super(TestBase, self).__init__(methodName)

    def buildNewMangoPayApi(self):
        sdk = MangoPayApi()
        # use test client credentails
        sdk.Config.ClientID = 'example'
        sdk.Config.ClientPassword = 'uyWsmnwMQyTnqKgi8Y35A3eVB7bGhqrebYqA1tL6x2vYNpGPiY'
        return sdk

    def getJohn(self):
        """Creates TestBase._john (test natural user) if not created yet"""
        if (TestBase._john == None):
            user = UserNatural()
            user.FirstName = "John"
            user.LastName = "Doe"
            user.Email = "john.doe@sample.org"
            user.Address = "Some Address"
            user.Birthday = int(time.mktime((1975, 12, 21, 0,0,0, -1, -1, -1)))
            user.Nationality = "FR"
            user.CountryOfResidence = "FR"
            user.Occupation = "programmer"
            user.IncomeRange = 3
            TestBase._john = self.sdk.users.Create(user)
            self.assertEqualInputProps(TestBase._john, user, True)
        return TestBase._john

    def getMatrix(self):
        """Creates TestBase._matrix (test legal user) if not created yet"""
        if (TestBase._matrix == None):
            john = self.getJohn()
            user = UserLegal()
            user.Name = "MartixSampleOrg"
            user.LegalPersonType = "BUSINESS"
            user.HeadquartersAddress = "Some Address"
            user.LegalRepresentativeFirstName = john.FirstName
            user.LegalRepresentativeLastName = john.LastName
            user.LegalRepresentativeAddress = john.Address
            user.LegalRepresentativeEmail = john.Email
            user.LegalRepresentativeBirthday = john.Birthday
            user.LegalRepresentativeNationality = john.Nationality
            user.LegalRepresentativeCountryOfResidence = john.CountryOfResidence
            TestBase._matrix = self.sdk.users.Create(user)
            self.assertEqualInputProps(TestBase._matrix, user, True)
        return TestBase._matrix
    
    def getJohnsAccount(self):
        """Creates TestBase._johnsAccount (bank account belonging to John) if not created yet"""
        if TestBase._johnsAccount == None:
            john = self.getJohn()
            account = BankAccount()
            account.Type = 'IBAN'
            account.OwnerName = john.FirstName + ' ' +  john.LastName
            account.OwnerAddress = john.Address
            account.IBAN = 'AD1200012030200359100100'
            account.BIC = 'BINAADADXXX'
            TestBase._johnsAccount = self.sdk.users.CreateBankAccount(john.Id, account)
            self.assertEqualInputProps(TestBase._johnsAccount, account, True)
        return TestBase._johnsAccount
    
    def getJohnsWallet(self):
        """Creates TestBase._johnsWallet (wallets belonging to John) if not created yet"""
        if TestBase._johnsWallet == None:
            john = self.getJohn()
            wallet = Wallet()
            wallet.Owners = [john.Id]
            wallet.Currency = 'EUR'
            wallet.Description = 'WALLET IN EUR'            
            TestBase._johnsWallet = self.sdk.wallets.Create(wallet)
            #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.assertEqualInputProps(TestBase._johnsWallet, wallet, True)
        return TestBase._johnsWallet
    
    def getPayInPaymentDetailsCard(self):
        """return PayInPaymentDetailsCard"""
        if TestBase._payInPaymentDetailsCard == None:
            TestBase._payInPaymentDetailsCard = PayInPaymentDetailsCard()
            TestBase._payInPaymentDetailsCard.CardType = 'AMEX'
            TestBase._payInPaymentDetailsCard.ReturnURL = 'https://test.com'
        return TestBase._payInPaymentDetailsCard
    
    def getPayInExecutionDetailsWeb(self):
        """return PayInExecutionDetailsWeb"""
        if TestBase._payInExecutionDetailsWeb == None:
            TestBase._payInExecutionDetailsWeb = PayInExecutionDetailsWeb()
            TestBase._payInExecutionDetailsWeb.TemplateURL = 'https://TemplateURL.com'
            TestBase._payInExecutionDetailsWeb.SecureMode = 'DEFAULT'
            TestBase._payInExecutionDetailsWeb.Culture = 'fr'
        return TestBase._payInExecutionDetailsWeb
    
    def getJohnsPayInCardWeb(self):
        """Creates Pay-In Card Web object"""
        if TestBase._johnsPayInCardWeb == None:
            wallet = self.getJohnsWallet()
            user = self.getJohn()
            
            payIn = PayIn()
            payIn.AuthorId = user.Id
            payIn.CreditedUserId = user.Id
            payIn.DebitedFunds = Money()
            payIn.DebitedFunds.Currency = 'EUR'
            payIn.DebitedFunds.Amount = 1000
            payIn.Fees = Money()
            payIn.Fees.Currency = 'EUR'
            payIn.Fees.Amount = 5
            payIn.CreditedWalletId = wallet.Id
            payIn.PaymentDetails = self.getPayInPaymentDetailsCard()
            payIn.ExecutionDetails = self.getPayInExecutionDetailsWeb()
            
            TestBase._johnsPayInCardWeb = self.sdk.payIns.Create(payIn)
            #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.assertEqualInputProps(TestBase._johnsPayInCardWeb, payIn, True)
        return TestBase._johnsPayInCardWeb

    def getJohnsPayOutBankWire(self):
        """Creates Pay-Out  Bank Wire object"""
        if TestBase._johnsPayOutBankWire == None:
            wallet = self.getJohnsWallet()
            user = self.getJohn()
            account = self.getJohnsAccount()

            payOut = PayOut()
            payOut.Tag = 'DefaultTag'
            payOut.AuthorId = user.Id
            payOut.CreditedUserId = user.Id
            payOut.DebitedFunds = Money()
            payOut.DebitedFunds.Currency = 'EUR'
            payOut.DebitedFunds.Amount = 10
            payOut.Fees = Money()
            payOut.Fees.Currency = 'EUR'
            payOut.Fees.Amount = 5

            payOut.DebitedWalletId = wallet.Id
            payOut.MeanOfPaymentDetails = PayOutPaymentDetailsBankWire()
            payOut.MeanOfPaymentDetails.BankAccountId = account.Id
            payOut.MeanOfPaymentDetails.Communication = 'Communication text'

            TestBase._johnsPayOutBankWire = self.sdk.payOuts.Create(payOut)
            self.assertEqualInputProps(TestBase._johnsPayOutBankWire, payOut, True)
        return TestBase._johnsPayOutBankWire

    def getJohnsTransfer(self):
        """Creates Pay-Out  Bank Wire object"""
        if TestBase._johnsTransfer == None:
            wallet = self.getJohnsWallet()
            user = self.getJohn()
            
            transfer = Transfer()
            transfer.Tag = 'DefaultTag'
            transfer.AuthorId = user.Id
            transfer.CreditedUserId = user.Id
            transfer.DebitedFunds = Money()
            transfer.DebitedFunds.Currency = 'EUR'
            transfer.DebitedFunds.Amount = 100
            transfer.Fees = Money()
            transfer.Fees.Currency = 'EUR'
            transfer.Fees.Amount = 10

            transfer.DebitedWalletId = wallet.Id
            transfer.CreditedWalletId = wallet.Id

            TestBase._johnsTransfer = self.sdk.transfers.Create(transfer)
            #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.assertEqualInputProps(TestBase._johnsTransfer, transfer, True)
        return TestBase._johnsTransfer

    def assertEqualInputProps(self, entity1, entity2, asFreshlyCreated = False):

        if (isinstance(entity1, UserNatural)):
            self.assertEqual(entity1.Tag, entity2.Tag)
            self.assertEqual(entity1.PersonType, entity2.PersonType)
            self.assertEqual(entity1.FirstName, entity2.FirstName)
            self.assertEqual(entity1.LastName, entity2.LastName)
            self.assertEqual(entity1.Email, entity2.Email)
            self.assertEqual(entity1.Address, entity2.Address)
            self.assertEqual(entity1.Birthday, entity2.Birthday)
            self.assertEqual(entity1.Nationality, entity2.Nationality)
            self.assertEqual(entity1.CountryOfResidence, entity2.CountryOfResidence)
            self.assertEqual(entity1.Occupation, entity2.Occupation)
            self.assertEqual(entity1.IncomeRange, entity2.IncomeRange)

        elif (isinstance(entity1, UserLegal)):
            self.assertEqual(entity1.Tag, entity2.Tag)
            self.assertEqual(entity1.PersonType, entity2.PersonType)
            self.assertEqual(entity1.Name, entity2.Name)
            self.assertEqual(entity1.HeadquartersAddress, entity2.HeadquartersAddress)
            self.assertEqual(entity1.LegalRepresentativeFirstName, entity2.LegalRepresentativeFirstName)
            self.assertEqual(entity1.LegalRepresentativeLastName, entity2.LegalRepresentativeLastName)
            #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.assertEqual(entity1.LegalRepresentativeAddress, entity2.LegalRepresentativeAddress, "***** TEMPORARY API ISSUE: RETURNED OBJECT MISSES THIS PROP AFTER CREATION *****")
            self.assertEqual(entity1.LegalRepresentativeEmail, entity2.LegalRepresentativeEmail)
            self.assertEqual(entity1.LegalRepresentativeBirthday, entity2.LegalRepresentativeBirthday, "***** TEMPORARY API ISSUE: RETURNED OBJECT HAS THIS PROP CHANGED FROM TIMESTAMP INTO ISO STRING AFTER CREATION *****")
            self.assertEqual(entity1.LegalRepresentativeNationality, entity2.LegalRepresentativeNationality)
            self.assertEqual(entity1.LegalRepresentativeCountryOfResidence, entity2.LegalRepresentativeCountryOfResidence)

        elif (isinstance(entity1, BankAccount)):
            self.assertEqual(entity1.Tag, entity2.Tag)
            self.assertEqual(entity1.Type, entity2.Type)
            self.assertEqual(entity1.OwnerName, entity2.OwnerName)
            self.assertEqual(entity1.OwnerAddress, entity2.OwnerAddress)
            self.assertEqual(entity1.IBAN, entity2.IBAN)
            self.assertEqual(entity1.BIC, entity2.BIC)
            if (not asFreshlyCreated): self.assertEqual(entity1.UserId, entity2.UserId)
            
        elif (isinstance(entity1, PayIn)):
            self.assertEqual(entity1.Tag, entity2.Tag)
            self.assertEqual(entity1.AuthorId, entity2.AuthorId)
            self.assertEqual(entity1.CreditedUserId, entity2.CreditedUserId)
            self.assertEqualInputProps(entity1.DebitedFunds, entity2.DebitedFunds)
            self.assertEqualInputProps(entity1.CreditedFunds, entity2.CreditedFunds)
            self.assertEqualInputProps(entity1.Fees, entity2.Fees)
            
        elif (isinstance(entity1, PayInPaymentDetailsCard)):
            self.assertEqual(entity1.CardType, entity2.CardType)
            self.assertEqual(entity1.RedirectURL, entity2.RedirectURL)
            self.assertEqual(entity1.ReturnURL, entity2.ReturnURL)
            
        elif (isinstance(entity1, PayInExecutionDetailsWeb)):
            self.assertEqual(entity1.TemplateURL, entity2.TemplateURL)
            self.assertEqual(entity1.Culture, entity2.Culture)
            self.assertEqual(entity1.SecureMode, entity2.SecureMode)
            
        elif (isinstance(entity1, PayOut)):
            self.assertEqual(entity1.Tag, entity2.Tag)
            self.assertEqual(entity1.AuthorId, entity2.AuthorId)
            self.assertEqual(entity1.CreditedUserId, entity2.CreditedUserId)
            self.assertEqualInputProps(entity1.DebitedFunds, entity2.DebitedFunds)
            self.assertEqualInputProps(entity1.CreditedFunds, entity2.CreditedFunds)
            self.assertEqualInputProps(entity1.Fees, entity2.Fees)
            self.assertEqualInputProps(entity1.MeanOfPayment, entity2.MeanOfPayment)
            
        elif (isinstance(entity1, Transfer)):
            self.assertEqual(entity1.Tag, entity2.Tag)
            self.assertEqual(entity1.AuthorId, entity2.AuthorId)
            self.assertEqual(entity1.CreditedUserId, entity2.CreditedUserId)
            self.assertEqualInputProps(entity1.DebitedFunds, entity2.DebitedFunds)
            self.assertEqualInputProps(entity1.CreditedFunds, entity2.CreditedFunds)
            self.assertEqualInputProps(entity1.Fees, entity2.Fees)
            
        elif (isinstance(entity1, PayOutPaymentDetailsBankWire)):
            self.assertEqual(entity1.BankAccountId, entity2.BankAccountId)
            self.assertEqual(entity1.Communication, entity2.Communication)
            
        elif (isinstance(entity1, Transaction)):
            self.assertEqual(entity1.Tag, entity2.Tag)
            self.assertEqualInputProps(entity1.DebitedFunds, entity2.DebitedFunds)
            self.assertEqualInputProps(entity1.CreditedFunds, entity2.CreditedFunds)
            self.assertEqualInputProps(entity1.Fees, entity2.Fees)
            self.assertEqual(entity1.Status, entity2.Status)

        elif (isinstance(entity1, Money)):
            self.assertEqual(entity1.Currency, entity2.Currency)
            self.assertEqual(entity1.Amount, entity2.Amount)
        else:
            raise Exception("Unsupported type")
