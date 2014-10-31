MangoPay SDK
=================================================

MangoPaySDK is a Python client library to work with
[MangoPay REST API](http://docs.mangopay.com/api-references/).


Installation and package dependencies
-------------------------------------------------
SDK has been written in Python 2.7 and requires:

	requests
	requests-oauthlib
	lockfile

	
If you have problem with using token file based cache (Configuration.TempPath) you can use memory cache:
	
	sdk = MangoPayApi()
	sdk.OAuthTokenManager.RegisterCustomStorageStrategy(MemoryStorageStrategy())

We strongly recommend using PIP as installation method:

    pip install mangopaysdk


License
-------------------------------------------------
MangoPaySDK is distributed under MIT license, see LICENSE file.


Unit Tests (not included in pip package)
-------------------------------------------------

    cd project_directory

    # runs ALL tests:
    python -m unittest test_suite

    # runs single module/class/method:
    python -m unittest test_module1 test_module2
    python -m unittest test_module.TestClass
    python -m unittest test_module.TestClass.test_method


Contact
-------------------------------------------------
Report bugs or suggest features using [issue tracker at GitHub](https://github.com/MangoPay/mangopay2-python-sdk).



Client creation example (you need to call it only once)
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

    client = api.clients.Create('your-client-id', 'your-client-name', 'your-client-email@sample.org')
    
    # you'll receive your passphrase here, note it down and keep in secret
    print(client.Passphrase)


Configuration
-------------------------------------------------
See the example above and call `api.clients.Create(...)` to get your passphrase.
Then set `api.Config.ClientId` to your MangoPay Client ID and `api.Config.ClientPassword` to your passphrase.

You also need to set a folder path in `api.Config.TempPath` that SDK needs to store temporary files. 
This path should be outside your www folder.
It could be `/tmp/` or `/var/tmp/` or any other location that Python can write to.

`api.Config.BaseUrl` is set to sandbox environment by default. To enable production environment, set it to `https://api.mangopay.com`.

Below is the example showing how to configure SDK:

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

	# configure client credentials
    api.Config.ClientId = 'your-client-id'
    api.Config.ClientPassword = 'your-client-passphrase'
    api.Config.TempPath = "C:\Temp\\" # or "/tmp" on linux
	api.Config.BaseUrl = "https://api.sandbox.mangopay.com"

    # call API methods, i.e.:
    users = api.users.GetAll()


Sample usage
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

	# configuration
	api.Config.ClientId = 'your-client-id'
    api.Config.ClientPassword = 'your-client-passphrase'
	
    # get some user by ID
    john = api.users.Get(userId)

    # change and update some of his data
    john.LastName += " - CHANGED"
    api.users.Update(john)

    # get all users (with pagination)
    from mangopaysdk.types.pagination import Pagination
    pagination = Pagination(1, 8) # get 1st page, 8 items per page
    users = api.users.GetAll(pagination)

    # get his bank accounts
    pagination = Pagination(2, 10) # get 2nd page, 10 items per page
    accounts = api.users.GetBankAccounts(john.Id, pagination)

