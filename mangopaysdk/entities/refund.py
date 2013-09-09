from mangopaysdk.entities.transaction import Transaction


class Refund(Transaction):
    """Refund entity"""
    
    def __init__(self, id = None):
        self.InitialTransactionId = None
        self.DebitedWalletId = None
        self.CreditedWalletId = None
        return super().__init__(id)