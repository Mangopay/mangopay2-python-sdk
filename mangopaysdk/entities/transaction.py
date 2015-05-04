from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.types.money import Money


class Transaction (EntityBase):
    """Transaction entity.
    Base class for: PayIn, PayOut, Transfer.
    """

    def __init__(self, id = None):
        self.AuthorId = None
        self.CreditedUserId = None
        # Money
        self.DebitedFunds = None
        # Money
        self.CreditedFunds = None
        # Money
        self.Fees = None
        # TransactionType {PAYIN, PAYOUT, TRANSFER}
        self.Type = None
        # TransactionNature {REGULAR, REFUND, REPUDIATION}
        self.Nature = None
        # TransactionStatus {CREATED, SUCCEEDED, FAILED}
        self.Status = None
        self.ResultCode = None
        self.ResultMessage = None
        # timestamp
        self.ExecutionDate = None
        return super(Transaction, self).__init__(id)

    def GetSubObjects(self):
        return {
            'DebitedFunds': 'Money' ,
            'CreditedFunds': 'Money' ,
            'Fees': 'Money'
        }

    def GetReadOnlyProperties(self):
        properties = super(Transaction, self).GetReadOnlyProperties()
        properties.append('Status' )        
        properties.append('ResultCode' )   
        properties.append('ResultMessage' )
        properties.append('ExecutionDate' )        
        return properties
