MangoPay SDK
=================================================
MangoPaySDK is a python client library to work with
[MangoPay REST API](http://docs.mangopay.com/api-references/).


Installation
-------------------------------------------------
SDK has been written in Python 3.3
and depends on requests and requests-oauthlib packages.

We strongly recommend using PIP as installation method:

    pip install mangopaysdk


License
-------------------------------------------------
MangoPaySDK is distributed under MIT license, see LICENSE file.


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
Report bugs or suggest features using
[issue tracker at GitHub](https://github.com/MangoPay/mangopay2-python-sdk).


Sample usage
-------------------------------------------------

    from mangopaysdk.mangopayapi import MangoPayApi
    api = MangoPayApi()

    # get some user by id
    john = api.users.Get(someId)

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

    api.Config.ClientId = 'your-client-id'
    api.Config.ClientPassword = 'your-client-password'
    print(api.Config.BaseUrl) # you probably dont have to change it

    # call some API methods...
    users = api.users.GetAll()
