from mangopaysdk.entities.entitybase import EntityBase


class User(EntityBase):

    def __init__(self, id = None):
        super(User, self).__init__(id)
        # Required
        self.Email = None
        # PersonType { LEGAL, NATURAL }
        self.PersonType = None

        # KYCLevel { LIGHT, REGULAR }
        self.KYCLevel = None

    def _setPersonType(self, personType):
        self.PersonType = personType

    def GetReadOnlyProperties(self):
        properties = super(User, self).GetReadOnlyProperties()
        properties.append('PersonType' )        
        properties.append('KYCLevel' )      
        return properties