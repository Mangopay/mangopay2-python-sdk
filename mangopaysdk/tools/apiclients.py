from mangopaysdk.tools.apibase import ApiBase


class ApiClients(ApiBase):
    """MangoPay API methods for users."""

    def Create(self, clientId, clientName, clientEmail):
        """Get client data for Basic Access Authentication.
        param string clientId Client identifier
        param string clientName Beautiful name for presentation
        param string clientEmail Client's email
        return Client object
        """

        urlMethod = self._getRequestUrl('authentication_base')
        requestType = self._getRequestType('authentication_base')
        requestData = {
            'ClientId' : clientId,
            'Name' : clientName,
            'Email' : clientEmail,
        }

        rest = self._getRestToolObject(False)
        response = rest.Request(urlMethod, requestType, requestData)
        return self._castResponseToEntity(response, 'Client');
