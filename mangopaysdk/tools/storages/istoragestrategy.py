

class IStorageStrategy(object):
    """Storage strategy interface."""

    def Get(self, envKey):
        """returns valid OAuthToken"""
    
    def Store(self, token, envKey):
        """stores OAuthToken object"""