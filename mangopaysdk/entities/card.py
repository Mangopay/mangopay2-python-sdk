from mangopaysdk.entities.entitybase import EntityBase


class Card(EntityBase):
    """Card entity"""
    
    def __init__(self, id = None):
        # MMYY
        self.ExpirationDate = None	
        # first 6 and last 4 are real card numbers for example: 497010XXXXXX4414
        self.Alias = None
        # CardType { CB_VISA_MASTERCARD, AMEX }
        self.CardType = None
        self.Product = None
        self.BankCode = None
        # Boolean
        self.Active = None
        self.Currency = None
        # UNKNOWN, VALID, INVALID
        self.Validity = None
        return super().__init__(id)
    