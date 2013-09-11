

class IStorageStrategy(object):
    """Storage strategy interface."""

    def Get(self):
        """returns valid OAuthToken"""
    
    def Store(self, token):
        """stores OAuthToken object"""