Mangopay SDK
=================================================

MangopaySDK is a Python client library to work with
[Mangopay REST API](http://docs.mangopay.com/api-references/).


Compatibility Note
-------------------------------------------------
Since v1.8 of this SDK, you must be using at least v2.01 of the API ([more information about the changes required](https://docs.mangopay.com/api-v2-01-overview/))


Installation and package dependencies
-------------------------------------------------
SDK has been written in Python 2.7+ and requires:

	requests
	requests-oauthlib
	fasteners

If you have problem with using token file based cache (Configuration.TempPath) you can use memory cache:

	sdk = MangoPayApi()
	sdk.OAuthTokenManager.RegisterCustomStorageStrategy(MemoryStorageStrategy())

We strongly recommend using PIP as installation method:

    pip install mangopaysdk


License
-------------------------------------------------
MangopaySDK is distributed under MIT license, see LICENSE file.


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


Account creation
-------------------------------------------------
You can get yourself a [free sandbox account](https://www.mangopay.com/signup/create-sandbox/) or sign up for a [production account](https://www.mangopay.com/signup/submit-your-app/go-live/) (note that validation of your production account can take a few days, so think about doing it in advance of when you actually want to go live).


Configuration
-------------------------------------------------
Using the credential info from the signup process above, you should then set `api.Config.ClientID` to your MangoPay Client ID and `api.Config.ClientPassword` to your passphrase.

You also need to set a folder path in `api.Config.TempPath` that SDK needs to store temporary files.
This path should be outside your www folder.
It could be `/tmp/` or `/var/tmp/` or any other location that Python can write to.

`api.Config.BaseUrl` is set to sandbox environment by default. To enable production environment, set it to `https://api.mangopay.com`.

Below is the example showing how to configure SDK:

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

	# configure client credentials
    api.Config.ClientID = 'your-client-id'
    api.Config.ClientPassword = 'your-client-passphrase'
    api.Config.TempPath = "C:\Temp\\" # or "/tmp" on linux
	api.Config.BaseUrl = "https://api.sandbox.mangopay.com"
	api.Config.SSLVerification = 'path-to-your-cacert.pem-file'

    # call API methods, i.e.:
    users = api.users.GetAll()


SSL verification
-------------------------------------------------
The default value of `SSLVerification` is `False`, which means there's no verification. In such a case you will be notified about that by the `InsecureRequestWarning` message, i.e.:
`InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html`

In order to easily verify your HTTPS requests (and remove warning message), you can put a path to the `cacert.pem` file as the value of `SSLVerification` property.
You should find that file in `Python_installation_folder\Lib\site-packages\requests`, so setting the path may look similar to the following (for Windows OS):

	sdk.Config.SSLVerification = 'C:\\Python27\\Lib\\site-packages\\requests\\cacert.pem'


Connection pooling
-------------------------------------------------
To benefit from HTTP connection reuse you need to set `api.Config.Session` like this:

    import requests
    api.Config.Session = requests.Session()

WARNING: sessions are not guaranteed to be thread-safe!

See the upstream [Session Objects](http://docs.python-requests.org/en/master/user/advanced/#session-objects) documentation for more details.


Sample usage
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

	# configuration
	api.Config.ClientID = 'your-client-id'
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

