from mangopaysdk.entities.transaction import Transaction


class Refund(Transaction):
    """Refund entity"""
        
    InitialTransactionId = 0
    
    DebitedWalletId = 0
    
    CreditedWalletId = 0