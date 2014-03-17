from mangopaysdk.tools.apibase import ApiBase

class ApiHooks(ApiBase):
    """MangoPay API for hooks and notifications."""

    def Create(self, hook):
        """Creates a new hook.
        param Hook hook
        return Newly created hook object returned from API
        """
        return self._createObject('hooks_create', hook, 'Hook')
    
    def Get(self, hookId):
        """Gets hook.
        param type hookId Hook identifier
        return Hook object returned from API
        """
        return self._getObject('hooks_get', hookId, 'Hook')
    
    def Update(self, hook):
        """Updates a hook.
        param Hook hook Hook object to update
        return Updated hook object returned from API
        """
        return self._saveObject('hooks_save', hook, 'Hook')
    
    def GetAll(self, pagination = None):
        """Gets all hooks.
        return Array of objects returned from API
        """
        return self._getList('hooks_all', pagination, 'Hook')