from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.transfer import Transfer


class ApiTransfers (ApiBase ):
    """MangoPay API methods for transfers."""

    def Create(self, transfer):
        """Create new transfer.
        param Transfer object
        return Transfer object returned from API
        """
        return self._createObject('transfers_create', transfer, 'Transfer')

    def Get(self, transferId):
        """Get transfer.
        param type transferId Transfer identifier
        return Transfer  object returned from API
        """
        return self._getObject('transfers_get', transferId, 'Transfer')

    def CreateRefund(self, transferId, refund):
        """Create refund for transfer object.
        param type transferId Transfer identifier
        param Refund refund Refund object to create
        return Refund Object returned by REST API
        """
        return self._createObject('transfers_createrefunds', transferId, 'Refund', refund)
        
    def GetRefund(self, transferId):
        """Get refund for transfer object.
        param type transferId Transfer identifier
        return Refund Object returned by REST API
        """
        return self._getObject('transfers_getrefunds', transferId, 'Refund')
       