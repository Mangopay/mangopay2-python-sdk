from mangopaysdk.mangopayapi import MangoPayApi
from tests.testbase import TestBase
from mangopaysdk.types.exceptions.responseexception import ResponseException


class Test_Configurations(TestBase):

    def test_confInConstruct(self):        
        self.sdk.Config.ClientId = "test_asd"
        self.sdk.Config.ClientPassword = "00000"
        self.sdk.OAuthTokenManager.StoreToken(None)
        with self.assertRaises(ResponseException) as cm:
            self.sdk.users.GetAll()