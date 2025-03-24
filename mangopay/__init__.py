client_id = None
apikey = None
api_url = 'https://api.mangopay.com/v2.01/'
api_sandbox_url = 'https://api.sandbox.mangopay.com/v2.01/'
temp_dir = None
api_version = 2.01
sandbox = True
uk_header_flag = False

package_version = None
try:
    with open('../setup.py', 'r') as f:
        for line in f:
            if line.startswith('    version'):
                package_version = line.split('=')[1].replace("'", "").replace(",", "").replace("\n", "")
except:
    None


from .api import APIRequest  # noqa
from .utils import memoize


def _get_default_handler():
    return APIRequest()

get_default_handler = memoize(_get_default_handler, {}, 0)
