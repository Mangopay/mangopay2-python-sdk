from mangopaysdk.entities.entitybase import EntityBase
from mangopaysdk.types.money import Money


class Wallet(EntityBase):

    # Array with owners identites
    Owners = []

    Description = ''

    # Money type
    Balance = Money()

    # Currency code in ISO
    Currency = 'EUR'

    def GetSubObjects(self):
        """Get array with mapping which property is object and what type of object.
        return dictionary
        """
        return {'Balance' : 'Money'}

    def GetReadOnlyProperties(self):
        properties = super().GetReadOnlyProperties()
        properties.append('Balance' )        
        return properties