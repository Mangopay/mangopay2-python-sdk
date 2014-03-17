import base64
from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.usernatural import UserNatural
from mangopaysdk.entities.bankaccount import BankAccount
from mangopaysdk.entities.kycdocument import KycDocument
from mangopaysdk.entities.kycpage import KycPage
import collections
import os.path


class ApiUsers(ApiBase):
    """MangoPay API methods for users."""

    def Create(self, user):
        """Create new user.
        param UserLegal/UserNatural user (list of required fields in coresponding entity class)
        return UserLegal/UserNatural User object returned from API
        """
        if isinstance(user, UserNatural):
            methodKey = 'users_createnaturals'
        elif isinstance(user, UserLegal):
            methodKey = 'users_createlegals'
        else:
            raise Exception('Wrong entity class for user');

        response = self._createObject(methodKey, user)
        return self.GetUserResponse(response)

    def GetAll(self, pagination = None):
        """Get all users.
        param Pagination object
        return array with users
        """
        usersList = self._getList('users_all', pagination)
        return [self.GetUserResponse(u) for u in usersList]

    def Get(self, userId):
        """Get natural or legal user by ID.
        param Int/GUID userId User identifier
        return UserLegal/UserNatural User object returned from API
        """
        response = self._getObject('users_get', userId)
        return self.GetUserResponse(response)

    def GetNatural(self, userId):
        """Get natural user by ID.
        param Int/GUID userId User identifier
        return UserLegal/UserNatural User object returned from API
        """
        response = self._getObject('users_getnaturals', userId)
        return self.GetUserResponse(response)

    def GetLegal(self, userId):
        """Get legal user by ID.
        param Int/GUID userId User identifier
        return UserLegal/UserNatural User object returned from API
        """
        response = self._getObject('users_getlegals', userId)
        return self.GetUserResponse(response)

    def Update(self, user):
        """Update user.
        param UserLegal/UserNatural
        return UserLegal/UserNatural User object returned from API
        """
        if isinstance(user, UserNatural):
            methodKey = 'users_savenaturals'
        elif isinstance(user, UserLegal):
            methodKey = 'users_savelegals'
        else:
            raise Exception('Wrong entity class for user')

        response = self._saveObject(methodKey, user)
        return self.GetUserResponse(response)

    def CreateBankAccount(self, userId, bankAccount):
        """Create bank account for user.
        param Int/GUID userId 
        param BankAccount Entity of bank account with fields: OwnerName, UserId, Type, OwnerAddress,IBAN, BIC, Tag
        return BankAccount Create bank account object
        """
        type = self.GetBankAccountType(bankAccount)
        return self._createObject('users_createbankaccounts_' + type, bankAccount, 'BankAccount', userId)

    def GetBankAccounts(self, userId, pagination = None):
        """Get all bank accounts for user.
        param Int/GUID userId 
        param Pagination object
        return array with bank account entities
        """
        return self._getList('users_allbankaccount', pagination, 'BankAccount', userId)
        
    def GetBankAccount(self, userId, bankAccountId):
        """Get bank account for user.
        param Int/GUID userId 
        param int bankAccountId number
        return BankAccount Entity of bank account object
        """
        return self._getObject('users_getbankaccount', userId, 'BankAccount', bankAccountId)

    def GetCards(self, userId, pagination = None):
        """Get user payment cards.
        param Int/GUID userId 
        param Pagination object
        return array or card entities
        """
        return self._getList('users_getcards', pagination, 'Card', userId)

    def GetTransactions(self, userId, pagination = None):
        """Get user payment cards.
        param Int/GUID userId 
        param Pagination object
        return array or transactions
        """
        return self._getList('users_transactions', pagination, 'Transaction', userId)

    def GetUserResponse(self, response):
        """Get correct user object - to be used internally.
        param object response Response from API
        return UserNatural User object returned from API
        throws Exception If occur unexpected response from API
        """
        if response['PersonType'] != None:
            if response['PersonType'].lower() == 'natural':
                return self._castResponseToEntity(response, 'UserNatural');
            elif response['PersonType'].lower() == 'legal':
                return self._castResponseToEntity(response, 'UserLegal');
            
        else:
            raise Exception('Unexpected response. Missing PersonType property')

    def CreateUserKycDocument(self, kycDocument, userId):
        """Create KycDocument
        param KycDocument entity with Type and Tag set
        param Int/GUID User identifier
        return KycDocument from API with fileds: Id, Tag, CreationDate, Type, Status, RefusedReasonType, RefusedReasonMessage
        """
        return self._createObject('users_createkycdocument', kycDocument, 'KycDocument', userId)

    def GetUserKycDocument(self, kycDocumentId, userId):
        """Get KycDocument by ID.
        param Int/GUID KycDocument identifier
        param Int/GUID User identifier
        return KycDocument from API with fileds: Id, Tag, CreationDate, Type, Status, RefusedReasonType, RefusedReasonMessage
        """
        return self._getObject('users_getkycdocument', userId, 'KycDocument', kycDocumentId)

    def CreateUserKycPage(self, kycPage, userId, kycDocumentId):
        """Create KycPage for existing KycDocument
        param KycPage entity (File should be base64 string)
        param Int/GUID User identifier
        param Int/GUID KycDocument identifier
        """
        return self._createObject('users_createkycpage', kycPage, None, userId, kycDocumentId)

    def UpdateUserKycDocument(self, kycDocument, userId, kycDocumentId):
        """Updates KycDocument     
        param KycDocument entity (field Status should be set)
        param Int/GUID User identifier
        param Int/GUID KycDocument identifier
        return KycDocument from API with fileds: Id, Tag, CreationDate, Type, Status, RefusedReasonType, RefusedReasonMessage
        """
        return self._saveObject('users_savekycdocument', kycDocument, 'KycDocument', userId, kycDocument.Id)

    def CreateKycPageFromFile(self, userId, kycDocumentId, file):
        """Create page for Kyc document from file
        param int userId User identifier
        param KycPage page Kyc
        """
        
        filePath = file
        #if (isinstance(file, collections.Sequence)):
        #    filePath = file['tmp_name']
        
        if (filePath == None or filePath == ''):
            raise Exception('Path of file cannot be empty')
        
        if (not os.path.isfile(filePath)):
            raise Exception('File not exist')
        
        kycPage = KycPage()
        with open(filePath) as f:
            encoded = base64.encodestring(f.read())
        kycPage.File = encoded
        
        if (kycPage.File == None):
            raise Exception('Content of the file cannot be empty')
        
        self.CreateUserKycPage(kycPage, userId, kycDocumentId)

    def GetBankAccountType(self, bankAccount):
        
        if (bankAccount.Details == None):
            raise Exception('Details is not defined or it is not object type')
        
        className = bankAccount.Details.__class__.__name__.replace('BankAccountDetails', '').lower()

        return className
    