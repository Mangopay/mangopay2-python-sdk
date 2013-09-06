from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.tools.apioauth import ApiOAuth
from tests.testbase import TestBase


class Test_Tokens(TestBase):
    """Tests basic methods for token management"""

    def test_forceToken(self):
        token = self.sdk.authenticationManager.CreateToken()
        # overwrite token in API
        self.sdk.OAuthToken = token
        self.sdk.users.GetAll(Pagination(1, 2))
        self.assertEqual(token.access_token, self.sdk.OAuthToken.access_token)

    def test_stadnardUseToken(self):
        self.sdk.users.GetAll(Pagination(1, 2))
        token = self.sdk.OAuthToken
        self.sdk.users.GetAll(Pagination(1, 2))
        self.assertEqual(token.access_token, self.sdk.OAuthToken.access_token)

    def test_isTokenLeaking(self):
        api = self.buildNewMangoPayApi()
        self.sdk.users.GetAll(Pagination(1, 2))
        api.users.GetAll(Pagination(1, 2))
        self.assertTrue(api.OAuthToken.access_token != self.sdk.OAuthToken.access_token)
