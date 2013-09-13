from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy
from mangopaysdk.configuration import Configuration
import os, json
import portalocker


class DefaultStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    cache_path = Configuration.TempPath + "cached-data.py"
    lock_path = Configuration.TempPath + "cached-data.lock"

    def Get(self):
       """Gets the currently stored objects as dictionary.
       return stored object dictionary or null.
       """
       if not os.path.exists(DefaultStorageStrategy.cache_path):
           return None
       fp = open(DefaultStorageStrategy.cache_path,'rb')
       portalocker.lock(fp, portalocker.LOCK_EX)
       serializedObj = fp.read().decode('UTF-8')
       try:
           cached = json.loads(serializedObj[1:])
       except:
           return None
       fp.close()
       return cached

    def Store(self, obj):
        """Stores authorization token passed as an argument.
        param obj instance to be stored.
        """
        if obj == None: 
            return
        fp = open(DefaultStorageStrategy.cache_path,'w')
        portalocker.lock(fp, portalocker.LOCK_EX | portalocker.LOCK_NB)
        # Write it to the result to the file as a pickled object
        # Use the binary protocol for better performance
        serializedObj = "#" + json.dumps(obj.__dict__)
        # add hash to prevent download token file via http when path is invalid 
        fp.write(serializedObj)
        fp.close()
