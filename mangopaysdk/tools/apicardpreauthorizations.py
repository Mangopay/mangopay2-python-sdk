from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.cardpreauthorization import CardPreAuthorization


class ApiCardPreAuthorizations (ApiBase):
    """Class to managemen MangoPay API for card pre-authorization.
       see: http://docs.mangopay.com/api-references/card/pre-authorization/
    """

    def Create(self, cardPreAuthorization):
        """Create new card preauthorization
        param CardPreAuthorization object to create
        return CardPreAuthorization Object returned from API
        """
        return self.CreateIdempotent(None, cardPreAuthorization)

    def CreateIdempotent(self, idempotencyKey, cardPreAuthorization):
        """Create new card preauthorization
        param string idempotencyKey Idempotency key for this request
        param CardPreAuthorization object to create
        return CardPreAuthorization Object returned from API
        """
        return self._createObjectIdempotent(idempotencyKey, 'preauthorizations_create', cardPreAuthorization, 'CardPreAuthorization')

    def Get(self, cardPreAuthorizationId):
        """Get card preauthorization
        param string CardPreAuthorization identifier
        return CardPreAuthorization Object returned from API
        """
        return self._getObject('preauthorizations_get', cardPreAuthorizationId, 'CardPreAuthorization')

    def Update(self, cardPreAuthorization):
        """Update card preauthorization
        param CardPreAuthorization object to save
        return CardPreAuthorization Object returned from API
        """
        return self._saveObject('preauthorizations_save', cardPreAuthorization, 'CardPreAuthorization')