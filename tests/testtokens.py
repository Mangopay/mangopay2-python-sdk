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
        self.assertEqual(newToken.access_token, storedToken.access_token)

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
        self.assertEqual(token1.access_token, token2.access_token)

    def test_isolateTokensBetweenEnvironments(self):
        api = MangoPayApi()
        api.Config.ClientID = "sdk-unit-tests"
        api.Config.ClientPassword = "cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju"
        api.Config.BaseUrl = "https://api.sandbox.mangopay.com"

        token1 = api.OAuthTokenManager.GetToken()

        api.Config.ClientID = "sdk_example"
        api.Config.ClientPassword = "Vfp9eMKSzGkxivCwt15wE082pTTKsx90vBenc9hjLsf5K46ciF"
        api.Config.BaseUrl = "https://api.sandbox.mangopay.com"

        token2 = api.OAuthTokenManager.GetToken()

        self.assertNotEqual(token1.access_token, token2.access_token)

        api.Config.ClientID = "sdk-unit-tests"
        api.Config.ClientPassword = "cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju"
        api.Config.BaseUrl = "https://api.sandbox.mangopay.com"

        token3 = api.OAuthTokenManager.GetToken()

        self.assertEqual(token1.access_token, token3.access_token)