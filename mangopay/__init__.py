import tempfile

client_id = None
passphrase = None
api_url = 'https://api.mangopay.com/v2.01/'
api_sandbox_url = 'https://api.sandbox.mangopay.com/v2.01/'
temp_dir = tempfile.gettempdir()
api_version = 2.01
sandbox = True


from .utils import memoize
from .api import APIRequest  # noqa


def _get_default_handler():
    return APIRequest()

get_default_handler = memoize(_get_default_handler, {}, 0)
