class RequestType:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class PersonType:
    Natural = 'NATURAL';
    Legal = 'LEGAL'


class LegalPersonType:
    BUSINESS = 'BUSINESS';
    ORGANIZATION = 'ORGANIZATION'


class TransactionStatus:
    CREATED = 'CREATED'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


class TransactionType:
    PAYIN = 'PAYIN'
    PAYOUT = 'PAYOUT'
    TRANSFER = 'TRANSFER'


class TransactionStatus:
    CREATED = 'CREATED'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'


class PayInPaymentType:
    CARD = 'CARD'
    BANK_WIRE = 'BANK_WIRE'
    AUTOMATIC_DEBIT = 'AUTOMATIC_DEBIT'
    DIRECT_DEBIT = 'DIRECT_DEBIT'


class ExecutionType:
    WEB = 'WEB'
    TOKEN = 'TOKEN'
    DIRECT = 'DIRECT'
    PREAUTHORIZED = 'PREAUTHORIZED'
    RECURRING_ORDER_EXECUTION = 'RECURRING_ORDER_EXECUTION'


class PayOutPaymentType:
     BANK_WIRE = 'BANK_WIRE'
     MERCHANT_EXPENSE = 'MERCHANT_EXPENSE'
     AMAZON_GIFTCARD = 'AMAZON_GIFTCARD'


class Mode3DSType:
    DEFAULT = 'DEFAULT'
    FORCE = 'FORCE'


class CardType:
    CB_VISA_MASTERCARD = 'CB_VISA_MASTERCARD'
    AMEX = 'AMEX'


class TransactionNature:
    REGULAR = 'REGULAR'
    REFUND = 'REFUND'
    REPUDIATION = 'REPUDIATION'


class CardRegistrationStatus:
    CREATED = 'CREATED',
    ERROR = 'ERROR',
    VALIDATED = 'VALIDATED'

#class AuthenticationType:
#    Basic = 'Basic'
#    Strong = 'Strong'
