from mangopaysdk.mangopayapi import MangoPayApi
from tests.testbase import TestBase
from mangopaysdk.types.exceptions.responseexception import ResponseException


class Test_Configurations(TestBase):

    def test_confInConstruct(self):
        sdk = MangoPayApi() 
        
        # store auth data, to not break unit tests order-independency rule
        clientId = sdk.Config.ClientID
        clientPassword = sdk.Config.ClientPassword
        token = sdk.OAuthTokenManager.GetToken()
             
        sdk.Config.ClientID = "test_asd"
        sdk.Config.ClientPassword = "00000"
        sdk.OAuthTokenManager.StoreToken(None)
        with self.assertRaises(ResponseException) as cm:
            sdk.users.GetAll()

        # bring valid auth data back
        sdk.Config.ClientID = clientId
        sdk.Config.ClientPassword = clientPassword
        sdk.OAuthTokenManager.StoreToken(token)