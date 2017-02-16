import six

from mangopay.signals import pre_save, post_save
from mangopay.utils import Money
from . import constants
from .base import BaseApiModel, BaseApiModelMethods

from .fields import (PrimaryKeyField, EmailField, CharField,
                     BooleanField, DateTimeField, DateField,
                     ManyToManyField, ForeignKeyField,
                     MoneyField, IntegerField, DisputeReasonField, RelatedManager, DictField, AddressField,
                     RefundReasonField, ListField, ReportFiltersField)

from .compat import python_2_unicode_compatible
from .query import InsertQuery, UpdateQuery, SelectQuery, ActionQuery


class BaseModel(BaseApiModel):
    id = PrimaryKeyField(api_name='Id')
    tag = CharField(api_name='Tag')
    update_date = DateTimeField(api_name='UpdateDate')


@python_2_unicode_compatible
class Client(BaseApiModel):
    client_id = PrimaryKeyField(api_name='ClientId', required=True)
    name = CharField(api_name='Name')
    primary_theme_colour = CharField(api_name='PrimaryThemeColour')
    primary_button_colour = CharField(api_name='PrimaryButtonColour')
    logo = CharField(api_name='Logo')
    tech_emails = ListField(api_name='TechEmails')
    admin_email = ListField(api_name='AdminEmails')
    fraud_emails = ListField(api_name='FraudEmails')
    billing_emails = ListField(api_name='BillingEmails')
    platform_description = ListField(api_name='PlatformDescription')
    platform_type = CharField(api_name='PlatformType', choices=constants.PLATFORM_TYPE)
    platform_url = CharField(api_name='PlatformURL')
    headquarters_address = AddressField(api_name='HeadquartersAddress')
    tax_number = CharField(api_name='TaxNumber')

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'
        url = {
            SelectQuery.identifier: '/clients',
            UpdateQuery.identifier: '/clients'
        }

    @classmethod
    def get(cls):
        return super(Client, cls).get('')

    def update(self, handler=None):
        data = self.__dict__
        update = UpdateQuery(self, '',
                             **data['_data']
                             )
        return update.execute(handler)


class ClientLogo(BaseModel):
    file = CharField(api_name='File')

    class Meta:
        verbose_name = 'client-logo'
        verbose_name_plural = 'client-logos'
        url = {
            'UPLOAD_CLIENT_LOGO': '/clients/logo/'
        }

    def upload(self, handler=None):
        self._handler = handler or self.handler

        action = ActionQuery(
            ClientLogo,
            self.get_pk(),
            'UPLOAD_CLIENT_LOGO',
            **{'File': self.file}
        )
        return action.execute(handler)


@python_2_unicode_compatible
class User(BaseModel):
    email = EmailField(api_name='Email', required=True)
    person_type = CharField(api_name='PersonType',
                            choices=constants.USER_TYPE_CHOICES,
                            default=constants.USER_TYPE_CHOICES.natural,
                            required=True)
    kyc_level = CharField(api_name='KYCLevel', choices=constants.KYC_LEVEL, default=constants.KYC_LEVEL.light)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users'

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.disputes = RelatedManager(self, Dispute)

    @classmethod
    def cast(cls, result):
        if 'PersonType' in result:
            if result['PersonType'] == 'NATURAL':
                return NaturalUser
            elif result['PersonType'] == 'LEGAL':
                return LegalUser

        return cls

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class NaturalUser(User):
    first_name = CharField(api_name='FirstName', required=True)
    last_name = CharField(api_name='LastName', required=True)
    address = AddressField(api_name='Address')
    birthday = DateField(api_name='Birthday')
    nationality = CharField(api_name='Nationality', required=True)
    country_of_residence = CharField(api_name='CountryOfResidence', required=True)
    occupation = CharField(api_name='Occupation')
    income_range = CharField(api_name='IncomeRange')
    proof_of_identity = CharField(api_name='ProofOfIdentity')
    proof_of_address = CharField(api_name='ProofOfAddress')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users/natural'

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class LegalUser(User):
    name = CharField(api_name='Name', required=True)
    legal_person_type = CharField(api_name='LegalPersonType',
                                  choices=constants.LEGAL_USER_TYPE_CHOICES,
                                  default=constants.LEGAL_USER_TYPE_CHOICES.organization,
                                  required=True)
    headquarters_address = AddressField(api_name='HeadquartersAddress')
    legal_representative_first_name = CharField(api_name='LegalRepresentativeFirstName', required=True)
    legal_representative_last_name = CharField(api_name='LegalRepresentativeLastName', required=True)
    legal_representative_address = AddressField(api_name='LegalRepresentativeAddress')
    legal_representative_email = EmailField(api_name='LegalRepresentativeEmail')
    legal_representative_birthday = DateField(api_name='LegalRepresentativeBirthday', required=True)
    legal_representative_nationality = CharField(api_name='LegalRepresentativeNationality', required=True)
    legal_representative_country_of_residence = CharField(api_name='LegalRepresentativeCountryOfResidence', required=True)
    legal_representative_proof_of_identity = CharField(api_name='LegalRepresentativeProofOfIdentity')
    statute = CharField(api_name='Statute')
    proof_of_registration = CharField(api_name='ProofOfRegistration')
    shareholder_declaration = CharField(api_name='ShareholderDeclaration')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users/legal'

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class Wallet(BaseModel):
    owners = ManyToManyField(User, api_name='Owners', related_name='wallets', required=True)
    description = CharField(api_name='Description', required=True)
    currency = CharField(api_name='Currency', required=True)
    balance = MoneyField(api_name='Balance')
    creation_date = DateField(api_name='CreationDate')

    class Meta:
        verbose_name = 'wallet'
        verbose_name_plural = 'wallets'
        url = '/wallets'

    def __init__(self, *args, **kwargs):
        super(Wallet, self).__init__(*args, **kwargs)
        self.disputes = RelatedManager(self, Dispute)

    def __str__(self):
        return 'Wallet n.%s' % self.id

    @classmethod
    def is_client_wallet(cls, obj):
        if isinstance(obj, Wallet) or isinstance(obj, ClientWallet):
            test_id = obj.id
        elif isinstance(obj, str):
            test_id = obj
        else:
            return False
        if test_id.startswith('FEES_') or \
                test_id.startswith('DEFAULT_') or \
                test_id.startswith('CREDIT_'):
            return True
        return False

    @classmethod
    def get(cls, *args, **kwargs):
        if len(args) == 1 and cls.is_client_wallet(args[0]):
            return ClientWallet.get(*tuple(args[0].split('_')), **kwargs)
        return super(Wallet, cls).get(*args, **kwargs)


@python_2_unicode_compatible
class Transfer(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True, related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    creation_date = DateField(api_name='CreationDate')
    credited_funds = MoneyField(api_name='CreditedFunds')
    status = CharField(api_name='Status',
                       choices=constants.STATUS_CHOICES,
                       default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')

    class Meta:
        verbose_name = 'transfer'
        verbose_name_plural = 'transfers'
        url = '/transfers'

    def __str__(self):
        return 'Transfer from wallet %s to wallet %s' % (self.debited_wallet_id, self.credited_wallet_id)


@python_2_unicode_compatible
class Card(BaseModel):
    creation_date = DateField(api_name='CreationDate')
    expiration_date = CharField(api_name='ExpirationDate')
    alias = CharField(api_name='Alias')
    card_provider = CharField(api_name='CardProvider')
    card_type = CharField(api_name='CardType',
                          choices=constants.CARD_TYPE_CHOICES,
                          default=None)
    country = CharField(api_name='Country')
    product = CharField(api_name='Product')
    bank_code = CharField(api_name='BankCode')
    active = BooleanField(api_name='Active')
    currency = CharField(api_name='Currency')
    validity = CharField(api_name='Validity',
                         choices=constants.VALIDITY_CHOICES,
                         default=constants.VALIDITY_CHOICES.unknown)
    user = ForeignKeyField(User, api_name='UserId', required=True, related_name='cards')

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'
        url = '/cards'

    def __str__(self):
        return '%s of user %s' % (self.card_type, self.user_id)


class CardRegistration(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', required=True, related_name='card_registrations')
    currency = CharField(api_name='Currency', required=True)
    card_type = CharField(api_name='CardType', choices=constants.CARD_TYPE_CHOICES, default=None)
    card_registration_url = CharField(api_name='CardRegistrationURL')
    access_key = CharField(api_name='AccessKey')
    preregistration_data = CharField(api_name='PreregistrationData')
    registration_data = CharField(api_name='RegistrationData')
    card = ForeignKeyField(Card, api_name='CardId')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    status = CharField(api_name='Status', choices=constants.CARD_STATUS_CHOICES, default=None)
    creation_date = DateField(api_name='CreationDate')

    class Meta:
        verbose_name = 'cardregistration'
        verbose_name_plural = 'cardregistrations'
        url = '/cardregistrations'


class Mandate(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', related_name='mandates')
    bank_account_id = CharField(api_name='BankAccountId', required=True)
    return_url = CharField(api_name='ReturnURL')
    redirect_url = CharField(api_name='RedirectURL')
    document_url = CharField(api_name='DocumentURL')
    culture = CharField(api_name='Culture')

    scheme = CharField(api_name='Scheme', choices=constants.MANDATE_SCHEME_CHOICES, default=None)

    status = CharField(api_name='Status',
                       choices=constants.MANDATE_STATUS_CHOICES,
                       default=None)

    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')

    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    mandate_type = CharField(api_name='MandateType', choiced=constants.MANDATE_TYPE_CHOICES, default=None)

    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'mandate'
        verbose_name_plural = 'mandates'
        url = {
            SelectQuery.identifier: '/mandates',
            InsertQuery.identifier: '/mandates/directdebit/web',
            'CANCEL_MANDATE': '/mandates/%(id)s/cancel/',
            'MANDATES_FOR_BANKACCOUNT': '/users/%(user_id)s/bankaccounts/%(id)s/mandates/'
        }

    def __str__(self):
        return 'Mandate n.%s' % self.id

    def cancel(self, handler=None):
        self._handler = handler or self.handler

        if self.status not in ('SUBMITTED', 'ACTIVE'):
            raise TypeError('Mandate status must be SUBMITTED or ACTIVE')

        action = ActionQuery(
            Mandate,
            self.get_pk(),
            'CANCEL_MANDATE'
        )
        return action.execute(handler)


class PayIn(BaseModel):
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True, related_name='credited_users')
    credited_funds = MoneyField(api_name='CreditedFunds')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    payment_type = CharField(api_name='PaymentType', choices=constants.PAYIN_PAYMENT_TYPE, default=None)
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = '/payins'

    @classmethod
    def cast(cls, result):
        payment_type = result.get('PaymentType')
        execution_type = result.get('ExecutionType')
        types = {
            ("CARD", "DIRECT"): DirectPayIn,
            ("CARD", "WEB"): CardWebPayIn,
            ("DIRECT_DEBIT", "DIRECT"): DirectDebitDirectPayIn,
            ("DIRECT_DEBIT", "WEB"): DirectDebitWebPayIn,
            ("PREAUTHORIZED", "DIRECT"): PreAuthorizedPayIn,
            ("BANK_WIRE", "DIRECT"): BankWirePayIn,
        }
        return types.get((payment_type, execution_type), cls)


@python_2_unicode_compatible
class DirectPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL')
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    creation_date = DateField(api_name='CreationDate')
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/card/direct',
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Direct Payin: %s to %s' % (self.author_id, self.credited_user_id)


@python_2_unicode_compatible
class BankWirePayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    declared_debited_funds = MoneyField(api_name='DeclaredDebitedFunds', required=True)
    declared_fees = MoneyField(api_name='DeclaredFees', required=True)
    wire_reference = CharField(api_name='WireReference')
    bank_account = CharField(api_name='BankAccount')
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/bankwire/direct',
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Bank Wire Payin: %s to %s' % (self.author_id, self.credited_user_id)


class CardWebPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    return_url = CharField(api_name='ReturnURL')
    template_url_options = CharField(api_name='TemplateURLOptions')
    culture = CharField(api_name='Culture')
    card_type = CharField(api_name='CardType', choices=constants.CARD_TYPE_CHOICES, default=None)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    redirect_url = CharField(api_name='RedirectURL')
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)

    class Meta:
        verbose_name = 'card_payin'
        verbose_name_plural = 'card_payins'
        url = {
            InsertQuery.identifier: '/payins/card/web',
            SelectQuery.identifier: '/payins'
        }


class DirectDebitWebPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    return_url = CharField(api_name='ReturnURL')
    template_url_options = CharField(api_name='TemplateURLOptions')
    culture = CharField(api_name='Culture')
    direct_debit_type = CharField(api_name='DirectDebitType', choices=constants.DIRECT_DEBIT_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    redirect_url = CharField(api_name='RedirectURL')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)

    class Meta:
        verbose_name = 'direct_debit_payin'
        verbose_name_plural = 'direct_debit_payins'
        url = {
            InsertQuery.identifier: '/payins/directdebit/web',
            SelectQuery.identifier: '/payins'
        }


class DirectDebitDirectPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    mandate = ForeignKeyField(Mandate, api_name='MandateId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True, related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')

    class Meta:
        verbose_name = 'direct_debit_direct_payin'
        verbose_name_plural = 'direct_debit_direct_payins'
        url = {
            InsertQuery.identifier: '/payins/directdebit/direct',
            SelectQuery.identifier: '/payins'
        }


class PreAuthorization(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    payment_status = CharField(api_name='PaymentStatus', choices=constants.PAYMENT_STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default,
                            required=True)
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL', required=True)
    expiration_date = DateField(api_name='ExpirationDate')
    payin = ForeignKeyField(PayIn, api_name='PayinId')

    class Meta:
        verbose_name = 'preauthorization'
        verbose_name_plural = 'preauthorizations'
        url = {
            InsertQuery.identifier: '/preauthorizations/card/direct',
            UpdateQuery.identifier: '/preauthorizations',
            SelectQuery.identifier: '/preauthorizations'
        }


class PreAuthorizedPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL')
    preauthorization = ForeignKeyField(PreAuthorization, api_name='PreauthorizationId', required=True)
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)

    class Meta:
        verbose_name = 'preauthorized_payin'
        verbose_name_plural = 'preauthorized_payins'
        url = {
            InsertQuery.identifier: '/payins/PreAuthorized/direct',
            SelectQuery.identifier: '/payins'
        }


@python_2_unicode_compatible
class BankAccount(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', related_name='bankaccounts')
    owner_name = CharField(api_name='OwnerName', required=True)
    owner_address = AddressField(api_name='OwnerAddress', required=True)
    creation_date = DateField(api_name='CreationDate')
    type = CharField(api_name='Type', choices=constants.BANK_ACCOUNT_TYPE_CHOICES, default=None, required=True)
    iban = CharField(api_name='IBAN')
    bic = CharField(api_name='BIC')
    account_number = CharField(api_name='AccountNumber')
    sort_code = CharField(api_name='SortCode')
    aba = CharField(api_name='ABA')
    deposit_account_type = CharField(api_name='DepositAccountType',
                                     choices=constants.DEPOSIT_CHOICES,
                                     default=constants.DEPOSIT_CHOICES.checking)
    bank_name = CharField(api_name='BankName')
    institution_number = CharField(api_name='InstitutionNumber')
    branch_code = CharField(api_name='BranchCode')
    country = CharField(api_name='Country')
    bic = CharField(api_name='BIC')
    active = BooleanField(api_name='Active', default=True)

    class Meta:
        verbose_name = 'bankaccount'
        verbose_name_plural = 'bankaccounts'
        url = {
            InsertQuery.identifier: '/users/%(user_id)s/bankaccounts/%(type)s',
            SelectQuery.identifier: '/users/%(user_id)s/bankaccounts',
            UpdateQuery.identifier: '/users/%(user_id)s/bankaccounts'
        }

    def __str__(self):
        return 'Bank account %s of user %s' % (self.type, self.user_id)

    def get_mandates(self, *args, **kwargs):
        kwargs['user_id'] = self.user_id
        kwargs['id'] = self.id
        select = SelectQuery(Mandate, *args, **kwargs)
        select.identifier = 'MANDATES_FOR_BANKACCOUNT'
        return select.all(*args, **kwargs)

    def deactivate(self):
        return BankAccount.update(self.id, active=False, user_id=self.user_id).execute()


@python_2_unicode_compatible
class BankWirePayOut(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    credited_funds = MoneyField(api_name='CreditedFunds')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId', required=True)
    bank_account = ForeignKeyField(BankAccount, api_name='BankAccountId', required=True)
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    payment_type = CharField(api_name='PaymentType', choices=constants.PAYOUT_PAYMENT_TYPE, default=None)
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    bank_wire_ref = CharField(api_name='BankWireRef')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId')

    class Meta:
        verbose_name = 'payout'
        verbose_name_plural = 'payouts'
        url = {
            InsertQuery.identifier: '/payouts/bankwire',
            SelectQuery.identifier: '/payouts'
        }

    def __str__(self):
        return 'PayOut request from user %s' % self.author_id


class Refund(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds')
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    refund_reason = RefundReasonField(api_name='RefundReason')
    initial_transaction_id = CharField(api_name='InitialTransactionId')
    initial_transaction_type = CharField(api_name='InitialTransactionType', choices=constants.TRANSACTION_TYPE_CHOICES,
                                         default=None)

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'
        url = '/refunds'


@python_2_unicode_compatible
class TransferRefund(Refund):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    transfer = ForeignKeyField(Transfer)

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'
        url = '/transfers/%(transfer_id)s/refunds'

    def __str__(self):
        return 'TransferRefund request from user %s' % self.author_id


@python_2_unicode_compatible
class PayInRefund(Refund):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')
    payin = ForeignKeyField(PayIn)

    class Meta:
        verbose_name = 'refund'
        verbose_name_plural = 'refunds'
        url = {
            InsertQuery.identifier: '/payins/%(payin_id)s/refunds',
            SelectQuery.identifier: '/refunds'
        }

    def __str__(self):
        return 'PayInRefund request from user %s' % self.author_id


class KYC(BaseModel):
    class Meta:
        verbose_name = 'kyc'
        verbose_name_plural = 'kycs'
        url = '/KYC/documents'


@python_2_unicode_compatible
class Document(KYC):
    user = ForeignKeyField(User, related_name='documents', api_name='UserId')
    type = CharField(api_name='Type', choices=constants.DOCUMENTS_TYPE_CHOICES, default=None)
    status = CharField(api_name='Status', choices=constants.DOCUMENTS_STATUS_CHOICES, default=None)
    refused_reason_type = CharField(api_name='RefusedReasonType')
    refused_reason_message = CharField(api_name='RefusedReasonMessage')

    class Meta:
        verbose_name = 'KYC/document'
        verbose_name_plural = 'KYC/documents'
        url = {
            InsertQuery.identifier: '/users/%(user_id)s/KYC/documents',
            UpdateQuery.identifier: '/users/%(user_id)s/KYC/documents',
            SelectQuery.identifier: '/KYC/documents'
        }

    def __str__(self):
        return 'Document for user %s' % self.user_id


@python_2_unicode_compatible
class Page(KYC):
    file = CharField(api_name='File', required=True, python_value_callback=lambda value: six.b(value))
    user = ForeignKeyField(User)
    document = ForeignKeyField(Document)

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'
        url = '/users/%(user_id)s/KYC/documents/%(document_id)s/pages'

    def __str__(self):
        return 'Page of document %s for user %s' % (self.document_id, self.user_id)


@python_2_unicode_compatible
class Transaction(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', related_name='transactions')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId')
    debited_funds = MoneyField(api_name='DebitedFunds')
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    wallet = ForeignKeyField(Wallet, related_name='transactions')

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        url = '/users/%(user_id)s/transactions'

    def __str__(self):
        return 'Transaction n.%s' % self.id


class Event(BaseModel):
    resource_id = IntegerField(api_name='ResourceId')
    event_type = CharField(api_name='EventType', choices=constants.EVENT_TYPE_CHOICES, default=None)
    date = DateTimeField(api_name='Date')

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        url = '/events'


class Notification(BaseModel):
    url = CharField(api_name='Url', required=True)
    status = CharField(api_name='Status', choices=constants.NOTIFICATION_STATUS_CHOICES, default=None)
    validity = CharField(api_name='Validity', choices=constants.NOTIFICATION_VALIDITY_CHOICES, default=None)
    event_type = CharField(api_name='EventType', choices=constants.EVENT_TYPE_CHOICES, default=None, required=True)
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'notification'
        verbose_name_plural = 'notifications'
        url = '/hooks'


@python_2_unicode_compatible
class ClientWallet(Wallet):
    funds_type = CharField(api_name='FundsType')

    class Meta:
        verbose_name = 'client_wallets'
        verbose_name_plural = 'client_wallets'
        fund_type_url = {'CREDIT': 'SELECT_BY_CREDIT', 'FEES': 'SELECT_BY_FEES', 'DEFAULT': 'SELECT_BY_DEFAULT'}
        url = {
            SelectQuery.identifier: '/clients/wallets',
            'SELECT_CLIENT_WALLET': '/clients/wallets/%(fund_type)s/%(currency)s',
            'SELECT_BY_CREDIT': '/clients/wallets/CREDIT',
            'SELECT_BY_FEES': '/clients/wallets/FEES',
            'SELECT_BY_DEFAULT': '/clients/wallets'
        }

    def __str__(self):
        return 'Client wallet n.%s' % self.id

    @classmethod
    def get(cls, funds_type, currency, **kwargs):
        kwargs['fund_type'], kwargs['currency'] = funds_type, currency
        args = '',
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = 'SELECT_CLIENT_WALLET'
        return select.get(*args, **kwargs)

    @classmethod
    def all_by_funds_type(cls, fund_type, *args, **kwargs):
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = cls._meta.fund_type_url[fund_type]
        return select.all(*args, **kwargs)

    def get_pk(self):
        return getattr(self, 'id', None)


class Dispute(BaseModel):
    initial_transaction_id = CharField(api_name='InitialTransactionId')
    initial_transaction_type = CharField(api_name='InitialTransactionType', choices=constants.TRANSACTION_TYPE_CHOICES,
                                         default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    dispute_reason = DisputeReasonField(api_name='DisputeReason')
    status = CharField(api_name='Status', choices=constants.DISPUTES_STATUS_CHOICES, default=None)
    status_message = CharField(api_name='StatusMessage')
    disputed_funds = MoneyField(api_name='DisputedFunds')
    contested_funds = MoneyField(api_name='ContestedFunds')
    repudiation_id = CharField(api_name='RepudiationId')

    dispute_type = CharField(api_name='DisputeType', choices=constants.DISPUTE_TYPE_CHOICE, default=None)
    contest_deadline_date = DateTimeField(api_name='ContestDeadlineDate')

    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'dispute'
        verbose_name_plural = 'disputes'
        url = {
            SelectQuery.identifier: '/disputes',
            UpdateQuery.identifier: '/disputes',
            'CLOSE_DISPUTE': '/disputes/%(id)s/close/',
            'SUBMIT_DISPUTE': '/disputes/%(id)s/submit/',
            'RE_SUBMIT_DISPUTE': '/disputes/%(id)s/submit/'
        }

    def __init__(self, *args, **kwargs):
        super(Dispute, self).__init__(*args, **kwargs)
        self.transactions = RelatedManager(self, Transaction)

    def __str__(self):
        return 'Dispute n.%s tag:%s' % (self.id, self.tag)

    def save(self, handler=None, cls=None):
        self._handler = handler or self.handler

        if cls is None:
            cls = self.__class__

        created = False

        pre_save.send(cls, instance=self)

        update = self.update(
            self.get_pk(),
            **{'tag': self.tag}
        )
        result = update.execute(handler)

        post_save.send(cls, instance=self, created=created)

        for key, value in result.items():
            setattr(self, key, value)

        return result

    def close(self, handler=None):
        self._handler = handler or self.handler
        action = ActionQuery(
            Dispute,
            self.get_pk(),
            'CLOSE_DISPUTE'
        )
        action.execute(handler)

    def contest(self, money, handler=None):
        self._handler = handler or self.handler
        if isinstance(money, Money):
            action = ActionQuery(
                Dispute,
                self.get_pk(),
                'SUBMIT_DISPUTE',
                **{'ContestedFunds': MoneyField().api_value(money)}
            )
            return action.execute(handler)

    def resubmit(self, handler=None):
        self._handler = handler or self.handler
        action = ActionQuery(
            Dispute,
            self.get_pk(),
            'RE_SUBMIT_DISPUTE'
        )
        return action.execute(handler)


class DisputeDocument(BaseModel):
    dispute = ForeignKeyField(Dispute, api_name='DisputeId', related_name='documents', required=True)
    status = CharField(api_name='Status', choices=constants.DOCUMENTS_STATUS_CHOICES, default=None)
    type = CharField(api_name='Type', choices=constants.DISPUTE_DOCUMENT_TYPE_CHOICES, defalut=None)
    refused_reason_message = CharField(api_name='RefusedReasonMessage')
    refused_reason_type = CharField(api_name='RefusedReasonType', choices=constants.REFUSED_REASON_TYPE_CHOICES,
                                    default=None)
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'
        url = {
            SelectQuery.identifier: '/dispute-documents',
            InsertQuery.identifier: 'disputes/%(dispute_id)s/documents/',
            'SUBMIT_DOCUMENT': '/disputes/%(dispute_id)s/documents/%(id)s'
        }

    def __str__(self):
        return 'Dispute document id:%s  status:%s  type:%s' % (self.id, self.status, self.type)

    def submit(self, status=None, handler=None):
        self._handler = handler or self.handler
        submit_status = status or self.status
        if submit_status is None or submit_status not in constants.DOCUMENTS_STATUS_CHOICES:
            raise TypeError('Invalid status')

        action = ActionQuery(
            DisputeDocument,
            self.get_pk(),
            'SUBMIT_DOCUMENT',
            params={'dispute_id': self.dispute_id},
            **{'Status': submit_status}
            )
        return action.execute(handler)


@python_2_unicode_compatible
class DisputeDocumentPage(BaseModel):
    file = CharField(api_name='File', required=True, python_value_callback=lambda value: six.b(value))
    document = ForeignKeyField(DisputeDocument)
    dispute = ForeignKeyField(Dispute)

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'
        url = '/disputes/%(dispute_id)s/documents/%(document_id)s/pages/'

    def __str__(self):
        return 'Page of dispute document %s for dispute %s' % (self.document_id, self.dispute_id)


class Repudiation(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId')
    disputed_funds = MoneyField(api_name='DisputedFunds')
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees')
    credited_wallet = CharField(Wallet, api_name='CreditedWalletId')
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId')
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    execution_date = DateField(api_name='ExecutionDate')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')

    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'repudiation'
        verbose_name_plural = 'repudiations'
        url = {
            SelectQuery.identifier: '/repudiations',
        }

    def __str__(self):
        return 'Repudiation n.%s' % self.id


class SettlementTransfer(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', required=True)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    execution_date = DateTimeField(api_name='ExecutionDate')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    repudiation = ForeignKeyField(Repudiation, api_name='RepudiationId')
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'settlement_transfer'
        verbose_name_plural = 'settlement_transfers'
        url = {
            SelectQuery.identifier: '/settlements',
            InsertQuery.identifier: '/repudiations/%(repudiation_id)s/settlementtransfer/'
        }

    def __str__(self):
        return 'SettlementTransfer n.%s' % self.id


class IdempotencyResponse(BaseApiModelMethods):
    status = CharField(api_name='StatusCode')
    content_length = CharField(api_name='ContentLength')
    content_type = CharField(api_name='ContentType')
    date = CharField(api_name='Date')
    resource = DictField(api_name='Resource')

    class Meta:
        verbose_name = 'idempotency'
        verbose_name_plural = 'idempotency'
        url = {
            SelectQuery.identifier: '/responses/',
        }

    @classmethod
    def get(cls, idempotency_key):
        return SelectQuery(cls).get(idempotency_key)

    def get_resource(self, model=BaseModel):
        query = SelectQuery(model)
        data = query.parse_result(self.resource)
        return model(**data)


class Report(BaseModel):
    creation_date = CharField(api_name='CreationDate')
    report_date = CharField(api_name='ReportDate')
    download_url = CharField(api_name='DownloadURL')
    callback_url = CharField(api_name='CallbackURL')
    download_format = CharField(api_name='DownloadFormat', choices=constants.DOWNLOAD_FORMAT, default='CSV')
    report_type = CharField(api_name='ReportType', choices=constants.REPORT_TYPE, default='TRANSACTIONS')
    sort = CharField(api_name='Sort')
    preview = BooleanField(api_name='Preview')
    filters = ReportFiltersField(api_name='Filters')
    columns = ListField(api_name='Columns')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        url = {
            SelectQuery.identifier: '/reports/',
            InsertQuery.identifier: '/reports/transactions/'
        }

