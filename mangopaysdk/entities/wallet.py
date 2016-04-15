from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.types.money import Money


class Wallet(EntityBase):

    def __init__(self, id = None):
        # Array with owners identites
        self.Owners = []
        self.Description = None
        # Money type
        self.Balance = None
        # Currency code in ISO
        self.Currency = None
        # The funds usage type
        self.FundsType = None
        return super(Wallet, self).__init__(id)
    
    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object.
        return dictionary
        """
        return {'Balance' : 'Money'}

    def GetReadOnlyProperties(self):
        properties = super(Wallet, self).GetReadOnlyProperties()
        properties.append('Balance' )        
        return properties