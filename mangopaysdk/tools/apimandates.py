from mangopaysdk.tools.apibase import ApiBase

class ApiMandates(ApiBase):
    """MangoPay API for mandates."""

    def Create(self, mandate):
        """Creates a new mandate.
        param Mandate mandate
        return Newly created mandate object returned from API
        """
        return self.CreateIdempotent(None, mandate)

    def CreateIdempotent(self, idempotencyKey, mandate):
        """Creates a new mandate.
        param string idempotencyKey Idempotency key for this request
        param Mandate mandate
        return Newly created mandate object returned from API
        """
        return self._createObjectIdempotent(idempotencyKey, 'mandate_create', mandate, 'Mandate')
    
    def Get(self, mandateId):
        """Gets mandate.
        param string mandateId Mandate identifier
        return Mandate object returned from API
        """
        return self._getObject('mandate_get', mandateId, 'Mandate')
    
    def Cancel(self, mandate):
        """Cancels a mandate.
        param Mandate mandate Mandate object to cancel
        return Canceled mandate object returned from API
        """
        return self._saveObject('mandate_cancel', mandate, 'Mandate')
    
    def GetAll(self, pagination = None, sorting = None, filters = None):
        """Gets all mandates.
        param Pagination pagination
        param Sorting sorting
        param Filter filter
        return Array of mandate objects returned from API
        """
        return self._getList('mandates_get_all', pagination, 'Mandate', None, filters, sorting)

    def GetForUser(self, userId, pagination = None, sorting = None, filters = None):
        """Gets mandates for user.
        param string userId User identifier.
        param Pagination pagination
        param Sorting sorting
        param Filter filter
        return Array of mandate objects returned from API.
        """
        return self._getList('mandates_get_for_user', pagination, 'Mandate', userId, filters, sorting)

    def GetForBankAccount(self, userId, bankAccountId, pagination = None, sorting = None, filters = None):
        """Gets mandates for user.
        param string userId User identifier.
        param string bankAccountId Bank account identifier.
        param Pagination pagination
        param Sorting sorting
        param Filter filter
        return Array of mandate objects returned from API.
        """
        return self._getList('mandates_get_for_bank_account', pagination, 'Mandate', userId, filters, sorting, bankAccountId)