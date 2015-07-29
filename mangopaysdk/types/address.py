from mangopaysdk.types.dto import Dto


class Address(Dto):
    """Class represents an address."""
    
    def __init__(self):
        self.AddressLine1 = None
        self.AddressLine2 = None
        self.City = None
        self.Region = None
        self.PostalCode = None
        self.Country = None
