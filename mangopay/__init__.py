import os

from .api import APIRequest  # noqa
from .utils import memoize

client_id = None
apikey = None
mangopay_url_env_var = os.getenv("MANGOPAY_URL")

if mangopay_url_env_var is not None:
    api_url = f'http://{mangopay_url_env_var}/v2.01/'
    api_sandbox_url = f'http://{mangopay_url_env_var}/v2.01/'
else:
    api_url = 'https://api.mangopay.com/v2.01/'
    api_sandbox_url = 'https://api.sandbox.mangopay.com/v2.01/'

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
