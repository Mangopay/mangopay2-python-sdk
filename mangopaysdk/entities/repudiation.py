from mangopaysdk.entities.entitybase import EntityBase


class Repudiation (EntityBase):
    """Repudiation entity."""
    
    def __init__(self, id = None):
        
        self.AuthorId = None
        self.DebitedFunds = None
        self.Fees = None
        self.CreditedFunds = None
        self.DebitedWalletId = None
        self.Status = None
        self.ResultCode = None
        self.ResultMessage = None
        self.ExecutionDate = None
        self.DisputeId = None
        self.InitialTransactionId = None
        self.InitialTransactionType = None

        return super(Repudiation, self).__init__(id)
    
    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object.
        return dictionary
        """
        return {
                'DebitedFunds' : 'Money',
                'Fees' : 'Money',
                'CreditedFunds' : 'Money'
                }