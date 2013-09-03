MangoPay SDK
=================================================
mangopaysdk is a client library to work with mangopay REST API
(http://www.mangopay.com/).


Installation
-------------------------------------------------
SDK has been written in Python 3.3
and depends on requests and requests-oauthlib packages.

We strongly recommend using PIP as installation method:

    pip install mangopaysdk


License
-------------------------------------------------
MangoPaySdk is distributed under MIT license, see LICENSE file.


Unit Tests (not included in pip package)
-------------------------------------------------

    cd project_directory

    # discovers and runs ALL tests:
    python -m unittest

    # runs single module/class/method:
    python -m unittest test_module1 test_module2
    python -m unittest test_module.TestClass
    python -m unittest test_module.TestClass.test_method


Contacts
-------------------------------------------------
Report bugs or suggest features using issue tracker at GitHub
(https://github.com/MangoPay/mangopay2-python-sdk).


Sample usage
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

    # get some user by id
    john = api.users.Get(someId)

    # change and update some of his data
    john.LastName += " - CHANGED"
    self.sdk.users.Update(john)

    # get all users (with pagination)
    from mangopaysdk.types.pagination import Pagination
    pagination = Pagination(1, 8) # get 1st page, 8 items per page
    users = api.users.GetAll(pagination)

    # get his bank accounts
    pagination = Pagination(2, 10) # get 2nd page, 10 items per page
    accounts = api.users.GetBankAccounts(john.Id, pagination)


Client creation example (you need to call it only once)
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

    client = api.clients.Create('your-client-id', 'your-client-name', 'your-client-email@sample.org')
    print(client.Passphrase) # you receive your password here


Configuration example
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

    api.Config.ClientID = 'your-client-id'
    api.Config.ClientPassword = 'your-client-password'
    print(api.Config.BaseUrl) # you probably dont have to change it

    # call some API methods...
    users = api.users.GetAll()


Example with auth token reusage
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

    # optionally you can reuse token from previous requests (unless expired)
    api.OAuthToken = myTokensPersistenceService.loadIfStored()

    # call some API methods...
    users = api.users.GetAll()

    # optionally store the token for future requests (until expires)
    myTokensPersistenceService.store(api.OAuthToken)
