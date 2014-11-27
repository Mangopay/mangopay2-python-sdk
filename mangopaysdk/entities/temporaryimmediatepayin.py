from mangopaysdk.entities.transaction import Transaction


class TemporaryImmediatePayIn(Transaction):
    """WARNING! 
    This is temporary entity and will be removed in future.
    Contact support before using these features or if have any queries.
    
    TemporaryImmediatePayIn entity
    """
    
    def __init__(self, id = None):
        self.PaymentCardId = None
        self.CreditedWalletId = None
        return super(TemporaryImmediatePayIn, self).__init__(id)