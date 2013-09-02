from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.types.money import Money


class Transaction (EntityBase):
    """Transaction entity.
    Base class for: PayIn, PayOut, Transfer.
    """

    AuthorId = 0

    CreditedUserId = 0

    # @var Money
    DebitedFunds = None

    # @var Money
    CreditedFunds = None

    # @var Money
    Fees = None

    # TransactionType {PAYIN, PAYOUT, TRANSFER}
    Type = None

    # TransactionNature {REGULAR, REFUND, REPUDIATION}
    Nature = None

    # TransactionStatus {CREATED, SUCCEEDED, FAILED}
    Status = None

    ResultCode = None

    # @var timestamp
    ExecutionDate = None

    def GetSubObjects(self):
        return {
            'DebitedFunds': 'Money' ,
            'CreditedFunds': 'Money' ,
            'Fees': 'Money'
        }

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('Status' )        
        properties.append('ResultCode' )        
        properties.append('ExecutionDate' )        
        return properties