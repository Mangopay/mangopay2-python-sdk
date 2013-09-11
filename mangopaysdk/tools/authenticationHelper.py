from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2
from mangopaysdk.tools import enums
from mangopaysdk.configuration import Configuration


class AuthenticationHelper:

    # Root/parent MangoPayApi instance that holds the OAuthToken and Configuration instance
    _root = None

    def __init__ (self, root):
       """Constructor.
       param MangoPayApi Root/parent instance that holds the OAuthToken and Configuration instance
       """
       self._root = root

    def GetRequestAuthObject(self, authRequired):
        """Get HTTP header value with authorization string.
        param authRequired - if False force basic auth
        return string Authorization string
        """
        if authRequired == False: # or self._root.Config.AuthenticationType == enums.AuthenticationType.Basic:
            return HTTPBasicAuth(self._root.Config.ClientID, self._root.Config.ClientPassword)
        else:
            oauth = self._root.OAuthTokenManager.GetToken()
            if not oauth or not oauth.access_token or not oauth.token_type:
                raise Exception('OAuthToken is not created (or is invalid) for strong authentication')
            token = {'access_token' : oauth.access_token, 'token_type' : oauth.token_type}
            return OAuth2(token = token, client_id = self._root.Config.ClientID)
