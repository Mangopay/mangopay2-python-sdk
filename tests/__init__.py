import mangopay

from . import settings

mangopay.client_id = settings.MANGOPAY_CLIENT_ID
mangopay.passphrase = settings.MANGOPAY_PASSPHRASE
