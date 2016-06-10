from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.types.address import Address


class BankAccount(EntityBase):
    """Bank Account entity."""
    
    def __init__(self, id = None):
        self.UserId = None
        # Type of bank account
        self.Type = None
        self.OwnerName = None
        self.OwnerAddress = None
        self.Active = None
        self.Details = None
        return super(BankAccount, self).__init__(id)

    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object.
        return dictionary
        """
        return {'OwnerAddress' : 'Address'}

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
