import os

from .api import APIRequest  # noqa
from .utils import is_env_var_truthy, memoize

client_id = None
apikey = None

MANGOPAY_IS_MOCK_SERVER_ENABLED = os.getenv("MANGOPAY_IS_MOCK_SERVER_ENABLED", "")
MANGOPAY_MOCK_SERVER_URL = os.getenv("MANGOPAY_MOCK_SERVER_URL", "")
MANGOPAY_URL = os.getenv("MANGOPAY_URL", "https://api.mangopay.com")
MANGOPAY_SANDBOX_URL = os.getenv("MANGOPAY_URL", "https://api.sandbox.mangopay.com")

def _get_api_url():
    if is_env_var_truthy(MANGOPAY_IS_MOCK_SERVER_ENABLED):
        return MANGOPAY_MOCK_SERVER_URL
    return MANGOPAY_URL

def _get_sandbox_url():
    if is_env_var_truthy(MANGOPAY_IS_MOCK_SERVER_ENABLED):
        return MANGOPAY_MOCK_SERVER_URL
    return MANGOPAY_SANDBOX_URL

api_url = f'{_get_api_url()}/v2.01/'
api_sandbox_url = f'{_get_sandbox_url()}/v2.01/'

temp_dir = None
api_version = 2.01
sandbox = True

package_version = None
try:
    with open('./setup.py', 'r') as f:
        for line in f:
            if line.startswith('    version'):
                package_version = line.split('=')[1].replace("'", "").replace(",", "").replace("\n", "")
except:
    None

def _get_default_handler():
    return APIRequest()

get_default_handler = memoize(_get_default_handler, {}, 0)
