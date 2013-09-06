from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.refund import Refund


class ApiRefunds(ApiBase):
    """Class to management MangoPay API for refunds"""

    def Get(self, refundId):
        """Get refund object
        param int refundId Refund Id
        return Refund object returned from API
        """
        return self._getObject('refunds_get', refundId, 'Refund')
