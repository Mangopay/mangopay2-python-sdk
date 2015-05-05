from mangopaysdk.entities.transaction import Transaction


class Refund(Transaction):
    """Refund entity"""
    
    def __init__(self, id = None):
        self.InitialTransactionId = None
        self.DebitedWalletId = None
        self.CreditedWalletId = None
        self.InitialTransactionType = None
        self.RefundReason = None
        return super(Refund, self).__init__(id)

    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object."""
        subobjects = super(Refund, self).GetSubObjects()
        subobjects['DebitedFunds'] = 'Money'
        subobjects['RefundReason'] = 'RefundReason'
        return subobjects

    def GetReadOnlyProperties(self):
        properties = super(Refund, self).GetReadOnlyProperties()
        properties.append('InitialTransactionType')
        properties.append('RefundReason')
        return properties