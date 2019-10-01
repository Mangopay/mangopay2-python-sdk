from . import settings

from mangopay.api import APIRequest

handler = APIRequest(client_id=settings.MANGOPAY_CLIENT_ID,
                     apikey=settings.MANGOPAY_APIKEY,
                     sandbox=settings.MANGOPAY_USE_SANDBOX)

from mangopay.resources import *  # noqa
