from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.payout import PayOut


class ApiPayOuts (ApiBase):
    """MangoPay API methods for pay-out transactions."""

    def Create(self, payOut):
        """Create new pay-out.
        param PayOut payOut
        return PayOut Object returned from API
        """
        return self.CreateIdempotent(None, payOut)

    def CreateIdempotent(self, idempotencyKey, payOut):
        """Create new pay-out.
        param string idempotencyKey Idempotency key for this request
        param PayOut payOut
        return PayOut Object returned from API
        """
        paymentKey = self._getPaymentKey(payOut)
        return self._createObjectIdempotent(idempotencyKey, 'payouts_' + paymentKey + '_create', payOut, 'PayOut')

    def Get(self, payOutId):
        """Get pay-out object.
        param payOutId PayOut identifier
        return PayOut Object returned from API
        """
        return self._getObject('payouts_get', payOutId, 'PayOut')
        
    def CreateRefund(self, payOutId, refund):
        """Create refund for pay-out object.
        param type payOutId Pay-out identifier
        param Refund refund Refund object to create
        return Refund Object returned by REST API
        """
        return self.CreateRefundIdempotent(None, payOutId, refund)
        
    def CreateRefundIdempotent(self, idempotencyKey, payOutId, refund):
        """Create refund for pay-out object.
        param string idempotencyKey Idempotency key for this request
        param type payOutId Pay-out identifier
        param Refund refund Refund object to create
        return Refund Object returned by REST API
        """
        return self._createObjectIdempotent(idempotencyKey, 'payouts_createrefunds', payOutId, 'PayOut', refund)

    def GetRefund(self, payOutId):
        """Get refund for pay-out object.
        param type payOutId Pay-out identifier
        return Refund Object returned by REST API
        """
        return self._getObject('payouts_getrefunds', payOutId, 'Refund')

    def _getPaymentKey(self, payOut):
        if payOut.MeanOfPaymentDetails == None:
            raise Exception('Mean of payment is not defined or it is not object type');

        className = payOut.MeanOfPaymentDetails.__class__.__name__.replace('PayOutPaymentDetails', '')
        return className.lower()
