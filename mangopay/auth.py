import base64
import hashlib
import json
import stat

import os
import tempfile

import six
import time

import mangopay
from mangopay.exceptions import AuthenticationError


class StorageStrategyBase(object):

    def get(self, env_key):
        pass

    def store(self, token, env_key):
        pass


class StaticStorageStrategy(StorageStrategyBase):

    _dict = dict()

    def get(self, env_key):
        return StaticStorageStrategy._dict[env_key]

    def store(self, token, env_key):
        StaticStorageStrategy._dict[env_key] = token


class FileStorageStrategy(StorageStrategyBase):

    def __init__(self):
        if mangopay.temp_dir is None:
            mangopay.temp_dir = tempfile.gettempdir()

    def get(self, env_key):
        cache_path = os.path.join(mangopay.temp_dir, "cached-data." + env_key + ".py")

        if not os.path.exists(cache_path):
            return None

        with open(cache_path, 'rb') as f:
            serialized_obj = f.read().decode('UTF-8')
            try:
                cached = json.loads(serialized_obj[1:])
            except:
                cached = None

        return cached

    def store(self, token, env_key):
        cache_path = os.path.join(mangopay.temp_dir, "cached-data." + env_key + ".py")
        if token is None:
            return

        with open(cache_path, 'w') as f:
            os.chmod(cache_path, stat.S_IRUSR | stat.S_IWUSR)
            serialized_obj = "#" + json.dumps(token)
            f.write(serialized_obj)


class AuthorizationTokenManager(object):

    def __init__(self, handler, storage_strategy):
        self._handler = handler
        self.authorization = ApiAuthorization(handler)
        if storage_strategy:
            self.storage_strategy = storage_strategy
        else:
            self.storage_strategy = StaticStorageStrategy()

    def basic_token(self):
        return self.authorization.basic_token()

    def get_token(self):
        try:
            token = self.storage_strategy.get(self.get_evn_key())
        except KeyError:
            token = None

        if not token or not token['timestamp'] or token['timestamp'] <= time.time():
            auth_result = self.authorization.oauth_token()
            if auth_result[0].status_code == 200:
                token = auth_result[1]
            else:
                return None
            token['timestamp'] = time.time() + (int(token['expires_in']) - 10)
            self.set_token(token)

        return token['token_type'] + ' ' + token['access_token']

    def set_token(self, token):
        self.storage_strategy.store(token, self.get_evn_key())

    def get_evn_key(self):
        return hashlib.md5((self._handler.client_id + self._handler.api_url +
                            self._handler.apikey).encode('utf-8')).hexdigest()


class ApiAuthorization(object):

    def __init__(self, handler):
        self._handler = handler

    def oauth_token(self):
        result = self._handler.request(method='POST',
                                       url='oauth/token',
                                       data={'grant_type': 'client_credentials'},
                                       oauth_request=True)
        return result

    def basic_token(self):
        if self._handler.client_id is None or self._handler.apikey is None:
            raise AuthenticationError(
                'Authentication failed. (Please set your Mangopay API username '
                'and password using "mangopay.client_id = CLIENT_ID" '
                'and "mangopay.apikey = APIKEY").')

        credentials = '%s:%s' % (self._handler.client_id, self._handler.apikey)
        credentials = base64.b64encode(credentials.encode('ascii'))

        if six.PY3:
            credentials = credentials.decode('utf-8')

        return 'Basic %s' % credentials
