import datetime
import json
import re
import sys
import time

import six

from .utils import timestamp_from_datetime, timestamp_from_date, Money, DebitedBankAccount, Address, ShippingAddress, \
    Reason, ReportTransactionsFilters, ReportWalletsFilters, \
    PlatformCategorization, Billing, SecurityInfo, Birthplace, ApplepayPaymentData, GooglepayPaymentData, \
    ScopeBlocked, BrowserInfo, Shipping, CurrentState, FallbackReason, InstantPayout, CountryAuthorizationData


class FieldDescriptor(object):
    def __init__(self, field):
        self.field = field
        self.att_name = self.field.name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return instance._data.get(self.att_name)

        return self.field

    def __set__(self, instance, value):
        instance._data[self.att_name] = value


class Field(object):
    default = None
    _field_counter = 0
    _order = 0

    def get_attributes(self):
        return {}

    def __init__(self, null=False, api_name=None,
                 help_text=None, api_value_callback=None,
                 choices=None, default=None,
                 python_value_callback=None, *args, **kwargs):
        self.null = null
        self.attributes = self.get_attributes()
        self.default = kwargs.get('default', None)
        self.api_name = api_name
        self.api_value_callback = api_value_callback
        self.python_value_callback = python_value_callback
        self.help_text = help_text
        self.required = kwargs.get('required', False)
        self.choices = choices
        self.default = default

        self.attributes.update(kwargs)

        self._order = Field._field_counter

    def add_to_class(self, klass, name):
        self.name = name
        self.model = klass
        self.api_name = self.api_name or re.sub('_+', ' ', name).title()

        klass._meta.fields[self.name] = self

        setattr(klass, name, FieldDescriptor(self))

    def null_wrapper(self, value, default=None):
        if (self.null and not value) or not default:
            return value
        return value or default

    def api_value(self, value):
        if self.api_value_callback:
            value = self.api_value_callback(value)
        return value

    def python_value(self, value):
        if self.python_value_callback:
            value = self.python_value_callback(value)
        return value


class CharField(Field):
    def python_value(self, value):
        if self.python_value_callback:
            value = self.python_value_callback(value)

        return value

    def api_value(self, value):
        if sys.version_info > (3, 0) and isinstance(value, six.binary_type):
            return value.decode('utf-8')

        return value


class DateTimeField(Field):
    def python_value(self, value):
        value = super(DateTimeField, self).python_value(value)

        if isinstance(value, six.string_types):
            value = value.rsplit('.', 1)[0]
            value = datetime.datetime(*time.strptime(value, '%Y-%m-%d %H:%M:%S')[:6])

        if isinstance(value, six.integer_types):
            value = datetime.datetime.utcfromtimestamp(value)

        return value

    def api_value(self, value):
        value = super(DateTimeField, self).api_value(value)

        if isinstance(value, datetime.datetime):
            value = timestamp_from_datetime(value)

        return value


class DateField(Field):
    def python_value(self, value):
        value = super(DateField, self).python_value(value)

        if isinstance(value, six.string_types):
            value = datetime.datetime.strptime(value, '%Y-%m-%d').date()

        if isinstance(value, six.integer_types):
            value = datetime.datetime.utcfromtimestamp(value).date()

        return value

    def api_value(self, value):
        value = super(DateField, self).api_value(value)

        if isinstance(value, datetime.date):
            value = timestamp_from_date(value)

        return value


class IntegerField(Field):
    def api_value(self, value):
        return self.null_wrapper(super(IntegerField, self).api_value(value), 0)

    def python_value(self, value):
        if value is not None:
            return int(super(IntegerField, self).python_value(value))


class FloatField(Field):
    def api_value(self, value):
        return self.null_wrapper(super(FloatField, self).api_value(value), 0.0)

    def python_value(self, value):
        if value is not None:
            return float(super(FloatField, self).python_value(value))


class DictField(Field):
    def api_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None and isinstance(value, str):
            return json.loads(value)
        elif isinstance(value, dict):
            return value


class PrimaryKeyField(CharField):
    pass


class ListField(Field):
    pass


class BooleanField(IntegerField):
    def api_value(self, value):
        value = super(BooleanField, self).api_value(value)

        if value:
            return 1
        return 0

    def python_value(self, value):
        value = super(BooleanField, self).python_value(value)

        return bool(value)


class EmailField(CharField):
    pass


class MoneyField(Field):
    def python_value(self, value):
        if value is not None:
            return Money(currency=value['Currency'], amount=value['Amount'])

        return value

    def api_value(self, value):
        value = super(MoneyField, self).api_value(value)

        if isinstance(value, Money):
            value = {
                'Currency': value.currency,
                'Amount': int(value.amount)
            }

        return value


class FallbackReasonField(Field):
    def python_value(self, value):
        if value is not None:
            return FallbackReason(code=value['Code'], message=value['Message'])

        return value

    def api_value(self, value):
        value = super(FallbackReasonField, self).api_value(value)

        if isinstance(value, FallbackReason):
            value = {
                'Code': value.code,
                'Message': value.message
            }

        return value


class InstantPayoutField(Field):
    def python_value(self, value):
        if value is not None:
            return InstantPayout(is_reachable=value['IsReachable'], unreachable_reason=value['UnreachableReason'])

        return value

    def api_value(self, value):
        value = super(InstantPayoutField, self).api_value(value)

        if isinstance(value, InstantPayoutField):
            value = {
                'IsReachable': value.is_reachable,
                'UnreachableReason': value.unreachable_reason
            }

        return value


class PlatformCategorizationField(Field):
    def python_value(self, value):
        if value is not None:
            return PlatformCategorization(business_type=value['BusinessType'], sector=value['Sector'])

        return value

    def api_value(self, value):
        value = super(PlatformCategorizationField, self).api_value(value)

        if isinstance(value, PlatformCategorization):
            value = {
                'BusinessType': value.business_type,
                'Sector': value.sector
            }

        return value


class BillingField(Field):
    def python_value(self, value):
        if value is not None:
            return Billing(first_name=value['FirstName'], last_name=value['LastName'], address=value['Address'])
        return value

    def api_value(self, value):
        value = super(BillingField, self).api_value(value)

        if isinstance(value, Billing):
            value = {
                'FirstName': value.first_name,
                'LastName': value.last_name,
                'Address': value.address
            }

        return value


class SecurityInfoField(Field):
    def python_value(self, value):
        if value is not None:
            return SecurityInfo(avs_result=value['AVSResult'])

        return value

    def api_value(self, value):
        value = super(SecurityInfoField, self).api_value(value)

        if isinstance(value, SecurityInfo):
            value = {
                'AVSResult': value.avs_result
            }

        return value


class DebitedBankAccountField(Field):
    def python_value(self, value):
        if value is not None:
            return DebitedBankAccount(owner_name=value['OwnerName'], account_number=value['AccountNumber'],
                                      iban=value['IBAN'], bic=value['BIC'], type=value['Type'],
                                      country=value['Country'])

        return value

    def api_value(self, value):
        value = super(DebitedBankAccountField, self).api_value(value)

        if isinstance(value, DebitedBankAccount):
            value = {
                'OwnerName': value.owner_name,
                'AccountNumber': value.account_number,
                'IBAN': value.iban,
                'BIC': value.bic,
                'Type': value.type,
                'Country': value.country
            }

        return value


class ReportTransactionsFiltersField(Field):
    def python_value(self, value):
        if value is not None:
            local_min_debited_funds_amount = ''
            local_max_debited_funds_amount = ''

            if 'MinDebitedFundsAmount' in value and value['MinDebitedFundsAmount']:
                local_min_debited_funds_amount = int(value['MinDebitedFundsAmount'])

            if 'MaxDebitedFundsAmount' in value and value['MaxDebitedFundsAmount']:
                local_max_debited_funds_amount = int(value['MaxDebitedFundsAmount'])

            author_id = None
            wallet_id = None
            if 'AuthorId' in value:
                author_id = value['AuthorId']
            if 'WalletId' in value:
                wallet_id = value['WalletId']

            return ReportTransactionsFilters(before_date=value['BeforeDate'],
                                             after_date=value['AfterDate'],
                                             transaction_type=value['Type'],
                                             status=value['Status'],
                                             nature=value['Nature'],
                                             min_debited_funds_amount=local_min_debited_funds_amount,
                                             min_debited_funds_currency=value['MinDebitedFundsCurrency'],
                                             max_debited_funds_amount=local_max_debited_funds_amount,
                                             max_debited_funds_currency=value['MaxDebitedFundsCurrency'],
                                             author_id=author_id, wallet_id=wallet_id
                                             )
        return value

    def api_value(self, value):
        value = super(ReportTransactionsFiltersField, self).api_value(value)

        if isinstance(value, ReportTransactionsFilters):

            if isinstance(value.before_date, datetime.datetime):
                local_before_date = timestamp_from_datetime(value.before_date)
            else:
                local_before_date = value.before_date

            if isinstance(value.after_date, datetime.datetime):
                local_after_date = timestamp_from_datetime(value.after_date)
            else:
                local_after_date = value.after_date

            value = {
                'BeforeDate': local_before_date,
                'AfterDate': local_after_date,
                'Type': value.transaction_type,
                'Status': value.status,
                'Nature': value.nature,
                'MinDebitedFundsAmount': value.min_debited_funds_amount,
                'MinDebitedFundsCurrency': value.min_debited_funds_currency,
                'MaxDebitedFundsAmount': value.max_debited_funds_amount,
                'MaxDebitedFundsCurrency': value.max_debited_funds_currency,
                'AuthorId': value.author_id,
                'WalletId': value.wallet_id,
            }

        return value


class ReportWalletsFiltersField(Field):
    def python_value(self, value):
        if value is not None:

            local_min_balance_amount = ''
            local_max_balance_amount = ''

            if 'MinBalanceAmount' in value and value['MinBalanceAmount']:
                local_min_balance_amount = int(value['MinBalanceAmount'])

            if 'MaxBalanceAmount' in value and value['MaxBalanceAmount']:
                local_max_balance_amount = int(value['MaxBalanceAmount'])

            return ReportWalletsFilters(before_date=value['BeforeDate'],
                                        after_date=value['AfterDate'],
                                        owner_id=value['OwnerId'],
                                        currency=value['Currency'],
                                        min_balance_amount=local_min_balance_amount,
                                        min_balance_currency=value['MinBalanceCurrency'],
                                        max_balance_amount=local_max_balance_amount,
                                        max_balance_currency=value['MaxBalanceCurrency']
                                        )

        return value

    def api_value(self, value):
        value = super(ReportWalletsFiltersField, self).api_value(value)

        if isinstance(value, ReportWalletsFilters):

            if isinstance(value.before_date, datetime.datetime):
                local_before_date = timestamp_from_datetime(value.before_date)
            else:
                local_before_date = value.before_date

            if isinstance(value.after_date, datetime.datetime):
                local_after_date = timestamp_from_datetime(value.after_date)
            else:
                local_after_date = value.after_date

            value = {
                'BeforeDate': local_before_date,
                'AfterDate': local_after_date,
                'OwnerId': value.owner_id,
                'Currency': value.currency,
                'MinBalanceAmount': value.min_balance_amount,
                'MinBalanceCurrency': value.min_balance_currency,
                'MaxBalanceAmount': value.max_balance_amount,
                'MaxBalanceCurrency': value.max_balance_currency,
            }

        return value


class DisputeReasonField(Field):
    def python_value(self, value):
        if value is not None:
            return Reason(type=value['DisputeReasonType'], message=value['DisputeReasonMessage'])

        return value

    def api_value(self, value):
        value = super(DisputeReasonField, self).api_value(value)

        if isinstance(value, Reason):
            value = {
                'DisputeReasonType': value.type,
                'DisputeReasonMessage': str(value.message)
            }

        return value


class RefundReasonField(Field):
    def python_value(self, value):
        if value is not None:
            return Reason(
                type=value.get('RefundReasonType'),
                message=value.get('RefundReasonMessage')
            )

        return value

    def api_value(self, value):
        value = super(RefundReasonField, self).api_value(value)

        if isinstance(value, Reason):
            value = {
                'RefusedReasonType': value.type,
                'RefusedReasonMessage': str(value.message)
            }

        return value


class AddressField(Field):
    def python_value(self, value):
        if value is not None:
            return Address(address_line_1=value['AddressLine1'], address_line_2=value['AddressLine2'],
                           city=value['City'], region=value['Region'],
                           postal_code=value['PostalCode'], country=value['Country'])

        return value

    def api_value(self, value):
        value = super(AddressField, self).api_value(value)

        if isinstance(value, Address):
            value = {
                'AddressLine1': value.address_line_1,
                'AddressLine2': value.address_line_2,
                'City': value.city,
                'Region': value.region,
                'PostalCode': value.postal_code,
                'Country': value.country
            }

        return value


class ShippingAddressField(Field):
    def python_value(self, value):
        return value if value is None else ShippingAddress(recipient_name=value['RecipientName'],
                                                           address=value['Address'])

    def api_value(self, value):
        value = super(ShippingAddressField, self).api_value(value)

        if isinstance(value, ShippingAddress):
            return {'RecipientName': value.recipient_name, 'Address': value.address}


class ReverseOneToOneRelatedObject(object):
    def __init__(self, related_model, name):
        self.field_name = name
        self.related_model = related_model

    def __get__(self, instance, instance_type=None):
        return instance.one(self.related_model)


class ForeignKeyField(CharField):
    def __init__(self, to, related_name=None, *args, **kwargs):
        self.to = to
        self.related_name = related_name

        super(ForeignKeyField, self).__init__(*args, **kwargs)

    def add_to_class(self, klass, name):
        self.descriptor = name
        self.name = name + '_id'
        self.model = klass

        self.api_name = self.api_name or re.sub('_', ' ', name).title()

        if self.related_name is None:
            self.related_name = klass._meta.verbose_name + '_set'

        klass._meta.rel_fields[name] = self.name
        setattr(klass, self.descriptor, ForeignRelatedObject(self.to, self.name, getattr(klass, self.descriptor)))
        setattr(klass, self.name, None)

        reverse_rel = ReverseForeignRelatedObject(klass, self.name)
        setattr(self.to, self.related_name, reverse_rel)
        self.to._meta.reverse_relations[self.related_name] = klass

    def api_value(self, value):
        from .base import BaseApiModel
        value = super(ForeignKeyField, self).api_value(value)

        if isinstance(value, BaseApiModel):
            value = value.get_pk()

        return value


class OneToOneField(ForeignKeyField):
    def add_to_class(self, klass, name):
        self.descriptor = name
        self.name = name + '_id'
        self.model = klass

        self.api_name = self.api_name or re.sub('_', ' ', name).title()

        if self.related_name is None:
            self.related_name = klass._meta.verbose_name

        klass._meta.rel_fields[name] = self.name
        setattr(klass, self.descriptor, ForeignRelatedObject(self.to, self.name))
        setattr(klass, self.name, None)

        reverse_rel = ReverseOneToOneRelatedObject(klass, self.name)
        setattr(self.to, self.related_name, reverse_rel)
        self.to._meta.reverse_relations[self.related_name] = klass


class ForeignRelatedObject(object):
    def __init__(self, to, name, old_field):
        self.field_name = name
        self.to = to
        self.cache_name = '_cache_%s' % name
        self.old_field = old_field

    def __get__(self, instance, instance_type=None):
        if not getattr(instance, self.cache_name, None):
            id = getattr(instance, self.field_name, 0)
            related = self.to.get(id, handler=instance.handler)
            setattr(instance, self.cache_name, related)
        return getattr(instance, self.cache_name)

    def __set__(self, instance, obj):
        assert isinstance(obj, self.to), "Cannot assign %s, invalid type" % obj
        setattr(instance, self.field_name, obj.get_pk())
        setattr(instance, self.cache_name, obj)


class ReverseForeignRelatedObject(object):
    def __init__(self, related_model, name):
        self.field_name = name
        self.related_model = related_model

    def __get__(self, instance, instance_type=None):
        fixed_kwargs = instance.fixed_kwargs()
        return RelatedManager(instance, self.related_model, fixed_kwargs)


class RelatedManager(object):
    def __init__(self, instance, related_model, fixed_kwargs=None):
        self.instance = instance
        self.related_model = related_model
        self.fixed_kwargs = fixed_kwargs

    def get(self, pk, **kwargs):
        kwargs.update(self.fixed_kwargs)
        return self.instance.get(pk, self.instance.handler, self.related_model, **kwargs)

    def all(self, **kwargs):
        return self.instance.list(self.related_model, **kwargs)


class ManyToManyField(ListField):
    def __init__(self, to, related_name=None, *args, **kwargs):
        self.to = to
        self.related_name = related_name

        super(ManyToManyField, self).__init__(*args, **kwargs)

    def add_to_class(self, klass, name):
        self.descriptor = name
        self.name = name + '_ids'
        self.model = klass

        self.api_name = self.api_name or re.sub('_', ' ', name).title()

        if self.related_name is None:
            self.related_name = klass._meta.verbose_name + '_set'

        klass._meta.rel_fields[name] = self.name
        setattr(klass, self.descriptor, ManyToManyRelatedObject(self.to, self.name))
        setattr(klass, self.name, None)

        reverse_rel = ManyToManyRelatedObject(klass, self.name)

        setattr(self.to, self.related_name, reverse_rel)
        self.to._meta.reverse_relations[self.related_name] = klass

    def api_value(self, value):
        from .base import BaseApiModel

        values = super(ManyToManyField, self).api_value(value)

        for i in range(len(values)):
            if isinstance(value, BaseApiModel):
                value = value.get_pk()
                values[i] = value

        return values


class ManyToManyRelatedObject(object):
    def __init__(self, related_model, name):
        self.related_model = related_model
        self.field_name = name

    def __get__(self, instance, instance_type=None):
        return instance.list(self.related_model)

    def __set__(self, instance, objs):
        setattr(instance, self.field_name, [obj.get_pk() for obj in objs])


class ApplepayPaymentDataField(Field):
    def python_value(self, value):
        if value is not None:
            return ApplepayPaymentData(transaction_id=value['TransactionId'], network=value['Network'],
                                       token_data=value['TokenData'])
        return value

    def api_value(self, value):
        value = super(ApplepayPaymentDataField, self).api_value(value)

        if isinstance(value, ApplepayPaymentData):
            value = {
                'TransactionId': value.transaction_id,
                'Network': value.network,
                'TokenData': value.token_data
            }
        return value


class GooglepayPaymentDataField(Field):
    def python_value(self, value):
        if value is not None:
            return GooglepayPaymentData(transaction_id=value['TransactionId'], network=value['Network'],
                                        token_data=value['TokenData'])
        return value

    def api_value(self, value):
        value = {
            'TransactionId': value.transaction_id,
            'Network': value.network,
            'TokenData': value.token_data
        }
        return value


class BirthplaceField(Field):
    def python_value(self, value):
        if value is not None:
            return Birthplace(city=value['City'], country=value['Country'])

        return value

    def api_value(self, value):
        value = super(BirthplaceField, self).api_value(value)

        if isinstance(value, Birthplace):
            value = {
                'City': value.city,
                'Country': value.country,
            }

        return value


class BrowserInfoField(Field):
    def python_value(self, value):
        if value is not None:
            return BrowserInfo(accept_header=value['AcceptHeader'], java_enabled=value['JavaEnabled'],
                               javascript_enabled=value['JavascriptEnabled'], language=value['Language'],
                               color_depth=value['ColorDepth'], screen_width=value['ScreenWidth'],
                               screen_height=value['ScreenHeight'], timezone_offset=value['TimeZoneOffset'],
                               user_agent=value['UserAgent'])

        return value

    def api_value(self, value):
        value = super(BrowserInfoField, self).api_value(value)

        if isinstance(value, BrowserInfo):
            value = {
                "AcceptHeader": value.accept_header,
                "JavaEnabled": value.java_enabled,
                "JavascriptEnabled": value.javascript_enabled,
                "Language": value.language,
                "ColorDepth": value.color_depth,
                "ScreenHeight": value.screen_height,
                "ScreenWidth": value.screen_width,
                "TimeZoneOffset": value.timezone_offset,
                "UserAgent": value.user_agent
            }

            return value


class ScopeBlockedField(Field):
    def python_value(self, value):
        if value is not None:
            return ScopeBlocked(inflows=value['Inflows'], outflows=value['Outflows'])

        return value

    def api_value(self, value):
        value = super(ScopeBlockedField, self).api_value(value)

        if isinstance(value, ScopeBlocked):
            value = {
                'Inflows': value.inflows,
                'Outflows': value.outflows,
            }

        return value


class ShippingField(Field):
    def python_value(self, value):
        if value is not None:
            return Shipping(first_name=value['FirstName'], last_name=value['LastName'], address=value['Address'])
        return value

    def api_value(self, value):
        value = super(ShippingField, self).api_value(value)

        if isinstance(value, Shipping):
            value = {
                'FirstName': value.first_name,
                'LastName': value.last_name,
                'Address': value.address
            }

        return value


class CurrentStateField(Field):
    def python_value(self, value):
        if value is not None:
            return CurrentState(payins_linked=value['PayinsLinked'],
                                cumulated_debited_amount=value['CumulatedDebitedAmount'],
                                cumulated_debited_fees=value['CumulatedFeesAmount'],
                                last_payin_id=value['LastPayinId'])
        return value

    def api_value(self, value):
        value = super(CurrentStateField, self).api_value(value)

        if isinstance(value, CurrentState):
            value = {
                'PayinsLinked ': value.payins_linked,
                'CumulatedDebitedAmount ': value.cumulated_debited_amount,
                'CumulatedFeesAmount  ': value.cumulated_debited_fees,
                'LastPayinId ': value.last_payin_id
            }

        return value


class CountryAuthorizationDataField(Field):
    def python_value(self, value):
        if value is not None:
            return CountryAuthorizationData(block_user_creation=value['BlockUserCreation'],
                                            block_bank_account_creation=value['BlockBankAccountCreation'],
                                            block_payout=value['BlockPayout'])

        return value

    def api_value(self, value):
        value = super(CountryAuthorizationDataField, self).api_value(value)

        if isinstance(value, CountryAuthorizationData):
            value = {
                'BlockUserCreation': value.block_user_creation,
                'BlockBankAccountCreation': value.block_bank_account_creation,
                'BlockPayout': value.block_payout
            }

        return value
