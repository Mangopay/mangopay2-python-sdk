from mangopaysdk.entities.entitybase import EntityBase


class PayInDirectCard(EntityBase):
    """PayInDirectCard entity"""

    AuthorId = ''
    CreditedFunds = ''

    # Money
    DebitedFunds = None
    # Money
    CreditedFunds = None
    # Money
    Fees = None

    # TransactionStatus { CREATED, SUCCEEDED, FAILED }
    Status = None
    
    # TransactionResultCode
    ResultCode = None

    # Date
    ExecutionDate = None

    # TransactionType {PAY_IN, PAY_OUT, TRANSFER}
    Type = None
    
    # TransactionNature { NORMAL, REFUND, REPUDIATION }
    Nature = None	
    
    CreditedWalletId = ''

    # PaymentType {CARD, BANK_WIRE, AUTOMATIC_DEBIT, DIRECT_DEBIT }
    PaymentType	= None
    
    # ExecutionType { WEB, TOKEN, DIRECT, PREAUTHORIZED, RECURRING_ORDER_EXECUTION }
    ExecutionType = None
    
    # CardType { CB_VISA_MASTERCARD, AMEX }
    CardType = None
    
    # Mode3DSType { DEFAULT, FORCE }
    SecureMode = None 
    
    CardId = ''
    SecureModeReturnURL = ''