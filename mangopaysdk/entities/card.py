from mangopaysdk.entities.entitybase import EntityBase


class Card(EntityBase):
    """Card entity"""

    # MMYY
    ExpirationDate = ''	
    
    # first 6 and last 4 are real card numbers for example: 497010XXXXXX4414
    Alias = ''

    CardType = None

    Product = ''
    BankCode = ''
    
    # Boolean
    Active = None
    
    Currency = ''
    
    # UNKNOWN, VALID, INVALID
    Validity = ''
    
    # Boolean
    Reusable = None