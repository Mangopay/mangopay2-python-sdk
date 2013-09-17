from datetime import datetime
import time


class OAuthToken:
    """Token data for OAuth Authentication."""
    
    def __init__(self, dict = None):
        # timestamp
        self.create_time = dict['create_time'] if (dict != None and 'create_time' in dict) else int(time.time() - 5)
        self.expires_in = dict['expires_in'] if dict != None else None
        self.access_token = dict['access_token'] if dict != None else None
        self.token_type = dict['token_type'] if dict != None else None

    def IsExpired(self):
        """Check that current tokens are expire and return true if yes.
		return bool
		"""
        return time.time() >= (self.create_time + self.expires_in)