from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy
from mangopaysdk.tools.apioauth import ApiOAuth
from mangopaysdk.types.oauthtoken import OAuthToken
from mangopaysdk.configuration import Configuration
import os
import pickle

class DefaultStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    cache_path = Configuration.TempPath + "cached-data.pickle"

    def Get(self):
       """Gets the currently stored token.
       return Currently stored token instance or null.
       """
       if not os.path.exists(DefaultStorageStrategy.cache_path):
           return None
       self.cached = pickle.load(open(DefaultStorageStrategy.cache_path,'rb'))
       #if self.cached != None: print(self.cached.access_token)
       return self.cached

    def Store(self, token):
        """Stores authorization token passed as an argument.
        param token Token instance to be stored.
        """        
        self.cache_file = open(DefaultStorageStrategy.cache_path,'wb')
        # Write it to the result to the file as a pickled object
        # Use the binary protocol for better performance
        pickle.dump(token, self.cache_file, protocol=1)
        self.cache_file.close()