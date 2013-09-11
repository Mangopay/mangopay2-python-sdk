from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.tools.apioauth import ApiOAuth
from mangopaysdk.types.pagination import Pagination
from tests.testbase import TestBase


class Test_Tokens(TestBase):
    """Tests basic methods for token management"""

    def test_forceToken(self):
        oldToken = self.sdk.OAuthTokenManager.GetToken()
        newToken = self.sdk.authenticationManager.CreateToken()       
        self.assertNotEqual(oldToken.access_token, newToken.access_token)
        self.sdk.OAuthTokenManager.StoreToken(newToken)
        storedToken = self.sdk.OAuthTokenManager.GetToken()
        self.assertEquals(newToken.access_token, storedToken.access_token)

    def test_stadnardUseToken(self):
        self.sdk.users.GetAll(Pagination(1, 2))
        token = self.sdk.OAuthTokenManager.GetToken()
        self.sdk.users.GetAll(Pagination(1, 2))
        self.assertEqual(token.access_token, self.sdk.OAuthTokenManager.GetToken().access_token)

    def test_isTokenLeaking(self):
        api = self.buildNewMangoPayApi()
        self.sdk.users.GetAll(Pagination(1, 2))
        token1 = self.sdk.OAuthTokenManager.GetToken()
        token2 = api.OAuthTokenManager.GetToken()
        self.assertEquals(token1.access_token, token2.access_token) 