from . import settings

from mangopay.api import APIRequest

handler = APIRequest(client_id=settings.MANGOPAY_CLIENT_ID,
                     passphrase=settings.MANGOPAY_PASSPHRASE,
                     sandbox=settings.MANGOPAY_USE_SANDBOX)

from mangopay.resources import *  # noqa
