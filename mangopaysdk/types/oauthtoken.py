from datetime import datetime
import time


class OAuthToken:
    """Token data for OAuth Authentication."""
    
    def __init__(self):
        # timestamp
        self.create_time = int(time.time() - 5)
        self.expires_in = None
        self.access_token = None
        self.token_type = None

    def IsExpired(self):
        """Check that current tokens are expire and return true if yes.
		return bool
		"""
        return time.time() >= (self.create_time + self.expires_in)