import os

from .api import APIRequest  # noqa
from .utils import env_to_bool, memoize

client_id = None
apikey = None

MANGOPAY_URL = os.getenv("MANGOPAY_URL", "https://api.mangopay.com")
MANGOPAY_SANDBOX_URL = os.getenv("MANGOPAY_URL", "https://api.sandbox.mangopay.com")

api_url = f'{MANGOPAY_URL}/v2.01/'
api_sandbox_url = f'{MANGOPAY_SANDBOX_URL}/v2.01/'

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
