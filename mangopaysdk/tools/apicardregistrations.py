from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.cardregistration import CardRegistration
from mangopaysdk.entities.temporarypaymentcard import TemporaryPaymentCard


class ApiCardRegistrations (ApiBase):
    """Class to management MangoPay API for card registrations."""

    def Create(self, cardRegistration):
        """Create new card registration
        param CardRegistration object to create
        return CardRegistration Object returned from API
        """
        return self.CreateIdempotent(None, cardRegistration)

    def CreateIdempotent(self, idempotencyKey, cardRegistration):
        """Create new card registration
        param string idempotencyKey Idempotency key for this request
        param CardRegistration object to create
        return CardRegistration Object returned from API
        """
        return self._createObjectIdempotent(idempotencyKey, 'cardregistration_create', cardRegistration, 'CardRegistration')

    def Get(self, cardRegistrationId):
        """Get card registration
        param string Card Registration identifier
        return CardRegistration Object returned from API
        """
        return self._getObject('cardregistration_get', cardRegistrationId, 'CardRegistration')

    def Update(self, cardRegistration):
        """Update card registration
        param CardRegistration object to save
        return CardRegistration Object returned from API
        """
        return self._saveObject('cardregistration_save', cardRegistration, 'CardRegistration')


    def CreateTemporaryPaymentCard(self, paymentCard):
        """WARNING! 
        This is temporary function and will be removed in future.
        Contact support before using these features or if have any queries.

        Creates new temporary payment card.
        param TemporaryPaymentCard Temporary payment card to be created
        return TemporaryPaymentCard Object returned from API
        """
        return self.CreateTemporaryPaymentCardIdempotent(None, paymentCard)

    def CreateTemporaryPaymentCardIdempotent(self, idempotencyKey, paymentCard):
        """WARNING! 
        This is temporary function and will be removed in future.
        Contact support before using these features or if have any queries.

        Creates new temporary payment card.
        param string idempotencyKey Idempotency key for this request
        param TemporaryPaymentCard Temporary payment card to be created
        return TemporaryPaymentCard Object returned from API
        """
        return self._createObjectIdempotent(idempotencyKey, 'temp_paymentcards_create', paymentCard, 'TemporaryPaymentCard')

    def GetTemporaryPaymentCard(self, paymentCardId):
        """WARNING! 
        This is temporary function and will be removed in future.
        Contact support before using these features or if have any queries.

        Gets temporary payment card.
        param string Temporary payment card identifier
        return TemporaryPaymentCard Object returned from API
        """
        return self._getObject('temp_paymentcards_get', paymentCardId, 'TemporaryPaymentCard')