from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.payin import PayIn


class ApiPayIns (ApiBase):
    """MangoPay API methods for pay-in transactions."""

    def Create(self, payIn):
        """Create new pay-in object.
        param PayIn payIn object
        return PayIn Object returned from API
        """
        paymentKey = self._getPaymentKey(payIn);
        executionKey = self._getExecutionKey(payIn);
        return self._createObject('payins_' + paymentKey + '-' + executionKey + '_create', payIn, 'PayIn')

    def Get(self, payInId):
        """Get pay-in object.
        param payInId Pay-in identifier
        return PayIn Object returned from API
        """
        return self._getObject('payins_get', payInId, 'PayIn')

    def CreateRefund(self, payInId, refund):
        """Create refund for pay-in object.
        param type payInId Pay-in identifier
        param Refund refund object to create
        return Refund Object returned by REST API
        """
        return self._createObject('payins_createrefunds', payInId, 'Refund', refund)

    def GetRefund(self, payInId):
        """Get refund for pay-in object.
        param type payInId Pay-in identifier
        return Refund Object returned by REST API
        """
        return self._getObject('payins_getrefunds', payInId, 'Refund')

    def _getPaymentKey(self, payIn):

        if payIn.PaymentDetails == None:
            raise Exception ('Payment is not defined or it is invalid object type')

        className = payIn.PaymentDetails.__class__.__name__.replace('PayInPaymentDetails', '')
        return className.lower()


    def _getExecutionKey(self, payIn):
        if payIn.ExecutionDetails == None:
            raise Exception ('Execution is not defined or it is not object type')

        className = payIn.ExecutionDetails.__class__.__name__.replace('PayInExecutionDetails', '')
        return className.lower()
