Usage
=====

Create an handler
-----------------

To manipulate resources (users, wallets, etc.) from this api you will have to
instanciate a new handler which is a connection authentication.

To create a new handler, you have to provide several parameters:

* **MANGOPAY_CLIENT_ID** - The client identifier used by `mangopay <http://www.mangopay.com/>`_ to identify you
* **MANGOPAY_APIKEY** - Your password

API host
--------

The host used to call the API.

We will see later when you are creating a new handler you can choose between
multiple environment hosts already registered.

Let's get to work, we will create our first handler with the sandbox host:

V2

.. code-block:: python

    from mangopaysdk.mangopayapi import MangoPayApi

    api = MangoPayApi()
    api.Config.ClientID = 'sdk-unit-tests'
    api.Config.ClientPassword = 'cqFfFrWfCcb7UadHNxx2C9Lo6Djw8ZduLi7J9USTmu8bhxxpju'

V3

.. code-block:: python

    import mangopay

    mangopay.client_id='my client id'
    mangopay.apikey='my password'

    from mangopay.api import APIRequest

    handler = APIRequest(sandbox=True)

Now we have a new handler which is using the sandbox host.

If you are not specifying that you are using the sandbox host nor an existing host,
it will use the sandbox host by default.

API proxy support
-----------------

When you are creating a new handler you can use proxies for https, http and ftp protocols.

V3 only

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

StaticStorageStrategy() - saves token in memory (MemoryStorageStrategy from V2)

FileStorageStrategy() - saves token in temporary file (DefaultStorageStrategy from V2)

V2

.. code-block:: python

    api.OAuthTokenManager.RegisterCustomStorageStrategy(MemoryStorageStrategy())
    api.OAuthTokenManager.RegisterCustomStorageStrategy(DefaultStorageStrategy())

If no strategy is sepcified, DefaultStorageStrategy will be used.

V3

.. code-block:: python

    handler = APIRequest(sandbox=True, storage_strategy=StaticStorageStrategy())
    handler = APIRequest(sandbox=True, storage_strategy=FileStorageStrategy())

If no strategy is specified, StaticStorageStrategy will be used.

API requests timeout
--------------------

When you create a new handler you can set the amount of time (in seconds) after that the requests will timeout.

V3 only

.. code-block:: python

    handler = APIRequest(sandbox=True, timeout=30.0)

The default timeout is 30 seconds.

Using resources
---------------

Following are a number of example API calls made through the SDK, with comparison V2 and V3 methods.

To manipulate your resources, the V3 library is heavily inspired from `peewee <https://github.com/coleifer/peewee/>`_,
so every operations will be like manipulating your favorite ORM.

For required parameters you can refer to the `reference api <https://docs.mangopay.com/api-references/>`_.

User
----

Create a natural user

V2

.. code-block:: python


    from mangopaysdk.types.address import Address
    from mangopaysdk.entities.usernatural import UserNatural

    user = UserNatural()
    user.FirstName = "John"
    user.LastName = "Doe"
    user.Email = "john.doe@sample.org"
    address = Address()
    address.AddressLine1 = "Address line 1"
    address.AddressLine2 = "Address line 2"
    address.City = "City"
    address.Region = "Region"
    address.PostalCode = "11222"
    address.Country = "PL"
    user.Address = address
    user.Birthday = 1300186358
    user.Nationality = "FR"
    user.CountryOfResidence = "FR"
    user.Occupation = "programmer"
    user.IncomeRange = 3
    saved_user = api.users.Create(user)

V3

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

V2

.. code-block:: python

    user = api.users.Get(1)

    print user.FirstName # Victor

V3

.. code-block:: python

    natural_user = NaturalUser.get(1) # 1 is an ID value, not an array index

    print natural_user.first_name # Victor

Detect a user which does not exist

V2

.. code-block:: python

    try:
        user = api.users.Get(1)
    except ResponseException as e:
        if (e.Code == 404)
            print 'The user 1 does not exist'

V3

.. code-block:: python

    try:
        natural_user = NaturalUser.get(2)
    except NaturalUser.DoesNotExist:
        print 'The natural user 2 does not exist'

Retrieve all users

V2

.. code-block:: python

    users = api.users.GetAll()
    print users # [<NaturalUser: victor@hugo.com>, <LegalUser: support@ulule.com>]

V3

.. code-block:: python

    users = User.all()
    print users  # [<NaturalUser: victor@hugo.com>, <LegalUser: support@ulule.com>]

Retrieve users with a pagination

V2

.. code-block:: python

    pagination = Pagination(Page=1, ItemsPerPage=2)
    users = User.all(pagination)

V3

.. code-block:: python

    users = User.all(page=1, per_page=2)

Retrieve a users's EMoney

V3 only

.. code-block:: python

    natural_user = NaturalUser.get(1)
    emoney = natural_user.get_emoney()

    print emoney.credited_emoney
    print emoney.debited_emoney

Wallet
------

Create a wallet

V2

.. code-block:: python

    user = api.users.Get(1)

    from mangopaysdk.entities.wallet import Wallet

    wallet = Wallet()
    wallet.Owners = [john.Id]
    wallet.Currency = 'EUR'
    wallet.Description = 'WALLET IN EUR'

    saved_wallet = api.wallets.Create(wallet)

V3

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

V2

.. code-block:: python

    wallets = api.users.GetWallets(userId=1)

V3

.. code-block:: python

    natural_user = NaturalUser.get(1)

    print natural_user.wallets  # [<Wallet: Wallet n.1169421>]

Transfer
--------

Create a transfer from a wallet to another one

V2

.. code-block:: python

    print debited_wallet.Balance # EUR 99.00
    print credited_wallet.Balance # EUR 0.00

    transfer = Transfer()
    transfer.AuthorId = debited_wallet.Owners[0]
    transfer.DebitedFunds = Money()
    transfer.DebitedFunds.Currency = 'EUR'
    transfer.DebitedFunds.Amount = 1000
    transfer.Fees = Money()
    transfer.Fees.Currency = 'EUR'
    transfer.Fees.Amount = 100
    transfer.DebitedWalletId = debited_wallet.Id
    transfer.CreditedWalletId = credited_wallet.Id

    saved_ransfer = api.transfers.Create(transfer)

    print debited_wallet.Balance # EUR 89.00
    print credited_wallet.Balance # EUR 9.00

V3

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

V2

.. code-block:: python

    print debited_wallet.Balance # EUR 89.00
    print credited_wallet.Balance # EUR 9.00

    refund = Refund()
    refund.DebitedWalletId = transfer.DebitedWalletId
    refund.CreditedWalletId = transfer.CreditedWalletId
    refund.AuthorId = transfer.AuthorId
    refund.DebitedFunds = Money()
    refund.DebitedFunds.Amount = transfer.DebitedFunds.Amount
    refund.DebitedFunds.Currency = transfer.DebitedFunds.Currency
    refund.Fees = Money()
    refund.Fees.Amount = transfer.Fees.Amount
    refund.Fees.Currency = transfer.Fees.Currency

    saved_refund = api.transfers.CreateRefund(transfer.Id, refund)

V3

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

V2

.. code-block:: python

    transactions = api.wallets.GetTransactions(wallet.Id)

    print transactions # [<Transaction: Transaction n.1174821>]

V3

.. code-block:: python

    print legal_user_wallet.transactions.all()  # [<Transaction: Transaction n.1174821>]

Retrieve user's transactions

V2

.. code-block:: python

    transactions = api.users.GetTransactions(user.Id)

    print transactions # [<Transaction: Transaction n.1174821>]

V3

.. code-block:: python

    print legal_user.transactions.all()  # [<Transaction: Transaction n.1174821>]

List all transactions made by a user (you can filter transactions by status)

V2

.. code-block:: python

    filter = FilterTransactions()
    filter.status = 'SUCCEEDED'

    transactions = api.users.GetTransactions(user.Id, None, None, filter)

V3

.. code-block:: python

    transactions = Transaction.all(user_id=natural_user.get_pk(), status='SUCCEEDED')

    print transactions  # [<Transaction: Transaction n.1174821>]

Card
----

To register a card for a user you have to create a RegistrationCard
object with the user and his currency as params

V2

.. code-block:: python

    card_registration = CardRegistration()
    card_registration.CardType = cardType
    card_registration.UserId = user.Id
    card_registration.Currency = 'EUR'

    saved_card_registration = api.cardRegistrations.Create(card_registration)

V3

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

V2

.. code-block:: python

    saved_card_registration.RegistrationData = response
    updated_card_registration = api.cardRegistrations.Update(saved_card_registration)

V3

.. code-block:: python

    card_registration.registration_data = response
    card_registration.save()

Now, we have a `card_id` and you can retrieve the new card

V2

.. code-block:: python

    print updated_card_registration.CardId # 1

    card = api.cards.Get(updated_card_registration.CardId) # CB_VISA_MASTERCARD of user 6641810

V3

.. code-block:: python

    print card_registration.card_id  # 1
    print card_registration.card  # CB_VISA_MASTERCARD of user 6641810

Retrieve user's cards

V2

.. code-block:: python

    print api.users.GetCards(user.Id) # [<Card: CB_VISTA_MASTERCARD of user 6641810>]

V3

.. code-block:: python

    print user.cards.all()  # [<Card: CB_VISA_MASTERCARD of user 6641810>]

    print user.cards.get(card.id)  # CB_VISA_MASTERCARD of user 6641810

Retrieve cards by fingerprint

V3 only

.. code-block:: python

    cards = Card.get_by_fingerprint(fingerprint) #return a list of card objects that matches with specified fingerprint.

PayIn
-----

Direct payment on a user's wallet

V2

.. code-block:: python

    pay_in = PayIn()
    pay_in.CreditedWalletId = credited_wallet.Id
    pay_in.AuthorId = credited_wallet.Owners[0]
    pay_in.DebitedFunds = Money()
    pay_in.DebitedFunds.Amount = 10000
    pay_in.DebitedFunds.Currency = 'EUR'
    pay_in.Fees = Money()
    pay_in.Fees.Amount = 0
    pay_in.Fees.Currency = 'EUR'
    # payment type as CARD
    pay_in.PaymentDetails = PayInPaymentDetailsCard()
    pay_in.PaymentDetails.CardType = card.CardType
    # execution type as DIRECT
    pay_in.ExecutionDetails = PayInExecutionDetailsDirect()
    pay_in.ExecutionDetails.CardId = card.Id
    pay_in.ExecutionDetails.SecureModeReturnURL = 'http://test.com'

    saved_pay_in = api.payIns.Create(pay_in)

V3

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

V2

.. code-block:: python

    account = BankAccount()
    account.OwnerName = user.FirstName + ' ' +  user.LastName
    account.OwnerAddress = user.Address
    account.UserId = user.Id
    account.Type = 'IBAN'
    account.IBAN = 'FR7618829754160173622224154'
    account.BIC = 'CMBRFR2BCME'

    saved_account = api.users.CreateBankAccount(user.Id, account)

V3

.. code-block:: python

    bankaccount_iban = BankAccount(owner_name="Victor Hugo",
                                  user_id="8494514",
                                  type="IBAN",
                                  owner_address=Address(address_line_1='AddressLine1', address_line_2='AddressLine2',
                                  postal_code='11222', country='FR'),
                                  iban="FR3020041010124530725S03383",
                                  bic="CRLYFRPP")

    bankaccount.save()

BankWirePayIn
-------------

And pay by bank wire

V2

.. code-block:: python

    pay_in = PayIn()
    pay_in.CreditedWalletId = wallet.Id
    pay_in.AuthorId = wallet.Owners[0]

    # payment type as CARD
    pay_in.PaymentDetails = PayInPaymentDetailsBankWire()
    pay_in.PaymentDetails.DeclaredDebitedFunds = Money()
    pay_in.PaymentDetails.DeclaredFees = Money()
    pay_in.PaymentDetails.DeclaredDebitedFunds.Currency = 'EUR'
    pay_in.PaymentDetails.DeclaredFees.Currency = 'EUR'
    pay_in.PaymentDetails.DeclaredDebitedFunds.Amount = 10000
    pay_in.PaymentDetails.DeclaredFees.Amount = 1000

    # execution type as DIRECT
    pay_in.ExecutionDetails = PayInExecutionDetailsDirect()
    pay_in.ExecutionType = ExecutionType.DIRECT

    saved_pay_in = api.payIns.Create(payIn)

V3

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

V3 only

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

V2

.. code-block:: python

    refund = Refund()
    refund.CreditedWalletId = pay_in.CreditedWalletId
    refund.AuthorId = pay_in.AuthorId
    refund.DebitedFunds = Money()
    refund.DebitedFunds.Amount = pay_in.DebitedFunds.Amount
    refund.DebitedFunds.Currency = pay_in.DebitedFunds.Currency
    refund.Fees = Money()
    refund.Fees.Amount = pay_in.Fees.Amount
    refund.Fees.Currency = pay_in.Fees.Currency

    saved_refund = api.payIns.CreateRefund(pay_in.Id, refund)

V3

.. code-block:: python

    payin_refund = PayInRefund(author=natural_user,
                               payin=direct_payin)

    payin_refund.save()


PayOut
------

Withdraw money from a wallet to a bank account

V2

.. code-block:: python

    pay_out = PayOut()
    pay_out.Tag = 'DefaultTag'
    pay_out.AuthorId = user.Id
    pay_out.CreditedUserId = user.Id
    pay_out.DebitedFunds = Money()
    pay_out.DebitedFunds.Currency = 'EUR'
    pay_out.DebitedFunds.Amount = 10
    pay_out.Fees = Money()
    pay_out.Fees.Currency = 'EUR'
    pay_out.Fees.Amount = 5

    pay_out.DebitedWalletId = wallet.Id
    pay_out.MeanOfPaymentDetails = payOutPaymentDetailsBankWire()
    pay_out.MeanOfPaymentDetails.BankAccountId = account.Id

    saved_pay_out = api.payOuts.Create(pay_out)

V3

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

V2

.. code-block:: python

    kyc_document = kyc_document()
    kyc_document.Tag = 'test tag 1'
    kyc_document.Type = KycDocumentType.IDENTITY_PROOF
    kyc_document.UserId = user.Id

    saved_kyc_document = api.users.CreateUserKycDocument(kycDocument, user.Id)

V3

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

V2

.. code-block:: python

    documents = api.users.GetKycDocuments(user.Id)

V3

.. code-block:: python

    documents = legal_user.documents.all()

To get the list of all the uploaded documents for all users:

V2

.. code-block:: python

    documents = api.kycdocuments.GetAll()

V3

.. code-block:: python

    documents = Document.all()

To get the list of KYC documents pages

V3 only

.. code-block:: python

    document_consult = DocumentConsult.get_kyc_document_consult(document.id)

Client
------

Get details about client.

1.Get Client:

V2

.. code-block:: python

    client = api.clients.Get()

V3

.. code-block:: python

    client = Client.get()

2.Update Client:

V2

.. code-block:: python

    client.PrimaryButtonColour = str("#%06x" % random.randint(0, 0xFFFFFF))
    client.PrimaryThemeColour = str("#%06x" % random.randint(0, 0xFFFFFF))

    updated_client = api.clients.Update(client)

V3

.. code-block:: python

    client.primary_button_colour = str("#%06x" % random.randint(0, 0xFFFFFF))
    client.primary_theme_colour = str("#%06x" % random.randint(0, 0xFFFFFF))
    new_client = client.update()

Dispute
-------

1. View disputes

V2

.. code-block:: python

    #view a dispute
    dispute = api.disputes.Get(dispute.Id)
    #view all disputes
    disputes = api.disputes.GetAll()

V3

.. code-block:: python

    #view a dispute
    dispute = Dispute.get('dispute_id')
    #view all disputes
    disputes = Dispute.all()

2. Get disputes transactions

V2

.. code-block:: python

    transactions = api.disputes.GetTransactions(dispute.Id)

V3

.. code-block:: python

    #dispute status must be 'NOT_CONTESTABLE'
    transactions = dispute.transactions.all()

3. Get wallet disputes

V3 only

.. code-block:: python

    #connection flow : dispute->initial_transaction->credited_wallet
    wallet.disputes.all()

4. Get user disputes

V3 only

.. code-block:: python

    #connection flow : dispute -> transactions -> author
    user.disputes.all()

5. Contest dispute:
    In order to contest a dispute, its status must be 'PENDING_CLIENT_ACTION' or 'REOPENED_PENDING_CLIENT_ACTION'
    and its type must be either 'CONTESTABLE' or 'RETRIEVAL'

V2

.. code-block:: python

    contested_funds = Money()
    contested_funds.amount = 100
    contested_funds.currency = 'EUR'

    result = api.disputes.ContestDispute(contested_funds, dispute.Id)


V3

.. code-block:: python

    if dispute.status == 'REOPENED_PENDING_CLIENT_ACTION':
    money = Money(100, 'EUR')

    result = dispute.contest(money)

6. Update a disputes tag

V2

.. code-block:: python

    new_tag = 'New tag ' + str(int(time.time()))
    result = api.disputes.UpdateTag(new_tag, dispute.Id)

V3

.. code-block:: python

    new_tag = 'New tag ' + str(int(time.time()))
    dispute.tag = new_tag
    result = dispute.save()

7. Close a dispute
    In order to close a dispute, its status must be 'PENDING_CLIENT_ACTION' or 'REOPENED_PENDING_CLIENT_ACTION'

V2

.. code-block:: python

    result = api.disputes.CloseDispute(dispute.Id)

V3

.. code-block:: python

    result = dispute.close()

8. Get repudiation

V2

.. code-block:: python

    repudiation = api.disputes.GetRepudiation(repudiation.id)

V3

.. code-block:: python

    #dispute type must be 'not_contestable' and its initial_transaction_id != None
    repudiation = dispute.transactions.all()

9. Create Settlement Transfer

V2

.. code-block:: python

    debited_funds = Money()
    fees = Money()
    debited_funds.Currency = 'EUR'
    debited_funds.Amount = 1
    fees.Currency = 'EUR'
    fees.Amount = 0

    transfer = Transfer()
    transfer.AuthorId = repudiation.AuthorId
    transfer.DebitedFunds = debited_funds
    transfer.Fees = fees

    result = api.disputes.CreateSettlementTransfer(transfer, repudiation.Id)

V3

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

V2

.. code-block:: python

    result = api.disputes.ResubmitDispute(dispute.Id)

V3

.. code-block:: python

    #dispute type must be 'REOPENED_PENDING_CLIENT_ACTION'
    result = dispute.resubmit()

11. To get the list of Dispute documents pages

V3 only

.. code-block:: python

    document_consult = DocumentConsult.get_dispute_document_consult(dispute_document.id)

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
