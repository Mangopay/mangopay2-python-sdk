from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.resttool import RestTool


class ApiEvents(ApiBase):
    """MangoPay API methods for events."""

    def Get(self, pagination = None, filter = None):
        """Get Events list
        param Pagination pagination object
        param FilterTransactions filter Object to filter data
        return Events[] from API
        """
        return self._getList('events_all', pagination, 'Event', None, filter)