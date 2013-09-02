from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.userlegal import UserLegal
from mangopaysdk.entities.usernatural import UserNatural
from mangopaysdk.entities.bankaccount import BankAccount


class ApiUsers(ApiBase):
    """MangoPay API methods for users."""

    def Create(self, user):
        """Create new user.
        param UserLegal/UserNatural user
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
        param int userId User Id
        param BankAccount Entity of bank account object
        return BankAccount Create bank account object
        """
        return self._createObject('users_createbankaccounts', bankAccount, 'BankAccount', userId)

    def GetBankAccounts(self, userId, pagination = None):
        """Get all bank accounts for user.
        param int userId User Id
        param Pagination object
        return array with bank account entities
        """
        return self._getList('users_allbankaccount', pagination, 'BankAccount', userId)
        
    def GetBankAccount(self, userId, bankAccountId):
        """Get bank account for user.
        param int userId User Id
        param int bankAccountId number
        return BankAccount Entity of bank account object
        """
        return self._getObject('users_getbankaccount', userId, 'BankAccount', bankAccountId)

    def GetUserResponse(self, response):
        """Get correct user object.
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
