from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.entities.cardregistration import CardRegistration


class ApiCardRegistrations (ApiBase):
    """Class to management MangoPay API for card registrations."""

    def Create(self, cardRegistration):
        """Create new card registration
        param CardRegistration object to create
        return CardRegistration Object returned from API
        """
        return self._createObject('cardregistration_create', cardRegistration, 'CardRegistration')

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