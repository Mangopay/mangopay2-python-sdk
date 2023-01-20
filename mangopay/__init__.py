import os

from .api import APIRequest  # noqa
from .utils import env_to_bool, memoize

client_id = None
apikey = None

PLENTIFIC_NAMESPACE = os.getenv("PLENTIFIC_NAMESPACE", "uk")
PLENTIFIC_IS_E2E = env_to_bool("PLENTIFIC_IS_E2E", False)

MANGOPAY_URL = os.getenv("MANGOPAY_URL", "https://api.mangopay.com")
MANGOPAY_SANDBOX_URL = os.getenv("MANGOPAY_URL", "https://api.sandbox.mangopay.com")

MANGOPAY_IS_MOCK_SERVER_ENABLED = os.getenv("MANGOPAY_IS_MOCK_SERVER_ENABLED", "")

MANGOPAY_DEFAULT_E2E_MOCK_SERVER_URL = f"https://localhost.plentific.com/mock-server/{PLENTIFIC_NAMESPACE}/mangopay"
MANGOPAY_DEFAULT_LOCAL_MOCK_SERVER_URL = f"http://mock-server:5000/mock-server/{PLENTIFIC_NAMESPACE}/mangopay"

MANGOPAY_MOCK_SERVER_URL = os.environ.get(
    "MANGOPAY_MOCK_SERVER_URL",
    MANGOPAY_DEFAULT_E2E_MOCK_SERVER_URL
    if PLENTIFIC_IS_E2E
    else MANGOPAY_DEFAULT_LOCAL_MOCK_SERVER_URL,
)

def _get_api_url():
    if env_to_bool("MANGOPAY_IS_MOCK_SERVER_ENABLED", ""):
        return MANGOPAY_MOCK_SERVER_URL
    return MANGOPAY_URL

def _get_sandbox_url():
    if env_to_bool("MANGOPAY_IS_MOCK_SERVER_ENABLED", ""):
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
