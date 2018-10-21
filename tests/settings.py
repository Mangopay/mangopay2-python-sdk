import sys

try:
    from .credentials import *  # noqa
except ImportError:
    sys.stdout.write('Can\'t find the file credentials.py. Hardcoded values are used.')

    MANGOPAY_CLIENT_ID = 'sdk-unit-tests'
    MANGOPAY_APIKEY = 'cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju'
    MANGOPAY_API_URL = 'https://api.mangopay.com/v2.01/'
    MANGOPAY_API_SANDBOX_URL = 'https://api.sandbox.mangopay.com/v2.01/'
    MANGOPAY_USE_SANDBOX = True
    MANGOPAY_API_VERSION = 2

MOCK_TESTS_RESPONSES = True
