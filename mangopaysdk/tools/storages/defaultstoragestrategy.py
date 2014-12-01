from mangopaysdk.tools.storages.istoragestrategy import IStorageStrategy
from mangopaysdk.configuration import Configuration
import os, json
from mangopaysdk.types.oauthtoken import OAuthToken
import lockfile.mkdirlockfile


class DefaultStorageStrategy(IStorageStrategy):
    """Default storage strategy implementation."""

    cache_path = ''

    def Get(self):
        """Gets the currently stored objects as dictionary.
        return stored Token dictionary or null.
        """
        DefaultStorageStrategy.cache_path = Configuration.TempPath + "cached-data.py"

        if not os.path.exists(DefaultStorageStrategy.cache_path):
           return None
        fp = open(DefaultStorageStrategy.cache_path,'rb')
        lock = lockfile.mkdirlockfile.MkdirLockFile(DefaultStorageStrategy.cache_path)
        while not lock.i_am_locking():
            try:
                lock.acquire(timeout=2) 
            except LockTimeout:
                lock.break_lock()
                lock.acquire()
        serializedObj = fp.read().decode('UTF-8')
        try:
           cached = json.loads(serializedObj[1:])
        except:
           cached = None
        fp.close()
        lock.release()     
        return OAuthToken(cached)

    def Store(self, obj):
        """Stores authorization token passed as an argument.
        param obj instance to be stored.
        """
        DefaultStorageStrategy.cache_path = Configuration.TempPath + "cached-data.py"

        if obj == None: 
            return
        fp = open(DefaultStorageStrategy.cache_path,'w')
        lock = lockfile.mkdirlockfile.MkdirLockFile(DefaultStorageStrategy.cache_path)
        while not lock.i_am_locking():
            try:
                lock.acquire(timeout=2) 
            except LockTimeout:
                lock.break_lock()
                lock.acquire()
        # Write it to the result to the file as a json
        serializedObj = "#" + json.dumps(obj.__dict__)
        # add hash to prevent download token file via http when path is invalid 
        fp.write(serializedObj)
        fp.close()
        lock.release()        
