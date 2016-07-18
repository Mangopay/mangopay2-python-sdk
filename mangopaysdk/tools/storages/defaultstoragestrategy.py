from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy
from mangopaysdk.configuration import Configuration
import os, json, stat
from mangopaysdk.types.oauthtoken import OAuthToken
import fasteners


class DefaultStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    cache_path = ''

    def Get(self, envKey):
        """Gets the currently stored objects as dictionary.
        return stored Token dictionary or null.
        """
        DefaultStorageStrategy.cache_path = os.path.join(Configuration.TempPath, "cached-data." + envKey + ".py")

        if not os.path.exists(DefaultStorageStrategy.cache_path):
           return None
        lock = fasteners.ReaderWriterLock()
        with lock.read_lock():
            fp = open(DefaultStorageStrategy.cache_path,'rb')
            serializedObj = fp.read().decode('UTF-8')
            try:
               cached = json.loads(serializedObj[1:])
            except:
               cached = None
            fp.close()
        return OAuthToken(cached)

    def Store(self, obj, envKey):
        """Stores authorization token passed as an argument.
        param obj instance to be stored.
        """
        DefaultStorageStrategy.cache_path = os.path.join(Configuration.TempPath, "cached-data." + envKey + ".py")

        if obj == None:
            return
        lock = fasteners.ReaderWriterLock()
        with lock.write_lock():
            fp = open(DefaultStorageStrategy.cache_path,'w')
            os.chmod(DefaultStorageStrategy.cache_path, stat.S_IRUSR|stat.S_IWUSR)
            # Write it to the result to the file as a json
            serializedObj = "#" + json.dumps(obj.__dict__)
            # add hash to prevent download token file via http when path is invalid
            fp.write(serializedObj)
            fp.close()
