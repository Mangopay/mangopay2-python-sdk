from mangopaysdk.mangopayapi import MangoPayApi
from mangopaysdk.tools.apioauth import ApiOAuth
from tests.testbase import TestBase


class Test_Tokens(TestBase):
    """Tests basic methods for token management"""

    def test_forceToken(self):
        token = self.sdk.authenticationManager.CreateToken()
        # overwrite token in API
        self.sdk.OAuthToken = token
        self.sdk.users.GetAll()
        self.assertEqual(token.access_token, self.sdk.OAuthToken.access_token)

    def test_stadnardUseToken(self):
        self.sdk.users.GetAll()
        token = self.sdk.OAuthToken
        self.sdk.users.GetAll()
        self.assertEqual(token.access_token, self.sdk.OAuthToken.access_token)

    def test_isTokenLeaking(self):
        api = MangoPayApi()
        self.sdk.users.GetAll()
        api.users.GetAll()
        self.assertTrue(api.OAuthToken.access_token != self.sdk.OAuthToken.access_token)