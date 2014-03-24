import unittest, logging, time, requests
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
from mangopaysdk.entities.card import Card
from mangopaysdk.entities.refund import Refund
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.entities.cardpreauthorization import CardPreAuthorization
from mangopaysdk.entities.hook import Hook
from mangopaysdk.tools.enums import *
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from mangopaysdk.types.payinexecutiondetailsweb import PayInExecutionDetailsWeb
from mangopaysdk.types.payoutpaymentdetailsbankwire import PayOutPaymentDetailsBankWire
from mangopaysdk.types.payinexecutiondetailsdirect import PayInExecutionDetailsDirect
from mangopaysdk.types.payinpaymentdetailsbankwire import PayInPaymentDetailsBankWire
from mangopaysdk.types.payinpaymentdetailspreauthorized import PayInPaymentDetailsPreAuthorized
from mangopaysdk.types.money import Money
from mangopaysdk.tools.storages.memorystoragestrategy import MemoryStorageStrategy
from mangopaysdk.types.pagination import Pagination
from mangopaysdk.types.bankaccountdetailsiban import BankAccountDetailsIBAN


class TestBase(unittest.TestCase):
        
    def __init__(self, methodName='runTest'):
        self.sdk = self.buildNewMangoPayApi()
        super(TestBase, self).__init__(methodName)
        self._john = None
        self._matrix = None
        self._johnsAccount = None
        self._johnsWallet = None
        self._johnsWalletWithMoney = None
        self._payInPaymentDetailsCard = None
        self._payInExecutionDetailsWeb = None
        self._johnsPayOutBankWire = None    
        self._johnsCardRegistration = None
        self._johnsKycDocument = None
        self._johnsCardPreAuthorization = None
        self._johnsHook = None

    def buildNewMangoPayApi(self):
        sdk = MangoPayApi()
        # use test client credentails
        sdk.Config.ClientID = 'sdk-unit-tests'
        sdk.Config.ClientPassword = 'cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju'
        sdk.OAuthTokenManager.RegisterCustomStorageStrategy(MemoryStorageStrategy())
        return sdk

    def getJohn(self):
        """Creates TestBase._john (test natural user) if not created yet"""
        if (self._john == None):
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
            self._john = self.sdk.users.Create(user)
            self.assertEqualInputProps(self._john, user, True)
        return self._john

    def getMatrix(self):
        """Creates TestBase._matrix (test legal user) if not created yet"""
        if (self._matrix == None):
            john = self.getJohn()
            user = UserLegal()
            user.Name = "MartixSampleOrg"
            user.Email = "john.doe@sample.org"
            user.LegalPersonType = "BUSINESS"
            user.HeadquartersAddress = "Some Address"
            user.LegalRepresentativeFirstName = john.FirstName
            user.LegalRepresentativeLastName = john.LastName
            user.LegalRepresentativeAddress = john.Address
            user.LegalRepresentativeEmail = john.Email
            user.LegalRepresentativeBirthday = john.Birthday
            user.LegalRepresentativeNationality = john.Nationality
            user.LegalRepresentativeCountryOfResidence = john.CountryOfResidence
            self._matrix = self.sdk.users.Create(user)
            self.assertEqualInputProps(self._matrix, user, True)
        return self._matrix
    
    def getJohnsAccount(self):
        """Creates TestBase._johnsAccount (bank account belonging to John) if not created yet"""
        if self._johnsAccount == None:
            john = self.getJohn()
            account = BankAccount()
            account.OwnerName = john.FirstName + ' ' +  john.LastName
            account.OwnerAddress = john.Address
            account.UserId = john.Id
            account.Type = 'IBAN'
            account.Details = BankAccountDetailsIBAN()
            account.Details.IBAN = 'FR7617906000320008335232973'
            account.Details.BIC = 'BINAADADXXX'
            self._johnsAccount = self.sdk.users.CreateBankAccount(john.Id, account)
            self.assertEqualInputProps(self._johnsAccount, account, True)
        return self._johnsAccount
    
    def getJohnsWallet(self):
        """Creates TestBase._johnsWallet (wallets belonging to John) if not created yet"""
        if self._johnsWallet == None:
            john = self.getJohn()
            wallet = Wallet()
            wallet.Owners = [john.Id]
            wallet.Currency = 'EUR'
            wallet.Description = 'WALLET IN EUR'            
            self._johnsWallet = self.sdk.wallets.Create(wallet)
            #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #self.assertEqualInputProps(self._johnsWallet, wallet, True)
        return self._johnsWallet
    
    def getJohnsWalletWithMoney(self, amount = 10000):
        """Creates static JohnsWallet (wallets belonging to John) if not created yet
        return Wallet
        """
        if self._johnsWalletWithMoney == None:
            john = self.getJohn()
            wallet = Wallet()
            wallet.Owners = [john.Id]
            wallet.Currency = 'EUR'
            wallet.Description = 'WALLET IN EUR'            
            wallet = self.sdk.wallets.Create(wallet)    
            cardRegistration = CardRegistration()
            cardRegistration.UserId = wallet.Owners[0]
            cardRegistration.Currency = 'EUR'
            cardRegistration = self.sdk.cardRegistrations.Create(cardRegistration)
            cardRegistration.RegistrationData = self.getPaylineCorrectRegistartionData(cardRegistration)
            cardRegistration = self.sdk.cardRegistrations.Update(cardRegistration)
            card = self.sdk.cards.Get(cardRegistration.CardId)
            # create pay-in CARD DIRECT
            payIn = PayIn()
            payIn.CreditedWalletId = wallet.Id
            payIn.AuthorId = cardRegistration.UserId
            payIn.DebitedFunds = Money()
            payIn.DebitedFunds.Amount = amount
            payIn.DebitedFunds.Currency = 'EUR'
            payIn.Fees = Money()
            payIn.Fees.Amount = 0
            payIn.Fees.Currency = 'EUR'
            # payment type as CARD
            payIn.PaymentDetails = PayInPaymentDetailsCard()
            if (card.CardType == 'CB' or card.CardType == 'VISA' or card.CardType == 'MASTERCARD' or card.CardType == CardType.CB_VISA_MASTERCARD):
                payIn.PaymentDetails.CardType = CardType.CB_VISA_MASTERCARD
            # elif (card.CardType == CardType.AMEX):
            #    payIn.PaymentDetails.CardType = CardType.AMEX

            # execution type as DIRECT
            payIn.ExecutionDetails = PayInExecutionDetailsDirect()
            payIn.ExecutionDetails.CardId = card.Id
            payIn.ExecutionDetails.SecureModeReturnURL = 'http://test.com'
            # create Pay-In
            self.sdk.payIns.Create(payIn)
            self._johnsWalletWithMoney = self.sdk.wallets.Get(wallet.Id)
        return self._johnsWalletWithMoney
    
    def getPayInPaymentDetailsCard(self):
        """return PayInPaymentDetailsCard"""
        if self._payInPaymentDetailsCard == None:
            self._payInPaymentDetailsCard = PayInPaymentDetailsCard()
            self._payInPaymentDetailsCard.CardType = CardType.CB_VISA_MASTERCARD
        return self._payInPaymentDetailsCard
    
    def getPayInExecutionDetailsWeb(self):
        """return PayInExecutionDetailsWeb"""
        if self._payInExecutionDetailsWeb == None:
            self._payInExecutionDetailsWeb = PayInExecutionDetailsWeb()
            self._payInExecutionDetailsWeb.ReturnURL = 'https://test.com'
            self._payInExecutionDetailsWeb.TemplateURL = 'https://TemplateURL.com'
            self._payInExecutionDetailsWeb.SecureMode = 'DEFAULT'
            self._payInExecutionDetailsWeb.Culture = 'fr'
        return self._payInExecutionDetailsWeb
    
    def getJohnsPayInCardWeb(self):
        """Creates Pay-In Card Web object"""       
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
        return self.sdk.payIns.Create(payIn)

    def getJohnsPayInCardDirect(self, wallet = None):
        """Creates Pay-In Card Direct object
        return PayIn
        """
        if wallet == None:
            wallet = self.getJohnsWallet()

        cardRegistration = CardRegistration()
        cardRegistration.UserId = wallet.Owners[0]
        cardRegistration.Currency = 'EUR'
        cardRegistration = self.sdk.cardRegistrations.Create(cardRegistration)
        cardRegistration.RegistrationData = self.getPaylineCorrectRegistartionData(cardRegistration)
        cardRegistration = self.sdk.cardRegistrations.Update(cardRegistration)
        card = self.sdk.cards.Get(cardRegistration.CardId)
            
        # create pay-in CARD DIRECT
        payIn = PayIn()
        payIn.CreditedWalletId = wallet.Id
        payIn.AuthorId = wallet.Owners[0]
        payIn.DebitedFunds = Money()
        payIn.DebitedFunds.Amount = 10000
        payIn.DebitedFunds.Currency = 'EUR'
        payIn.Fees = Money()
        payIn.Fees.Amount = 0
        payIn.Fees.Currency = 'EUR'
        # payment type as CARD
        payIn.PaymentDetails = PayInPaymentDetailsCard()
        if (card.CardType == 'CB' or card.CardType == 'VISA' or card.CardType == 'MASTERCARD' or card.CardType == CardType.CB_VISA_MASTERCARD):
            payIn.PaymentDetails.CardType = CardType.CB_VISA_MASTERCARD
        #elif (card.CardType == CardType.AMEX):
        #    payIn.PaymentDetails.CardType = CardType.AMEX
        # execution type as DIRECT
        payIn.ExecutionDetails = PayInExecutionDetailsDirect()
        payIn.ExecutionDetails.CardId = card.Id
        payIn.ExecutionDetails.SecureModeReturnURL = 'http://test.com'
        return self.sdk.payIns.Create(payIn)
    
    def getJohnsPayInBankWireDirect(self):
        wallet = self.getJohnsWallet()        
        payIn = PayIn()
        payIn.CreditedWalletId = wallet.Id
        payIn.AuthorId = wallet.Owners[0]
       
        # payment type as CARD
        payIn.PaymentDetails = PayInPaymentDetailsBankWire()
        payIn.PaymentDetails.DeclaredDebitedFunds = Money()
        payIn.PaymentDetails.DeclaredFees = Money()
        payIn.PaymentDetails.DeclaredDebitedFunds.Currency = 'EUR'
        payIn.PaymentDetails.DeclaredFees.Currency = 'EUR'
        payIn.PaymentDetails.DeclaredDebitedFunds.Amount = 10000
        payIn.PaymentDetails.DeclaredFees.Amount = 1000
       
        # execution type as DIRECT
        payIn.ExecutionDetails = PayInExecutionDetailsDirect()
        payIn.ExecutionType = ExecutionType.DIRECT
        return self.sdk.payIns.Create(payIn)
    
    def getJohnsPayOutBankWire(self):
        """Creates Pay-Out  Bank Wire object"""
        if self._johnsPayOutBankWire == None:
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

            self._johnsPayOutBankWire = self.sdk.payOuts.Create(payOut)
        return self._johnsPayOutBankWire

    def getJohnsTransfer(self, walletWithMoney = None, wallet = None):
        """Creates Pay-Out  Bank Wire object"""
        
        if walletWithMoney == None:
            walletWithMoney = self.getJohnsWalletWithMoney()
        if wallet == None:
            wallet = Wallet()
            wallet.Owners = [walletWithMoney.Owners[0]]
            wallet.Currency = 'EUR'
            wallet.Description = 'WALLET IN EUR'
            wallet = self.sdk.wallets.Create(wallet)

        transfer = Transfer()
        transfer.Tag = 'DefaultTag'
        transfer.AuthorId = walletWithMoney.Owners[0]
        transfer.CreditedUserId = walletWithMoney.Owners[0]
        transfer.DebitedFunds = Money()
        transfer.DebitedFunds.Currency = 'EUR'
        transfer.DebitedFunds.Amount = 100
        transfer.Fees = Money()
        transfer.Fees.Currency = 'EUR'
        transfer.Fees.Amount = 0
        transfer.DebitedWalletId = walletWithMoney.Id
        transfer.CreditedWalletId = wallet.Id
        return self.sdk.transfers.Create(transfer)

    def getJohnsRefundForTransfer(self, transfer = None):
        """Creates refund object for transfer
        return Refund
        """
        if transfer == None:
            transfer = self.getJohnsTransfer()
        refund = Refund()
        refund.DebitedWalletId = transfer.DebitedWalletId
        refund.CreditedWalletId = transfer.CreditedWalletId
        refund.AuthorId = transfer.AuthorId
        refund.DebitedFunds = Money()
        refund.DebitedFunds.Amount = transfer.DebitedFunds.Amount
        refund.DebitedFunds.Currency = transfer.DebitedFunds.Currency
        refund.Fees = Money()
        refund.Fees.Amount = transfer.Fees.Amount
        refund.Fees.Currency = transfer.Fees.Currency
        return self.sdk.transfers.CreateRefund(transfer.Id, refund)
    
    def getJohnsRefundForPayIn(self, payIn = None):
        """ Creates refund object for PayIn
        return Refund
        """
        if payIn == None:
            payIn = self.getJohnsPayInCardDirect()
        
        refund = Refund()
        refund.CreditedWalletId = payIn.CreditedWalletId
        refund.AuthorId = payIn.AuthorId
        refund.DebitedFunds = Money()
        refund.DebitedFunds.Amount = payIn.DebitedFunds.Amount
        refund.DebitedFunds.Currency = payIn.DebitedFunds.Currency
        refund.Fees = Money()
        refund.Fees.Amount = payIn.Fees.Amount
        refund.Fees.Currency = payIn.Fees.Currency
        return self.sdk.payIns.CreateRefund(payIn.Id, refund)
        
    def getJohnsCardRegistration(self):
        """Creates card registration object.
        return CardRegistration 
        """
        if (self._johnsCardRegistration == None):
            user = self.getJohn()
            cardRegistration = CardRegistration()
            cardRegistration.UserId = user.Id
            cardRegistration.Currency = 'EUR'
            self._johnsCardRegistration = self.sdk.cardRegistrations.Create(cardRegistration)
        return self._johnsCardRegistration

    def getJohnsCardPreAuthorization(self):
        """Creates card pre authorization object.
        return CardPreAuthorization 
        """
        if (self._johnsCardPreAuthorization == None):
            user = self.getJohn()
            payIn = self.getJohnsPayInCardDirect()
            cardPreAuthorization = CardPreAuthorization()
            cardPreAuthorization.AuthorId = user.Id
            cardPreAuthorization.Tag = 'Test Card PreAuthorization'
            cardPreAuthorization.CardId = payIn.ExecutionDetails.CardId
            cardPreAuthorization.SecureMode = Mode3DSType.DEFAULT
            cardPreAuthorization.SecureModeReturnURL = 'https://test.com'
            cardPreAuthorization.DebitedFunds = Money()
            cardPreAuthorization.DebitedFunds.Amount = 1000
            cardPreAuthorization.DebitedFunds.Currency = 'EUR'
            self._johnsCardPreAuthorization = self.sdk.cardPreAuthorizations.Create(cardPreAuthorization)
        return self._johnsCardPreAuthorization


    def getPaylineCorrectRegistartionData(self, cardRegistration):
        """Get registration data from Payline service
        param CardRegistration cardRegistration
        return string
        """
        data = 'data=' + cardRegistration.PreregistrationData + '&accessKeyRef=' + cardRegistration.AccessKey;
        data += '&cardNumber=4970100000000154&cardExpirationDate=1214&cardCvx=123'
        headers = {"Content-Type" : "application/x-www-form-urlencoded", 'Connection':'close'}
        response = requests.post(cardRegistration.CardRegistrationURL, data, verify=False, headers=headers)
        if response.status_code != requests.codes.ok:
            raise ResponseException(response.request.url, response.status_code, response.text)
        return response.text
    
    def getUserKycDocument(self):
        """Creates KycDocument
        return KycDocument 
        """
        if (self._johnsKycDocument == None):
            user = self.getJohn()
            kycDocument = KycDocument()
            kycDocument.Tag = 'test tag 1'
            kycDocument.Type = KycDocumentType.IDENTITY_PROOF
            self._johnsKycDocument = self.sdk.users.CreateUserKycDocument(kycDocument, user.Id)
        return self._johnsKycDocument

    def getJohnHook(self):
        if self._johnsHook == None:
            pagination = Pagination(1, 1)
            list = self.sdk.hooks.GetAll(pagination)
            
            if list[0] != None:
                self._johnsHook = list[0]
            else:
                hook = Hook()
                hook.EventType = EventType.PAYIN_NORMAL_CREATED
                hook.Url = 'http://test.com'
                self._johnsHook = self.sdk.hooks.Create(hook)
        
        return self._johnsHook

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
            self.assertEqual(entity1.UserId, entity2.UserId)
            self.assertEqual(entity1.Type, entity2.Type)
            self.assertEqual(entity1.OwnerName, entity2.OwnerName)
            self.assertEqual(entity1.OwnerAddress, entity2.OwnerAddress)
            if (entity1.Type == 'IBAN'):
                self.assertEqual(entity1.Details.IBAN, entity2.Details.IBAN)
                self.assertEqual(entity1.Details.BIC, entity2.Details.BIC)
            elif (entity1.Type == 'GB'):
                self.assertEqual(entity1.Details.AccountNumber, entity2.Details.AccountNumber)
                self.assertEqual(entity1.Details.SortCode, entity2.Details.SortCode)
            elif (entity1.Type == 'US'):
                self.assertEqual(entity1.Details.AccountNumber, entity2.Details.AccountNumber)
                self.assertEqual(entity1.Details.ABA, entity2.Details.ABA)
            elif (entity1.Type == 'CA'):
                self.assertEqual(entity1.Details.BankName, entity2.Details.BankName)
                self.assertEqual(entity1.Details.InstitutionNumber, entity2.Details.InstitutionNumber)
                self.assertEqual(entity1.Details.BranchCode, entity2.Details.BranchCode)
                self.assertEqual(entity1.Details.AccountNumber, entity2.Details.AccountNumber)
            elif (entity1.Type == 'OTHER'):
                self.assertEqual(entity1.Details.Type, entity2.Details.Type)
                self.assertEqual(entity1.Details.Country, entity2.Details.Country)
                self.assertEqual(entity1.Details.BIC, entity2.Details.BIC)
                self.assertEqual(entity1.Details.AccountNumber, entity2.Details.AccountNumber)
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
