from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy


class MemoryStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    CachedObject = None

    def Get(self):
       """Gets the currently stored token.
       return Currently stored token instance or null.
       """
       return MemoryStorageStrategy.CachedObject

    def Store(self, token):
        """Stores authorization token passed as an argument.
        param token Token instance to be stored.
        """        
        MemoryStorageStrategy.CachedObject = token