from mangopaysdk.entities.entitybase import EntityBase


class BankAccount(EntityBase):
    """Bank Account entity."""
    
    def __init__(self, id = None):
        self.UserId = None
        # Type of bank account
        self.Type = None
        self.OwnerName = None
        self.OwnerAddress = None
        # must be valid ^[a-zA-Z]{2}\d{2}\s*(\w{4}\s*){2,7}\w{1,4}
        #self.IBAN = None
        self.Details = None
        # example BREXPLPWKRA
        #self.BIC = None
        return super(BankAccount, self).__init__(id)

    def GetReadOnlyProperties(self):
        properties = super(BankAccount, self).GetReadOnlyProperties()
        properties.append('UserId')
        properties.append('Type')
        return properties

    def GetDependsObjects(self):
        return { 
                'Type': {
                    '_property_name': 'Details', 
                    'IBAN': 'BankAccountDetailsIBAN',
                    'GB': 'BankAccountDetailsGB',
                    'US': 'BankAccountDetailsUS',
                    'CA': 'BankAccountDetailsCA',
                    'OTHER': 'BankAccountDetailsOTHER'
                }
        }