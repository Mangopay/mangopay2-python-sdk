from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.resttool import RestTool
from mangopaysdk.entities.client import Client
from mangopaysdk.entities.clientlogo import ClientLogo
from mangopaysdk.tools.enums import FundsType
from mangopaysdk.tools.filtertransactions import FilterTransactions
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

    def GetWallets(self, fundsType, pagination = None):
        
        if (fundsType == None):
            return None

        if (fundsType == FundsType.DEFAULT):
            return self._getList('client_get_wallets_default', pagination, 'Wallet')
        else:
            if (fundsType == FundsType.FEES):
                return self._getList('client_get_wallets_fees', pagination, 'Wallet')
            else:
                if (fundsType == FundsType.CREDIT):
                    return self._getList('client_get_wallets_credit', pagination, 'Wallet')

        return None

    def GetWallet(self, fundsType, currency):

        if (fundsType == None or currency == None):
            return None

        if (fundsType == FundsType.DEFAULT):
            return self._getObject('client_get_wallets_default_with_currency', currency, 'Wallet')
        else:
            if (fundsType == FundsType.FEES):
                return self._getObject('client_get_wallets_fees_with_currency', currency, 'Wallet')
            else:
                if (fundsType == FundsType.CREDIT):
                    return self._getObject('client_get_wallets_credit_with_currency', currency, 'Wallet')

        return None

    def GetWalletTransactions(self, fundsType, currency, pagination = None, filter = None, sorting = None):

        if (filter == None):
            filter = FilterTransactions()

        return self._getList('client_get_wallet_transactions', pagination, 'Transaction', fundsType, filter, sorting, currency)