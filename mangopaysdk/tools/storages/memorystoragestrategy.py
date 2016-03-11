from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy


class MemoryStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    CachedObject = {};

    def Get(self, envKey):
       """Gets the currently stored token.
       return Currently stored token instance or null.
       """
       if not envKey in MemoryStorageStrategy.CachedObject:
           return None

       return MemoryStorageStrategy.CachedObject[envKey]

    def Store(self, token, envKey):
        """Stores authorization token passed as an argument.
        param token Token instance to be stored.
        """        
        MemoryStorageStrategy.CachedObject[envKey] = token