from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.resttool import RestTool
from mangopaysdk.entities.client import Client
from mangopaysdk.entities.clientlogo import ClientLogo
import os

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

        rest = RestTool(self._root, False)
        response = rest.Request(urlMethod, requestType, requestData)
        return self._castResponseToEntity(response, 'Client');

    def Get(self):
        return self._getObject('client_get', None, 'Client')

    def Update(self, client):
        return self._saveObject('client_save', client, 'Client')

    def UploadLogo(self, filePath):

        if (filePath == None or filePath == ''):
            raise Exception('Path of file cannot be empty')

        if (not os.path.isfile(filePath)):
            raise Exception('File not exist: ' + filePath)

        clientLogo = ClientLogo().LoadFromFile(filePath)

        if (clientLogo.File == None):
            raise Exception('Content of the file cannot be empty')

        self._saveObject('client_upload_logo', clientLogo)