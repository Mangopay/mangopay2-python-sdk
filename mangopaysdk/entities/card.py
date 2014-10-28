from mangopaysdk.entities.entitybase import EntityBase


class Card(EntityBase):
    """Card entity"""
    
    def __init__(self, id = None):
        self.UserId = None
        # MMYY
        self.ExpirationDate = None	
        # first 6 and last 4 are real card numbers for example: 497010XXXXXX4414
        self.Alias = None
        # The card provider, it could be CB, VISA, MASTERCARD, etc.
        self.CardProvider = None
        # CardType enum
        self.CardType = None
        self.Country = None
        self.Product = None
        self.BankCode = None
        # Boolean
        self.Active = None
        self.Currency = None
        # UNKNOWN, VALID, INVALID
        self.Validity = None
        return super(Card, self).__init__(id)
    
