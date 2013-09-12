from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy
from mangopaysdk.configuration import Configuration
import os, pickle
import portalocker


class DefaultStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    cache_path = Configuration.TempPath + "cached-data.pickle"
    lock_path = Configuration.TempPath + "cached-data.pickle.lock"

    def Get(self):
       """Gets the currently stored token.
       return Currently stored token instance or null.
       """
       if not os.path.exists(DefaultStorageStrategy.cache_path):
           return None
       fp = open(DefaultStorageStrategy.cache_path,'rb')
       portalocker.lock(fp, portalocker.LOCK_EX)
       cached = pickle.load(fp)
       fp.close()
       return cached

    def Store(self, token):
        """Stores authorization token passed as an argument.
        param token Token instance to be stored.
        """
        if token == None: 
            return
        fp = open(DefaultStorageStrategy.cache_path,'wb')
        portalocker.lock(fp, portalocker.LOCK_EX | portalocker.LOCK_NB)
        pickle.dump(token, fp, protocol=1)
        # Write it to the result to the file as a pickled object
        # Use the binary protocol for better performance
        fp.close()
