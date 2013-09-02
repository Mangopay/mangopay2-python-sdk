from datetime import datetime
import time


class OAuthToken:
    """Token data for OAuth Authentication."""

    # timestamp
    _create_time = 0

    expires_in = 0

    access_token = ''

    token_type = ''

    def __init__(self):
        self.create_time = int(time.time() - 5)

    def IsExpire(self):
        """Check that current tokens are expire and return true if yes.
		return bool
		"""
        return time.time() >= (self.create_time + self.expires_in)