from mangopaysdk.entities.transaction import Transaction


class Transfer (Transaction):

    def __init__(self, id = None):
        self.DebitedWalletId = None
        self.CreditedWalletId = None
        return super().__init__(id)