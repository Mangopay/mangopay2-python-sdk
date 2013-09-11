from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy
from mangopaysdk.tools.apioauth import ApiOAuth
from mangopaysdk.types.oauthtoken import OAuthToken


class DefaultStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    Token = None

    def Get(self):
       """Gets the currently stored token.
       return Currently stored token instance or null.
       """
       return DefaultStorageStrategy.Token

    def Store(self, token):
        """Stores authorization token passed as an argument.
        param token Token instance to be stored.
        """
        DefaultStorageStrategy.Token = token