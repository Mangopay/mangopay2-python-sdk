from mangopaysdk.entities.entitybase import EntityBase


class BankAccount(EntityBase):
    """Bank Account entity."""
    
    def __init__(self, id = None):
        self.UserId = None
        # Type of bank account
        self.Type = 'IBAN'
        self.OwnerName = None
        self.OwnerAddress = None
        # must be valid ^[a-zA-Z]{2}\d{2}\s*(\w{4}\s*){2,7}\w{1,4}
        self.IBAN = None
        # example BREXPLPWKRA
        self.BIC = None
        return super(BankAccount, self).__init__(id)

    def GetReadOnlyProperties(self):
        properties = super(BankAccount, self).GetReadOnlyProperties()
        properties.append('UserId' )        
        return properties