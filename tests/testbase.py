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
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.types.payinpaymentdetailscard import PayInPaymentDetailsCard
from mangopaysdk.types.payinexecutiondetailsweb import PayInExecutionDetailsWeb
from mangopaysdk.types.payoutpaymentdetailsbankwire import PayOutPaymentDetailsBankWire
from mangopaysdk.types.payinexecutiondetailsdirect import PayInExecutionDetailsDirect
from mangopaysdk.types.money import Money
from mangopaysdk.tools.storages.memorystoragestrategy import MemoryStorageStrategy


class TestBase(unittest.TestCase):

    _john = None
    _matrix = None
    _johnsAccount = None
    _johnsWallet = None
    _johnsWalletWithMoney = None
    _payInPaymentDetailsCard = None
    _payInExecutionDetailsWeb = None
    _johnsPayOutBankWire = None    
    _johnsCardRegistration = None
    
    def __init__(self, methodName='runTest'):
        self.sdk = self.buildNewMangoPayApi()
        super(TestBase, self).__init__(methodName)

    def buildNewMangoPayApi(self):
        sdk = MangoPayApi()
        # use test client credentails
        sdk.Config.ClientID = 'example'
        sdk.Config.ClientPassword = 'uyWsmnwMQyTnqKgi8Y35A3eVB7bGhqrebYqA1tL6x2vYNpGPiY'
        sdk.OAuthTokenManager.RegisterCustomStorageStrategy(MemoryStorageStrategy())
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
    
    def getJohnsWalletWithMoney(self, amount = 10000):
        """Creates static JohnsWallet (wallets belonging to John) if not created yet
        return Wallet
        """
        if TestBase._johnsWalletWithMoney == None:
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
            if (card.CardType == 'CB' or card.CardType == 'VISA' or card.CardType == 'MASTERCARD'):
                payIn.PaymentDetails.CardType = 'CB_VISA_MASTERCARD'
            elif (card.CardType == 'AMEX'):
                payIn.PaymentDetails.CardType = 'AMEX'

            # execution type as DIRECT
            payIn.ExecutionDetails = PayInExecutionDetailsDirect()
            payIn.ExecutionDetails.CardId = card.Id
            payIn.ExecutionDetails.SecureModeReturnURL = 'http://test.com'
            # create Pay-In
            self.sdk.payIns.Create(payIn)
            TestBase._johnsWalletWithMoney = self.sdk.wallets.Get(wallet.Id)
        return TestBase._johnsWalletWithMoney
    
    def getPayInPaymentDetailsCard(self):
        """return PayInPaymentDetailsCard"""
        if TestBase._payInPaymentDetailsCard == None:
            TestBase._payInPaymentDetailsCard = PayInPaymentDetailsCard()
            TestBase._payInPaymentDetailsCard.CardType = 'AMEX'
        return TestBase._payInPaymentDetailsCard
    
    def getPayInExecutionDetailsWeb(self):
        """return PayInExecutionDetailsWeb"""
        if TestBase._payInExecutionDetailsWeb == None:
            TestBase._payInExecutionDetailsWeb = PayInExecutionDetailsWeb()
            TestBase._payInExecutionDetailsWeb.ReturnURL = 'https://test.com'
            TestBase._payInExecutionDetailsWeb.TemplateURL = 'https://TemplateURL.com'
            TestBase._payInExecutionDetailsWeb.SecureMode = 'DEFAULT'
            TestBase._payInExecutionDetailsWeb.Culture = 'fr'
        return TestBase._payInExecutionDetailsWeb
    
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
        if (card.CardType == 'CB' or card.CardType == 'VISA' or card.CardType == 'MASTERCARD'):
            payIn.PaymentDetails.CardType = 'CB_VISA_MASTERCARD'
        elif (card.CardType == 'AMEX'):
            payIn.PaymentDetails.CardType = 'AMEX'
        # execution type as DIRECT
        payIn.ExecutionDetails = PayInExecutionDetailsDirect()
        payIn.ExecutionDetails.CardId = card.Id
        payIn.ExecutionDetails.SecureModeReturnURL = 'http://test.com'
        return self.sdk.payIns.Create(payIn)
    
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
        return TestBase._johnsPayOutBankWire

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

    def getPaylineCorrectRegistartionData(self, cardRegistration):
        """Get registration data from Payline service
        param CardRegistration cardRegistration
        return string
        """
        data = 'data=' + cardRegistration.PreregistrationData + '&accessKeyRef=' + cardRegistration.AccessKey;
        data += '&cardNumber=4970101122334406&cardExpirationDate=1214&cardCvx=123'
        headers = {"Content-Type" : "application/x-www-form-urlencoded", 'Connection':'close'}
        response = requests.post(cardRegistration.CardRegistrationURL, data, verify=False, headers=headers)
        if response.status_code != requests.codes.ok:
            raise ResponseException(response.request.url, response.status_code, response.text)
        return response.text
    
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
