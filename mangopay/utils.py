# see: http://hustoknow.blogspot.com/2011/01/m2crypto-and-facebook-python-sdk.html
from __future__ import unicode_literals

import copy
import datetime
import decimal
import inspect
import sys
from calendar import timegm
from functools import wraps

import pytz
import six

from .compat import python_2_unicode_compatible
from .exceptions import CurrencyMismatch

if six.PY3:
    from urllib import request

    orig = request.URLopener.open_https
    request.URLopener.open_https = orig  # uncomment this line back and forth
elif six.PY2:
    import urllib

    orig = urllib.URLopener.open_https
    urllib.URLopener.open_https = orig


class AliasProperty(object):
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        return setattr(instance, self.name, value)


def add_camelcase_aliases(cls):
    for name in cls().__dict__.keys():
        if name[0] == '_':
            continue
        setattr(cls, name.title().replace('_', ''), AliasProperty(name))
    return cls


@add_camelcase_aliases
@python_2_unicode_compatible
class Money(object):
    __hash__ = None

    def __init__(self, amount="0", currency=None):
        try:
            self.amount = decimal.Decimal(amount)
        except decimal.InvalidOperation:
            raise ValueError("amount value could not be converted to "
                             "Decimal(): '{}'".format(amount))
        self.currency = currency

    def __repr__(self):
        return "{} {}".format(self.currency, self.amount)

    def __str__(self):
        return force_text("{} {:,.2f}".format(self.currency, self.amount))

    def __lt__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '<')
            other = other.amount
        return self.amount < other

    def __le__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '<=')
            other = other.amount
        return self.amount <= other

    def __eq__(self, other):
        if isinstance(other, Money):
            return ((self.amount == other.amount) and
                    (self.currency == other.currency))
        return False

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '>')
            other = other.amount
        return self.amount > other

    def __ge__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '>=')
            other = other.amount
        return self.amount >= other

    def __bool__(self):
        return bool(self.amount)

    def __add__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '+')
            other = other.amount
        amount = self.amount + other
        return self.__class__(amount, self.currency)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '-')
            other = other.amount
        amount = self.amount - other
        return self.__class__(amount, self.currency)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError("multiplication is unsupported between "
                            "two money objects")
        amount = self.amount * other
        return self.__class__(amount, self.currency)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '/')

            if other.amount == 0:
                raise ZeroDivisionError()

            return self.amount / other.amount

        if other == 0:
            raise ZeroDivisionError()

        amount = self.amount / other

        return self.__class__(amount, self.currency)

    def __floordiv__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, '//')

            if other.amount == 0:
                raise ZeroDivisionError()
            return self.amount // other.amount

        if other == 0:
            raise ZeroDivisionError()

        amount = self.amount // other
        return self.__class__(amount, self.currency)

    def __mod__(self, other):
        if isinstance(other, Money):
            raise TypeError("modulo is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        if other == 0:
            raise ZeroDivisionError()

        amount = self.amount % other
        return self.__class__(amount, self.currency)

    def __divmod__(self, other):
        if isinstance(other, Money):
            if other.currency != self.currency:
                raise CurrencyMismatch(self.currency, other.currency, 'divmod')

            if other.amount == 0:
                raise ZeroDivisionError()

            return divmod(self.amount, other.amount)

        if other == 0:
            raise ZeroDivisionError()

        whole, remainder = divmod(self.amount, other)

        return (self.__class__(whole, self.currency),
                self.__class__(remainder, self.currency))

    def __pow__(self, other):
        if isinstance(other, Money):
            raise TypeError("power operator is unsupported between two '{}' "
                            "objects".format(self.__class__.__name__))
        amount = self.amount ** other
        return self.__class__(amount, self.currency)

    def __neg__(self):
        return self.__class__(-self.amount, self.currency)

    def __pos__(self):
        return self.__class__(+self.amount, self.currency)

    def __abs__(self):
        return self.__class__(abs(self.amount), self.currency)

    def __int__(self):
        return int(self.amount)

    def __float__(self):
        return float(self.amount)

    def __round__(self, ndigits=0):
        return self.__class__(round(self.amount, ndigits), self.currency)


@add_camelcase_aliases
class PlatformCategorization(object):
    def __init__(self, business_type=None, sector=None):
        self.business_type = business_type
        self.sector = sector

    def __str__(self):
        return 'PlatformCategorization: %s %s' % (self.business_type, self.sector)


@add_camelcase_aliases
class Billing(object):
    def __init__(self, first_name=None, last_name=None, address=None):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def __str__(self):
        return 'Billing: %s' % \
               (self.first_name, self.last_name, self.address)


@add_camelcase_aliases
class FallbackReason(object):
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def __str__(self):
        return 'FallbackReason: %s' % \
               (self.code, self.message)


@add_camelcase_aliases
class InstantPayout(object):
    def __init__(self, is_reachable=None, unreachable_reason=None):
        self.is_reachable = is_reachable
        self.unreachable_reason = unreachable_reason

    def __str__(self):
        return 'InstantPayout: %s' % \
               (self.code, self.message)


@add_camelcase_aliases
class SecurityInfo(object):
    def __init__(self, avs_result=None):
        self.avs_result = avs_result

    def __str__(self):
        return 'AVS Result: %s' % self.avs_result


@add_camelcase_aliases
class DebitedBankAccount(object):
    def __init__(self, owner_name=None, account_number=None, iban=None,
                 bic=None, type=None, country=None):
        self.owner_name = owner_name
        self.account_number = account_number
        self.iban = iban
        self.bic = bic
        self.type = type
        self.country = country

    def __str__(self):
        return 'DebitedBankAccount: %s' % \
               (self.owner_name, self.account_number, self.iban, self.bic, self.type, self.country)

    def __eq__(self, other):
        if isinstance(other, DebitedBankAccount):
            stat = (self.owner_name == other.owner_name and
                    self.account_number == other.account_number and
                    self.iban == other.iban and
                    self.bic == other.bic and
                    self.type == other.type and
                    self.country == other.country)

            return stat
        return False


@add_camelcase_aliases
class Address(object):
    def __init__(self, address_line_1=None, address_line_2=None, city=None, region=None,
                 postal_code=None, country=None):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.region = region
        self.postal_code = postal_code
        self.country = country

    def __str__(self):
        return 'Address: %s, %s , %s, %s, %s , %s' % \
               (self.address_line_1, self.address_line_2, self.postal_code, self.city, self.region, self.country)

    def __eq__(self, other):
        if isinstance(other, Address):
            stat = ((self.address_line_1 == other.address_line_1) and
                    (self.address_line_2 == other.address_line_2) and
                    (self.postal_code == other.postal_code) and
                    (self.city == other.city) and
                    (self.region == other.region) and
                    (self.country == other.country))
            return stat
        return False

    def to_api_json(self):
        return {
            "AddressLine1": self.address_line_1,
            "AddressLine2": self.address_line_2,
            "PostalCode": self.postal_code,
            "City": self.city,
            "Region": self.region,
            "Country": self.country,
        }


@add_camelcase_aliases
class ShippingAddress(object):
    def __init__(self, recipient_name=None, address=None):
        self.recipient_name = recipient_name
        self.address = address

    def __str__(self):
        return 'Recipient name: %s, %s' % (self.recipient_name, self.address)

    def __eq__(self, other):
        if isinstance(other, ShippingAddress):
            return self.recipient_name == other.recipient_name and self.address == other.address
        return False


@add_camelcase_aliases
class ApplepayPaymentData(object):
    def __init__(self, transaction_id=None, network=None, token_data=None):
        self.transaction_id = transaction_id
        self.network = network
        self.token_data = token_data

    def __eq__(self, other):
        if isinstance(other, ApplepayPaymentData):
            return self.transaction_id == other.transaction_id and self.network == other.network and self.token_data == other.token_data
        return False


@add_camelcase_aliases
class GooglepayPaymentData(object):
    def __init__(self, transaction_id=None, network=None, token_data=None):
        self.transaction_id = transaction_id
        self.network = network
        self.token_data = token_data

    def __eq__(self, other):
        if isinstance(other, GooglepayPaymentData):
            return self.transaction_id == other.transaction_id and self.network == other.network and self.token_data == other.token_data
        return False


@add_camelcase_aliases
class ReportTransactionsFilters(object):
    def __init__(self, before_date=None, after_date=None, transaction_type=None, status=None, nature=None,
                 min_debited_funds_amount=None, min_debited_funds_currency=None, max_debited_funds_amount=None,
                 max_debited_funds_currency=None, author_id=None, wallet_id=None):
        self.before_date = before_date
        self.after_date = after_date
        self.transaction_type = transaction_type
        self.status = status
        self.nature = nature
        self.min_debited_funds_amount = min_debited_funds_amount
        self.min_debited_funds_currency = min_debited_funds_currency
        self.max_debited_funds_amount = max_debited_funds_amount
        self.max_debited_funds_currency = max_debited_funds_currency
        self.author_id = author_id
        self.wallet_id = wallet_id

    def __eq__(self, other):
        if isinstance(other, ReportTransactionsFilters):
            stat = ((self.before_date == other.before_date) and
                    (self.after_date == other.after_date) and
                    (self.transaction_type == other.transaction_type) and
                    (self.status == other.status) and
                    (self.nature == other.nature) and
                    (self.min_debited_funds_amount == other.min_debited_funds_amount) and
                    (self.min_debited_funds_currency == other.min_debited_funds_currency) and
                    (self.max_debited_funds_amount == other.max_debited_funds_amount) and
                    (self.max_debited_funds_currency == other.max_debited_funds_currency) and
                    (self.author_id == other.author_id) and
                    (self.wallet_id == other.wallet_id)
                    )
            return stat
        return False


@add_camelcase_aliases
class ReportWalletsFilters(object):
    def __init__(self, before_date=None, after_date=None, owner_id=None, currency=None,
                 min_balance_amount=None, min_balance_currency=None, max_balance_amount=None,
                 max_balance_currency=None):
        self.before_date = before_date
        self.after_date = after_date
        self.owner_id = owner_id
        self.currency = currency
        self.min_balance_amount = min_balance_amount
        self.min_balance_currency = min_balance_currency
        self.max_balance_amount = max_balance_amount
        self.max_balance_currency = max_balance_currency

    def __eq__(self, other):
        if isinstance(other, ReportWalletsFilters):
            stat = ((self.before_date == other.before_date) and
                    (self.after_date == other.after_date) and
                    (self.owner_id == other.owner_id) and
                    (self.currency == other.currency) and
                    (self.min_balance_amount == other.min_balance_amount) and
                    (self.min_balance_currency == other.min_balance_currency) and
                    (self.max_balance_amount == other.max_balance_amount) and
                    (self.max_balance_currency == other.max_balance_currency)
                    )
            return stat
        return False


class Reason(object):
    def __init__(self, type=None, message=None):
        self.type = type
        self.message = message

    def __str__(self):
        return 'Reason: %s Message: %s' % (self.type, self.message)

    def __eq__(self, other):
        if isinstance(other, Reason):
            return ((self.type == other.type) and
                    (self.message == other.message))
        return False


@add_camelcase_aliases
class Birthplace(object):
    def __init__(self, city=None, country=None):
        self.city = city
        self.country = country

    def __str__(self):
        return 'Birthplace: %s, %s' % (self.city, self.country)

    def __eq__(self, other):
        if isinstance(other, Birthplace):
            stat = ((self.city == other.city) and
                    (self.country == other.country))
            return stat
        return False

    def to_api_json(self):
        return {
            "City": self.city,
            "Country": self.country,
        }


@add_camelcase_aliases
class BrowserInfo(object):
    def __init__(self, accept_header=None, java_enabled=None, javascript_enabled=None,
                 language=None, color_depth=None, screen_height=None, screen_width=None,
                 timezone_offset=None, user_agent=None):
        self.user_agent = user_agent
        self.timezone_offset = timezone_offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color_depth = color_depth
        self.language = language
        self.accept_header = accept_header
        self.java_enabled = java_enabled
        self.javascript_enabled = javascript_enabled

    def __str__(self):
        return 'BrowserInfo: %s %s %s %s %s %s %s %s %s' % (self.java_enabled, self.accept_header, self.language,
                                                            self.color_depth, self.screen_height, self.screen_width,
                                                            self.timezone_offset, self.user_agent,
                                                            self.javascript_enabled)

    def __eq__(self, other):
        if isinstance(other, BrowserInfo):
            stat = ((self.user_agent == other.user_agent) and
                    (self.timezone_offset == other.timezone_offset) and
                    (self.screen_width == other.screen_width) and
                    (self.screen_height == other.screen_height) and
                    (self.color_depth == other.color_depth) and
                    (self.language == other.language) and
                    (self.accept_header == other.accept_header) and
                    (self.java_enabled == other.java_enabled) and
                    (self.javascript_enabled == other.javascript_enabled))
            return stat
        return False

    def to_api_json(self):
        return {
            "AcceptHeader": self.accept_header,
            "JavaEnabled": self.java_enabled,
            "JavascriptEnabled": self.javascript_enabled,
            "Language": self.language,
            "ColorDepth": self.color_depth,
            "ScreenHeight": self.screen_height,
            "ScreenWidth": self.screen_width,
            "TimeZoneOffset": self.timezone_offset,
            "UserAgent": self.user_agent
        }


@add_camelcase_aliases
class Shipping(object):
    def __init__(self, first_name=None, last_name=None, address=None):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def __str__(self):
        return 'Shipping: %s' % \
               (self.first_name, self.last_name, self.address)


@add_camelcase_aliases
class CurrentState(object):
    def __init__(self, payins_linked=None, cumulated_debited_amount=None, cumulated_debited_fees=None,
                 last_payin_id=None):
        self.payins_linked = payins_linked
        self.cumulated_debited_amount = cumulated_debited_amount
        self.cumulated_debited_fees = cumulated_debited_fees
        self.last_payin_id = last_payin_id

    def __str__(self):
        return 'CurrentState: %s' % \
               (self.cumulated_debited_amount, self.cumulated_debited_fees, self.last_payin_id, self.payins_linked)


@add_camelcase_aliases
class ScopeBlocked(object):
    def __init__(self, inflows=None, outflows=None):
        self.inflows = inflows
        self.outflows = outflows

    def __str__(self):
        return 'ScopeBlocked: %s, %s' % (self.inflows, self.outflows)

    def __eq__(self, other):
        if isinstance(other, ScopeBlocked):
            stat = ((self.inflows == other.inflows) and
                    (self.outflows == other.outflows))
            return stat
        return False

    def to_api_json(self):
        return {
            "Inflows": self.inflows,
            "Outflows": self.outflows,
        }


# This code belongs to https://github.com/carljm/django-model-utils
class Choices(object):
    """
    A class to encapsulate handy functionality for lists of choices
    for a Django model field.
    Each argument to ``Choices`` is a choice, represented as either a
    string, a two-tuple, or a three-tuple.
    If a single string is provided, that string is used as the
    database representation of the choice as well as the
    human-readable presentation.
    If a two-tuple is provided, the first item is used as the database
    representation and the second the human-readable presentation.
    If a triple is provided, the first item is the database
    representation, the second a valid Python identifier that can be
    used as a readable label in code, and the third the human-readable
    presentation. This is most useful when the database representation
    must sacrifice readability for some reason: to achieve a specific
    ordering, to use an integer rather than a character field, etc.
    Regardless of what representation of each choice is originally
    given, when iterated over or indexed into, a ``Choices`` object
    behaves as the standard Django choices list of two-tuples.
    If the triple form is used, the Python identifier names can be
    accessed as attributes on the ``Choices`` object, returning the
    database representation. (If the single or two-tuple forms are
    used and the database representation happens to be a valid Python
    identifier, the database representation itself is available as an
    attribute on the ``Choices`` object, returning itself.)
    Option groups can also be used with ``Choices``; in that case each
    argument is a tuple consisting of the option group name and a list
    of options, where each option in the list is either a string, a
    two-tuple, or a triple as outlined above.
    """

    def __init__(self, *choices):
        # list of choices expanded to triples - can include optgroups
        self._triples = []
        # list of choices as (db, human-readable) - can include optgroups
        self._doubles = []
        # dictionary mapping db representation to human-readable
        self._display_map = {}
        # dictionary mapping Python identifier to db representation
        self._identifier_map = {}
        # set of db representations
        self._db_values = set()

        self._process(choices)

    def _store(self, triple, triple_collector, double_collector):
        self._identifier_map[triple[1]] = triple[0]
        self._display_map[triple[0]] = triple[2]
        self._db_values.add(triple[0])
        triple_collector.append(triple)
        double_collector.append((triple[0], triple[2]))

    def _process(self, choices, triple_collector=None, double_collector=None):
        if triple_collector is None:
            triple_collector = self._triples
        if double_collector is None:
            double_collector = self._doubles

        store = lambda c: self._store(c, triple_collector, double_collector)

        for choice in choices:
            if isinstance(choice, (list, tuple)):
                if len(choice) == 3:
                    store(choice)
                elif len(choice) == 2:
                    if isinstance(choice[1], (list, tuple)):
                        # option group
                        group_name = choice[0]
                        subchoices = choice[1]
                        tc = []
                        triple_collector.append((group_name, tc))
                        dc = []
                        double_collector.append((group_name, dc))
                        self._process(subchoices, tc, dc)
                    else:
                        store((choice[0], choice[0], choice[1]))
                else:
                    raise ValueError(
                        "Choices can't take a list of length %s, only 2 or 3"
                        % len(choice))
            else:
                store((choice, choice, choice))

    def __len__(self):
        return len(self._doubles)

    def __iter__(self):
        return iter(self._doubles)

    def __getattr__(self, attname):
        try:
            return self._identifier_map[attname]
        except KeyError:
            raise AttributeError(attname)

    def __getitem__(self, key):
        return self._display_map[key]

    def __add__(self, other):
        if isinstance(other, self.__class__):
            other = other._triples
        else:
            other = list(other)
        return Choices(*(self._triples + other))

    def __radd__(self, other):
        # radd is never called for matching types, so we don't check here
        other = list(other)
        return Choices(*(other + self._triples))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._triples == other._triples
        return False

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(("%s" % repr(i) for i in self._triples)))

    def __contains__(self, item):
        return item in self._db_values

    def __deepcopy__(self, memo):
        return self.__class__(*copy.deepcopy(self._triples, memo))


def timestamp_from_datetime(dt):
    """
    Compute timestamp from a datetime object that could be timezone aware
    or unaware.
    """
    try:
        utc_dt = dt.astimezone(pytz.utc)
    except ValueError:
        utc_dt = dt.replace(tzinfo=pytz.utc)
    return timegm(utc_dt.timetuple())


def timestamp_from_date(date):
    epoch = datetime.date(1970, 1, 1)
    diff = date - epoch
    return diff.days * 24 * 3600 + diff.seconds


if six.PY3:
    memoryview = memoryview
else:
    memoryview = buffer  # noqa


def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_text(strings_only=True).
    """
    return isinstance(obj, six.integer_types + (type(None), float, decimal.Decimal,
                                                datetime.datetime, datetime.date, datetime.time))


def force_text(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_text, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first, saves 30-40% when s is an instance of
    # six.text_type. This function gets called often in that setting.
    if isinstance(s, six.text_type):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, six.string_types):
            if hasattr(s, '__unicode__'):
                s = s.__unicode__()
            else:
                if six.PY3:
                    if isinstance(s, bytes):
                        s = six.text_type(s, encoding, errors)
                    else:
                        s = six.text_type(s)
                else:
                    s = six.text_type(bytes(s), encoding, errors)
        else:
            # Note: We use .decode() here, instead of six.text_type(s, encoding,
            # errors), so that if s is a SafeBytes, it ends up being a
            # SafeText at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError:
        # If we get to here, the caller has passed in an Exception
        # subclass populated with non-ASCII bytestring data without a
        # working unicode method. Try to handle this without raising a
        # further exception by individually forcing the exception args
        # to unicode.
        s = ' '.join([force_text(arg, encoding, strings_only,
                                 errors) for arg in s])
    return s


def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, memoryview):
        s = bytes(s)
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and (s is None or isinstance(s, int)):
        return s
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join([force_bytes(arg, encoding, strings_only,
                                              errors) for arg in s])
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)


if six.PY3:
    force_str = force_text
else:
    force_str = force_bytes


def memoize(func, cache, num_args):
    """
    Wrap a function so that results for any argument tuple are stored in
    'cache'. Note that the args to the function must be usable as dictionary
    keys.
    Only the first num_args are considered when creating the key.
    """

    @wraps(func)
    def wrapper(*args):
        mem_args = args[:num_args]
        if mem_args in cache:
            return cache[mem_args]
        result = func(*args)
        cache[mem_args] = result
        return result

    return wrapper


def reraise_as(new_exception_or_type):
    """
    Obtained from https://github.com/dcramer/reraise/blob/master/src/reraise.py
    >>> try:
    >>>     do_something_crazy()
    >>> except Exception:
    >>>     reraise_as(UnhandledException)
    """
    __traceback_hide__ = True  # NOQA

    e_type, e_value, e_traceback = sys.exc_info()

    if inspect.isclass(new_exception_or_type):
        new_type = new_exception_or_type
        new_exception = new_exception_or_type()
    else:
        new_type = type(new_exception_or_type)
        new_exception = new_exception_or_type

    new_exception.__cause__ = e_value

    try:
        six.reraise(new_type, new_exception, e_traceback)
    finally:
        del e_traceback


def truncatechars(value, length=255):
    if isinstance(value, dict):
        for k, v in value.items():
            value[k] = truncatechars(v)
    elif isinstance(value, six.string_types):
        return (value[:length] + '...') if len(value) > length else value

    return value


class CountryAuthorizationData(object):
    def __init__(self, block_user_creation=None, block_bank_account_creation=None, block_payout=None):
        self.block_user_creation = block_user_creation
        self.block_bank_account_creation = block_bank_account_creation
        self.block_payout = block_payout

    def __str__(self):
        return 'CountryAuthorizationData: %s, %s , %s' % \
               (self.block_user_creation, self.block_bank_account_creation, self.block_payout)

    def __eq__(self, other):
        if isinstance(other, CountryAuthorizationData):
            stat = ((self.block_user_creation == other.block_user_creation) and
                    (self.block_bank_account_creation == other.block_bank_account_creation) and
                    (self.block_payout == other.block_payout))
            return stat
        return False

    def to_api_json(self):
        return {
            "BlockUserCreation": self.block_user_creation,
            "BlockBankAccountCreation": self.block_bank_account_creation,
            "BlockPayout": self.block_payout
        }
