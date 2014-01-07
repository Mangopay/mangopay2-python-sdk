from mangopaysdk.mangopayapi import MangoPayApi
from tests.testbase import TestBase
from mangopaysdk.types.exceptions.responseexception import ResponseException


class Test_Configurations(TestBase):

    def test_confInConstruct(self):
        sdk = MangoPayApi()      
        sdk.Config.ClientID = "test_asd"
        sdk.Config.ClientPassword = "00000"
        sdk.OAuthTokenManager.StoreToken(None)
        with self.assertRaises(ResponseException) as cm:
            sdk.users.GetAll()