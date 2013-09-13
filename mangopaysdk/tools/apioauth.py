from mangopaysdk.types.oauthtoken import OAuthToken
from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.resttool import RestTool
import logging


class ApiOAuth(ApiBase):
    """MangoPay API methods for users."""

    def CreateToken(self):
        """Get token information for OAuth Authentication.
        return MangoPay OAuthToken object with token information
        """
        urlMethod = self._getRequestUrl('authentication_oauth')
        requestType = self._getRequestType('authentication_oauth')
        requestData = {
            'grant_type' : 'client_credentials'
        }

        rest = RestTool(self._root, False)
        response = rest.Request(urlMethod, requestType, requestData)
        token = self._castAuthResponseToEntity(response)
        return token
        
    def _castAuthResponseToEntity(self, dict):
        res = OAuthToken()
        res.access_token = dict['access_token']
        res.token_type = dict['token_type']
        res.expires_in = dict['expires_in']
        res.valid = True

        if (self._root.Config.DebugMode): 
            logging.getLogger(__name__).debug('New token created: {0} '.format(res.access_token))
        return res
