from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.transfer import Transfer


class ApiTransfers (ApiBase ):
    """MangoPay API methods for transfers."""

    def Create(self, transfer):
        """Create new transfer.
        param Transfer object with fields: AuthorId, CreditedUserId, DebitedFunds,Fees, DebitedWalletID, CreditedWalletID, Tag
        return Transfer object returned from API
        """
        return self.CreateIdempotent(None, transfer)

    def CreateIdempotent(self, idempotencyKey, transfer):
        """Create new transfer.
        param string idempotencyKey Idempotency key for this request
        param Transfer object with fields: AuthorId, CreditedUserId, DebitedFunds,Fees, DebitedWalletID, CreditedWalletID, Tag
        return Transfer object returned from API
        """
        return self._createObjectIdempotent(idempotencyKey, 'transfers_create', transfer, 'Transfer')

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
        return self._createObject('transfers_createrefunds', refund, 'Refund', transferId)

    def CreateRefundIdempotent(self, idempotencyKey, transferId, refund):
        """Create refund for transfer object.
        param string idempotencyKey Idempotency key for this request
        param type transferId Transfer identifier
        param Refund refund Refund object to create
        return Refund Object returned by REST API
        """
        return self._createObjectIdempotent(idempotencyKey, 'transfers_createrefunds', refund, 'Refund', transferId)
        
    def GetRefund(self, transferId):
        """Get refund for transfer object.
        param type transferId Transfer identifier
        return Refund Object returned by REST API
        """
        return self._getObject('transfers_getrefunds', transferId, 'Refund')
       