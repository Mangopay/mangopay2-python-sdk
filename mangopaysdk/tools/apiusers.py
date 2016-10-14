import base64
import warnings

from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.sorting import Sorting
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
        return self.CreateIdempotent(None, user)

    def CreateIdempotent(self, idempotencyKey, user):
        """Create new user.
        param string idempotencyKey Idempotency key for this request
        param UserLegal/UserNatural user (list of required fields in coresponding entity class)
        return UserLegal/UserNatural User object returned from API
        """
        if isinstance(user, UserNatural):
            methodKey = 'users_createnaturals'
        elif isinstance(user, UserLegal):
            methodKey = 'users_createlegals'
        else:
            raise Exception('Wrong entity class for user');

        response = self._createObjectIdempotent(idempotencyKey, methodKey, user)
        return self.GetUserResponse(response)

    def GetAll(self, pagination = None, sorting = None):
        """Get all users.
        param Pagination object
        param Sorting object
        return Array with users
        """
        usersList = self._getList('users_all', pagination, None, None, None, sorting)
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
        return self.CreateBankAccountIdempotent(None, userId, bankAccount)

    def UpdateBankAccount(self, userId, bankAccount, bankAccountId):
        """Update bank account.
        param Int/GUID userId
        param BankAccount Entity of bank account with two (optional) fields: Tag and Active (the latter one if provided has to be boolean False)
        param Int/GUID bankAccountId
        return BankAccount Updated bank account object
        """
        return self._saveObject('users_updatebankaccount', bankAccount, 'BankAccount', userId, bankAccountId)

    def CreateBankAccountIdempotent(self, idempotencyKey, userId, bankAccount):
        """Create bank account for user.
        param string idempotencyKey Idempotency key for this request
        param Int/GUID userId
        param BankAccount Entity of bank account with fields: OwnerName, UserId, Type, OwnerAddress,IBAN, BIC, Tag
        return BankAccount Create bank account object
        """
        type = self.GetBankAccountType(bankAccount)
        return self._createObjectIdempotent(idempotencyKey, 'users_createbankaccounts_' + type, bankAccount, 'BankAccount', userId)

    def GetBankAccounts(self, userId, pagination = None, sorting = None):
        """Get all bank accounts for user.
        param Int/GUID userId
        param Pagination object
        param Sorting object
        return array with bank account entities
        """
        return self._getList('users_allbankaccount', pagination, 'BankAccount', userId, None, sorting)

    def GetBankAccount(self, userId, bankAccountId):
        """Get bank account for user.
        param Int/GUID userId
        param int bankAccountId number
        return BankAccount Entity of bank account object
        """
        return self._getObject('users_getbankaccount', userId, 'BankAccount', bankAccountId)

    def GetCards(self, userId, pagination = None, sorting = None):
        """Get user payment cards.
        param Int/GUID userId
        param Pagination object
        param Sorting object
        return array or card entities
        """
        return self._getList('users_getcards', pagination, 'Card', userId, None, sorting)

    def GetTransactions(self, userId, pagination = None, sorting = None, filter = None):
        """Get user payment cards.
        param Int/GUID userId
        param Pagination object
        param Sorting object
        param object filter Object to filter data
        return array or transactions
        """
        return self._getList('users_transactions', pagination, 'Transaction', userId, filter, sorting)

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
        return self.CreateUserKycDocumentIdempotent(None, kycDocument, userId)

    def CreateUserKycDocumentIdempotent(self, idempotencyKey, kycDocument, userId):
        """Create KycDocument
        param string idempotencyKey Idempotency key for this request
        param KycDocument entity with Type and Tag set
        param Int/GUID User identifier
        return KycDocument from API with fileds: Id, Tag, CreationDate, Type, Status, RefusedReasonType, RefusedReasonMessage
        """
        return self._createObjectIdempotent(idempotencyKey, 'users_createkycdocument', kycDocument, 'KycDocument', userId)

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
        return self.CreateUserKycPageIdempotent(None, kycPage, userId, kycDocumentId)

    def CreateUserKycPageIdempotent(self, idempotencyKey, kycPage, userId, kycDocumentId):
        """Create KycPage for existing KycDocument
        param string idempotencyKey Idempotency key for this request
        param KycPage entity (File should be base64 string)
        param Int/GUID User identifier
        param Int/GUID KycDocument identifier
        """
        return self._createObjectIdempotent(idempotencyKey, 'users_createkycpage', kycPage, None, userId, kycDocumentId)

    def UpdateUserKycDocument(self, kycDocument, userId, kycDocumentId=None):
        """Updates KycDocument
        param KycDocument entity (field Status should be set)
        param Int/GUID User identifier
        param Int/GUID KycDocument identifier
        return KycDocument from API with fileds: Id, Tag, CreationDate, Type, Status, RefusedReasonType, RefusedReasonMessage
        """
        if kycDocumentId is not None:
            warnings.warn(
                ("The kycDocumentId argument in the UpdateUserKycDocument "
                 "method has been deprecated and will be removed in the next "
                 "version"),
                DeprecationWarning)
        return self._saveObject('users_savekycdocument', kycDocument, 'KycDocument', userId, kycDocument.Id)

    def CreateKycPageFromFile(self, userId, kycDocumentId, file):
        """Create page for Kyc document from file
        param int userId User identifier
        param KycPage page Kyc
        """

        self.CreateKycPageFromFileIdempotent(None, userId, kycDocumentId, file)

    def CreateKycPageFromFileIdempotent(self, idempotencyKey, userId, kycDocumentId, file):
        """Create page for Kyc document from file
        param string idempotencyKey Idempotency key for this request
        param int userId User identifier
        param KycPage page Kyc
        """

        filePath = file
        #if (isinstance(file, collections.Sequence)):
        #    filePath = file['tmp_name']

        if (filePath == None or filePath == ''):
            raise Exception('Path of file cannot be empty')

        if (not os.path.isfile(filePath)):
            raise Exception('File not exist: ' + filePath)

        kycPage = KycPage().LoadDocumentFromFile(filePath)

        if (kycPage.File == None):
            raise Exception('Content of the file cannot be empty')

        self.CreateUserKycPageIdempotent(idempotencyKey, kycPage, userId, kycDocumentId)

    def GetBankAccountType(self, bankAccount):

        if (bankAccount.Details == None):
            raise Exception('Details is not defined or it is not object type')

        className = bankAccount.Details.__class__.__name__.replace('BankAccountDetails', '').lower()

        return className

    def GetWallets(self, userId, pagination = None, sorting = None):
        """Get all wallets for user.
        param Int/GUID userId
        param Pagination object
        param Sorting sorting
        return array with wallet entities
        """
        return self._getList('users_allwallets', pagination, 'Wallet', userId, None, sorting)

    def GetKycDocuments(self, userId, pagination = None, sorting = None):
        """Gets all KYC documents gor user.
        param string userId
        param Pagination object
        param Sorting object
        return array with KYC documents"""
        return self._getList('users_allkycdocuments', pagination, 'KycDocument', userId, None, sorting)
