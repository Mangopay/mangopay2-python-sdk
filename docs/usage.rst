Usage
=====

Create an handler
-----------------

To manipulate resources (users, wallets, etc.) from this api you will have to
instanciate a new handler which is a connection authentication.

To create a new handler, you have to provide several parameters:

* **MANGOPAY_CLIENT_ID** - The client identifier used by `mangopay <http://www.mangopay.com/>`_ to identify you
* **MANGOPAY_PASSPHRASE** - Your password

API host
--------

The host used to call the API.

We will see later when you are creating a new handler you can choose between
multiple environment hosts already registered.

Let's get to work, we will create our first handler with the sandbox host:

.. code-block:: python

    import mangopay

    mangopay.client_id='my client id'
    mangopay.passphrase='my password'

    from mangopay.api import APIRequest

    handler = APIRequest(sandbox=True)

Now we have a new handler which is using the sandbox host.

If you are not specifying that you are using the sandbox host nor an existing host,
it will use the sandbox host by default.

API proxy support
-----------------

When you are creating a new handler you can use proxies for https, http and ftp protocols.

.. code-block:: python

    http_proxy  = "http://10.10.1.10:3128"
    https_proxy = "https://10.10.1.11:1080"
    ftp_proxy   = "ftp://10.10.1.10:3128"

    proxyDict = {
              "http": http_proxy,
              "https": https_proxy,
              "ftp": ftp_proxy
                }

     handler = APIRequest(sandbox=True, proxies=proxyDict)

This parameter is optional and by default it is None.

Using storage strategy
----------------------

The storage strategy used for OAuth token.

StaticStorageStrategy() - saves token in memory

FileStorageStrategy() - saves token in temporary file

.. code-block:: python

    handler = APIRequest(sandbox=True, storage_strategy=StaticStorageStrategy())
    handler = APIRequest(sandbox=True, storage_strategy=FileStorageStrategy())

If no strategy is specified, StaticStorageStrategy will be used.

API requests timeout
--------------------

When you create a new handler you can set the amount of time (in seconds) after that the requests will timeout.

.. code-block:: python

    handler = APIRequest(sandbox=True, timeout=30.0)

The default timeout is 30 seconds.

Using resources
---------------

To manipulate your resources, this library is heavily inspired from `peewee <https://github.com/coleifer/peewee/>`_,
so every operations will be like manipulating your favorite ORM.

For required parameters you can refer to the `reference api <https://docs.mangopay.com/api-references/>`_.

User
----

Create a natural user

.. code-block:: python

    from mangopay.resources import User, NaturalUser
    from mangopay.utils import Address


    natural_user = NaturalUser(first_name='Victor',
                               last_name='Hugo',
                               address=Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                   city='City', region='Region',
                                   postal_code='11222', country='FR'),
                               birthday=1300186358,
                               nationality='FR',
                               country_of_residence='FR',
                               occupation='Writer',
                               income_range='6',
                               proof_of_identity=None,
                               proof_of_address=None,
                               person_type='NATURAL',
                               email='victor@hugo.com',
                               tag='custom tag')

    natural_user.save() # save the new user

    print natural_user.get_pk() # retrieve the primary key

Retrieve an existing user

.. code-block:: python

    natural_user = NaturalUser.get(1) # 1 is an ID value, not an array index

    print natural_user.first_name # Victor

Detect a user which does not exist

.. code-block:: python

    try:
        natural_user = NaturalUser.get(2)
    except NaturalUser.DoesNotExist:
        print 'The natural user 2 does not exist'

Retrieve all users

.. code-block:: python

    users = User.all()
    print users  # [<NaturalUser: victor@hugo.com>, <LegalUser: support@ulule.com>]

Retrieve users with a pagination

.. code-block:: python

    users = User.all(page=1, per_page=2)

Retrieve a users's EMoney

.. code-block:: python

    natural_user = NaturalUser.get(1)
    emoney = natural_user.get_emoney()

    print emoney.credited_emoney
    print emoney.debited_emoney

Wallet
------

Create a wallet

.. code-block:: python

    natural_user = NaturalUser.get(1)

    from mangopay.resources import Wallet

    wallet = Wallet(owners=[natural_user],
                    description='Wallet of Victor Hugo',
                    currency='EUR',
                    tag='wallet for user n.1')

    wallet.save() # save the new wallet

    print wallet.get_pk() # 1

    print wallet.balance  # EUR 0.00

Retrieve user's wallets

.. code-block:: python

    natural_user = NaturalUser.get(1)

    print natural_user.wallets  # [<Wallet: Wallet n.1169421>]

Transfer
--------

Create a transfer from a wallet to another one

.. code-block:: python

    print legal_user_wallet.balance  # EUR 99.00
    print natural_user_wallet.balance  # EUR 0.00


    transfer = Transfer(author=legal_user,
                        credited_user=natural_user,
                        debited_funds=Money(amount=1000, currency='EUR'),  # Create a EUR 10.00 transfer
                        fees=Money(amount=100, currency='EUR'),  # With EUR 1.00 of fees
                        debited_wallet=legal_user_wallet,
                        credited_wallet=natural_user_wallet)

    transfer.save()


    print legal_user_wallet.balance  # EUR 89.00
    print natural_user_wallet.balance  # EUR 9.00

Transfer refund
---------------

Transfer money back to the wallet where it came from (transfer refund)

.. code-block:: python

    print legal_user_wallet.balance  # EUR 89.00
    print natural_user_wallet.balance  # EUR 9.00


    transfer_refund = TransferRefund(author=legal_user,
                                     transfer_id=transfer.get_pk())

    transfer_refund.save()


    print natural_user_wallet.balance  # EUR 0.00
    print legal_user_wallet.balance  # EUR 99.00

Transactions
------------

Retrieve wallet's transactions

.. code-block:: python

    print legal_user_wallet.transactions.all()  # [<Transaction: Transaction n.1174821>]

Retrieve user's transactions

.. code-block:: python

    print legal_user.transactions.all()  # [<Transaction: Transaction n.1174821>]

List all transactions made by a user (you can filter transactions by status)

.. code-block:: python

    transactions = Transaction.all(user_id=natural_user.get_pk(), status='SUCCEEDED')

    print transactions  # [<Transaction: Transaction n.1174821>]

Card
----

To register a card for a user you have to create a RegistrationCard
object with the user and his currency as params

.. code-block:: python

    card_registration = CardRegistration(user=natural_user, currency='EUR')
    card_registration.save()

Then, you have to retrieve user's cards details through a form and
send them to the Mangopay Tokenization server.

Mandatory information are:

* The card number
* The card CVX
* The expiration date

And hidden field:

* The access key ref
* The preregistered data (from the `card_registration` instance you created just before)


Update the `card_registration` instance with the response
provided by the Mangopay Tokenization server.

.. code-block:: python

    card_registration.registration_data = response
    card_registration.save()

Now, we have a `card_id` and you can retrieve the new card

.. code-block:: python

    print card_registration.card_id  # 1
    print card_registration.card  # CB_VISA_MASTERCARD of user 6641810

Retrieve user's cards

.. code-block:: python

    print user.cards.all()  # [<Card: CB_VISA_MASTERCARD of user 6641810>]

    print user.cards.get(card.id)  # CB_VISA_MASTERCARD of user 6641810

PayIn
-----

Direct payment on a user's wallet

.. code-block:: python

    direct_payin = DirectPayIn(author=natural_user,
                               debited_funds=Money(amount=100, currency='EUR'),
                               fees=Money(amount=1, currency='EUR'),
                               credited_wallet_id=legal_user_wallet,
                               card_id=card,
                               secure_mode=DEFAULT",
                               secure_mode_return_url="https://www.ulule.com/")

    direct_payin.save()

    print legal_user_wallet.balance  # EUR 99.00

BankAccount
-----------

Register a bank account

.. code-block:: python

    bankaccount = BankAccountIBAN(owner_name="Victor Hugo",
                                  user=natural_user,
                                  type="IBAN",
                                  owner_address=Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                  postal_code='11222', country='FR'),
                                  iban="FR3020041010124530725S03383",
                                  bic="CRLYFRPP")

    bankaccount.save()

BankWirePayIn
-------------

And pay by bank wire

.. code-block:: python

    bank_wire_payin = BankWirePayIn(credited_user_id=legal_user,
                                    credited_wallet_id=legal_user_wallet,
                                    declared_debited_funds=Money(amount=100, currency='EUR'),
                                    declared_fees=Money(amount=1, currency='EUR'))

    bank_wire_payin.save()

    print legal_user_wallet.balance  # EUR 99.00

PaypalPayIn
-------------

Pay by paypal

.. code-block:: python

    paypal_payin = PayPalPayIn(author=natural_user,
                               debited_funds=Money(amount=100, currency='EUR'),
                               fees=Money(amount=1, currency='EUR'),
                               return_url = 'http://test.test',
                               credited_wallet_id=natural_user_wallet)

    paypal_payin.save()

    print natural_user_wallet.balance  # EUR 99.00

Refund
------

Refund a user on his payment card

.. code-block:: python

    payin_refund = PayInRefund(author=natural_user,
                               payin=direct_payin)

    payin_refund.save()


PayOut
------

Withdraw money from a wallet to a bank account

.. code-block:: python

    payout = PayOut(author=legal_user,
                           debited_funds=Money(amount=100, currency='EUR'),
                           fees=Money(amount=1, currency='EUR'),
                           debited_wallet=legal_user_wallet,
                           bank_account=bankaccount,
                           bank_wire_ref="John Doe's trousers")

    payout.save()

KYC (Know Your Customer) / Identification documents
---------------------------------------------------

To get identification documents of your customers you will have to follow
required steps.

1. Create a Document

.. code-block:: python

    document = Document(type='IDENTITY_PROOF', user=legal_user)
    document.save()

2. Create a Page with uploaded file encoded in base64

.. code-block:: python

    with open(file_path, "rb") as image_file:
        encoded_file = base64.b64encode(image_file.read())

    page = Page(document=document, file=encoded_file, user=legal_user)
    page.save()

Once you have done with these steps, you will be able to get a list of all
the uploaded documents for this particular user

.. code-block:: python

    documents = legal_user.documents.all()

To get the list of all the uploaded documents for all users:

.. code-block:: python

    documents = Document.all()

Client
------

Get details about client.

1.Get Client:

.. code-block:: python

    client = Client.get()

2.Update Client:

.. code-block:: python

    client.primary_button_colour = str("#%06x" % random.randint(0, 0xFFFFFF))
    client.primary_theme_colour = str("#%06x" % random.randint(0, 0xFFFFFF))
    new_client = client.update()

Dispute
-------

1. View disputes

.. code-block:: python

    #view a dispute
    dispute = Dispute.get('dispute_id')
    #view all disputes
    disputes = Dispute.all()

2. Get disputes transactions

.. code-block:: python

    #dispute status must be 'NOT_CONTESTABLE'
    transactions = dispute.transactions.all()

3. Get wallet disputes

.. code-block:: python

    #connection flow : dispute->initial_transaction->credited_wallet
    wallet.disputes.all()

4. Get user disputes

.. code-block:: python

    #connection flow : dispute -> transactions -> author
    user.disputes.all()

5. Contest dispute:
    In order to contest a dispute, its status must be 'PENDING_CLIENT_ACTION' or 'REOPENED_PENDING_CLIENT_ACTION'
    and its type must be either 'CONTESTABLE' or 'RETRIEVAL'

.. code-block:: python

    if dispute.status == 'REOPENED_PENDING_CLIENT_ACTION':
    money = Money(100, 'EUR')

    result = dispute.contest(money)

6. Update a disputes tag

.. code-block:: python

    new_tag = 'New tag ' + str(int(time.time()))
    dispute.tag = new_tag
    result = dispute.save()

7. Close a dispute
    In order to close a dispute, its status must be 'PENDING_CLIENT_ACTION' or 'REOPENED_PENDING_CLIENT_ACTION'

.. code-block:: python

    result = dispute.close()

8. Get repudiation

.. code-block:: python

    #dispute type must be 'not_contestable' and its initial_transaction_id != None
    repudiation = dispute.transactions.all()

9. Create Settlement Transfer

.. code-block:: python

    #dispute status must be 'CLOSED' and its type must be 'NOT_CONTESTABLE'
    repudiation = dispute.transactions.all()[0]
    debit_funds = Money()
    fees = Money()
    debit_funds.currency = 'EUR'
    debit_funds.amount = 1
    fees.currency = 'EUR'
    fees.amount = 0

    st = SettlementTransfer()
    st.author = repudiation.author
    st.debited_funds = debit_funds
    st.fees = fees
    st.repudiation_id = repudiation.id
    result = st.save()

10. Resubmit dispute:

.. code-block:: python

    #dispute type must be 'REOPENED_PENDING_CLIENT_ACTION'
    result = dispute.resubmit()

Idempotency Support
-------------------

To make a request with idempotency support, just add 'idempotency_key' parameter to your function
For example:

.. code-block:: python

    pay_out_post = BankWirePayOut()
    pay_out_post.author = john #john must be a valid user
    pay_out_post.debited_wallet = johns_wallet #valid wallet of johns
    debited_funds = Money()
    debited_funds.amount = 10
    debited_funds.currency = 'EUR'
    pay_out_post.debited_funds = debited_funds
    fees = Money()
    fees.amount = 5
    fees.currency = 'EUR'
    pay_out_post.fees = fees
    pay_out_post.bank_account = johns_account #valid BankAccount of johns
    pay_out_post.bank_wire_ref = "Johns bank wire ref"
    pay_out_post.tag = "DefaultTag"
    pay_out_post.credited_user = john
    pay_out = pay_out_post.save(idempotency_key=key)

In order to get the current idempotency response:

.. code-block:: python

    result = IdempotencyResponse.get(key)

Mandate
-------

1.Create mandate

.. code-block:: python

    mandate = Mandate()
    mandate.bank_account_id = bank_account # valid BankAccount
    mandate.return_url = 'http://test.test'
    mandate.culture = 'FR'
    mandate = Mandate(**mandate.save()) #mandate.save() will return a dict Mandate(**mandate.save())
                                        #will create a Mandate object

2.Get mandates for bank account:

.. code-block:: python

    bank_account.get_mandates() #bank_account must be a valid BankAccount

Banking Aliases
------

1.Create IBAN Bankig Alias

.. code-block:: python

    bankingAlias = BankingAliasIBAN(
        wallet = natural_user_wallet,
        credited_user = natural_user,
        owner_name = natural_user.first_name,
        country ='LU'
    )
    bankingAlias.save()

2. Get all banking aliases for a wallet

.. code-block:: python

    walletBankingAliases = BankingAlias(
        wallet = natural_user_wallet
    )

    allBankingAliases = walletBankingAliases.all()

Sort and filter lists
---------------------

To manage your lists you can pass filters and sorting parameters to
the **all** method.

For example with a transaction list:

.. code-block:: python

    transactions = Transaction.all(handler=handler,
                                   user_id=legal_user.get_pk(),
                                   status='SUCCEEDED',
                                   sort='CreationDate:asc')

* **status** - a specific filter
* **sort** - a sorting parameter

Please refer to the `documentation <https://docs.mangopay.com/api-references/sort-lists/>`_
to know the specific format parameters.
