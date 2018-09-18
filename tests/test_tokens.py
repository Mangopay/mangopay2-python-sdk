import time

from mangopay import APIRequest
from mangopay.auth import StaticStorageStrategy
from mangopay.resources import User
from tests.test_base import BaseTestLive


class TokenTestLive(BaseTestLive):

    def test_ForceToken(self):
        old_token = BaseTestLive.get_oauth_manager().get_token()
        new_token_result = BaseTestLive.get_oauth_manager().authorization.oauth_token()
        new_token = new_token_result[1]['token_type'] + ' ' + new_token_result[1]['access_token']

        self.assertFalse(old_token == new_token)
        new_token_result[1]['timestamp'] = time.time() + (int(new_token_result[1]['expires_in']) - 10)
        BaseTestLive.get_oauth_manager().set_token(new_token_result[1])

        stored_token = BaseTestLive.get_oauth_manager().get_token()

        self.assertEqual(stored_token, new_token)

    def test_StandardUseToken(self):
        User.all()
        token = BaseTestLive.get_oauth_manager().get_token()
        User.all()

        self.assertEqual(token, BaseTestLive.get_oauth_manager().get_token())

    def test_ShareTokenBetweenInstances(self):
        new_handler = APIRequest(storage_strategy=StaticStorageStrategy())

        token1 = BaseTestLive.get_oauth_manager().get_token()
        token2 = new_handler.auth_manager.get_token()

        self.assertEqual(token1, token2)

    def test_IsolateTokensBetweenEnvironments(self):
        handler = APIRequest(client_id='sdk-unit-tests',
                             apikey='cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju',
                             api_sandbox_url='https://api.sandbox.mangopay.com/v2.01/',
                             storage_strategy=StaticStorageStrategy())
        token1 = handler.auth_manager.get_token()

        handler = APIRequest(client_id='sdk_example',
                             apikey='Vfp9eMKSzGkxivCwt15wE082pTTKsx90vBenc9hjLsf5K46ciF',
                             api_sandbox_url='https://api.sandbox.mangopay.com/v2.01/',
                             storage_strategy=StaticStorageStrategy())
        token2 = handler.auth_manager.get_token()

        self.assertNotEqual(token1, token2)

        handler = APIRequest(client_id='sdk-unit-tests',
                             apikey='cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju',
                             api_sandbox_url='https://api.sandbox.mangopay.com/v2.01/',
                             storage_strategy=StaticStorageStrategy())

        token3 = handler.auth_manager.get_token()

        self.assertEqual(token1, token3)
