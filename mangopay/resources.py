import six

from mangopay.signals import pre_save, post_save
from mangopay.utils import Money, Address, Birthplace
from . import constants
from .base import BaseApiModel, BaseApiModelMethods
from .compat import python_2_unicode_compatible
from .fields import (PrimaryKeyField, EmailField, CharField,
                     BooleanField, DateTimeField, DateField,
                     ManyToManyField, ForeignKeyField,
                     MoneyField, IntegerField, DisputeReasonField, RelatedManager, DictField, AddressField,
                     DebitedBankAccountField,
                     ShippingAddressField, RefundReasonField, ListField, ReportTransactionsFiltersField,
                     ReportWalletsFiltersField, BillingField, SecurityInfoField, PlatformCategorizationField,
                     BirthplaceField, ApplepayPaymentDataField, GooglepayPaymentDataField, ScopeBlockedField,
                     BrowserInfoField, ShippingField, CurrentStateField, FallbackReasonField, InstantPayoutField,
                     CountryAuthorizationDataField)
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
    platform_categorization = PlatformCategorizationField(api_name='PlatformCategorization')
    platform_url = CharField(api_name='PlatformURL')
    headquarters_address = AddressField(api_name='HeadquartersAddress')
    headquarters_phone_number = CharField(api_name='HeadquartersPhoneNumber')
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
    kyc_level = CharField(api_name='KYCLevel', choices=constants.KYC_LEVEL, default=constants.KYC_LEVEL.light)
    terms_and_conditions_accepted = BooleanField(api_name='TermsAndConditionsAccepted')
    terms_and_conditions_accepted_date = DateTimeField(api_name='TermsAndConditionsAcceptedDate')
    user_category = CharField(api_name='UserCategory')

    def fixed_kwargs(self):
        return {"user_id": self.id}

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

    def get_emoney(self, *args, **kwargs):
        kwargs['user_id'] = self.id
        select = SelectQuery(EMoney, *args, **kwargs)
        if kwargs.__contains__('month') and kwargs.__contains__('year'):
            select.identifier = 'FOR_MONTH'
        elif kwargs.__contains__('year'):
            select.identifier = 'FOR_YEAR'
        else:
            select.identifier = 'ALL'
        return select.all(*args, **kwargs)

    def get_pre_authorizations(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(PreAuthorization, *args, **kwargs)
        select.identifier = 'USER_GET_PREAUTHORIZATIONS'
        return select.all(*args, **kwargs)

    def get_block_status(self, *args, **kwargs):
        kwargs['user_id'] = self.id
        select = SelectQuery(UserBlockStatus, *args, **kwargs)
        select.identifier = 'USERS_BLOCK_STATUS'
        return select.get("", *args, **kwargs)

    def get_regulatory(self, *args, **kwargs):
        kwargs['user_id'] = self.id
        select = SelectQuery(UserBlockStatus, *args, **kwargs)
        select.identifier = 'USERS_REGULATORY'
        return select.get("", *args, **kwargs)

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class NaturalUser(User):
    person_type = CharField(api_name='PersonType',
                            choices=constants.USER_TYPE_CHOICES,
                            default=constants.USER_TYPE_CHOICES.natural,
                            required=True)
    first_name = CharField(api_name='FirstName', required=True)
    last_name = CharField(api_name='LastName', required=True)
    address = AddressField(api_name='Address')
    birthday = DateField(api_name='Birthday')
    nationality = CharField(api_name='Nationality')
    country_of_residence = CharField(api_name='CountryOfResidence')
    occupation = CharField(api_name='Occupation')
    income_range = CharField(api_name='IncomeRange')
    proof_of_identity = CharField(api_name='ProofOfIdentity')
    proof_of_address = CharField(api_name='ProofOfAddress')
    capacity = CharField(api_name='Capacity', choices=constants.NATURAL_USER_CAPACITY_CHOICES)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users/natural'

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class LegalUser(User):
    person_type = CharField(api_name='PersonType',
                            choices=constants.USER_TYPE_CHOICES,
                            default=constants.USER_TYPE_CHOICES.legal,
                            required=True)
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
    legal_representative_birthday = DateField(api_name='LegalRepresentativeBirthday')
    legal_representative_nationality = CharField(api_name='LegalRepresentativeNationality')
    legal_representative_country_of_residence = CharField(api_name='LegalRepresentativeCountryOfResidence')
    legal_representative_proof_of_identity = CharField(api_name='LegalRepresentativeProofOfIdentity')
    statute = CharField(api_name='Statute')
    proof_of_registration = CharField(api_name='ProofOfRegistration')
    shareholder_declaration = CharField(api_name='ShareholderDeclaration')
    company_number = CharField(api_name='CompanyNumber')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        url = '/users/legal'

    def __str__(self):
        return '%s' % self.email


@python_2_unicode_compatible
class EMoney(BaseModel):
    user = ForeignKeyField(User, api_name='UserId', related_name='emoney')
    credited_emoney = MoneyField(api_name='CreditedEMoney')
    debited_emoney = MoneyField(api_name='DebitedEMoney')

    class Meta:
        verbose_name = 'emoney'
        url = {
            'ALL': '/users/%(user_id)s/emoney',
            'FOR_YEAR': '/users/%(user_id)s/emoney/%(year)s',
            'FOR_MONTH': '/users/%(user_id)s/emoney/%(year)s/%(month)s'
        }

    def __str__(self):
        return 'EMoney for user %s' % self.user_id


@python_2_unicode_compatible
class Wallet(BaseModel):
    owners = ManyToManyField(User, api_name='Owners', related_name='wallets', required=True)
    description = CharField(api_name='Description', required=True)
    currency = CharField(api_name='Currency', required=True)
    balance = MoneyField(api_name='Balance')
    creation_date = DateTimeField(api_name='CreationDate')

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
    creation_date = DateTimeField(api_name='CreationDate')
    credited_funds = MoneyField(api_name='CreditedFunds')
    status = CharField(api_name='Status',
                       choices=constants.STATUS_CHOICES,
                       default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')

    def get_refunds(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Refund, *args, **kwargs)
        select.identifier = 'TRANSFER_GET_REFUNDS'
        return select.all(*args, **kwargs)

    class Meta:
        verbose_name = 'transfer'
        verbose_name_plural = 'transfers'
        url = '/transfers'

    def __str__(self):
        return 'Transfer from wallet %s to wallet %s' % (self.debited_wallet_id, self.credited_wallet_id)


@python_2_unicode_compatible
class Card(BaseModel):
    creation_date = DateTimeField(api_name='CreationDate')
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
    fingerprint = CharField(api_name='Fingerprint')

    @classmethod
    def get_by_fingerprint(cls, fingerprint, *args, **kwargs):
        kwargs['fingerprint'] = fingerprint
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = 'CARDS_FOR_FINGERPRINT'
        return select.all(*args, **kwargs)

    def get_pre_authorizations(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(PreAuthorization, *args, **kwargs)
        select.identifier = 'CARD_PRE_AUTHORIZATIONS'
        return select.all(*args, **kwargs)

    def get_transactions(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Transaction, *args, **kwargs)
        select.identifier = 'CARD_GET_TRANSACTIONS'
        return select.all(*args, **kwargs)

    def validate(self, *args, **kwargs):
        kwargs['id'] = self.id
        insert = InsertQuery(self, **kwargs)
        insert.identifier = 'CARD_VALIDATE'
        return insert.execute()

    class Meta:
        verbose_name = 'card'
        verbose_name_plural = 'cards'
        url = {
            SelectQuery.identifier: '/cards',
            UpdateQuery.identifier: '/cards',
            'CARDS_FOR_FINGERPRINT': '/cards/fingerprints/%(fingerprint)s',
            'CARD_VALIDATE': '/cards/%(id)s/validate'}

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
    creation_date = DateTimeField(api_name='CreationDate')

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
    bank_reference = CharField(api_name='BankReference')

    scheme = CharField(api_name='Scheme', choices=constants.MANDATE_SCHEME_CHOICES, default=None)

    status = CharField(api_name='Status',
                       choices=constants.MANDATE_STATUS_CHOICES,
                       default=None)

    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')

    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    mandate_type = CharField(api_name='MandateType', choiced=constants.MANDATE_TYPE_CHOICES, default=None)

    creation_date = DateTimeField(api_name='CreationDate')

    def get_transactions(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Transaction, *args, **kwargs)
        select.identifier = 'MANDATE_GET_TRANSACTIONS'
        return select.all(*args, **kwargs)

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
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', related_name='credited_users')
    credited_funds = MoneyField(api_name='CreditedFunds')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    payment_type = CharField(api_name='PaymentType', choices=constants.PAYIN_PAYMENT_TYPE, default=None)
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)

    def get_refunds(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Refund, args, kwargs)
        select.identifier = 'PAYIN_GET_REFUNDS'
        return select.all(*args, **kwargs)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = '/payins'

    @classmethod
    def cast(cls, result):
        if cls.__name__ == "RecurringPayInCIT":
            return RecurringPayInCIT

        if cls.__name__ == "RecurringPayInMIT":
            return RecurringPayInMIT

        payment_type = result.get('PaymentType')
        execution_type = result.get('ExecutionType')

        types = {
            ("CARD", "DIRECT"): DirectPayIn,
            ("CARD", "WEB"): CardWebPayIn,
            ("DIRECT_DEBIT", "DIRECT"): DirectDebitDirectPayIn,
            ("DIRECT_DEBIT", "WEB"): DirectDebitWebPayIn,
            ("PREAUTHORIZED", "DIRECT"): PreAuthorizedPayIn,
            ("BANK_WIRE", "DIRECT"): BankWirePayIn,
            ("BANK_WIRE", "EXTERNAL_INSTRUCTION"): BankWirePayInExternalInstruction,
            ("APPLEPAY", "DIRECT"): ApplepayPayIn,
            ("GOOGLEPAY", "DIRECT"): GooglepayPayIn
        }

        return types.get((payment_type, execution_type), cls)


@python_2_unicode_compatible
class RecurringPayInRegistration(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    user = ForeignKeyField(User, api_name='CreditedUserId')
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    first_transaction_debited_funds = MoneyField(api_name='FirstTransactionDebitedFunds', required=True)
    first_transaction_fees = MoneyField(api_name='FirstTransactionFees', required=True)
    billing = BillingField(api_name='Billing', required=False)
    shipping = ShippingField(api_name='Shipping', required=False)
    end_date = DateField(api_name='EndDate')
    frequency = CharField(api_name='Frequency')
    fixed_next_amount = BooleanField(api_name='FixedNextAmount')
    fractioned_payment = BooleanField(api_name='FractionedPayment')
    migration = BooleanField(api_name='Migration')
    next_transaction_debited_funds = MoneyField(api_name='NextTransactionDebitedFunds')
    next_transaction_fees = MoneyField(api_name='NextTransactionFees')
    free_cycles = IntegerField(api_name='FreeCycles', required=False)
    cycle_number = IntegerField(api_name='CycleNumber')
    total_amount = MoneyField(api_name='TotalAmount')
    recurring_type = CharField(api_name='RecurringType')
    current_state = CurrentStateField(api_name='CurrentState')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)

    def get_read_only_properties(self):
        read_only = ["Id", "FreeCycles", "CycleNumber", "TotalAmount", "RecurringType", "Status", "CurrentState"]
        return read_only

    class Meta:
        verbose_name = 'recurring_registration_payin'
        verbose_name_plural = 'recurring_registration_payins'
        url = {
            InsertQuery.identifier: '/recurringpayinregistrations',
            SelectQuery.identifier: '/recurringpayinregistrations',
            UpdateQuery.identifier: '/recurringpayinregistrations'
        }


@python_2_unicode_compatible
class RecurringPayInCIT(PayIn):
    recurring_payin_registration_id = CharField(api_name='RecurringPayinRegistrationId', required=True)
    browser_info = BrowserInfoField(api_name='BrowserInfo', required=True)
    ip_address = CharField(api_name='IpAddress', required=True)
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')
    author = ForeignKeyField(User, api_name='AuthorId')
    billing = BillingField(api_name='Billing')
    card = ForeignKeyField(Card, api_name='CardId')
    creation_date = DateTimeField(api_name='CreationDate')
    culture = CharField(api_name='Culture')
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    shipping = ShippingField(api_name='Shipping')

    def get_read_only_properties(self):
        read_only = ["AuthorId", "Applied3DSVersion", "CardId", "CreationDate", "Culture", "SecureModeNeeded"
            , "SecureMode", "SecureModeRedirectURL", "SecurityInfo"]
        return read_only

    class Meta:
        verbose_name = 'recurring_payin'
        verbose_name_plural = 'recurring_payins'
        url = {
            InsertQuery.identifier: '/payins/recurring/card/direct',
            SelectQuery.identifier: '/payins'
        }


@python_2_unicode_compatible
class RecurringPayInMIT(PayIn):
    recurring_payin_registration_id = CharField(api_name='RecurringPayinRegistrationId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds')
    fees = MoneyField(api_name='Fees')
    statement_descriptor = CharField(api_name='StatementDescriptor')
    browser_info = BrowserInfoField(api_name='BrowserInfo')
    ip_address = CharField(api_name='IpAddress')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')
    author = ForeignKeyField(User, api_name='AuthorId')
    billing = BillingField(api_name='Billing')
    card = ForeignKeyField(Card, api_name='CardId')
    creation_date = DateTimeField(api_name='CreationDate')
    culture = CharField(api_name='Culture')
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    shipping = ShippingField(api_name='Shipping')

    def get_read_only_properties(self):
        read_only = ["AuthorId", "Applied3DSVersion", "CardId", "CreationDate", "Culture", "SecureModeNeeded"
            , "SecureMode", "SecureModeRedirectURL", "SecurityInfo", "DebitedFunds", "Fees",
                     "StatementDescriptor", "BrowserInfo", "IpAddress", "SecureModeReturnURL"]
        return read_only

    class Meta:
        verbose_name = 'recurring_payin'
        verbose_name_plural = 'recurring_payins'
        url = {
            InsertQuery.identifier: '/payins/recurring/card/direct',
            SelectQuery.identifier: '/payins'
        }


@python_2_unicode_compatible
class DirectPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    secure_mode_redirect_url = CharField(api_name='SecureModeRedirectURL')
    secure_mode_return_url = CharField(api_name='SecureModeReturnURL', required=True)
    card = ForeignKeyField(Card, api_name='CardId', required=True)
    secure_mode_needed = BooleanField(api_name='SecureModeNeeded')
    secure_mode = CharField(api_name='SecureMode',
                            choices=constants.SECURE_MODE_CHOICES,
                            default=constants.SECURE_MODE_CHOICES.default)
    creation_date = DateTimeField(api_name='CreationDate')
    statement_descriptor = CharField(api_name='StatementDescriptor')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    billing = BillingField(api_name='Billing')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    culture = CharField(api_name='Culture')
    ip_address = CharField(api_name='IpAddress')
    browser_info = BrowserInfoField(api_name='BrowserInfo')
    shipping = ShippingField(api_name='Shipping')
    requested_3ds_version = CharField(api_name='Requested3DSVersion')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')

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


@python_2_unicode_compatible
class BankWirePayInExternalInstruction(PayIn):
    banking_alias_id = CharField(api_name='BankingAliasId')
    wire_reference = CharField(api_name='WireReference')
    debited_bank_account = DebitedBankAccountField(api_name='DebitedBankAccount')

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            SelectQuery.identifier: '/payins'
        }

    def __str__(self):
        return 'Bank Wire Payin External Instruction'


@python_2_unicode_compatible
class PayPalPayIn(PayIn):
    tag = CharField(api_name='Tag')
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    return_url = CharField(api_name='ReturnURL', required=False)
    redirect_url = CharField(api_name='RedirectURL', required=False)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId', required=True)
    shipping_address = ShippingAddressField(api_name='ShippingAddress')
    buyer_account_email = CharField(api_name="PaypalBuyerAccountEmail", required=False)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/paypal/web',
            SelectQuery.identifier: '/payins'
        }


@python_2_unicode_compatible
class PayconiqPayIn(PayIn):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    return_url = CharField(api_name='ReturnURL', required=False)
    redirect_url = CharField(api_name='RedirectURL', required=False)
    creation_date = DateField(api_name='CreationDate', required=False)
    expiration_date = CharField(api_name='ExpirationDate', required=False)
    deep_link_url = CharField(api_name='DeepLinkURL', required=False)

    class Meta:
        verbose_name = 'payin'
        verbose_name_plural = 'payins'
        url = {
            InsertQuery.identifier: '/payins/payconiq/web',
            SelectQuery.identifier: '/payins'
        }


class ApplepayPayIn(PayIn):
    tag = CharField(api_name='Applepay PayIn')
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    payment_data = ApplepayPaymentDataField(api_name='PaymentData', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')

    class Meta:
        verbose_name = 'applepay_payin'
        verbose_name_plural = 'applepay_payins'
        url = {
            InsertQuery.identifier: '/payins/applepay/direct'
        }


class GooglepayPayIn(PayIn):
    tag = CharField(api_name='Googlepay PayIn')
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    payment_type = GooglepayPaymentDataField(api_name='PaymentData', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    fees = MoneyField(api_name='Fees', required=True)
    statement_descriptor = CharField(api_name='StatementDescriptor')

    class Meta:
        verbose_name = 'googlepay_payin'
        verbose_name_plural = 'googlepay_payins'
        url = {
            InsertQuery.identifier: '/payins/googlepay/direct'
        }


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
    shipping = ShippingField(api_name='Shipping')

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
    charge_date = CharField(api_name='ChargeDate')
    culture = CharField(api_name='Culture')

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
    remaining_funds = MoneyField(api_name='RemainingFunds')
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
    expiration_date = DateTimeField(api_name='ExpirationDate')
    payin = ForeignKeyField(PayIn, api_name='PayInId')
    billing = BillingField(api_name='Billing')
    security_info = SecurityInfoField(api_name='SecurityInfo')
    multi_capture = BooleanField(api_name='MultiCapture')
    ip_address = CharField(api_name='IpAddress')
    browser_info = BrowserInfoField(api_name='BrowserInfo')
    shipping = ShippingField(api_name='Shipping')
    requested_3ds_version = CharField(api_name='Requested3DSVersion')
    applied_3ds_version = CharField(api_name='Applied3DSVersion')

    def get_transactions(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Transaction, *args, **kwargs)
        select.identifier = 'PRE_AUTHORIZATION_TRANSACTIONS'
        return select.all(*args, **kwargs)

    class Meta:
        verbose_name = 'preauthorization'
        verbose_name_plural = 'preauthorizations'
        url = {
            InsertQuery.identifier: '/preauthorizations/card/direct',
            UpdateQuery.identifier: '/preauthorizations',
            SelectQuery.identifier: '/preauthorizations',
            'USER_GET_PREAUTHORIZATIONS': '/users/%(id)s/preauthorizations',
            'CARD_PRE_AUTHORIZATIONS': '/cards/%(id)s/preauthorizations'
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
    culture = CharField(api_name='Culture')

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
    creation_date = DateTimeField(api_name='CreationDate')
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
    active = BooleanField(api_name='Active', default=True)

    def get_transactions(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Transaction, *args, **kwargs)
        select.identifier = 'BANK_ACCOUNT_GET_TRANSACTIONS'
        return select.all(*args, **kwargs)

    def create_client_bank_account(self, **kwargs):
        insert = InsertQuery(self, **kwargs)
        insert.identifier = 'CLIENT_CREATE_BANK_ACCOUNT'
        insert.insert_query = self.get_field_dict()
        return insert.execute()

    class Meta:
        verbose_name = 'bankaccount'
        verbose_name_plural = 'bankaccounts'
        url = {
            InsertQuery.identifier: '/users/%(user_id)s/bankaccounts/%(type)s',
            SelectQuery.identifier: '/users/%(user_id)s/bankaccounts',
            UpdateQuery.identifier: '/users/%(user_id)s/bankaccounts',
            'CLIENT_CREATE_BANK_ACCOUNT': '/clients/bankaccounts/iban'
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
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    payment_type = CharField(api_name='PaymentType', choices=constants.PAYOUT_PAYMENT_TYPE, default=None)
    execution_type = CharField(api_name='ExecutionType', choices=constants.EXECUTION_TYPE_CHOICES, default=None)
    bank_wire_ref = CharField(api_name='BankWireRef')
    payout_mode_requested = CharField(api_name='PayoutModeRequested')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId')
    creation_date = DateTimeField(api_name='CreationDate')
    mode_requested = CharField(api_name='ModeRequested')
    mode_applied = CharField(api_name='ModeApplied')
    fallback_reason = FallbackReasonField(api_name='FallbackReason')

    def get_refunds(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Refund, *args, **kwargs)
        select.identifier = 'PAYOUT_GET_REFUNDS'
        return select.all(*args, **kwargs)

    def create_client_payout(self, **kwargs):
        insert = InsertQuery(self, **kwargs)
        insert.identifier = 'CLIENT_CREATE_PAYOUT'
        insert.insert_query = self.get_field_dict()
        return insert.execute()

    @classmethod
    def get_bankwire(cls, payout_id, **kwargs):
        kwargs['id'] = payout_id
        args = '',
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = 'PAYOUT_BANKWIRE_GET'
        return select.get(*args, **kwargs)

    class Meta:
        verbose_name = 'payout'
        verbose_name_plural = 'payouts'
        url = {
            InsertQuery.identifier: '/payouts/bankwire',
            SelectQuery.identifier: '/payouts',
            'PAYOUT_BANKWIRE_GET': '/payouts/bankwire/%(id)s',
            'CLIENT_CREATE_PAYOUT': '/clients/payouts'
        }

    def __str__(self):
        return 'PayOut request from user %s' % self.author_id


@python_2_unicode_compatible
class PayOutEligibilityResult(BaseModel):
    instant_payout = InstantPayoutField(api_name='InstantPayout')


@python_2_unicode_compatible
class PayOutEligibility(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    debited_funds = MoneyField(api_name='DebitedFunds', required=True)
    bank_account = ForeignKeyField(BankAccount, api_name='BankAccountId', required=True)
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId', required=True)
    fees = MoneyField(api_name='Fees')
    payout_mode_requested = CharField(api_name='PayoutModeRequested')
    bank_wire_ref = CharField(api_name='BankWireRef')

    def check_eligibility(self, **kwargs):
        insert = InsertQuery(self, **kwargs)
        insert.identifier = 'PAYOUT_CHECK_ELIGIBILITY'
        insert.insert_query = self.get_field_dict()
        return insert.execute(model_klass=PayOutEligibilityResult)

    class Meta:
        verbose_name = 'payout_eligibility'
        verbose_name_plural = 'payouts_eligibility'
        url = {
            'PAYOUT_CHECK_ELIGIBILITY': '/payouts/reachability'
        }


class Refund(BaseModel):
    author = ForeignKeyField(User, api_name='AuthorId', required=True)
    credited_user = ForeignKeyField(User, api_name='CreditedUserId', related_name='credited_users')
    debited_funds = MoneyField(api_name='DebitedFunds')
    credited_funds = MoneyField(api_name='CreditedFunds')
    fees = MoneyField(api_name='Fees')
    status = CharField(api_name='Status', choices=constants.STATUS_CHOICES, default=None)
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    execution_date = DateTimeField(api_name='ExecutionDate')
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
        url = {
            SelectQuery.identifier: '/refunds',
            InsertQuery.identifier: '/refunds',
            UpdateQuery.identifier: '/refunds',
            'REPUDIATION_GET_REFUNDS': '/repudiations/%(id)s/refunds',
            'TRANSFER_GET_REFUNDS': '/transfers/%(id)s/refunds',
            'PAYOUT_GET_REFUNDS': '/payouts/%(id)s/refunds',
            'PAYIN_GET_REFUNDS': '/payins/%(id)s/refunds'
        }


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
    processedDate = DateTimeField(api_name='ProcessedDate')
    flags = ListField(api_name='Flags')

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
    execution_date = DateTimeField(api_name='ExecutionDate')
    type = CharField(api_name='Type', choices=constants.TRANSACTION_TYPE_CHOICES, default=None)
    nature = CharField(api_name='Nature', choices=constants.NATURE_CHOICES, default=None)
    credited_wallet = ForeignKeyField(Wallet, api_name='CreditedWalletId')
    debited_wallet = ForeignKeyField(Wallet, api_name='DebitedWalletId')
    wallet = ForeignKeyField(Wallet, related_name='transactions')
    creation_date = DateTimeField(api_name='CreationDate')

    class Meta:
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
        url = {
            SelectQuery.identifier: '/users/%(user_id)s/transactions',
            InsertQuery.identifier: '/users/%(user_id)s/transactions',
            UpdateQuery.identifier: '/users/%(user_id)s/transactions',
            'MANDATE_GET_TRANSACTIONS': '/mandates/%(id)s/transactions',
            'CARD_GET_TRANSACTIONS': '/cards/%(id)s/transactions',
            'BANK_ACCOUNT_GET_TRANSACTIONS': '/bankaccounts/%(id)s/transactions',
            'PRE_AUTHORIZATION_TRANSACTIONS': '/preauthorizations/%(id)s/transactions'
        }

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
        fund_type_url = {
            'CREDIT': 'SELECT_BY_CREDIT',
            'FEES': 'SELECT_BY_FEES',
            'DEFAULT': 'SELECT_BY_DEFAULT'
        }
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
            'RE_SUBMIT_DISPUTE': '/disputes/%(id)s/submit/',
            'PENDING_SETTLEMENT': '/disputes/pending-settlement'
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

    @classmethod
    def get_pending_settlement(cls, *args, **kwargs):
        select = SelectQuery(cls, *args, **kwargs)
        select.identifier = 'PENDING_SETTLEMENT'
        return select.all(*args, **kwargs)


class DisputeDocument(BaseModel):
    dispute = ForeignKeyField(Dispute, api_name='DisputeId', related_name='documents', required=True)
    status = CharField(api_name='Status', choices=constants.DOCUMENTS_STATUS_CHOICES, default=None)
    type = CharField(api_name='Type', choices=constants.DISPUTE_DOCUMENT_TYPE_CHOICES, defalut=None)
    refused_reason_message = CharField(api_name='RefusedReasonMessage')
    refused_reason_type = CharField(api_name='RefusedReasonType', choices=constants.REFUSED_REASON_TYPE_CHOICES,
                                    default=None)
    creation_date = DateTimeField(api_name='CreationDate')
    processed_date = DateTimeField(api_name='ProcessedDate')

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


class DocumentConsult(BaseModel):
    url = CharField(api_name='Url')
    expiration_date = DateField(api_name='ExpirationDate')

    class Meta:
        verbose_name = 'consult_page'
        verbose_name_plural = 'consult_pages'
        url = {
            'DISPUTE_CONSULT': '/dispute-documents/%(id)s/consult',
            'KYC_CONSULT': '/KYC/documents/%(id)s/consult'
        }

    @classmethod
    def _get_document_consult(cls, id, identifier, handler=None):
        query = ActionQuery(cls, id, identifier, 'POST')
        return query.execute(handler)

    @classmethod
    def get_kyc_document_consult(cls, KYCDocId, handler=None):
        return DocumentConsult._get_document_consult(KYCDocId, 'KYC_CONSULT', handler)

    @classmethod
    def get_dispute_document_consult(cls, disputeDocId, handler=None):
        return DocumentConsult._get_document_consult(disputeDocId, 'DISPUTE_CONSULT', handler)


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
    execution_date = DateTimeField(api_name='ExecutionDate')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')

    creation_date = DateTimeField(api_name='CreationDate')

    def get_refunds(self, *args, **kwargs):
        kwargs['id'] = self.id
        select = SelectQuery(Refund, *args, **kwargs)
        select.identifier = 'REPUDIATION_GET_REFUNDS'
        return select.all(*args, **kwargs)

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
    report_type = CharField(api_name='ReportType', choices=constants.REPORT_TYPE, default='transactions',
                            related_name='report_type')
    sort = CharField(api_name='Sort')
    preview = BooleanField(api_name='Preview')
    columns = ListField(api_name='Columns')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        url = {
            SelectQuery.identifier: '/reports/',
            InsertQuery.identifier: '/reports/%(report_type)s/'
        }


class ReportTransactions(BaseModel):
    creation_date = CharField(api_name='CreationDate')
    report_date = CharField(api_name='ReportDate')
    download_url = CharField(api_name='DownloadURL')
    callback_url = CharField(api_name='CallbackURL')
    download_format = CharField(api_name='DownloadFormat', choices=constants.DOWNLOAD_FORMAT, default='CSV')
    report_type = CharField(api_name='ReportType', choices=constants.REPORT_TYPE, default='transactions',
                            related_name='report_type')
    sort = CharField(api_name='Sort')
    preview = BooleanField(api_name='Preview')
    columns = ListField(api_name='Columns')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    filters = ReportTransactionsFiltersField(api_name='Filters')

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        url = {
            SelectQuery.identifier: '/reports/',
            InsertQuery.identifier: '/reports/transactions/'
        }


class ReportWallets(BaseModel):
    creation_date = CharField(api_name='CreationDate')
    report_date = CharField(api_name='ReportDate')
    download_url = CharField(api_name='DownloadURL')
    callback_url = CharField(api_name='CallbackURL')
    download_format = CharField(api_name='DownloadFormat', choices=constants.DOWNLOAD_FORMAT, default='CSV')
    report_type = CharField(api_name='ReportType', choices=constants.REPORT_TYPE, default='transactions',
                            related_name='report_type')
    sort = CharField(api_name='Sort')
    preview = BooleanField(api_name='Preview')
    columns = ListField(api_name='Columns')
    result_code = CharField(api_name='ResultCode')
    result_message = CharField(api_name='ResultMessage')
    filters = ReportWalletsFiltersField(api_name='Filters')

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'
        url = {
            SelectQuery.identifier: '/reports/',
            InsertQuery.identifier: '/reports/wallets/'
        }


class BankingAlias(BaseModel):
    tag = CharField(api_name='Tag')
    credited_user = ForeignKeyField(User, api_name='CreditedUserId')
    wallet = ForeignKeyField(Wallet, api_name='WalletId', related_name='wallet_id')
    type = CharField(api_name='Type')
    owner_name = CharField(api_name='OwnerName')
    active = BooleanField(api_name='Active')

    class Meta:
        verbose_name = 'bankingalias'
        verbose_name_plural = 'bankingaliases'
        url = '/bankingaliases'
        url = {
            InsertQuery.identifier: '/bankingaliases/',
            SelectQuery.identifier: '/bankingaliases/%(id)s',
            UpdateQuery.identifier: '/bankingaliases/%(id)s',
            'SELECT_ALL_BANKING_ALIASES': '/wallets/%(wallet_id)s/bankingaliases'
        }

    @classmethod
    def cast(cls, result):
        if 'Type' in result:
            if result['Type'] == 'IBAN':
                return BankingAliasIBAN
            elif result['Type'] == 'OTHER':
                return BankingAliasOther
            else:
                return BankingAlias

    def __str__(self):
        return '%s banking alias account of user %s' % (self.type, self.credited_user)

    def all(self, *args, **kwargs):
        kwargs['wallet_id'] = self.wallet_id
        select = SelectQuery(self.__class__, *args, **kwargs)
        select.identifier = 'SELECT_ALL_BANKING_ALIASES'
        return select.all(*args, **kwargs)


class BankingAliasIBAN(BankingAlias):
    type = CharField(api_name='Type', default='IBAN', required=True)
    iban = CharField(api_name='IBAN')
    bic = CharField(api_name='BIC')
    country = CharField(api_name='Country', required=True)

    class Meta:
        verbose_name = 'bankingalias'
        verbose_name_plural = 'bankingaliases'
        url = {
            InsertQuery.identifier: '/wallets/%(wallet_id)s/bankingaliases/iban',
            SelectQuery.identifier: '/bankingaliases/%(id)s',
            UpdateQuery.identifier: '/bankingaliases/%(id)s'
        }


class BankingAliasOther(BankingAlias):
    type = CharField(api_name='Type', default='OTHER', required='True')
    account_number = CharField(api_name='AccountNumber')
    bic = CharField(api_name='BIC')
    country = CharField(api_name='Country', required=True)

    class Meta:
        verbose_name = 'bankingalias'
        verbose_name_plural = 'bankingaliases'
        url = {
            InsertQuery.identifier: '/wallets/%(wallet_id)s/bankingaliases/accountNumber',
            SelectQuery.identifier: '/bankingaliases/%(id)s',
            UpdateQuery.identifier: '/bankingaliases/%(id)s'
        }


class UboDeclaration(BaseModel):
    creation_date = DateTimeField(api_name='CreationDate')
    processed_date = DateTimeField(api_name='ProcessedDate')
    reason = CharField(api_name='Reason')
    message = CharField(api_name='Message')
    status = CharField(api_name='Status', choices=constants.UBO_DECLARATION_STATUS_CHOICES, default=None)
    ubos = ListField(api_name='Ubos')
    user = ForeignKeyField(User)

    class Meta:
        verbose_name = 'ubodeclaration'
        verbose_name_plural = 'ubodeclarations'

        # For Update as well as Select, 'ubo_declaration_id' is provided by the 'reference' param of the update method
        url = {
            InsertQuery.identifier: '/users/%(user_id)s/kyc/ubodeclarations',
            UpdateQuery.identifier: '/users/%(user_id)s/kyc/ubodeclarations',
            SelectQuery.identifier: '/users/%(user_id)s/kyc/ubodeclarations'
        }

    def create(self, **kwargs):
        insert = InsertQuery(self, **kwargs)
        return insert.execute()

    def get_read_only_properties(self):
        read_only = ["ProcessedDate", "Reason", "Message"]
        return read_only

    def get_sub_objects(self, sub_objects=None):
        sub_objects['Ubos'] = Ubo
        return sub_objects


class Ubo(BaseModel):
    first_name = CharField(api_name='FirstName', required=True)
    last_name = CharField(api_name='LastName', required=True)
    address = AddressField(api_name='Address', required=True)
    nationality = CharField(api_name='Nationality', required=True)
    birthday = DateField(api_name='Birthday', required=True)
    birthplace = BirthplaceField(api_name='Birthplace', required=True)
    user = ForeignKeyField(User)
    ubo_declaration = ForeignKeyField(UboDeclaration)
    isActive = BooleanField(api_name='IsActive')

    class Meta:
        verbose_name = 'ubo'
        verbose_name_plural = 'ubos'

        # For Update, 'ubo_id' is provided by the 'reference' param of the update method
        url = {
            InsertQuery.identifier: '/users/%(user_id)s/kyc/ubodeclarations/%(ubo_declaration_id)s/ubos',
            UpdateQuery.identifier: '/users/%(user_id)s/kyc/ubodeclarations/%(ubo_declaration_id)s/ubos',
            SelectQuery.identifier: '/users/%(user_id)s/kyc/ubodeclarations/%(ubo_declaration_id)s/ubos/'
        }

    def get_sub_objects(self, sub_objects=None):
        sub_objects['Address'] = Address
        sub_objects['Birthplace'] = Birthplace
        return sub_objects


class UserBlockStatus(BaseModel):
    scope_blocked = ScopeBlockedField(api_name='ScopeBlocked', required=True)
    action_code = CharField(api_name='ActionCode', required=True)

    class Meta:
        verbose_name = 'userblockstatus'
        verbose_name_plural = 'userblockstatuses'

        url = {
            'USERS_BLOCK_STATUS': '/users/%(user_id)s/blockStatus',
            'USERS_REGULATORY': '/users/%(user_id)s/Regulatory'
        }


class CountryAuthorization(BaseModel):
    country_code = CharField(api_name='CountryCode')
    country_name = CharField(api_name='CountryName')
    authorization = CountryAuthorizationDataField(api_name='Authorization')
    last_update = DateTimeField(api_name='LastUpdate')

    class Meta:
        verbose_name = 'country_authorization'
        verbose_name_plural = 'country_authorizations'
        url = {
            'COUNTRY_AUTHORIZATIONS': 'countries/%(id)s/authorizations',
            'ALL_COUNTRIES_AUTHORIZATIONS': 'countries/authorizations'
        }

    @classmethod
    def get_country_authorizations(cls, country_code, **kwargs):
        kwargs['id'] = country_code
        args = '',
        select = SelectQuery(CountryAuthorization, *args, **kwargs)
        select.identifier = 'COUNTRY_AUTHORIZATIONS'
        return select.get(without_client_id=True, *args, **kwargs)

    @classmethod
    def get_all_countries_authorizations(cls, *args, **kwargs):
        select = SelectQuery(CountryAuthorization, *args, **kwargs)
        select.identifier = 'ALL_COUNTRIES_AUTHORIZATIONS'
        return select.all(without_client_id=True, *args, **kwargs)
