import hashlib

from mangopaysdk.tools.apibase import ApiBase
from mangopaysdk.tools.storages.defaultstoragestrategy import DefaultStorageStrategy
from mangopaysdk.types.oauthtoken import OAuthToken


class AuthorizationTokenManager(ApiBase):
    """Authorization token manager."""

    def __init__(self, api):
        self._storageStrategy = DefaultStorageStrategy()
        super(AuthorizationTokenManager, self).__init__(api)
    
    def GetToken(self):
        """Gets the current authorization token.
        In the very first call, this method creates a new token before returning.
        If currently stored token is expired, this method creates a new one.
        return Valid OAuthToken instance.
        """
        token = self._storageStrategy.Get(self.GetEnvKey())
        if token == None or token.IsExpired():
            token = self._root.authenticationManager.CreateToken()
            self.StoreToken(token)        
        return token
    
    def StoreToken(self, token):
        """Stores authorization token passed as an argument in the underlying
        storage strategy implementation.
        param token Token instance to be stored.
        """
        self._storageStrategy.Store(token, self.GetEnvKey())
    
    def RegisterCustomStorageStrategy(self, customStorageStrategy):
         """Registers custom storage strategy implementation.
         By default, the <code>DefaultStorageStrategy</code> instance is used. 
         There is no need to explicitly call this method until some more complex 
         storage implementation is needed.
         param customStorageStrategy IStorageStrategy interface implementation.
         """
         self._storageStrategy = customStorageStrategy
   
    def GetEnvKey(self):
        return hashlib.md5((self._root.Config.ClientID + self._root.Config.BaseUrl + self._root.Config.ClientPassword).encode('utf-8')).hexdigest()